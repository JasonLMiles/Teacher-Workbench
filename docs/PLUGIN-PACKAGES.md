# Generate Teacher Workbench plugins

The **Build skill plugins** GitHub Actions workflow packages the current source into five target formats. It searches recursively for unpacked `SKILL.md` folders and ZIP-format `.skill` files, selects `tw-*` skills, and preserves their resource subfolders. Existing ZIPs under `skill-packages/` are excluded so the canonical sources remain authoritative.

## Run a build

1. Open [Actions → Build skill plugins](https://github.com/JasonLMiles/Teacher-Workbench/actions/workflows/build-skill-plugins.yml).
2. Select **Run workflow**, choose `main`, and optionally enter a version such as `2.0.1`. Leave it blank to use `package_version` in `skill-catalog.json`.
3. Wait for the build and packager tests to finish.
4. Open the completed run and download its **teacher-workbench-plugins-…** artifact under **Artifacts**. Extract that download to get the individual packages, build report, checksums, and Gemini installation guide.

The workflow also runs on pushes to `main`, pull requests, and `v*` tags. A version tag builds the same packages and creates a **draft** GitHub Release with the download assets attached. Review and publish that draft when ready. This repository's visibility controls who can access its runs and releases.

## Packages produced

For the current 45 skills and version `2.0.0`, the build creates 53 ZIPs:

| Target | Files | Installation |
|---|---|---|
| Copilot Cowork | Three `teacher-workbench-01/02/03-copilot-2.0.0.zip` packages containing 20, 20, and 5 skills | Use the tenant's custom-app/plugin upload process; install all three parts |
| ChatGPT / Work | `teacher-workbench-chatgpt-2.0.0.zip` and `teacher-workbench-chatgpt-marketplace-2.0.0.zip` | Use the plugin or extracted repository marketplace through the host's supported installation process |
| Claude Cowork | `teacher-workbench-claude-2.0.0.zip` and `teacher-workbench-claude-marketplace-2.0.0.zip` | Upload the individual plugin, or distribute the extracted marketplace |
| Gemini app | 45 `teacher-workbench--tw-<skill>-gemini-app-2.0.0.zip` files | **Customize → Skills → Upload**; one ZIP per skill |
| Gemini CLI | `teacher-workbench-gemini-cli-2.0.0.zip` | Extract into `teacher-workbench/`, then run `gemini extensions install ./teacher-workbench` |

Install the complete suite when using the full orchestrator. It still selects relevant specialists for each task. Copilot parts must be updated together because sorted membership can change as skills are added or removed. Each exported skill includes the repository's MIT license. A GitHub artifact is a download bundle; install the individual packages appropriate for your host.

`GEMINI-INSTALL.md` contains exact Gemini download names and instructions. `build-report.json` records selected sources, file hashes, package membership, validation warnings, and portability hints. `SHA256SUMS` records the archive checksums; its paths are relative to the builder output directory.

For one-command Gemini CLI installation from a GitHub URL, publish the extracted extension tree in a dedicated distribution repository with `gemini-extension.json` at the root. Use the local extracted-folder command above with this repository's mixed release assets.

## Configuration and maintenance

- `plugin-bundles.yml` selects the source skills, publisher metadata, license, and target-specific options.
- `.github/actions/build-skill-plugins/` contains the reusable builder and its tests.
- `.github/workflows/build-skill-plugins.yml` connects the builder to Actions, artifacts, and tagged draft releases.
- The workflow's `targets` value is `copilot,chatgpt,claude,gemini-app,gemini-cli`. Remove a target to build only the formats you need.

Edit skills under `skills/` and commit the change to rebuild the packages. The builder also handles additional nested source directories; skill names must remain unique within the bundle. It never executes the skill scripts while packaging. The [builder reference](../.github/actions/build-skill-plugins/README.md) documents selection patterns, target overlays, resource exclusions, and local execution.

Gemini app packages must satisfy its resource restrictions. The builder checks the 100 MB limit and supported text/PDF/PNG/JPEG resources. Its network-script scan flags the Learning Commons API helper because uploaded Gemini app scripts cannot access the internet; that workflow needs an available authorized host connection or supplied reference data. A successful package build verifies structure, not live connector access or model behavior.

The Copilot packages currently use generated development icons. Supply approved 192×192 color and 32×32 outline PNGs using the `microsoft.color_icon` and `microsoft.outline_icon` configuration fields before wider distribution. The publisher links point to this repository and its notices; use links accessible to your intended audience when publishing outside it.

## Run locally

From the repository root, using Python 3.12:

```sh
python -m pip install -r .github/actions/build-skill-plugins/requirements.txt
python .github/actions/build-skill-plugins/scripts/build_plugins.py \
  --source . --config plugin-bundles.yml \
  --output dist/skill-plugins --version 2.0.0
python -m unittest discover -s .github/actions/build-skill-plugins/tests -v
```

Use an absent or empty output directory; the builder refuses to overwrite a previous build. `dist/` is ignored by Git. Keep the existing individual-skill ZIP workflow in `tools/build_skill_archives.py` for consumers who use those source-distribution uploads.

## Privacy and data handling

The packages contain instructions, reference material, templates, and scripts from this repository. Teacher Workbench supplies no hosted service, account credentials, or telemetry service. Packaging does not execute skill scripts or connect to curriculum systems.

When a teacher uses a package, the chosen AI host and any connected services process the prompts, files, and tool requests under their own terms, settings, and organization policies. Some skills can use external sources or services when the host supports them and the user authorizes access. Use approved environments and deidentified or synthetic learner data, as described in the main README. Keep student records, private curriculum, secrets, and credentials out of repository contents and build artifacts.

The [MIT license](../license.md) governs the original distributed materials; third-party referenced materials retain their own terms.
