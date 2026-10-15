# Choose your Teacher Workbench setup

Official documentation checked **October 15, 2026**. Interfaces, account eligibility, and organization settings can change. These instructions are documentation-reviewed; this release has not been installed and exercised in every vendor environment.

| Environment | Route | Guides |
|---|---|---|
| Gemini Apps with Skills | Upload individual ZIPs | [Install](google-install.md) · [Use](google-use.md) |
| School Google account with Gems | Adapt a focused workflow into a Gem | [Install](google-install.md#school-account-or-gems-route) · [Use](google-use.md) |
| Gemini CLI | Install complete local folders | [Install](google-install.md#gemini-cli-route) · [Use](google-use.md) |
| Microsoft Copilot Cowork | Upload individual ZIPs in Customize | [Install](copilot-cowork-install.md) · [Use](copilot-cowork-use.md) |
| ChatGPT desktop / Codex local | Copy folders to a supported skill location | [Install](openai-install.md) · [Use](openai-use.md) |
| ChatGPT web without standalone skill installation | Attach selected source files for the task | [Install](openai-install.md#chatgpt-web-or-a-workspace-without-local-skills) · [Use](openai-use.md) |

## A manageable first set

For a lesson-preparation trial, install `tw-orchestrator`, `tw-curriculum-search`, `tw-curriculum-document-intake`, `tw-lesson-unit-planning`, `tw-differentiation-accessibility`, `tw-multilingual-instruction`, `tw-formative-checks`, and `tw-pedagogical-review`. Add your subject specialist. The [catalog](../SKILL_CATALOG.md) describes all 45.

Some requests need other specialists. Ask the assistant to identify unavailable skills and continue with available instructions when reasonable. Installing only the orchestrator does not install its specialists.

## Before and after installation

Use an account approved for your work. Begin with a public lesson, your own material, or synthetic data. Download and extract the repository, keeping each skill's resources together. The ZIPs in `skill-packages/` contain one `SKILL.md` at the top level; the whole repository ZIP is not a single skill.

After installation, start a new conversation and ask:

> Can you find tw-orchestrator and tw-formative-checks? Read their instructions and identify supporting files you cannot access. Then create an original three-question grade 5 fractions exit ticket with an answer key. Do not claim alignment to a standard you have not checked.

Review the questions and key, then try a familiar classroom task. The [teacher guide](../USER_GUIDE.pdf) provides a longer introduction.
