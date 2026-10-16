# Draft validation

Builder 0.2.1 includes Teacher Workbench's collection-license option. The 0.2.0 base was validated locally on 2026-10-16 UTC with Python 3.12.14 and PyYAML 6.0.3. Original-format schema checks were performed on 2026-10-15.

## Completed

- **34 automated tests passed.** The original 24 checks cover recursive folder/archive discovery, nested wrappers and skill roots, resource bytes and executable flags, duplicate names and paths, bundle partitioning, transitive dependencies, target overrides, Copilot limits and automatic splitting, stable app identities, unsafe ZIP entries, broken links, empty input, existing-output protection, reproducible archives, glob semantics, duplicate YAML keys, and strict portability hints.
- **10 Gemini tests passed as part of that suite.** They cover nested sources and preserved resource subfolders; one SKILL.md at each app ZIP root; CLI manifests and flat skill discovery; target-specific overlays and explicit exclusions; rejected binary/Office resources; size-boundary enforcement including instructions; cross-skill file-link rejection; entrypoint/link protection after exclusions; network-script hints and strict mode; separately imported dependencies; deterministic Gemini ZIPs; collision-free filenames across bundles; and the command-line defaults with GitHub outputs and summary. One test can cover several related assertions.
- **Command-line integration passed with all five targets.** A synthetic collection of 45 skill folders several directories deep produced three Copilot app ZIPs, one ChatGPT plugin ZIP, one Claude plugin ZIP, 45 Gemini app skill ZIPs, one Gemini CLI extension, and two marketplace ZIPs: **53 ZIPs total**. Every checksum was verified. Each Gemini app ZIP had its SKILL.md and nested reference file at the expected paths; the CLI extension included all 45 skills. The generated installation guide listed every Gemini archive and the declared dependency. The automated CLI test also verified GitHub action outputs and the job summary.
- **Original sample manifests passed official JSON schemas on 2026-10-15.** The three Microsoft manifests were checked against Microsoft's v1.28 schema, and the ChatGPT manifest against Agent Plugins 1.0.0, using jsonschema 4.26.0 with format checking. This earlier schema verification was not repeated for the Gemini update; existing manifest behavior remains covered by the automated regression tests. The action's built-in checks do not embed those complete schemas.
- **Action and workflow YAML parsed successfully**, including composite run-step shell declarations and expected workflow triggers.
- **Python syntax compilation passed.**

## Not exercised

- Execution on a hosted GitHub Actions runner, including downloading actions, installing Python/dependencies, artifact upload, and draft release creation.
- Installation or execution inside Copilot Cowork, ChatGPT, Claude Cowork, Gemini app, or Gemini CLI; vendor upload/marketplace review.
- Real user skill content, connector access, script runtime dependencies, model behavior, and cross-plugin orchestration after Copilot splitting.
- Windows or macOS runners.
- Claude's own plugin validator or a complete vendor validator for the marketplace catalogs.
- Gemini's live upload validation, script execution, account rollout, or repository/release extension installation. Gemini file-type checks are conservative and network checks are heuristic.

The original standalone draft validation did not modify a user repository or application account. Synthetic test fixtures were generated in temporary directories and are not included as installable skills.

## Reproduce the automated tests

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Schema sources

- [Microsoft 365 app manifest v1.28](https://developer.microsoft.com/json-schemas/teams/v1.28/MicrosoftTeams.schema.json)
- [Agent Plugins manifest 1.0.0](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)

The manifest schema checks validate package metadata, not whether the skills' instructions or dependencies work in the destination host.

## Teacher Workbench integration

- All **36** packager tests passed locally, including two collection-license checks.
- The actual 45 Teacher Workbench skill folders produced **53 ZIPs** across all five targets.
- Every exported skill retained the repository MIT license, every archive checksum matched, and the repository source skill files were unchanged.
- Workflow, composite action, and bundle YAML parsed successfully. GitHub-hosted execution is recorded separately in the repository Actions history.
