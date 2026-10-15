"""Build reproducible, single-skill uploads from the canonical source folders."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
import hashlib

ROOT = Path(__file__).resolve().parents[1]
STAMP = (2026, 10, 15, 0, 0, 0)


def main():
    output = ROOT / "skill-packages"
    output.mkdir(exist_ok=True)
    license_bytes = (ROOT / "license.md").read_bytes()
    archives = []
    for folder in sorted((ROOT / "skills").glob("tw-*")):
        if not (folder / "SKILL.md").is_file():
            raise ValueError(f"Missing SKILL.md: {folder}")
        path = output / (folder.name + ".zip")
        members = {p.relative_to(folder).as_posix(): p.read_bytes()
                   for p in folder.rglob("*") if p.is_file()
                   and "__pycache__" not in p.parts and p.suffix != ".pyc"}
        members["license.md"] = license_bytes
        with ZipFile(path, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
            for name, content in sorted(members.items()):
                item = ZipInfo(name, STAMP)
                item.compress_type = ZIP_DEFLATED
                item.create_system = 3
                item.external_attr = 0o100644 << 16
                archive.writestr(item, content)
        archives.append(path)
    checksum_text = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n"
                            for p in archives)
    (output / "SHA256SUMS").write_text(checksum_text, encoding="utf-8")
    print(f"Built {len(archives)} skill ZIPs with root-level SKILL.md and MIT license.")


if __name__ == "__main__":
    main()
