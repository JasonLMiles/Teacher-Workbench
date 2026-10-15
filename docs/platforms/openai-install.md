# Install Teacher Workbench with OpenAI

Checked October 15, 2026. This source-only guide covers **ChatGPT desktop/Work and Codex local skills**, with a file-based web fallback. [Usage guide](openai-use.md).

## ChatGPT desktop and Codex local skills

OpenAI documents standalone skills in ChatGPT desktop, Codex CLI, and the IDE extension. Codex discovers project skills in `.agents/skills/` and personal skills in `~/.agents/skills/`. See [Build skills](https://learn.chatgpt.com/docs/build-skills).

1. Extract Teacher Workbench.
2. Create `.agents/skills/` in your teaching-work project, or use the personal location above.
3. Copy complete `tw-*` folders from `skills/` into that location, preserving supporting files. Include `license.md` with redistributed copies.
4. Open that project in the desktop app or launch Codex there. Check Skills and restart the session if needed.

For project-local installation, run from the extracted repository root on macOS/Linux:

```sh
mkdir -p .agents/skills
cp -R skills/tw-* .agents/skills/
cp license.md .agents/skills/license.md
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force .agents/skills | Out-Null
Copy-Item -Path ./skills/tw-* -Destination .agents/skills/ -Recurse
Copy-Item ./license.md .agents/skills/license.md
```

These are first-install examples. Back up customized folders before updating and replace the intended version deliberately. The repository ignores these local copies in Git; `skills/` remains authoritative.

In ChatGPT, select a skill with `@`; in Codex use `/skills` or `$tw-orchestrator`. See [discovery and invocation guidance](https://learn.chatgpt.com/docs/build-skills). Run the [installation check](readme.md#before-and-after-installation).

For desktop projects with multiple folders, make the folder containing `.agents/skills/` primary. See [Projects and chats](https://learn.chatgpt.com/docs/projects).

## ChatGPT web or a workspace without local skills

If your workspace supplies an approved standalone skill import/creation flow, follow it for complete folders. Otherwise:

1. Attach relevant `SKILL.md` files and supporting references/templates, or provide extracted source in a Work environment that can read it.
2. Ask ChatGPT to read and apply those files. Have it identify unavailable dependencies.
3. Supply the lesson or deidentified evidence and request a finished resource.

This uses files for the conversation; it is not persistent installation of the suite. Uploading a repository ZIP to an ordinary chat does not by itself register skills. See [file and Work guidance](https://learn.chatgpt.com/docs/use-chatgpt).

## Update or remove local copies

Download the reviewed version, preserve customizations, replace only corresponding installed `tw-*` folders, and start a fresh session. Remove installed copies to uninstall, leaving unrelated skills alone. Avoid duplicate old `tosagpt-*` and new `tw-*` workflows; see [migration notes](../MIGRATION.md).

Python helpers need the runtime described in the [README](../../readme.md). A limited host may apply instructions without executing scripts; request an honest execution summary.
