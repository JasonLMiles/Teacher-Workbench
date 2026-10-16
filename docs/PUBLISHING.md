# Source publication and contributions

This edition is the Teacher Workbench source distribution. Its initial publication branch is `initial` in [JasonLMiles/Teacher-Workbench](https://github.com/JasonLMiles/Teacher-Workbench). The current setup instructions are in the [README](../readme.md) and [platform guides](platforms/readme.md).

## What to share

Share a reviewed branch or commit, or the repository ZIP. Individual files in `skill-packages/` are single-skill upload archives, not a whole-suite installer. Each carries the MIT license. Preserve that license when redistributing source folders too. The original creation specifications remain as design records; their plugin packaging directions are outside this source release's setup workflow.

## Propose a change

Describe the teacher's problem, the expected result, and the relevant skill. Use synthetic or deidentified examples. Keep source citations attached to claims and keep the teacher's decisions explicit. Preserve scripts' input-policy distinctions, including missing evidence versus zero scores.

Edit canonical files under `skills/`, then rebuild archives with `python3 -B tools/build_skill_archives.py`. Run the relevant existing numerical/helper checks and `python3 -B tests/validate_package.py`. Update the catalog and guides if behavior changes. Record whether a result was checked offline, through a live host, or with a classroom workflow; keep those claims separate.

A useful report includes the host, skill name, package version or commit, a reproducible prompt, a deidentified input, and what needed correction. Do not include student records, credentials, or proprietary curriculum in issues or pull requests.

## Release checks

Confirm all intended source files are present, archives match the source, local links resolve, the copyright notice is retained, and the platform documentation check date is explicit. Review source and tests before publishing. Avoid committing generated local installation folders, caches, or account-specific configuration.
