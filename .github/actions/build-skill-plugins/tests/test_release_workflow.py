"""Exercise the actual workflow scripts with temporary files and a fake GitHub CLI."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


WORKFLOW = Path(__file__).resolve().parents[3] / "workflows/build-skill-plugins.yml"


class ReleaseWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workflow = yaml.safe_load(WORKFLOW.read_text())

    def script(self, job, name):
        return next(s["run"] for s in self.workflow["jobs"][job]["steps"] if s.get("name") == name)

    def run_script(self, script, **env):
        return subprocess.run(["bash", "-euo", "pipefail", "-c", script], cwd=self.root,
                              env={**os.environ, **env}, text=True, capture_output=True)

    def test_legacy_tags_use_catalog_versions_and_explicit_versions_are_validated(self):
        source = self.root / "source"
        source.mkdir()
        (source / "skill-catalog.json").write_text(json.dumps({"package_version": "2.0.0"}))
        for tag, requested, expected in [("0.1", "", "2.0.0"), ("v2.1.0", "", "2.1.0"),
                                         ("", "", "2.0.0"), ("0.1", "v2.2.0", "2.2.0"),
                                         ("0.1", "invalid", None), ("", "65536.0.0", None)]:
            with self.subTest(tag=tag, requested=requested):
                output = self.root / "github-output"
                output.write_text("")
                result = self.run_script(self.script("build", "Resolve package version"), RELEASE_TAG=tag,
                                         REQUESTED_VERSION=requested, GITHUB_OUTPUT=str(output))
                if expected is None:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(output.read_text(), "")
                else:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(output.read_text(), f"value={expected}\n")

    def test_backfill_selects_the_exact_tag_and_rejects_invalid_refs(self):
        for tag, expected in [("0.1", "refs/tags/0.1"), ("v2.1.0", "refs/tags/v2.1.0"),
                              ("", "a" * 40), ("bad\nref", None), ("-bad", None)]:
            with self.subTest(tag=tag):
                output = self.root / "source-output"
                output.write_text("")
                result = self.run_script(self.script("build", "Select package source"), RELEASE_TAG=tag,
                                         GITHUB_SHA="a" * 40, GITHUB_OUTPUT=str(output))
                if expected is None:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(output.read_text(), "")
                else:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(output.read_text(), f"ref={expected}\nrelease_tag={tag}\n")

    def test_release_upload_includes_platform_and_individual_archives_without_recreating_existing_releases(self):
        for folder in ("platforms", "archives"):
            (self.root / "dist/skill-plugins" / folder).mkdir(parents=True)
            (self.root / "dist/skill-plugins" / folder / "example.zip").write_bytes(b"zip fixture")
        for file in ("build-report.json", "SHA256SUMS", "GEMINI-INSTALL.md"):
            (self.root / "dist/skill-plugins" / file).write_text("fixture")
        executable = self.root / "bin/gh"
        executable.parent.mkdir()
        executable.write_text("#!/usr/bin/env python3\nimport json, os, sys\n"
                              "with open(os.environ['GH_CALL_LOG'], 'a') as f: f.write(json.dumps(sys.argv[1:]) + '\\n')\n"
                              "sys.exit(int(os.environ['VIEW_STATUS']) if sys.argv[1:3] == ['release', 'view'] else 0)\n")
        executable.chmod(0o755)
        for exists in (True, False):
            with self.subTest(existing_release=exists):
                log = self.root / "gh-calls"
                log.write_text("")
                result = self.run_script(self.script("release", "Attach release assets or create draft release"),
                                         PATH=str(executable.parent) + os.pathsep + os.environ["PATH"],
                                         GH_CALL_LOG=str(log), VIEW_STATUS="0" if exists else "1",
                                         RELEASE_TAG="0.1", RELEASE_REPOSITORY="example/repo")
                self.assertEqual(result.returncode, 0, result.stderr)
                calls = [json.loads(line) for line in log.read_text().splitlines()]
                self.assertEqual(len(calls), 2)
                command = calls[-1]
                self.assertEqual(command[:3], ["release", "upload" if exists else "create", "0.1"])
                self.assertIn("--clobber" if exists else "--draft", command)
                for path in ("platforms/example.zip", "archives/example.zip", "build-report.json", "SHA256SUMS", "GEMINI-INSTALL.md"):
                    self.assertIn("dist/skill-plugins/" + path, command)


if __name__ == "__main__":
    unittest.main()
