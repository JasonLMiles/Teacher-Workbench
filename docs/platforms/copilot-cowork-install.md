# Install Teacher Workbench in Copilot Cowork

For **Microsoft Copilot Cowork**, checked October 15, 2026. Use an organization-approved account with Cowork and custom skills available. [Usage guide](copilot-cowork-use.md).

## Upload the skills

For bundled plugin packages, use the [Build skill plugins workflow](../PLUGIN-PACKAGES.md). The current suite produces three Copilot app ZIPs; install all three through your tenant's custom-app/plugin process. The steps below remain the individual-skill upload route.

1. Extract Teacher Workbench and open `skill-packages/`.
2. In Cowork, open **Customize → Skills → Add → Upload skill** using the arrow beside Add. Some layouts expose Customize through **+**.
3. Upload `tw-orchestrator.zip`. Wait for validation and synchronization; confirm it appears under **Your skills**.
4. Repeat for the [starter set](readme.md#a-manageable-first-set) or full suite. Start a new conversation and run the [installation check](readme.md#before-and-after-installation).

Microsoft accepts ZIP or `.skill` archives with `SKILL.md` at the root and companion files. These ZIPs use that layout and include the license. The repository ZIP is not one skill. See [Customize Copilot Cowork](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-customize).

## Capacity and folder alternative

Microsoft documents 50 custom skills, so all 45 need sufficient free capacity. Its manual route uses complete skill folders beneath **OneDrive → Documents → Cowork → skills**, discovered in a new session. Custom skills are not supported on Cowork mobile in the documentation checked here. See [Use Copilot Cowork](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/use-cowork).

For that route, copy the selected `tw-*` folders from `skills/` into the OneDrive location, preserving nested resources. Include a copy of `license.md` with redistributed folders.

## Updates and troubleshooting

Back up customizations first. Microsoft says uploading a same-named skill keeps both and adds a number to the new name. After checking the replacement, remove the obsolete copy so routing does not select it. See [upload guidance](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-customize).

Read any validation error and compare the ZIP with the source folder. Local archive checks do not establish vendor acceptance or execution. If Customize or Upload skill is absent, ask your Microsoft 365 administrator about availability. GitHub Copilot setup instructions apply to a different product.
