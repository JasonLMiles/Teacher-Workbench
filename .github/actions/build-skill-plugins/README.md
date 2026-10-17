# Skill Plugin Builder

A reusable GitHub Action that discovers skills recursively and packages them for **Copilot Cowork**, **ChatGPT / Work**, **Claude Cowork**, **Gemini app**, and **Gemini CLI**. It accepts both ZIP-format `.skill` exports and ordinary folders containing `SKILL.md`.

This is a working draft of a **skills-only packager**. It preserves instructions and companion files, generates platform manifests, and reports potential portability issues. It does not create MCP services, authenticate connectors, or translate tool calls automatically. The same code also runs locally.

## Start with the supplied repository layout

1. Copy this directory's contents, including `.github/`, into a GitHub repository.
2. Add your `.skill` archives and/or unpacked skill folders anywhere beneath the repository root. Nested directories are supported automatically.
3. Edit `plugin-bundles.yml`: set your publisher metadata and choose one or more bundles. The default includes every discovered skill in `team-skills`.
4. Push to `main`, open a pull request, or run **Build skill plugins** from the Actions tab.
5. Download the `skill-plugins-<run>-<attempt>` artifact. It contains plugin and extension ZIPs, individual Gemini app skill ZIPs, marketplace ZIPs, a build report, SHA-256 checksums, and `GEMINI-INSTALL.md`.

The supplied workflow uses the root `action.yml` via `uses: ./`. It creates a **draft GitHub Release** on tags such as `v1.2.3`; it does not install or publish plugins into Microsoft, OpenAI, Anthropic, or Google accounts. Publish the draft release when you are ready to offer its downloads to your users. Remove the `release` job if you only want workflow artifacts. Adjust the `main` branch trigger if your default branch has another name.

Required publisher URLs and generated icons are development placeholders. Replace them with your actual website, privacy policy, terms, and branding before distributing the Copilot packages. The action reports these placeholders in its build warnings.

## Reuse it from an existing skills repository

Place `action.yml`, `requirements.txt`, and `scripts/` together at `.github/actions/build-skill-plugins/`; put a copy of `plugin-bundles.yml` at the repository root. Use this workflow in the existing repository:

```yaml
name: Package skills
on:
  workflow_dispatch:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  package:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          persist-credentials: false

      - uses: ./.github/actions/build-skill-plugins
        id: plugins
        with:
          source: .
          config: plugin-bundles.yml
          targets: copilot,chatgpt,claude,gemini-app,gemini-cli
          version: 1.0.0
          output: dist/skill-plugins

      - uses: actions/upload-artifact@v7
        with:
          name: skill-plugins
          path: |
            dist/skill-plugins/archives/*.zip
            dist/skill-plugins/platforms/*.zip
            dist/skill-plugins/build-report.json
            dist/skill-plugins/SHA256SUMS
            dist/skill-plugins/GEMINI-INSTALL.md
          if-no-files-found: error
          compression-level: 0
```

After publishing the action in its own repository, the same step can use `OWNER/REPOSITORY@v1`. Replace that example with your real repository and release. Pin third-party actions and your published action to reviewed commit SHAs for a controlled production workflow; the draft uses documented major-version tags.

### Upgrade an existing installation

Replace the installed action's `action.yml` and `scripts/build_plugins.py` with this version; `requirements.txt` is unchanged. Add `gemini-app,gemini-cli` to any explicit `targets:` value in your workflow. If you omit `targets`, both are now included by default. Add `dist/skill-plugins/GEMINI-INSTALL.md` to your artifact upload paths. Your existing bundle configuration continues to work; Gemini app resources must pass its additional checks below.

`examples/existing-repo-workflow.yml` is a ready-to-copy workflow for the `.github/actions/build-skill-plugins/` installation. Copy it to `.github/workflows/build-skill-plugins.yml`. The root-layout workflow supplied in `.github/workflows/` continues to use `uses: ./`.

## Platform download bundles

Every selected target also receives one `platforms/<catalog>-<target>-<version>-bundle.zip`. A Copilot bundle contains every split part; ChatGPT and Claude bundles contain the plugin ZIPs and their marketplace ZIP; Gemini app bundles contain the individual skill uploads. Extract the outer bundle and install its inner archives. The original archives are preserved byte for byte. Each platform report filters packages, install sets, and portability hints to its own target.

Include `platforms/*.zip` in artifact and release uploads. The Teacher Workbench workflow also exposes each platform bundle as a separate Actions artifact. Its release job attaches both the platform bundles and individual archives, with support for published releases and manual backfills through `release_tag`. See the [repository package guide](../../../docs/PLUGIN-PACKAGES.md).

## What recursive discovery means

All of these input locations are supported in a single run:

| Input path | Discovered as |
|---|---|
| `lesson-plan.skill` | ZIP-format skill archive at the source root |
| `departments/education/grade-four/lesson-plan.skill` | Archive several directories deep |
| `teams/writing/editorial/SKILL.md` | Unpacked skill folder |
| `exports/2026/october/bundle.skill` containing `wrapper/v1/my-skill/SKILL.md` | Skill beneath nested archive wrapper directories |
| `parent/SKILL.md` and `parent/children/child/SKILL.md` | Two separate skill roots |

Discovery walks every directory under `source`; you do not need to supply a shell `**` glob. `.skill` extensions are recognized case-insensitively. `SKILL.md` itself is case-sensitive.

Within each bundle, every skill is staged as `skills/<frontmatter-name>/SKILL.md`. Organizational directories above the skill are omitted from the package. Subdirectories *inside* the skill are preserved exactly: `references/deeper/guide.md`, `scripts/python/process.py`, templates, and binary assets retain their relative paths and bytes, subject to each target’s format checks. Gemini app ZIPs are created from the contents of each individual skill directory, so `SKILL.md` is at the ZIP root. Executable flags are preserved on runners that expose POSIX permissions.

For a nested skill root, its files belong to that nearest root rather than being duplicated in the parent's resources. A `.skill` archive may contain several skill roots. Loose archive wrapper files outside those roots are omitted with a warning. Archive files inside an archive are treated as resources; they are not recursively decompressed.

The builder skips `.git`, `.hg`, `.svn`, `.venv`, `venv`, `node_modules`, `__pycache__`, `.tox`, common OS metadata, and Python bytecode. It automatically excludes the configured output directory and every configured overlay directory. Other exclusions can be set in the configuration.

## Bundle selection and dependencies

`plugins` defines logical bundles. Each bundle has a unique lowercase `name`, a display name, a description, and optional selectors:

```yaml
schema_version: 1
catalog_name: company-workflows
publisher:
  name: Your organization
  website_url: https://example.com
  privacy_url: https://example.com/privacy
  terms_url: https://example.com/terms

plugins:
  - name: teaching
    display_name: Teaching
    description: Teaching and curriculum workflows.
    include: ['name:tw-*']

  - name: finance
    display_name: Finance
    description: Finance workflows.
    include: ['path:departments/finance/**']
    exclude: ['path:**/experimental/**']
```

Use your actual publisher URLs in place of `example.com`.

- `name:` selectors match the `name` in YAML frontmatter. `*`, `?`, and character classes are supported.
- `path:` selectors match the source-relative skill folder or original archive path. They use `/` separators on every operating system. `*` matches within a path segment; `**` matches zero or more directories. `path:**/*.skill` includes archives both at the root and several levels down.
- Includes are ORed; any matching exclusion removes that source from the bundle. Omitting `include` means `['name:*']`. An empty include list or a bundle matching no skills fails.
- For several skills inside one archive, the path selector applies to the archive as a whole. Use name selectors to distinguish its individual skills.
- A skill may appear in several bundles. The report lists inputs that no bundle selected.
- Identical copies with the same name and contents are deduplicated within each bundle, preserving all source locations in the report. Different contents with the same name fail instead of overwriting each other. Use path selectors to put conflicting variants in different bundles, or rename them deliberately.

Declare required specialist skills explicitly:

```yaml
requires:
  tw-orchestrator:
    - tw-lesson-unit-planning
    - tw-assessment-design
  tw-lesson-unit-planning:
    - tw-california-curriculum-alignment
```

Dependencies are included transitively, even when they were not selected by the include patterns. A missing, explicitly excluded, or ambiguous required skill fails the build. Cyclic dependency declarations are handled without recursion loops. The action does not infer dependencies from prose or generate host-level plugin dependency declarations.

## Copilot's 20-skill package limit

Microsoft's app schema permits **20 skills per plugin**. For a larger logical bundle, the default `microsoft.split: auto` sorts skills by name and creates parts such as `team-skills-01`, `team-skills-02`, and `team-skills-03`. A 45-skill bundle produces parts containing 20, 20, and 5 skills. ChatGPT, Claude, and Gemini CLI keep the original logical bundle. Gemini app emits one ZIP per skill.

The report's `install_sets` identifies all parts that must be installed together and any declared dependency crossing between them. The builder guarantees those skill files are packaged; it does not guarantee that host-specific orchestration instructions work across plugin namespaces. Relative file links crossing a split package boundary fail validation, since those files would not exist inside that package. Use deliberate bundles or platform-specific instructions for that case.

All parts must be updated together. Sorted membership can change when you add or remove skills. Crossing the 20-skill boundary also changes one unsuffixed app into several suffixed app identities. For stable long-term deployments, define permanent bundles of at most 20 skills and use:

```yaml
microsoft:
  split: error
  app_id: 6c9ab65c-b1d6-4e07-a4a0-8443ff739b67  # Replace with your own stable UUID.
```

Without `app_id`, the app UUID is deterministically derived from `publisher.website_url` and the emitted plugin name. For automatically split bundles with an explicit base `app_id`, each part receives a deterministic derived UUID. Duplicate app IDs fail the build.

The builder also enforces Microsoft's per-skill companion limits: 20 files, 5 MB per file, and 10 MB combined. It conservatively interprets MB as decimal bytes. Invalid companion names and hidden companion files fail; the builder never drops required resources to fit the limit.

## Platform-specific overrides

Overrides let you change instructions or resources without maintaining separate source collections:

```yaml
overlays:
  copilot: overrides/copilot/my-plugin
  chatgpt: overrides/chatgpt/my-plugin
  claude: overrides/claude/my-plugin
  gemini-app: overrides/gemini-app/my-plugin
  gemini-cli: overrides/gemini-cli/my-plugin
```

These paths are relative to the configuration file. Each override directory contains paths such as `skills/article/SKILL.md` or `skills/article/references/storage.md`. Overrides replace entire files or add resources; they do not append text, delete files, or run templating. They may only address skills selected for the original logical bundle. Overrides for a different automatic Copilot part are applied when that part is built.

The builder validates the resulting skill again and disallows renaming it through an override. It also records every overridden file. Overrides cannot inject arbitrary manifests or MCP configurations; those require a separate implementation and validation path.

## Inputs and outputs

Teacher Workbench's vendored builder adds an optional top-level `license_file` configuration field, resolved relative to the configuration file. It copies that notice to `license.md` inside every selected skill when the skill has no existing case-insensitive `license.md`. Existing skill-specific notices are preserved. The final target checks include the added license in file counts and size limits.

| Input | Default | Meaning |
|---|---|---|
| `source` | `.` | Recursively searched source directory |
| `config` | `plugin-bundles.yml` | Bundle configuration |
| `output` | `dist/skill-plugins` | Empty destination directory |
| `targets` | `copilot,chatgpt,claude,gemini-app,gemini-cli` | Comma-separated subset of target formats |
| `version` | `0.1.0` | Three numeric components, optionally prefixed with `v` |
| `strict-portability` | `false` | Fail on heuristic host-specific instruction hints |

`source`, `config`, and `output` resolve from the calling process's working directory, normally the checked-out repository root. Overlay and icon paths resolve relative to the configuration file. Package versions use a common `MAJOR.MINOR.PATCH` subset with components from 0 to 65535; prerelease labels are rejected.

Outputs are `output-directory`, `report`, `archives` (a JSON array of absolute individual/marketplace ZIP paths), `archive-count`, `platform-archives` (a JSON array of absolute platform bundle ZIP paths), `platform-archive-count`, `skill-count`, and `gemini-install-guide` (empty when neither Gemini target is selected). The existing archive count excludes the new platform bundles, preserving its previous meaning. GitHub also receives a job summary. The output directory must be absent or empty; rerunning locally requires a fresh output path or deliberate removal of the old build. The builder will not erase unrelated files.

| Generated path | Purpose |
|---|---|
| `copilot/plugins/<plugin>/manifest.json` | Microsoft 365 app manifest v1.28 |
| `chatgpt/plugins/<plugin>/plugin.json` | Agent Plugins 1.0 manifest |
| `claude/plugins/<plugin>/.claude-plugin/plugin.json` | Claude plugin manifest |
| `gemini-cli/plugins/<plugin>/gemini-extension.json` | Gemini CLI extension manifest |
| `<target>/plugins/<plugin>/skills/` | Normalized skills and resources |
| `chatgpt/.agents/plugins/marketplace.json` | OpenAI repository marketplace catalog |
| `claude/.claude-plugin/marketplace.json` | Claude marketplace catalog |
| `archives/<plugin>-<target>-<version>.zip` | Individual plugin or CLI extension; contents at ZIP root |
| `archives/<bundle>--<skill>-gemini-app-<version>.zip` | One Gemini app skill; `SKILL.md` at ZIP root |
| `GEMINI-INSTALL.md` | Generated import instructions, exact package names, and declared Gemini app dependencies |
| `archives/<catalog>-<target>-marketplace-<version>.zip` | ChatGPT or Claude catalog plus all its plugin folders |
| `build-report.json` | Sources, hashes, overrides, explicit Gemini app omissions/dependencies, warnings, split install sets, and compatibility hints |
| `platforms/<catalog>-<target>-<version>-bundle.zip` | One download per selected target, containing that target’s original archives, a README, report, checksums, license when configured, and Gemini guidance when applicable |
| `SHA256SUMS` | Checksums of individual ZIPs and platform bundles; paths relative to the output directory |

ZIP ordering, timestamps, and permissions are normalized. Repeated builds with identical inputs and dependency/runtime versions produce identical ZIPs. ZIPs preserve dot-prefixed plugin metadata, avoiding artifact-upload hidden-file exclusions.

## Using the results

- **Copilot Cowork:** use the individual Copilot app ZIPs for sideloading or your tenant's custom-app distribution process. Install every package listed in a split install set. The draft targets Microsoft's documented manual-package schema v1.28 and does not add connectors.
- **ChatGPT / Work:** the marketplace ZIP contains a repository-ready catalog and plugin folders. Extract the whole marketplace ZIP, preserving `.agents/`, for the supported local/repository marketplace workflow, or commit that tree to a dedicated distribution repository for an appropriate workspace import process. A workflow artifact or GitHub Release attachment is not itself an installed marketplace. Public-directory submission is separate.
- **Gemini app:** download and upload individual skill ZIPs as described below.
- **Gemini CLI:** extract the extension ZIP, then install its folder as described below.
- **Claude Cowork:** use an individual Claude plugin ZIP for custom-plugin upload, or use the extracted Claude marketplace tree with supported marketplace distribution. Preserve `.claude-plugin/`.

The action does not commit generated catalogs back to your repository or change application settings.

## Distribute to Gemini users

### Gemini app: one importable ZIP per skill

The `gemini-app` target uses the same recursive inventory, bundle selections, and dependency graph as the other formats. It emits one ZIP per selected skill with `SKILL.md` at the root and resource subfolders preserved. A multi-skill logical bundle therefore produces several uploads. Archive names include both bundle and skill, separated by `--`, to prevent collisions between bundles.

Publish these ZIPs and the generated `GEMINI-INSTALL.md` as GitHub Release assets. In Gemini, users open **Customize → Skills → Upload**, select a skill ZIP, review it, and choose **Create**. Repeat for the skills needed by the workflow. Declared dependencies appear in the generated guide and each app package's `requires` field in `build-report.json`; users must import those skills separately. To update, use **Replace skill** with the complete new ZIP. Imported copies do not automatically track GitHub releases.

The builder enforces a conservative 100,000,000-byte uncompressed limit per skill, including instructions. It accepts UTF-8 plain-text resources, including scripts and SVG, plus signature-checked PDF, PNG, and JPEG files. Google's documentation permits other image types too; this draft intentionally validates only these explicitly supported binary formats. Office documents such as `.docx` and `.xlsx`, other binary files, and invalid PDF/image signatures fail the app build. Existing targets retain their own resource rules.

Use an app-specific overlay to adapt instructions and supply supported replacements. If you need to remove an unsupported source resource from **only** the Gemini app export, explicitly configure patterns relative to each skill root:

```yaml
plugins:
  - name: team-skills
    description: Shared team workflows.
    include: ['name:*']
    gemini_app:
      exclude_files:
        - 'assets/**/*.docx'
        - 'assets/**/*.xlsx'
    overlays:
      gemini-app: overrides/gemini-app/team-skills
```

For example, the overlay can add `skills/my-skill/assets/template.md` and replace that skill's instructions to use it. Exclusions apply after overlays and are recorded in `omitted_files`; source files and other targets are untouched. Excluding `SKILL.md` fails. Remaining inline Markdown links to omitted resources also fail. References to sibling skills' files fail for this target because each skill ZIP must stand alone; refer to separately imported skills by name in the instructions.

Gemini app scripts cannot make requests to external websites. Review network-access hints and adapt any connector-dependent workflows. The packager does not execute scripts, provision connected apps, or prove runtime compatibility. Account availability and organization settings control access to skill uploads.

### Gemini CLI: one extension per bundle

The `gemini-cli` target emits `gemini-extension.json` at the ZIP root with `name`, `version`, and `description`, plus `skills/<skill-name>/SKILL.md` and each skill's resources. It retains the configured bundle intact and supports a separate `gemini-cli` overlay. Deep organizational folders in the source are normalized to immediate children of `skills/`, which Gemini CLI discovers.

Download the extension ZIP and extract its contents into a directory such as `team-skills/`. Install from your terminal:

```bash
gemini extensions install ./team-skills
```

Restart Gemini CLI, then use `/skills list` to confirm discovery. The generated guide gives the exact ZIP filename and command for each bundle.

For URL-based installation, publish the generated extension directory in a dedicated distribution repository with `gemini-extension.json` at its root. Users can run `gemini extensions install https://github.com/OWNER/EXTENSION-REPO`. A release containing multiple platform ZIPs and individual app skills does not provide the single generic extension asset expected by automatic release selection; use the local extracted-folder route for this action's mixed releases. Gallery listing is optional: Google's documentation describes the `gemini-cli-extension` repository topic and root-manifest requirements.

## Validation and limits

The build checks frontmatter, names, duplicate paths and identities, selected dependencies, missing resources referenced by simple inline relative Markdown links, target-specific companion restrictions, and package layouts. It rejects archive path traversal, symlinks, special files, encrypted archives, and case-insensitive file collisions. An archive or unpacked skill is limited to 10,000 files and 256 MiB of uncompressed content. No skill scripts execute during the build.

Portability scanning is deliberately heuristic. It flags examples such as `skill://` references, named host tool runtimes, host-local paths, ChatGPT Library references, and exact `mcp__...` tool names. For Gemini app scripts it also flags common network-access hints such as `requests`, `curl`, and URLs. This is a heuristic, not complete static analysis or a guarantee of offline execution. A hint may be intentional, including a reference appropriate for its target; absence of hints does not prove portability. The default reports hints without blocking packaging. Review them and use overrides where needed.

The Markdown checker handles straightforward inline links outside fenced code blocks. It is not a complete Markdown parser, does not check remote URLs, and cannot resolve instruction prose, dynamically constructed paths, or connector availability. Scripts are copied without installing or verifying their runtime dependencies.

This draft's built-in validation is structural and based on the cited format rules; it is not a complete embedded copy of each vendor's schema validator. Install a sample package in each target host and exercise the actual workflows before rolling out broadly. `VALIDATION.md` records the tests performed while drafting this release.

## Run locally

```bash
python -m pip install -r requirements.txt
python scripts/build_plugins.py \
  --source ./my-skills \
  --config ./plugin-bundles.yml \
  --output ./dist/skill-plugins \
  --targets copilot,chatgpt,claude,gemini-app,gemini-cli \
  --version 1.2.3
python -m unittest discover -s tests -v
```

Python 3.12 is used by the action. The supplied workflow targets GitHub-hosted Ubuntu. Other platforms have not been exercised for this draft.

## Format references

Original formats verified 2026-10-15; Gemini formats added and verified 2026-10-16 UTC. These are the upstream contracts used for the generated layouts:

- [Copilot Cowork plugin development and validation rules](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development)
- [Microsoft 365 app manifest v1.28 schema](https://developer.microsoft.com/json-schemas/teams/v1.28/MicrosoftTeams.schema.json)
- [OpenAI: Package your plugin, including repository marketplaces](https://developers.openai.com/plugins/build/plugins)
- [Agent Plugins 1.0 manifest schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)
- [Claude plugin manifest reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude marketplace creation](https://code.claude.com/docs/en/plugin-marketplaces)
- [Using plugins in Claude, including Cowork uploads](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
- [Anthropic's ZIP-format .skill packager](https://github.com/anthropics/skills/blob/main/skills/skill-creator/scripts/package_skill.py)

- [Gemini app skill uploads, supported resources, and limits](https://support.google.com/gemini/answer/17094296?hl=en)
- [Gemini CLI extension format and installation](https://geminicli.com/docs/extensions/reference/)
- [Gemini CLI repository and release distribution](https://geminicli.com/docs/extensions/releasing/)
