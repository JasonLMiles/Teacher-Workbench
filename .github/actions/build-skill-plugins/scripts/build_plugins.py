#!/usr/bin/env python3
"""Build skills-only plugin packages. Python 3.12+, PyYAML; never runs skill code."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import html
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import struct
import sys
import tempfile
from dataclasses import dataclass, replace
from functools import lru_cache
from urllib.parse import unquote, urlsplit
import uuid
import zipfile
import zlib

import yaml


TARGETS = ("copilot", "chatgpt", "claude", "gemini-app", "gemini-cli")
IGNORE_DIRS = {".git", ".hg", ".svn", ".venv", "venv", "node_modules", "__pycache__", ".tox"}
IGNORE_FILES = {".DS_Store", "Thumbs.db"}
MAX_FILES = 10_000
MAX_BYTES = 256 * 1024 * 1024  # Per archive or unpacked skill.
GEMINI_APP_MAX_BYTES = 100_000_000  # Conservative decimal interpretation of 100 MB.
GEMINI_APP_OFFICE_FILES = {".doc", ".docx", ".docm", ".xls", ".xlsx", ".xlsm", ".ppt", ".pptx", ".pptm", ".odt", ".ods", ".odp"}
GEMINI_NETWORK_HINT = re.compile(r"https?://|\b(?:urllib|requests|httpx|aiohttp|curl|wget)\b|\bfetch\s*\(", re.I)
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
PORTABILITY = {
    "ChatGPT Library": r"\bChatGPT Library\b|\blibrary-file:",
    "host skill URI": r"skill://",
    "host-specific MCP tool name": r"\bmcp__[A-Za-z0-9_]+",
    "ChatGPT tool runtime": r"\bfunctions\.exec\b|\bnodeRepl\b|\bcua_repl\b",
    "Claude plugin variable": r"\$\{CLAUDE_[A-Z_]+\}",
    "host-local path": r"/root/\.codex/|/mnt/data/|/workspace/|sandbox:/",
}


class BuildError(Exception):
    pass


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of accepting silent overwrites."""


def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            if key in result:
                raise BuildError(f"Duplicate YAML key: {key!r}")
            result[key] = loader.construct_object(value_node, deep=deep)
        except TypeError as exc:
            raise BuildError("YAML mapping keys must be scalar values") from exc
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_yaml(text, label):
    try:
        return yaml.load(text, Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise BuildError(f"Invalid YAML in {label}: {exc}") from exc


def mapping(value, label, allowed):
    if not isinstance(value, dict):
        raise BuildError(f"{label} must be a mapping")
    extra = set(value) - set(allowed)
    if extra:
        raise BuildError(f"Unknown keys in {label}: {', '.join(map(str, extra))}")
    return value


def string(value, label, max_length=None):
    if not isinstance(value, str) or not value.strip():
        raise BuildError(f"{label} must be a nonempty string")
    if max_length and len(value) > max_length:
        raise BuildError(f"{label} exceeds {max_length} characters")
    return value


def name(value, label):
    string(value, label, 64)
    if not NAME.fullmatch(value):
        raise BuildError(f"{label} must be lowercase kebab-case: {value!r}")
    return value


def strings(value, label):
    if not isinstance(value, list) or not all(isinstance(v, str) and v for v in value):
        raise BuildError(f"{label} must be a list of nonempty strings")
    return value


def https_url(value, label):
    string(value, label)
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise BuildError(f"{label} must be an HTTPS URL without embedded credentials")
    return value


def inside(path: Path, parent: Path):
    return path == parent or parent in path.parents


def safe_path(value: str):
    if not value or "\\" in value or "\x00" in value or any(ord(c) < 32 for c in value):
        raise BuildError(f"Unsafe file path: {value!r}")
    parts = value.rstrip("/").split("/")
    if any(p in ("", ".", "..") or ":" in p for p in parts):
        raise BuildError(f"Unsafe file path: {value!r}")
    return PurePosixPath(*parts).as_posix()


@lru_cache(maxsize=4096)
def path_match(path, pattern):
    """POSIX glob: * is one segment; ** is zero or more segments."""
    parts, pats = tuple(path.split("/")), tuple(pattern.removeprefix("./").split("/"))

    @lru_cache(maxsize=None)
    def match(i, j):
        if j == len(pats):
            return i == len(parts)
        if pats[j] == "**":
            return match(i, j + 1) or (i < len(parts) and match(i + 1, j))
        return i < len(parts) and fnmatch.fnmatchcase(parts[i], pats[j]) and match(i + 1, j + 1)

    return match(0, 0)


def excluded(path, patterns, directory=False):
    return any(path_match(path, p) or (directory and p.endswith("/**") and path_match(path, p[:-3]))
               for p in patterns)


@dataclass(frozen=True)
class Blob:
    data: bytes
    executable: bool = False


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    files: dict[str, Blob]
    source_path: str  # Collection-relative archive path OR skill-directory path.
    origins: tuple[str, ...]

    @property
    def digest(self):
        return tree_hash(self.files)


def tree_hash(files):
    digest = hashlib.sha256()
    for path, blob in sorted(files.items()):
        digest.update(path.encode("utf-8") + b"\0")
        digest.update(b"x" if blob.executable else b"-")
        digest.update(hashlib.sha256(blob.data).digest())
    return digest.hexdigest()


def parse_skill(files, label, source_path):
    if "SKILL.md" not in files:
        raise BuildError(f"{label}: no SKILL.md")
    try:
        text = files["SKILL.md"].data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise BuildError(f"{label}: SKILL.md is not UTF-8") from exc
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise BuildError(f"{label}: SKILL.md must begin with YAML frontmatter")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise BuildError(f"{label}: unterminated YAML frontmatter")
    metadata = load_yaml("\n".join(lines[1:end]), label)
    if not isinstance(metadata, dict):
        raise BuildError(f"{label}: frontmatter must be a mapping")
    skill_name = name(metadata.get("name"), f"{label}: name")
    description = string(metadata.get("description"), f"{label}: description", 1024)
    if not "\n".join(lines[end + 1:]).strip():
        raise BuildError(f"{label}: missing skill instructions")
    validate_file_set(files, label)
    return Skill(skill_name, description, files, source_path, (label,))


def validate_file_set(files, label):
    if len(files) > MAX_FILES or sum(len(b.data) for b in files.values()) > MAX_BYTES:
        raise BuildError(f"{label}: exceeds {MAX_FILES} files or 256 MiB uncompressed")
    seen = set()
    for path in files:
        safe_path(path)
        folded = path.casefold()
        if folded in seen:
            raise BuildError(f"{label}: case-insensitive path collision: {path}")
        seen.add(folded)
    for path in files:
        if any(p.as_posix().casefold() in seen for p in PurePosixPath(path).parents if str(p) != "."):
            raise BuildError(f"{label}: file/directory collision at {path}")


def read_blob(path):
    if path.is_symlink() or not path.is_file():
        raise BuildError(f"Symlink or non-regular file is not supported: {path}")
    if path.stat().st_size > MAX_BYTES:
        raise BuildError(f"File exceeds 256 MiB: {path}")
    return Blob(path.read_bytes(), bool(path.stat().st_mode & 0o111))


def read_archive(path, source_path, warnings):
    files = {}
    try:
        with zipfile.ZipFile(path) as archive:
            members = archive.infolist()
            if len(members) > MAX_FILES or sum(i.file_size for i in members) > MAX_BYTES:
                raise BuildError(f"{source_path}: archive exceeds 10,000 entries or 256 MiB uncompressed")
            seen = set()
            for info in members:
                entry = safe_path(info.filename)
                if entry.casefold() in seen:
                    raise BuildError(f"{source_path}: duplicate archive entry: {entry}")
                seen.add(entry.casefold())
                file_type = stat.S_IFMT(info.external_attr >> 16)
                if file_type not in (0, stat.S_IFREG, stat.S_IFDIR) or info.flag_bits & 1:
                    raise BuildError(f"{source_path}: links, special files, or encrypted entries are unsupported")
                if info.is_dir():
                    continue
                if any(p in IGNORE_DIRS for p in PurePosixPath(entry).parts) or PurePosixPath(entry).name in IGNORE_FILES:
                    continue
                files[entry] = Blob(archive.read(info), bool((info.external_attr >> 16) & 0o111))
    except (zipfile.BadZipFile, NotImplementedError, RuntimeError) as exc:
        raise BuildError(f"{source_path}: invalid or unsupported ZIP-format .skill archive: {exc}") from exc
    validate_file_set(files, source_path)
    roots = sorted({str(PurePosixPath(p).parent) for p in files if PurePosixPath(p).name == "SKILL.md"},
                   key=lambda p: len(PurePosixPath(p).parts), reverse=True)
    if not roots:
        raise BuildError(f"{source_path}: archive contains no SKILL.md at any depth")
    assigned = {root: {} for root in roots}
    unassigned = []
    for file, blob in files.items():
        for root in roots:
            prefix = "" if root == "." else root + "/"
            if file.startswith(prefix):
                assigned[root][file[len(prefix):]] = blob
                break
        else:
            unassigned.append(file)
    if unassigned:
        warnings.append(f"{source_path}: omitted {len(unassigned)} wrapper file(s) outside skill roots")
    return [parse_skill(assigned[r], f"{source_path}!/{r}", source_path) for r in sorted(assigned)]


def load_config(path, targets):
    cfg = mapping(load_yaml(path.read_text(encoding="utf-8"), str(path)), "config",
                  {"schema_version", "catalog_name", "publisher", "exclude", "plugins", "license_file"})
    if cfg.get("schema_version") != 1:
        raise BuildError("config.schema_version must be 1")
    name(cfg.get("catalog_name", "skill-plugins"), "catalog_name")
    pub = mapping(cfg.get("publisher"), "publisher", {"name", "website_url", "privacy_url", "terms_url"})
    string(pub.get("name"), "publisher.name", 32 if "copilot" in targets else None)
    if "copilot" in targets:
        for key in ("website_url", "privacy_url", "terms_url"):
            https_url(pub.get(key), f"publisher.{key}")
    cfg.setdefault("exclude", [])
    strings(cfg["exclude"], "exclude")
    if "license_file" in cfg:
        string(cfg["license_file"], "license_file")
        read_blob(path.parent / cfg["license_file"])
    plugins = cfg.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        raise BuildError("plugins must be a nonempty list")
    known = set()
    for plugin in plugins:
        mapping(plugin, "plugin", {"name", "display_name", "description", "include", "exclude", "requires", "overlays", "microsoft", "gemini_app"})
        slug = name(plugin.get("name"), "plugin.name")
        if slug in known:
            raise BuildError(f"Duplicate plugin name: {slug}")
        known.add(slug)
        string(plugin.get("description"), f"{slug}.description", 4000 if "copilot" in targets else None)
        string(plugin.get("display_name", slug), f"{slug}.display_name", 30 if "copilot" in targets else None)
        for field, default in (("include", ["name:*"]), ("exclude", [])):
            plugin.setdefault(field, default)
            for selector in strings(plugin[field], f"{slug}.{field}"):
                if not selector.startswith(("name:", "path:")) or not selector.split(":", 1)[1]:
                    raise BuildError(f"{slug}: selector must start with name: or path: ({selector})")
        requirements = plugin.get("requires", {})
        if not isinstance(requirements, dict):
            raise BuildError(f"{slug}.requires must map skill names to lists of required skill names")
        for key, values in requirements.items():
            name(key, "requires key")
            for value in strings(values, f"requires.{key}"):
                name(value, "required skill")
        overlays = mapping(plugin.get("overlays", {}), f"{slug}.overlays", TARGETS)
        for target, value in overlays.items():
            string(value, f"{slug}.overlays.{target}")
            overlay = path.parent / value
            if overlay.is_symlink() or not overlay.is_dir():
                raise BuildError(f"Overlay must be an existing ordinary directory: {overlay}")
        app = mapping(plugin.get("gemini_app", {}), f"{slug}.gemini_app", {"exclude_files"})
        patterns = strings(app.get("exclude_files", []), f"{slug}.gemini_app.exclude_files")
        if excluded("SKILL.md", patterns):
            raise BuildError(f"{slug}: gemini_app.exclude_files cannot remove SKILL.md")
        ms = mapping(plugin.get("microsoft", {}), f"{slug}.microsoft", {"app_id", "color_icon", "outline_icon", "split"})
        if ms.get("split", "auto") not in ("auto", "error"):
            raise BuildError(f"{slug}.microsoft.split must be auto or error")
        if "app_id" in ms:
            try:
                uuid.UUID(ms["app_id"])
            except (ValueError, TypeError, AttributeError) as exc:
                raise BuildError(f"{slug}.microsoft.app_id must be a UUID") from exc
    return cfg


def discover(source, output, cfg, config_path, warnings):
    ignored_paths = [output]
    for plugin in cfg["plugins"]:
        ignored_paths.extend((config_path.parent / p).resolve() for p in plugin.get("overlays", {}).values())
    if any(inside(source, p) for p in ignored_paths):
        raise BuildError("Source may not be inside an output or overlay directory")
    roots, archives = [], []
    file_index = []
    for current, dirs, files in os.walk(source, followlinks=False):
        current = Path(current)
        kept = []
        for d in sorted(dirs):
            path = current / d
            rel = path.relative_to(source).as_posix()
            if d in IGNORE_DIRS or any(inside(path.resolve(), p) for p in ignored_paths) or excluded(rel, cfg["exclude"], True):
                continue
            if path.is_symlink():
                raise BuildError(f"Symlink directory is not supported: {rel}")
            kept.append(d)
        dirs[:] = kept
        for filename in sorted(files):
            path = current / filename
            rel = path.relative_to(source).as_posix()
            if filename in IGNORE_FILES or filename.endswith((".pyc", ".pyo")) or excluded(rel, cfg["exclude"]):
                continue
            if path.is_symlink():
                raise BuildError(f"Symlink file is not supported: {rel}")
            file_index.append(path)
            if filename == "SKILL.md":
                roots.append(current)
            elif path.suffix.lower() == ".skill":
                archives.append(path)
    # Assign each file to its nearest SKILL.md ancestor. Nested skill roots
    # become independent skills; child skill content is not copied twice.
    root_set = set(roots)
    folder_files = {r: {} for r in roots}
    for path in file_index:
        if path in archives:
            continue
        owner = next((p for p in path.parents if p in root_set), None)
        if owner is not None:
            folder_files[owner][path.relative_to(owner).as_posix()] = read_blob(path)
            # Bound memory while reading, not only after a skill is complete.
            if len(folder_files[owner]) > MAX_FILES or sum(len(b.data) for b in folder_files[owner].values()) > MAX_BYTES:
                raise BuildError(f"{owner}: exceeds input size limits")
    skills = []
    for root in sorted(roots):
        rel = root.relative_to(source).as_posix()
        skills.append(parse_skill(folder_files[root], rel, rel))
    for archive in sorted(archives):
        skills.extend(read_archive(archive, archive.relative_to(source).as_posix(), warnings))
    if not skills:
        raise BuildError(f"No .skill archives or SKILL.md folders found recursively beneath {source}")
    return skills


def matches(skill, selector):
    kind, pattern = selector.split(":", 1)
    return fnmatch.fnmatchcase(skill.name, pattern) if kind == "name" else path_match(skill.source_path, pattern)


def merge_identical(skills, context):
    merged = {}
    for skill in skills:
        previous = merged.get(skill.name)
        if previous:
            if previous.digest != skill.digest:
                raise BuildError(f"{context}: conflicting skill name '{skill.name}' in "
                                 f"{', '.join(previous.origins)} and {', '.join(skill.origins)}. "
                                 "Use path selectors to separate them into bundles, or rename one skill.")
            skill = replace(previous, origins=tuple(sorted(set(previous.origins + skill.origins))))
        merged[skill.name] = skill
    return merged


def select_skills(inventory, plugin):
    include = lambda s: any(matches(s, p) for p in plugin["include"])
    exclude = lambda s: any(matches(s, p) for p in plugin["exclude"])
    selected = merge_identical([s for s in inventory if include(s) and not exclude(s)], plugin["name"])
    if not selected:
        raise BuildError(f"{plugin['name']}: bundle matched no skills")
    pending = list(selected)
    checked = set()
    while pending:
        current = pending.pop()
        if current in checked:
            continue
        checked.add(current)
        for dependency in plugin.get("requires", {}).get(current, []):
            if dependency not in selected:
                candidates = [s for s in inventory if s.name == dependency and not exclude(s)]
                if not candidates:
                    raise BuildError(f"{plugin['name']}: {current} requires missing or excluded skill {dependency}")
                selected[dependency] = merge_identical(candidates, plugin["name"])[dependency]
            pending.append(dependency)
    return [selected[k] for k in sorted(selected)]


def target_bundles(bundles, target, warnings):
    """The M365 manifest caps each app at 20 skills; retain all selected skills."""
    result = []
    for plugin, skills in bundles:
        if target != "copilot" or len(skills) <= 20:
            result.append((plugin, skills, plugin["name"]))
            continue
        if plugin.get("microsoft", {}).get("split", "auto") == "error":
            raise BuildError(f"{plugin['name']}: {len(skills)} skills exceeds Copilot's 20-skill limit; define smaller bundles or enable microsoft.split: auto")
        chunks = [skills[i:i + 20] for i in range(0, len(skills), 20)]
        warnings.append(f"{plugin['name']}/copilot: split into {len(chunks)} parts; install/update every part together. Membership can move when skills are added or removed.")
        for index, chunk in enumerate(chunks, 1):
            suffix = f"-{index:02d}"
            label = f" ({index}/{len(chunks)})"
            part = {**plugin, "name": plugin["name"][:64 - len(suffix)].rstrip("-") + suffix,
                    "display_name": plugin.get("display_name", plugin["name"])[:30 - len(label)].rstrip() + label,
                    "microsoft": dict(plugin.get("microsoft", {}))}
            if part["microsoft"].get("app_id"):
                part["microsoft"]["app_id"] = str(uuid.uuid5(uuid.UUID(part["microsoft"]["app_id"]), f"part-{index:02d}"))
            result.append((part, chunk, plugin["name"]))
    names = [p["name"] for p, _, _ in result]
    if len(names) != len(set(names)):
        raise BuildError(f"{target}: automatic part names collide with another bundle; choose distinct bundle names")
    return result


def write_blob(path, blob):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(blob.data)
    path.chmod(0o755 if blob.executable else 0o644)


def write_json(path, data):
    write_blob(path, Blob((json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")))


def png(size, outline=False):
    """Deterministic development placeholder, no imaging dependency."""
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    rows = bytearray()
    for y in range(size):
        rows.append(0)
        for x in range(size):
            edge = (4 <= x < size - 4 and 4 <= y < size - 4 and
                    (x < 6 or x >= size - 6 or y < 6 or y >= size - 6))
            rows.extend((255, 255, 255, 255 if edge else 0) if outline else (38, 80, 164, 255))
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(bytes(rows), 9)) + chunk(b"IEND", b"")


def check_png(data, size, label):
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR" or struct.unpack(">II", data[16:24]) != (size, size):
        raise BuildError(f"{label} must be a {size} x {size} PNG")


def apply_overlay(root, path, selected, allowed):
    applied = []
    for current, dirs, files in os.walk(path, followlinks=False):
        dirs.sort()
        if any((Path(current) / d).is_symlink() for d in dirs):
            raise BuildError(f"Symlink directory in overlay: {current}")
        for filename in sorted(files):
            file = Path(current) / filename
            rel = file.relative_to(path).as_posix()
            parts = PurePosixPath(safe_path(rel)).parts
            if len(parts) < 3 or parts[0] != "skills" or parts[1] not in allowed:
                raise BuildError(f"Overlay file must be under skills/<selected-skill>/: {rel}")
            if parts[1] not in selected:
                continue  # A valid override for a different automatically split part.
            write_blob(root / rel, read_blob(file))
            applied.append(rel)
    return applied


def read_tree(root):
    return {p.relative_to(root).as_posix(): read_blob(p) for p in sorted(root.rglob("*")) if p.is_file()}


def check_links(root, files, warnings, label):
    # Simple inline Markdown links only; not a semantic Markdown/code analyser.
    for rel, blob in files.items():
        if not rel.endswith(".md"):
            continue
        try:
            text = blob.data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise BuildError(f"{label}/{rel}: Markdown must be UTF-8") from exc
        text = re.sub(r"(?ms)^\s*(```|~~~).*?^\s*\1[^\n]*$", "", text)
        for link in re.findall(r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)", text):
            link = link.strip("<>")
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            if "${" in link or "{{" in link:
                warnings.append(f"{label}/{rel}: dynamic Markdown link requires runtime verification")
                continue
            destination = (root / rel).parent / unquote(parsed.path)
            if not inside(destination.resolve(), root.resolve()) or not destination.exists():
                raise BuildError(f"{label}/{rel}: missing or out-of-package relative link {link!r}")


def check_copilot_skill(skill):
    companions = [(p, b) for p, b in skill.files.items() if p != "SKILL.md"]
    if len(companions) > 20 or sum(len(b.data) for _, b in companions) > 10_000_000:
        raise BuildError(f"{skill.name}: Copilot allows 20 companion files and 10 MB total per skill")
    for path, blob in companions:
        if len(blob.data) > 5_000_000:
            raise BuildError(f"{skill.name}/{path}: exceeds Copilot's 5 MB companion limit")
        for component in PurePosixPath(path).parts:
            if (component.startswith(".") or not re.fullmatch(r"[A-Za-z0-9_. !-]+", component)
                    or re.fullmatch(r"(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])", component.split(".")[0])):
                raise BuildError(f"{skill.name}/{path}: invalid Copilot companion path")


def check_gemini_app_skill(skill):
    """Conservative upload checks, not a replacement for Gemini's importer."""
    if sum(len(b.data) for b in skill.files.values()) > GEMINI_APP_MAX_BYTES:
        raise BuildError(f"{skill.name}: Gemini app upload exceeds 100 MB uncompressed")
    for path, blob in skill.files.items():
        suffix = PurePosixPath(path).suffix.lower()
        data = blob.data
        if suffix == ".pdf" and data.startswith(b"%PDF-"):
            continue
        if suffix == ".png" and data.startswith(b"\x89PNG\r\n\x1a\n"):
            continue
        if suffix in (".jpg", ".jpeg") and data.startswith(b"\xff\xd8\xff"):
            continue
        try:
            text = data.decode("utf-8-sig")
            plain = not any(ord(c) < 32 and c not in "\t\r\n\f" for c in text)
        except UnicodeDecodeError:
            plain = False
        if suffix in GEMINI_APP_OFFICE_FILES or suffix in (".pdf", ".png", ".jpg", ".jpeg") or not plain:
            raise BuildError(f"{skill.name}/{path}: unsupported Gemini app resource. Use UTF-8 text, PDF, PNG, or JPEG; "
                             "or explicitly omit it with gemini_app.exclude_files and update references with an overlay.")


def make_manifest(root, target, plugin, cfg, version, config_path, warnings):
    slug = plugin["name"]
    pub = cfg["publisher"]
    common = {"name": slug, "version": version, "description": plugin["description"], "author": {"name": pub["name"]}}
    if target == "claude":
        write_json(root / ".claude-plugin/plugin.json", common)
    elif target == "chatgpt":
        write_json(root / "plugin.json", {"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", **common})
    elif target == "gemini-cli":
        write_json(root / "gemini-extension.json", {"name": slug, "version": version, "description": plugin["description"]})
    elif target == "copilot":
        ms = plugin.get("microsoft", {})
        if len(list((root / "skills").iterdir())) > 20:
            raise BuildError(f"{slug}: Copilot manifest cannot contain more than 20 skills")
        identity = pub["website_url"].rstrip("/") + "/skill-plugins/" + slug
        app_id = str(uuid.UUID(ms["app_id"])) if ms.get("app_id") else str(uuid.uuid5(uuid.NAMESPACE_URL, identity))
        manifest = {
            "$schema": "https://developer.microsoft.com/json-schemas/teams/v1.28/MicrosoftTeams.schema.json",
            "manifestVersion": "1.28", "version": version, "id": app_id,
            "developer": {"name": pub["name"], "websiteUrl": pub["website_url"], "privacyUrl": pub["privacy_url"], "termsOfUseUrl": pub["terms_url"]},
            "name": {"short": plugin.get("display_name", slug), "full": plugin.get("display_name", slug)},
            "description": {"short": plugin["description"][:80], "full": plugin["description"]},
            "icons": {"color": "color.png", "outline": "outline.png"}, "accentColor": "#2650A4",
            "agentSkills": [{"folder": "./skills/" + p.name} for p in sorted((root / "skills").iterdir())],
        }
        write_json(root / "manifest.json", manifest)
        for key, size, outline, filename in (("color_icon", 192, False, "color.png"), ("outline_icon", 32, True, "outline.png")):
            if key in ms:
                data = read_blob(config_path.parent / ms[key]).data
                check_png(data, size, key)
            else:
                data = png(size, outline)
                warnings.append(f"{slug}/copilot: generated development placeholder {filename}; supply branding before publication")
            write_blob(root / filename, Blob(data))
    else:
        raise BuildError(f"No plugin manifest exporter for target: {target}")


def deterministic_zip(root, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for rel, blob in sorted(read_tree(root).items()):
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | (0o755 if blob.executable else 0o644)) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, blob.data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return hashlib.sha256(destination.read_bytes()).hexdigest()


def write_gemini_guide(staging, packages):
    app = [p for p in packages if p["target"] == "gemini-app"]
    cli = [p for p in packages if p["target"] == "gemini-cli"]
    if not app and not cli:
        return None
    lines = ["# Install the Gemini packages", ""]
    if app:
        lines += ["## Gemini app", "",
                  "Download the individual skill ZIPs below. In https://gemini.google.com, open Customize → Skills → Upload. "
                  "Select one skill ZIP, review it, and choose Create. Repeat for the other skills you want to use.", "",
                  "Install every skill in a bundle when it includes an orchestrator or declared dependencies. "
                  "Dependencies are separate imports; uploading one ZIP does not install the others. "
                  "Skill availability depends on your account rollout and administrator settings.", "",
                  "| Bundle | Skill | Download | Declared dependencies |", "|---|---|---|---|"]
        for p in app:
            filename = PurePosixPath(p["archive"]).name
            lines.append(f"| {p['bundle']} | {p['skills'][0]['name']} | `{filename}` | {', '.join(p['requires']) or '—'} |")
        lines += ["", "Each ZIP has SKILL.md at its root with its resource subfolders. "
                  "For updates, use Replace skill and upload the complete new ZIP. "
                  "These copies do not automatically synchronize with GitHub.", "",
                  "Gemini app scripts cannot access external websites. Review the build report for omitted files and "
                  "portability hints, and test any script or tool-dependent workflow in Gemini.", "",
                  "[Google's import instructions and limits](https://support.google.com/gemini/answer/17094296?hl=en)", ""]
    if cli:
        lines += ["## Gemini CLI", "",
                  "Download an extension ZIP and extract its contents into a folder named for the extension. "
                  "That folder must directly contain gemini-extension.json and skills/. Then run the corresponding "
                  "command in your terminal and restart Gemini CLI:", "",
                  "| Extension ZIP | Install after extraction |", "|---|---|"]
        for p in cli:
            lines.append(f"| `{PurePosixPath(p['archive']).name}` | `gemini extensions install ./{p['plugin']}` |")
        lines += ["", "Use /skills list inside Gemini CLI to check discovery. Each extension includes all selected "
                  "skills in its configured bundle. Relative resource folders and executable file permissions are preserved.", "",
                  "For installation by GitHub URL, publish each generated extension tree in a dedicated distribution "
                  "repository with gemini-extension.json at its root. Users can then run "
                  "`gemini extensions install https://github.com/OWNER/EXTENSION-REPO`. "
                  "A mixed release containing many app-skill and other-platform ZIPs has no single generic extension "
                  "asset for the CLI to select; use the downloaded-and-extracted path above for this build's release.", "",
                  "[Gemini CLI extension reference](https://geminicli.com/docs/extensions/reference/)", "",
                  "[Gemini CLI distribution](https://geminicli.com/docs/extensions/releasing/)", ""]
    write_blob(staging / "GEMINI-INSTALL.md", Blob(("\n".join(lines) + "\n").encode("utf-8")))
    return "GEMINI-INSTALL.md"


def write_platform_bundles(staging, catalog, report, license_blob):
    """Group installable archives by their recorded target, without changing them."""
    version = report["package_version"]
    archive_index = {a["path"]: a for a in report["archives"]}
    instructions = {
        "copilot": "Install every Copilot plugin part in archives/ through your host's custom-app/plugin upload process.",
        "chatgpt": "Use a plugin ZIP from archives/, or extract the marketplace ZIP for repository marketplace distribution.",
        "claude": "Upload a plugin ZIP from archives/, or extract the marketplace ZIP for repository marketplace distribution.",
        "gemini-app": "Upload the individual skill ZIPs in archives/ separately. Install the complete set when using the orchestrator. See GEMINI-INSTALL.md.",
        "gemini-cli": "Extract the extension ZIP from archives/ into a folder containing gemini-extension.json and skills/, then install that folder with Gemini CLI. See GEMINI-INSTALL.md.",
    }
    bundles = []
    for target in report["targets"]:
        packages = [p for p in report["packages"] if p["target"] == target]
        selected = {p["archive"] for p in packages}
        if target in ("chatgpt", "claude"):
            selected.add(f"archives/{catalog}-{target}-marketplace-{version}.zip")
        archives = [archive_index[path] for path in sorted(selected)]
        root = staging / "platform-contents" / target
        for archive in archives:
            write_blob(root / archive["path"], Blob((staging / archive["path"]).read_bytes()))
        platform_report = {**report, "targets": [target], "packages": packages, "archives": archives,
                           "install_sets": [s for s in report["install_sets"] if s["target"] == target],
                           "portability_hints": [h for h in report["portability_hints"] if h["target"] == target],
                           "gemini_install_guide": report["gemini_install_guide"] if target.startswith("gemini-") else None}
        write_json(root / "build-report.json", platform_report)
        write_blob(root / "SHA256SUMS", Blob("".join(f"{a['sha256']}  {a['path']}\n" for a in archives).encode()))
        if license_blob:
            write_blob(root / "license.md", license_blob)
        if platform_report["gemini_install_guide"]:
            write_gemini_guide(root, packages)
        lines = [f"# {catalog} for {target}", "", f"Package version: {version}", "",
                 "Extract this download bundle first. Install the appropriate ZIPs inside archives/; "
                 "the outer bundle itself is not a host plugin or skill upload.", "", instructions[target], "",
                 "## Included downloads", ""]
        lines += [f"- [{PurePosixPath(a['path']).name}]({a['path']})" for a in archives]
        lines += ["", "Review build-report.json for package membership and compatibility findings. "
                  "SHA256SUMS verifies the inner ZIPs from this extracted directory.", ""]
        write_blob(root / "README.md", Blob("\n".join(lines).encode()))
        relative = f"platforms/{catalog}-{target}-{version}-bundle.zip"
        bundles.append({"target": target, "path": relative,
                        "sha256": deterministic_zip(root, staging / relative),
                        "archives": [a["path"] for a in archives]})
    shutil.rmtree(staging / "platform-contents")
    return bundles


def build(args):
    source, output, config_path = Path(args.source).resolve(), Path(args.output).resolve(), Path(args.config).resolve()
    if not source.is_dir() or not config_path.is_file():
        raise BuildError("Source directory and configuration file must exist")
    if any("\n" in str(p) or "\r" in str(p) for p in (source, output, config_path)):
        raise BuildError("Source/config/output paths cannot contain newlines")
    if inside(source, output):
        raise BuildError("Output may not equal or contain the source directory")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise BuildError(f"Output must be empty; refusing to overwrite existing files: {output}")
    targets = list(dict.fromkeys(t.strip() for t in args.targets.split(",")))
    if not targets or any(t not in TARGETS for t in targets):
        raise BuildError("targets must be a comma-separated subset of " + ",".join(TARGETS))
    version = args.version.removeprefix("v")
    if not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version) or any(int(n) > 65535 for n in version.split(".")):
        raise BuildError("version must be MAJOR.MINOR.PATCH (each component 0..65535), optionally prefixed with v")
    cfg = load_config(config_path, targets)
    license_blob = read_blob(config_path.parent / cfg["license_file"]) if "license_file" in cfg else None
    warnings = []
    if "copilot" in targets and any("example.com" in str(v) for v in cfg["publisher"].values()):
        warnings.append("Replace example.com publisher URLs before installation/distribution")
    inventory = discover(source, output, cfg, config_path, warnings)
    bundles = [(p, select_skills(inventory, p)) for p in cfg["plugins"]]
    assigned_origins = {o for _, skills in bundles for s in skills for o in s.origins}
    unassigned = sorted({o for s in inventory for o in s.origins} - assigned_origins)
    if unassigned:
        warnings.append(f"{len(unassigned)} discovered skill source(s) were not selected by any bundle")
    catalog = cfg.get("catalog_name", "skill-plugins")
    packages, archives, portability = [], [], []
    plans = {target: target_bundles(bundles, target, warnings) for target in targets}
    logical_bundles = {p["name"]: skills for p, skills in bundles}
    install_sets = []
    for target in targets:
        for plugin, skills in bundles:
            parts = [p["name"] for p, _, origin in plans[target] if origin == plugin["name"]]
            if len(parts) > 1:
                skill_parts = {s.name: p["name"] for p, ss, origin in plans[target] if origin == plugin["name"] for s in ss}
                crossings = [{"skill": s.name, "requires": dep, "from_plugin": skill_parts[s.name], "in_plugin": skill_parts[dep]}
                             for s in skills for dep in plugin.get("requires", {}).get(s.name, [])
                             if skill_parts[s.name] != skill_parts[dep]]
                install_sets.append({"bundle": plugin["name"], "target": target, "install_all": parts, "cross_plugin_dependencies": crossings})
                if crossings:
                    warnings.append(f"{plugin['name']}/{target}: {len(crossings)} declared dependency edge(s) cross plugin parts; verify host invocation after installing every part")
    with tempfile.TemporaryDirectory(prefix="skill-plugin-build-") as temp:
        staging = Path(temp)
        for target in targets:
            for plugin, selected, logical_name in plans[target]:
                root = staging / target / "plugins" / plugin["name"]
                for skill in selected:
                    for rel, blob in skill.files.items():
                        write_blob(root / "skills" / skill.name / rel, blob)
                    if license_blob:
                        # Retain any skill-specific license; add the collection license when absent.
                        existing = next((p for p in skill.files if p.casefold() == "license.md"), None)
                        if existing is None:
                            write_blob(root / "skills" / skill.name / "license.md", license_blob)
                overlay = plugin.get("overlays", {}).get(target)
                applied = apply_overlay(root, config_path.parent / overlay, {s.name for s in selected},
                                        {s.name for s in logical_bundles[logical_name]}) if overlay else []
                actual, omitted = [], []
                for skill in selected:
                    skill_root = root / "skills" / skill.name
                    files = read_tree(skill_root)
                    if target == "gemini-app":
                        patterns = plugin.get("gemini_app", {}).get("exclude_files", [])
                        for rel in list(files):
                            if excluded(rel, patterns):
                                # Only remove generated staging copies explicitly selected by configuration.
                                (skill_root / rel).unlink()
                                del files[rel]
                                omitted.append(f"skills/{skill.name}/{rel}")
                    staged = parse_skill(files, f"{plugin['name']}/{target}/{skill.name}", skill.source_path)
                    if staged.name != skill.name:
                        raise BuildError(f"Overlay cannot change a skill's name: {skill.name}")
                    if target == "copilot":
                        check_copilot_skill(staged)
                    elif target == "gemini-app":
                        check_gemini_app_skill(staged)
                        check_links(skill_root, files, warnings, f"{plugin['name']}/{target}/{skill.name}")
                    actual.append({"name": skill.name, "sources": list(skill.origins), "source_sha256": skill.digest,
                                   "packaged_sha256": staged.digest, "file_count": len(files),
                                   "uncompressed_bytes": sum(len(b.data) for b in files.values())})
                    for rel, blob in files.items():
                        if rel.endswith(".md"):
                            text = blob.data.decode("utf-8-sig")
                            for kind, pattern in PORTABILITY.items():
                                if re.search(pattern, text):
                                    portability.append({"plugin": plugin["name"], "target": target, "skill": skill.name, "file": rel, "reason": kind})
                        if target == "gemini-app" and (blob.executable or PurePosixPath(rel).suffix.lower() in (".py", ".sh", ".js", ".ts", ".bash", ".ps1")):
                            if GEMINI_NETWORK_HINT.search(blob.data.decode("utf-8", errors="ignore")):
                                portability.append({"plugin": plugin["name"], "target": target, "skill": skill.name, "file": rel,
                                                    "reason": "script may access the network, which Gemini app skills do not support"})
                if target == "gemini-app":
                    for info in actual:
                        skill_name = info["name"]
                        prefix = f"skills/{skill_name}/"
                        # '--' cannot occur in valid bundle/skill names, preventing filename collisions.
                        relative = f"archives/{plugin['name']}--{skill_name}-gemini-app-{version}.zip"
                        digest = deterministic_zip(root / "skills" / skill_name, staging / relative)
                        packages.append({"plugin": plugin["name"], "bundle": logical_name, "target": target,
                                         "archive": relative, "sha256": digest, "skills": [info],
                                         "requires": sorted(set(plugin.get("requires", {}).get(skill_name, []))),
                                         "overridden_files": [p for p in applied if p.startswith(prefix)],
                                         "omitted_files": [p for p in omitted if p.startswith(prefix)]})
                        archives.append({"path": relative, "sha256": digest})
                    if omitted:
                        warnings.append(f"{plugin['name']}/gemini-app: omitted {len(omitted)} resource file(s) explicitly selected by gemini_app.exclude_files")
                    continue
                make_manifest(root, target, plugin, cfg, version, config_path, warnings)
                check_links(root, read_tree(root), warnings, f"{plugin['name']}/{target}")
                relative = f"archives/{plugin['name']}-{target}-{version}.zip"
                digest = deterministic_zip(root, staging / relative)
                packages.append({"plugin": plugin["name"], "bundle": logical_name, "target": target, "archive": relative, "sha256": digest,
                                 "skills": actual, "overridden_files": applied})
                archives.append({"path": relative, "sha256": digest})
        copilot_ids = [json.loads((staging / "copilot/plugins" / p["plugin"] / "manifest.json").read_text())["id"]
                       for p in packages if p["target"] == "copilot"]
        if len(copilot_ids) != len(set(copilot_ids)):
            raise BuildError("Two Copilot packages use the same app_id; each plugin needs its own stable UUID")
        if portability and args.strict_portability == "true":
            detail = "; ".join(f"{p['plugin']}/{p['target']}/{p['skill']}: {p['reason']}" for p in portability[:8])
            raise BuildError(f"Host-specific instruction hints found ({len(portability)}): {detail}. Review or provide target overlays.")
        for target in ("chatgpt", "claude"):
            if target not in targets:
                continue
            if target == "chatgpt":
                entries = [{"name": p["name"], "source": {"source": "local", "path": "./plugins/" + p["name"]},
                            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "category": "Productivity"}
                           for p, _ in bundles]
                file, data = ".agents/plugins/marketplace.json", {"name": catalog, "plugins": entries}
            else:
                entries = [{"name": p["name"], "source": "./plugins/" + p["name"], "description": p["description"]} for p, _ in bundles]
                file, data = ".claude-plugin/marketplace.json", {"name": catalog, "owner": {"name": cfg["publisher"]["name"]}, "plugins": entries}
            write_json(staging / target / file, data)
            relative = f"archives/{catalog}-{target}-marketplace-{version}.zip"
            archives.append({"path": relative, "sha256": deterministic_zip(staging / target, staging / relative)})
        gemini_guide = write_gemini_guide(staging, packages)
        report = {
            "builder_version": "0.3.0", "package_version": version, "targets": targets,
            "discovered_sources": len(inventory), "included_skills": len({(s.name, s.digest) for _, ss in bundles for s in ss}),
            "bundle_count": len(bundles), "packages": packages, "archives": archives,
            "unassigned_sources": unassigned, "warnings": sorted(set(warnings)), "portability_hints": portability, "install_sets": install_sets,
            "gemini_install_guide": gemini_guide,
            "validation": {"scope": "Local structural and documented format checks; not complete vendor schema validation or host installation",
                           "runtime_tested": False, "connectors_generated": False},
        }
        report["platform_archives"] = write_platform_bundles(staging, catalog, report, license_blob)
        write_json(staging / "build-report.json", report)
        all_archives = archives + report["platform_archives"]
        write_blob(staging / "SHA256SUMS", Blob("".join(f"{a['sha256']}  {a['path']}\n" for a in sorted(all_archives, key=lambda x: x["path"])).encode()))
        output.mkdir(parents=True, exist_ok=True)
        shutil.copytree(staging, output, dirs_exist_ok=True)
    emit_outputs(output, report)
    return report


def emit_outputs(output, report):
    outputs = {"output-directory": str(output), "report": str(output / "build-report.json"),
               "archives": json.dumps([str(output / a["path"]) for a in report["archives"]]),
               "platform-archives": json.dumps([str(output / a["path"]) for a in report["platform_archives"]]),
               "platform-archive-count": str(len(report["platform_archives"])),
               "archive-count": str(len(report["archives"])), "skill-count": str(report["included_skills"]),
               "gemini-install-guide": str(output / report["gemini_install_guide"]) if report["gemini_install_guide"] else ""}
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as file:
            for key, value in outputs.items():
                file.write(f"{key}={value}\n")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        summary = ["## Skill plugin packages", "", "| Plugin | Target | Skills |", "|---|---|---|"]
        summary += [f"| {html.escape(p['plugin'])}{' / ' + p['skills'][0]['name'] if p['target'] == 'gemini-app' else ''} | {p['target']} | {len(p['skills'])} |" for p in report["packages"]]
        summary += ["", "## Platform downloads", "", "Extract the bundle for your host, then install the ZIPs inside archives/.", "",
                    "| Platform | Download bundle | Inner ZIPs |", "|---|---|---|"]
        summary += [f"| {a['target']} | `{PurePosixPath(a['path']).name}` | {len(a['archives'])} |" for a in report["platform_archives"]]
        summary += ["", f"Built {len(report['archives'])} package ZIPs and {len(report['platform_archives'])} platform bundles. See build-report.json for provenance and compatibility hints.",
                    "", "Validation covers local structure; target applications have not been exercised by this build."]
        if report["gemini_install_guide"]:
            summary += ["", "See GEMINI-INSTALL.md for Gemini app imports, dependencies, and CLI extension installation."]
        if report["warnings"] or report["portability_hints"]:
            summary += ["", f"Review {len(report['warnings'])} build warning(s) and {len(report['portability_hints'])} portability hint(s)."]
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as file:
            file.write("\n".join(summary) + "\n")
    print(f"Built {len(report['archives'])} package ZIPs and {len(report['platform_archives'])} platform bundles from {report['included_skills']} distinct skills across {report['bundle_count']} bundle(s).")
    print(f"Report: {output / 'build-report.json'}")
    for warning in report["warnings"]:
        print(f"WARNING: {warning}")
    if report["portability_hints"]:
        print(f"WARNING: {len(report['portability_hints'])} host-specific instruction hint(s); review build-report.json")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=".")
    parser.add_argument("--config", default="plugin-bundles.yml")
    parser.add_argument("--output", default="dist/skill-plugins")
    parser.add_argument("--targets", default=",".join(TARGETS))
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--strict-portability", choices=("true", "false"), default="false")
    args = parser.parse_args()
    try:
        build(args)
    except (BuildError, OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
