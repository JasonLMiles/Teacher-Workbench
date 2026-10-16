"""Behaviour tests for recursive discovery, package formats, and file safety."""
from argparse import Namespace
import contextlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_plugins as builder


def skill_text(name, body="Complete the requested workflow."):
    metadata = yaml.safe_dump({"name": name, "description": f"Use the {name} workflow when requested."}, sort_keys=False)
    return f"---\n{metadata}---\n\n{body}\n".encode()


class BuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "inputs"
        self.source.mkdir()
        self.config = self.root / "config.yml"
        self.cfg = {
            "schema_version": 1, "catalog_name": "test-catalog",
            "publisher": {"name": "Example Team", "website_url": "https://team.test",
                          "privacy_url": "https://team.test/privacy", "terms_url": "https://team.test/terms"},
            "plugins": [{"name": "test-tools", "display_name": "Test Tools", "description": "Test workflows.", "include": ["name:*"]}],
        }
        self.output = self.source / "dist" / "plugins"

    def folder(self, relative, name, body="Complete the requested workflow."):
        root = self.source / relative
        root.mkdir(parents=True, exist_ok=True)
        (root / "SKILL.md").write_bytes(skill_text(name, body))
        return root

    def archive(self, relative, entries):
        archive = self.source / relative
        archive.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive, "w") as file:
            for name, data in entries.items():
                file.writestr(name, data)
        return archive

    def run_build(self, **kwargs):
        self.config.write_text(yaml.safe_dump(self.cfg, sort_keys=False), encoding="utf-8")
        options = dict(source=str(self.source), config=str(self.config), output=str(self.output),
                       targets="copilot,chatgpt,claude", version="v1.2.3", strict_portability="false")
        options.update(kwargs)
        with contextlib.redirect_stdout(io.StringIO()), patch.dict(os.environ, {"GITHUB_OUTPUT": "", "GITHUB_STEP_SUMMARY": ""}):
            return builder.build(Namespace(**options))

    def test_recursive_archives_folders_and_resource_bytes(self):
        folder = self.folder("department/education/grade-four/planning", "lesson-plan",
                             "Read [reference](references/deeper/notes.md) and run the supplied script.")
        (folder / "references/deeper").mkdir(parents=True)
        (folder / "references/deeper/notes.md").write_text("# Notes\n", encoding="utf-8")
        (folder / "scripts").mkdir()
        script = folder / "scripts/run.sh"
        script.write_text("#!/bin/sh\nexit 23\n", encoding="utf-8")
        script.chmod(0o755)
        self.archive("exports/quarter/final/article.skill", {
            "wrapper/deeper/article/SKILL.md": skill_text("article"),
            "wrapper/deeper/article/assets/sample.bin": b"\x00\xff\x01",
        })
        report = self.run_build()
        self.assertEqual(report["included_skills"], 2)
        self.assertEqual(len(report["archives"]), 5)
        for target in ("copilot", "chatgpt", "claude"):
            with zipfile.ZipFile(self.output / f"archives/test-tools-{target}-1.2.3.zip") as z:
                self.assertEqual(z.read("skills/article/assets/sample.bin"), b"\x00\xff\x01")
                self.assertEqual(z.read("skills/lesson-plan/references/deeper/notes.md"), b"# Notes\n")
                self.assertTrue((z.getinfo("skills/lesson-plan/scripts/run.sh").external_attr >> 16) & 0o111)
                self.assertNotIn("department", " ".join(z.namelist()))
        self.assertFalse((self.source / "ran-script").exists())

    def test_platform_manifests_and_catalogs_have_resolvable_paths(self):
        self.folder("x/y/skill", "alpha")
        self.run_build()
        ms = json.loads((self.output / "copilot/plugins/test-tools/manifest.json").read_text())
        self.assertEqual(ms["manifestVersion"], "1.28")
        self.assertEqual(ms["agentSkills"], [{"folder": "./skills/alpha"}])
        builder.check_png((self.output / "copilot/plugins/test-tools/color.png").read_bytes(), 192, "color")
        for target, manifest in (("chatgpt", "plugin.json"), ("claude", ".claude-plugin/plugin.json")):
            data = json.loads((self.output / target / "plugins/test-tools" / manifest).read_text())
            self.assertEqual(data["name"], "test-tools")
            self.assertEqual(data["version"], "1.2.3")
        for target, file in (("chatgpt", ".agents/plugins/marketplace.json"), ("claude", ".claude-plugin/marketplace.json")):
            catalog = json.loads((self.output / target / file).read_text())
            source = catalog["plugins"][0]["source"]
            path = source["path"] if isinstance(source, dict) else source
            self.assertTrue((self.output / target / path / "skills/alpha/SKILL.md").exists())
            with zipfile.ZipFile(self.output / f"archives/test-catalog-{target}-marketplace-1.2.3.zip") as z:
                self.assertIn(file, z.namelist())

    def test_root_archive_and_multiple_nested_skills(self):
        self.archive("direct.skill", {"SKILL.md": skill_text("direct"), "references/a.md": b"A"})
        self.archive("nested/deeper/multiple.skill", {
            "skills/one/SKILL.md": skill_text("one"), "skills/two/SKILL.md": skill_text("two")})
        report = self.run_build()
        self.assertEqual(report["included_skills"], 3)

    def test_nested_skill_roots_are_independent(self):
        self.folder("parent", "parent")
        self.folder("parent/children/deeper/child", "child")
        self.run_build()
        root = self.output / "claude/plugins/test-tools/skills"
        self.assertTrue((root / "child/SKILL.md").is_file())
        self.assertFalse((root / "parent/children/deeper/child/SKILL.md").exists())

    def test_identical_duplicates_deduplicate_and_record_both_sources(self):
        self.folder("a/alpha", "alpha")
        self.archive("backup/export.skill", {"alpha/SKILL.md": skill_text("alpha")})
        report = self.run_build()
        self.assertEqual(report["included_skills"], 1)
        self.assertEqual(len(report["packages"][0]["skills"][0]["sources"]), 2)

    def test_conflicting_duplicates_fail_without_partial_output(self):
        self.folder("a/alpha", "alpha", "First workflow.")
        self.folder("b/alpha", "alpha", "Different workflow.")
        with self.assertRaisesRegex(builder.BuildError, "conflicting skill name"):
            self.run_build()
        self.assertFalse(self.output.exists())

    def test_name_conflicts_can_be_partitioned_by_nested_paths(self):
        self.folder("north/a/alpha", "alpha", "North workflow.")
        self.folder("south/b/alpha", "alpha", "South workflow.")
        self.cfg["plugins"] = [{"name": side, "description": side + " workflows.", "include": [f"path:{side}/**"]}
                               for side in ("north", "south")]
        report = self.run_build()
        self.assertEqual(len(report["packages"]), 6)

    def test_transitive_required_skills_are_included(self):
        for skill in ("orchestrator", "specialist", "shared"):
            self.folder(f"nested/{skill}", skill)
        self.cfg["plugins"][0].update(include=["name:orchestrator"], requires={"orchestrator": ["specialist"], "specialist": ["shared"]})
        report = self.run_build()
        self.assertEqual(report["included_skills"], 3)

    def test_missing_or_excluded_dependency_fails(self):
        self.folder("orchestrator", "orchestrator")
        self.cfg["plugins"][0]["requires"] = {"orchestrator": ["missing"]}
        with self.assertRaisesRegex(builder.BuildError, "requires missing or excluded"):
            self.run_build()

    def test_overlays_are_excluded_from_discovery_and_applied_per_target(self):
        self.folder("original", "alpha", "Use ChatGPT Library.")
        overlay = self.source / "overrides/copilot"
        (overlay / "skills/alpha").mkdir(parents=True)
        (overlay / "skills/alpha/SKILL.md").write_bytes(skill_text("alpha", "Use the user's connected document store."))
        self.cfg["plugins"][0]["overlays"] = {"copilot": "inputs/overrides/copilot"}
        report = self.run_build()
        self.assertEqual(report["discovered_sources"], 1)
        self.assertEqual({p["target"] for p in report["portability_hints"]}, {"chatgpt", "claude"})
        copied = (self.output / "copilot/plugins/test-tools/skills/alpha/SKILL.md").read_text()
        self.assertIn("connected document store", copied)
        self.assertIn("ChatGPT Library", (self.source / "original/SKILL.md").read_text())

    def test_overlay_cannot_change_name_or_add_unselected_skill(self):
        self.folder("alpha", "alpha")
        overlay = self.root / "override/skills/beta"
        overlay.mkdir(parents=True)
        (overlay / "SKILL.md").write_bytes(skill_text("beta"))
        self.cfg["plugins"][0]["overlays"] = {"copilot": "override"}
        with self.assertRaisesRegex(builder.BuildError, "selected-skill"):
            self.run_build()

    def test_copilot_companion_limit_is_enforced(self):
        folder = self.folder("alpha", "alpha")
        for i in range(21):
            (folder / f"ref-{i}.txt").write_text("reference")
        with self.assertRaisesRegex(builder.BuildError, "20 companion files"):
            self.run_build()
        report = self.run_build(targets="chatgpt,claude")
        self.assertEqual(len(report["packages"]), 2)

    def test_bad_archive_paths_and_links_are_rejected(self):
        for entry in ("../escape", "/absolute", "C:/escape", "a\\b", "foo/../../escape"):
            with self.subTest(entry=entry):
                path = self.archive("bad.skill", {"alpha/SKILL.md": skill_text("alpha"), entry: b"bad"})
                with self.assertRaisesRegex(builder.BuildError, "Unsafe file path"):
                    self.run_build()
                path.unlink()
        info = zipfile.ZipInfo("alpha/link")
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        with zipfile.ZipFile(self.source / "link.skill", "w") as z:
            z.writestr("alpha/SKILL.md", skill_text("alpha"))
            z.writestr(info, "/etc/passwd")
        with self.assertRaisesRegex(builder.BuildError, "links, special files"):
            self.run_build()

    def test_case_collisions_and_duplicate_archive_entries_fail(self):
        self.archive("bad.skill", {"a/SKILL.md": skill_text("alpha"), "a/Ref.md": b"a", "a/ref.md": b"b"})
        with self.assertRaisesRegex(builder.BuildError, "duplicate archive entry"):
            self.run_build()

    def test_broken_relative_link_fails(self):
        self.folder("alpha", "alpha", "Read [missing](references/not-there.md).")
        with self.assertRaisesRegex(builder.BuildError, "relative link"):
            self.run_build()

    def test_empty_source_and_empty_bundle_fail(self):
        with self.assertRaisesRegex(builder.BuildError, "No .skill archives"):
            self.run_build()
        self.folder("alpha", "alpha")
        self.cfg["plugins"][0]["include"] = ["name:no-match"]
        with self.assertRaisesRegex(builder.BuildError, "matched no skills"):
            self.run_build()

    def test_existing_output_is_not_overwritten_or_ingested(self):
        self.folder("alpha", "alpha")
        self.output.mkdir(parents=True)
        (self.output / "do-not-delete.txt").write_text("keep me")
        with self.assertRaisesRegex(builder.BuildError, "refusing to overwrite"):
            self.run_build()
        self.assertEqual((self.output / "do-not-delete.txt").read_text(), "keep me")

    def test_identical_builds_have_identical_zips_and_stable_app_ids(self):
        self.folder("deep/a/alpha", "alpha")
        first = self.run_build()
        second_path = self.root / "other-output"
        second = self.run_build(output=str(second_path))
        self.assertEqual(first["archives"], second["archives"])
        file = "copilot/plugins/test-tools/manifest.json"
        self.assertEqual(json.loads((self.output / file).read_text())["id"], json.loads((second_path / file).read_text())["id"])

    def test_glob_double_star_matches_zero_or_more_directories(self):
        self.assertTrue(builder.path_match("root.skill", "**/*.skill"))
        self.assertTrue(builder.path_match("a/b/root.skill", "**/*.skill"))
        self.assertFalse(builder.path_match("a/b/root.skill", "a/*.skill"))
        self.assertTrue(builder.path_match("a/root.skill", "a/**/*.skill"))

    def test_strict_portability_fails_with_actionable_message(self):
        self.folder("alpha", "alpha", "Read skill://host/references.")
        with self.assertRaisesRegex(builder.BuildError, "Host-specific instruction hints"):
            self.run_build(strict_portability="true")
        self.assertFalse(self.output.exists())

    def test_duplicate_yaml_keys_fail(self):
        with self.assertRaisesRegex(builder.BuildError, "Duplicate YAML key"):
            builder.load_yaml("name: first\nname: second\n", "test")

    def test_large_copilot_bundle_splits_without_losing_skills_or_overlays(self):
        for i in range(45):
            self.folder(f"collection/deep/skill-{i:02d}", f"skill-{i:02d}")
        self.cfg["plugins"][0]["requires"] = {"skill-00": ["skill-44"]}
        self.cfg["plugins"][0]["microsoft"] = {"app_id": "6c9ab65c-b1d6-4e07-a4a0-8443ff739b67"}
        overlay = self.root / "overrides"
        for i in (0, 44):
            path = overlay / f"skills/skill-{i:02d}"
            path.mkdir(parents=True)
            (path / "SKILL.md").write_bytes(skill_text(f"skill-{i:02d}", "Copilot-specific instructions."))
        self.cfg["plugins"][0]["overlays"] = {"copilot": "overrides"}
        report = self.run_build()
        packages = [p for p in report["packages"] if p["target"] == "copilot"]
        self.assertEqual([len(p["skills"]) for p in packages], [20, 20, 5])
        self.assertEqual(len({s["name"] for p in packages for s in p["skills"]}), 45)
        self.assertEqual(len(report["install_sets"][0]["cross_plugin_dependencies"]), 1)
        self.assertEqual(len(report["install_sets"][0]["install_all"]), 3)
        self.assertEqual(len({json.loads((self.output / "copilot/plugins" / p["plugin"] / "manifest.json").read_text())["id"] for p in packages}), 3)
        self.assertEqual([len(p["skills"]) for p in report["packages"] if p["target"] != "copilot"], [45, 45])
        self.assertEqual(sum(len(p["overridden_files"]) for p in packages), 2)

    def test_copilot_split_can_be_disabled(self):
        for i in range(21):
            self.folder(f"s-{i}", f"s-{i}")
        self.cfg["plugins"][0]["microsoft"] = {"split": "error"}
        with self.assertRaisesRegex(builder.BuildError, "20-skill limit"):
            self.run_build()

    def test_duplicate_microsoft_id_fails(self):
        self.folder("alpha", "alpha")
        self.cfg["plugins"] = [{"name": slug, "description": "Test workflows.",
                                "microsoft": {"app_id": "6c9ab65c-b1d6-4e07-a4a0-8443ff739b67"}} for slug in ("one", "two")]
        with self.assertRaisesRegex(builder.BuildError, "same app_id"):
            self.run_build()

    def test_gemini_nested_inputs_preserve_resources_and_individual_upload_roots(self):
        folder = self.folder("departments/a/deep/parent", "parent", "Read [notes](references/deeper/notes.md).")
        (folder / "references/deeper").mkdir(parents=True)
        (folder / "references/deeper/notes.md").write_text("Reference text.", encoding="utf-8")
        script = folder / "run.sh"
        script.write_text("#!/bin/sh\nexit 23\n", encoding="utf-8")
        script.chmod(0o755)
        self.folder("departments/a/deep/parent/child/deeper", "child")
        self.archive("exports/2026/deep/bundle.skill", {
            "wrapper/v2/alpha/SKILL.md": skill_text("alpha"),
            "wrapper/v2/alpha/assets/image.png": builder.png(32),
            "wrapper/v2/alpha/assets/reference.pdf": b"%PDF-1.4\n%%EOF\n",
            "wrapper/v2/beta/SKILL.md": skill_text("beta"),
        })
        report = self.run_build(targets="gemini-app,gemini-cli")
        self.assertEqual(report["included_skills"], 4)
        self.assertEqual(len(report["archives"]), 5)
        for p in report["packages"]:
            with zipfile.ZipFile(self.output / p["archive"]) as z:
                if p["target"] == "gemini-app":
                    self.assertIn("SKILL.md", z.namelist())
                    self.assertEqual(sum(n.endswith("SKILL.md") for n in z.namelist()), 1)
                    self.assertNotIn("gemini-extension.json", z.namelist())
                    if p["skills"][0]["name"] == "parent":
                        self.assertEqual(z.read("references/deeper/notes.md"), b"Reference text.")
                        self.assertTrue((z.getinfo("run.sh").external_attr >> 16) & 0o111)
                    if p["skills"][0]["name"] == "alpha":
                        self.assertEqual(z.read("assets/image.png"), builder.png(32))
                else:
                    self.assertEqual(json.loads(z.read("gemini-extension.json")),
                                     {"name": "test-tools", "version": "1.2.3", "description": "Test workflows."})
                    for skill in ("parent", "child", "alpha", "beta"):
                        self.assertIn(f"skills/{skill}/SKILL.md", z.namelist())
                    self.assertNotIn("skills/parent/child/deeper/SKILL.md", z.namelist())

    def test_gemini_app_overlays_and_explicit_resource_exclusions(self):
        folder = self.folder("original", "alpha", "Use [template](assets/forms/template.docx).")
        (folder / "assets/forms").mkdir(parents=True)
        (folder / "assets/forms/template.docx").write_bytes(b"PK\x00\xff")
        overlay = self.source / "overrides/app/skills/alpha"
        (overlay / "assets/forms").mkdir(parents=True)
        (overlay / "SKILL.md").write_bytes(skill_text("alpha", "Use [template](assets/forms/template.md)."))
        (overlay / "assets/forms/template.md").write_text("Text template.", encoding="utf-8")
        self.cfg["plugins"][0].update(overlays={"gemini-app": "inputs/overrides/app"},
                                       gemini_app={"exclude_files": ["assets/**/*.docx"]})
        report = self.run_build(targets="gemini-app,gemini-cli")
        self.assertEqual(report["discovered_sources"], 1)
        app = next(p for p in report["packages"] if p["target"] == "gemini-app")
        self.assertEqual(app["omitted_files"], ["skills/alpha/assets/forms/template.docx"])
        self.assertNotEqual(app["skills"][0]["source_sha256"], app["skills"][0]["packaged_sha256"])
        with zipfile.ZipFile(self.output / app["archive"]) as z:
            self.assertIn("assets/forms/template.md", z.namelist())
            self.assertNotIn("assets/forms/template.docx", z.namelist())
        self.assertEqual((self.output / "gemini-cli/plugins/test-tools/skills/alpha/assets/forms/template.docx").read_bytes(), b"PK\x00\xff")
        self.assertTrue((folder / "assets/forms/template.docx").exists())

    def test_gemini_app_rejects_unsupported_resources_without_partial_output(self):
        folder = self.folder("alpha", "alpha")
        for filename, data in (("template.docx", b"text"), ("sheet.xlsx", b"PK\x00"),
                               ("resource.bin", b"\x00\xff"), ("fake.png", b"not a PNG")):
            with self.subTest(filename=filename):
                path = folder / filename
                path.write_bytes(data)
                with self.assertRaisesRegex(builder.BuildError, "unsupported Gemini app resource"):
                    self.run_build(targets="chatgpt,gemini-app")
                self.assertFalse(self.output.exists())
                path.unlink()

    def test_gemini_app_size_limit_includes_skill_instructions(self):
        self.folder("alpha", "alpha")
        size = len(skill_text("alpha"))
        with patch.object(builder, "GEMINI_APP_MAX_BYTES", size - 1):
            with self.assertRaisesRegex(builder.BuildError, "100 MB"):
                self.run_build(targets="gemini-app")
        with patch.object(builder, "GEMINI_APP_MAX_BYTES", size):
            report = self.run_build(targets="gemini-app")
        self.assertEqual(report["packages"][0]["skills"][0]["uncompressed_bytes"], size)

    def test_gemini_app_links_cannot_cross_individual_package_boundaries(self):
        self.folder("alpha", "alpha", "Read [beta](../beta/SKILL.md).")
        self.folder("beta", "beta")
        with self.assertRaisesRegex(builder.BuildError, "out-of-package"):
            self.run_build(targets="gemini-app")
        self.run_build(targets="gemini-cli")

    def test_gemini_app_exclusions_cannot_remove_entrypoint_or_break_links(self):
        folder = self.folder("alpha", "alpha", "Read [notes](notes.md).")
        (folder / "notes.md").write_text("Notes", encoding="utf-8")
        self.cfg["plugins"][0]["gemini_app"] = {"exclude_files": ["**/*.md"]}
        with self.assertRaisesRegex(builder.BuildError, "cannot remove SKILL.md"):
            self.run_build(targets="gemini-app")
        self.cfg["plugins"][0]["gemini_app"] = {"exclude_files": ["notes.md"]}
        with self.assertRaisesRegex(builder.BuildError, "relative link"):
            self.run_build(targets="gemini-app")

    def test_gemini_app_network_script_hints_and_strict_mode(self):
        folder = self.folder("alpha", "alpha")
        (folder / "fetch.py").write_text("import requests\nrequests.get('https://example.com')\n", encoding="utf-8")
        with self.assertRaisesRegex(builder.BuildError, "network"):
            self.run_build(targets="gemini-app", strict_portability="true")
        report = self.run_build(targets="gemini-app,gemini-cli")
        self.assertEqual({p["target"] for p in report["portability_hints"]}, {"gemini-app"})

    def test_gemini_dependency_imports_and_deterministic_archives(self):
        for skill in ("orchestrator", "specialist", "shared"):
            self.folder(f"deep/{skill}", skill)
        self.cfg["plugins"][0].update(include=["name:orchestrator"],
                                       requires={"orchestrator": ["specialist"], "specialist": ["shared"]})
        report = self.run_build(targets="gemini-app,gemini-cli")
        second = self.run_build(targets="gemini-app,gemini-cli", output=str(self.root / "second"))
        self.assertEqual(report["archives"], second["archives"])
        app = [p for p in report["packages"] if p["target"] == "gemini-app"]
        self.assertEqual(len(app), 3)
        self.assertEqual(next(p for p in app if p["skills"][0]["name"] == "orchestrator")["requires"], ["specialist"])
        guide = (self.output / report["gemini_install_guide"]).read_text()
        for package in report["packages"]:
            self.assertIn(Path(package["archive"]).name, guide)
        self.assertIn("Dependencies are separate imports", guide)

    def test_gemini_app_archive_names_are_unique_across_bundles(self):
        self.folder("first", "b-c")
        self.folder("second", "c")
        self.cfg["plugins"] = [
            {"name": "a", "description": "First", "include": ["name:b-c"]},
            {"name": "a-b", "description": "Second", "include": ["name:c"]},
        ]
        report = self.run_build(targets="gemini-app")
        paths = [p["path"] for p in report["archives"]]
        self.assertEqual(len(set(paths)), 2)
        for path in paths:
            self.assertTrue((self.output / path).is_file())

    def test_collection_license_is_included_in_every_target(self):
        self.folder("deep/alpha", "alpha")
        (self.root / "license.md").write_text("Collection copyright and permission notice.\n", encoding="utf-8")
        self.cfg["license_file"] = "license.md"
        report = self.run_build(targets=",".join(builder.TARGETS))
        for p in report["packages"]:
            path = "license.md" if p["target"] == "gemini-app" else "skills/alpha/license.md"
            with zipfile.ZipFile(self.output / p["archive"]) as z:
                self.assertEqual(z.read(path), b"Collection copyright and permission notice.\n")

    def test_collection_license_preserves_existing_skill_license(self):
        folder = self.folder("alpha", "alpha")
        (folder / "LICENSE.md").write_text("Skill-specific license.\n", encoding="utf-8")
        (self.root / "license.md").write_text("Collection license.\n", encoding="utf-8")
        self.cfg["license_file"] = "license.md"
        report = self.run_build(targets="gemini-app")
        with zipfile.ZipFile(self.output / report["packages"][0]["archive"]) as z:
            self.assertEqual(z.read("LICENSE.md"), b"Skill-specific license.\n")
            self.assertNotIn("license.md", z.namelist())

    def test_command_line_defaults_build_five_targets_and_emit_github_outputs(self):
        self.folder("very/deep/alpha", "alpha")
        self.config.write_text(yaml.safe_dump(self.cfg), encoding="utf-8")
        out, summary = self.root / "github-output", self.root / "github-summary"
        result = subprocess.run([sys.executable, str(Path(builder.__file__)), "--source", str(self.source),
                                 "--config", str(self.config), "--output", str(self.output)],
                                env={**os.environ, "GITHUB_OUTPUT": str(out), "GITHUB_STEP_SUMMARY": str(summary)},
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((self.output / "build-report.json").read_text())
        self.assertEqual(set(report["targets"]), {"copilot", "chatgpt", "claude", "gemini-app", "gemini-cli"})
        outputs = dict(line.split("=", 1) for line in out.read_text().splitlines())
        self.assertEqual(outputs["archive-count"], "7")
        self.assertEqual(Path(outputs["gemini-install-guide"]).name, "GEMINI-INSTALL.md")
        self.assertTrue(Path(outputs["gemini-install-guide"]).is_file())
        self.assertEqual(len(json.loads(outputs["archives"])), 7)
        self.assertIn("gemini-app", summary.read_text())
        self.assertIn("gemini-cli", summary.read_text())


if __name__ == "__main__":
    unittest.main()
