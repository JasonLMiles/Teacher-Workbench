# Teacher Workbench

**Practical AI skills that assist teachers and are designed to give teachers back time.**

Teacher Workbench is an open collection of 45 reusable skills for planning, preparing materials, reviewing student work, and deciding what to teach next. It combines instructions, reference guidance, editable templates, and selected calculation tools so teachers can spend less time explaining the same workflow to an AI assistant.

Teachers set the goals, supply the classroom context, and make the instructional decisions. The package helps prepare work they can inspect and adapt. Its educational references begin with California K–12; teachers elsewhere should supply their own standards, curriculum, and local requirements.

Version: **2.0.0** · Skill prefix: **`tw-`** · Start with **`tw-orchestrator`**.

## Start here

1. Download the bundle for your AI platform from **[Releases](https://github.com/JasonLMiles/Teacher-Workbench/releases) → Assets**. See [Download a platform package](#download-a-platform-package) below for filenames and instructions. If you want to edit the source, use **Code → Download ZIP**, or clone the repository:

   ```sh
   git clone --branch main https://github.com/JasonLMiles/Teacher-Workbench.git
   cd Teacher-Workbench
   ```

2. Follow the guide for your environment:

   | Environment | Installation | Everyday use |
   |---|---|---|
   | Google: Gemini Apps, school-account Gems, and Gemini CLI | [Install](docs/platforms/google-install.md) | [Use](docs/platforms/google-use.md) |
   | Microsoft Copilot Cowork | [Install](docs/platforms/copilot-cowork-install.md) | [Use](docs/platforms/copilot-cowork-use.md) |
   | OpenAI: ChatGPT desktop/Work and Codex | [Install](docs/platforms/openai-install.md) | [Use](docs/platforms/openai-use.md) |

3. Try a familiar preparation task with material you are allowed to share:

   > Use Teacher Workbench and tw-orchestrator. I teach grade 5 mathematics. Using the attached lesson, prepare a 35-minute lesson on equivalent fractions, a worked example, two supported practice tasks, and a three-question exit ticket with a separate key. Keep the learning goal intact and identify assumptions I need to review.

The [platform overview](docs/platforms/readme.md) explains account differences. The [teacher guide](docs/USER_GUIDE.pdf) starts with a ten-minute task; [Word](docs/USER_GUIDE.docx) and [Markdown](docs/USER_GUIDE.md) editions are included.

## What teachers can do

- Prepare lessons, units, teaching aids, substitute packets, and activities for instructional assistants.
- Adapt access and language supports while preserving the learning goal.
- Create assessments, answer keys, rubrics, formative checks, and student reflection tools.
- Review deidentified work, plan flexible intervention groups, and prepare next steps.
- Rehearse lessons, review materials, and draft family communication for teacher review.
- Audit grade calculations and analyze assessment evidence with documented assumptions.

The coordinating skill selects relevant specialists; it does not run all 45 for every request. See the [complete catalog](docs/SKILL_CATALOG.md) and [worked teaching workflows](docs/TEACHING_WORKFLOWS.md).

## Contents

| Location | Contents |
|---|---|
| `skills/` | 45 complete skill folders, with references, templates, and available scripts |
| `skill-packages/` | One ZIP per skill, with `SKILL.md` at the archive root, companion files, and the MIT license |
| `docs/platforms/` | Installation and usage guides for Google, Copilot Cowork, and OpenAI |
| `docs/` | Teacher guide, workflow guides, migration notes, source records, and validation scope |
| `tests/` | Synthetic numerical and workflow checks, plus package validation |
| `tools/build_skill_archives.py` | Rebuilds individual skill ZIPs and their checksums |
| `.github/workflows/build-skill-plugins.yml` | Builds plugin packages for Copilot, ChatGPT, Claude, Gemini app, and Gemini CLI |
| `plugin-bundles.yml` | Bundle selection, publisher metadata, and package configuration |
| `Teacher_Workbench_*_Prompt.md` | Detailed creation specifications and historical design context |

The source folders are authoritative. The ZIPs package those files for individual skill uploads. Appearance metadata in `agents/openai.yaml` is optional for other hosts. This source distribution does not require a plugin manifest. The retained creation specifications describe earlier packaging options; use this README and the platform guides for current setup.

## Download a platform package

1. Open **[Releases](https://github.com/JasonLMiles/Teacher-Workbench/releases)** and choose a release.
2. Expand **Assets** and download the ZIP for your platform. For package version `2.0.0`, the names are:

   | Platform | Download from Assets | Contents |
   |---|---|---|
   | Microsoft Copilot Cowork | `teacher-workbench-copilot-2.0.0-bundle.zip` | All three Copilot plugin parts |
   | OpenAI ChatGPT / Work | `teacher-workbench-chatgpt-2.0.0-bundle.zip` | ChatGPT plugin and repository marketplace |
   | Claude Cowork | `teacher-workbench-claude-2.0.0-bundle.zip` | Claude plugin and repository marketplace |
   | Google Gemini app | `teacher-workbench-gemini-app-2.0.0-bundle.zip` | All 45 individual skill uploads |
   | Google Gemini CLI | `teacher-workbench-gemini-cli-2.0.0-bundle.zip` | Gemini CLI extension |

3. Extract the download and read its `README.md`. The installable ZIPs are in **`archives/`**. Install those inner packages using your platform's guide; the outer `-bundle.zip` groups the downloads and is not itself a plugin upload. Copilot needs all three parts; Gemini app imports one skill ZIP at a time.

Each platform bundle includes its package report and checksums; Gemini bundles also include their installation guide. The individual plugin, skill, extension, and marketplace ZIPs remain available directly under release **Assets** as well. GitHub's automatically generated **Source code (zip)** and **Source code (tar.gz)** downloads contain repository source, not the generated platform packages.

If a release only shows source-code downloads, its packages have not been attached yet. For the latest build, open **[Actions → Build skill plugins](https://github.com/JasonLMiles/Teacher-Workbench/actions/workflows/build-skill-plugins.yml)**, choose a successful run, and scroll to **Artifacts**. Download the named platform bundle, or the **teacher-workbench-plugins-…** artifact for all platforms together. GitHub requires sign-in for Actions artifact downloads, and those artifacts expire; published release assets are the intended distribution point.

## Generate plugin packages

Open **[Actions → Build skill plugins](https://github.com/JasonLMiles/Teacher-Workbench/actions/workflows/build-skill-plugins.yml) → Run workflow**. Choose `main`, optionally enter a package version, and run it. Leave `release_tag` blank for an Actions-only build. The current 45 skills produce **five platform download bundles**, alongside 53 individual/plugin/marketplace ZIPs. Each platform bundle appears separately in the run's **Artifacts** list.

Pushes to `main` rebuild automatically. Pushing a `vMAJOR.MINOR.PATCH` tag creates a draft release with both the platform bundles and individual packages attached; publishing a release also runs the packaging workflow. Review a draft before publishing it.

**To add packages to an existing release such as `0.1`:** run the workflow from `main`, enter `0.1` in **release_tag**, and leave **version** blank. The workflow uses the current packager with the exact source from that tag, then uploads the packages into that release's **Assets**. It preserves the release notes and published/draft status. Repeating the run replaces matching generated assets. A tag such as `0.1` uses the package version recorded in its `skill-catalog.json` (`2.0.0` for that release); the release tag and package filename can therefore differ.

See [package generation and installation](docs/PLUGIN-PACKAGES.md) for additional setup and maintenance details.

## Requirements and practical limits

Instruction-based work needs a compatible assistant with access to the selected skill and its supporting files. The package supplies no AI subscription, account connection, or external service credentials. Reading private curriculum, writing a Google Sheet, creating a Canva design, browsing current sources, and running a schedule require the relevant host capability and authorization.

Bundled Python helpers and offline tests use Python 3.9 or later and the standard library. Scheduling examples also need an IANA timezone database; install Python's `tzdata` package on systems without one. A skill can prepare a workflow even when the host cannot execute every step, but it should identify what it actually completed.

Use your school's approved AI environment and deidentified or synthetic learner data. Review materials, keys, citations, calculations, and decisions before use. Keep private records, proprietary curriculum, and credentials out of this public repository. Linked research and third-party materials retain their own terms.

## Validation and maintenance

The suite has 55 existing offline tests for calculations and helper logic. These do not establish classroom effectiveness or measured time savings. Platform guides were checked against official documentation on **October 15, 2026**; installation in each vendor environment has not been tested for this distribution. See [validation details](docs/VALIDATION.md).

```sh
python3 -B tools/build_skill_archives.py
python3 -B tests/test_measurement.py
python3 -B tests/test_grading_growth.py
python3 -B tests/v15/test_helpers.py
python3 -B tests/validate_package.py
```

Existing TOSAGPT users can follow the [migration notes](docs/MIGRATION.md). Contributions should describe the classroom problem and include a deidentified example that makes the change reviewable. See [publication and contribution notes](docs/PUBLISHING.md).

## Why I am sharing this

I am going back to my roots in education with Teacher Workbench, both as a demonstration of one way to share reusable AI skills and as a give back to a community I learned a great deal from. The aim is to assist teachers with the preparation around teaching and give them back time.

Special thanks to **[CITE.org](https://www.cite.org/) CTO Mentor Cohort 15** for help testing.

## Copyright and license

Copyright (c) 2026 Jason Miles.

Teacher Workbench's original source, instructions, templates, and documentation are available under the **MIT License**. You may use, copy, modify, and redistribute them under its terms. Retain the copyright and permission notices in copies or substantial portions. See [license.md](license.md) for the complete license, including the warranty disclaimer. This license does not grant rights to third-party materials merely linked or referenced by the package.
