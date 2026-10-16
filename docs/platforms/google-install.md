# Install Teacher Workbench for Google

Checked October 15, 2026. Choose the route available in your approved Google environment. [Usage guide](google-use.md).

## Gemini Apps with Skills

Google currently describes Skills as a gradual rollout for personal accounts, ages 18+, with Keep Activity enabled; work and school accounts are not yet eligible. Do not move school records to a personal account for this feature. See [Google's skill documentation](https://support.google.com/gemini/answer/17094296?hl=en).

1. Extract Teacher Workbench and open `skill-packages/`.
2. In Gemini, open **Customize → Skills → Upload**. Upload `tw-orchestrator.zip`, review it, and select **Create**.
3. Repeat for the [starter set](readme.md#a-manageable-first-set), or all 45.
4. Confirm the names and run the [installation check](readme.md#before-and-after-installation).

The ZIPs include supporting files. Google does not support internet-dependent scripts inside uploaded skills; supply references or use available host research tools. For updates, use **Replace skill** with the complete ZIP. These steps follow [Google's guidance](https://support.google.com/gemini/answer/17094296?hl=en).

## School-account or Gems route

If your approved account offers Gems:

1. In [Gemini](https://gemini.google.com/), open **Gems → New Gem**.
2. Name it **Teacher Workbench — Lesson Preparation**. Paste [gem-instructions.md](gem-instructions.md) into its instructions.
3. Under **Knowledge**, add your approved lesson template and relevant plain-text skill/reference files. Start with lesson planning and formative checks, including their grounding and output guidance.
4. Preview a request, review it, and select **Save**.

See Google's [Gem creation](https://support.google.com/gemini/answer/15146780?hl=en) and [knowledge-file guidance](https://support.google.com/gemini/answer/15235603?hl=en). This is a focused adaptation; it does not install all 45 skills or automatically supply scripts and routing. If Gems are absent, use these instructions and files in a permitted chat for the task.

## Gemini CLI route

First follow Google's [CLI installation](https://geminicli.com/docs/get-started/installation/) and sign in with an approved account. Open a terminal in the extracted repository root. Install one skill:

```sh
gemini skills install ./skills/tw-orchestrator --scope user
```

All 45, using a macOS/Linux POSIX shell:

```sh
for skill_dir in ./skills/tw-*; do
  gemini skills install "$skill_dir" --scope user
done
gemini skills list
```

PowerShell:

```powershell
Get-ChildItem ./skills -Directory -Filter 'tw-*' | ForEach-Object {
    gemini skills install $_.FullName --scope user
}
gemini skills list
```

Review installation prompts. In an existing session, run `/skills reload`, then `/skills list`. Google's [Agent Skills documentation](https://geminicli.com/docs/cli/skills/) covers these commands and activation approval. Use `--scope workspace` for a project-only installation.

Preserve customizations before updating and reinstall reviewed folders according to current CLI behavior. Remove a selected skill with `gemini skills uninstall tw-orchestrator --scope user`, substituting its name and original scope.
