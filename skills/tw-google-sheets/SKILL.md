---
name: tw-google-sheets
description: "Create, format and verify Google Sheets for lesson schedules, scope/sequence maps, assessment trackers, student reflection/progress logs and teacher dashboards. Use a connected Google Workspace/Drive capability when available; otherwise produce an explicitly labeled editable workbook or CSV fallback without claiming a native Google Sheet."
---

# tw-google-sheets

Read [grounding and citations](references/grounding-and-citations.md) every time and [coordination](references/coordination.md) when routing work. Verify sources at use; apply only the foundations relevant to this task. Honor teacher AI preferences and preserve documented supports.


## Inputs and route
Use the workbook purpose, audience, target account/folder or existing file, source data, metrics and requested sharing. For blank templates, use no real student records. Read [production and verification](references/sheets-production.md) and use the [workbook specification](assets/workbook-spec.json). Reuse prior account choices; ask only for an ambiguous destination or consequential metric definition.

## Workflow
1. Define tabs, row grain, columns, units, date/locale/time zone, validations, formulas, charts, input versus calculated fields and source records. Separate teacher-only data from each student's visible information. Choose simple measures tied to instructional decisions; do not equate completion/confidence with mastery.
2. Discover actual available Google Sheets/Workspace tools, including through the Google Drive plugin where it is the entrypoint. Inspect write permissions and supported operations. If no sufficient connection exists, use provider/plugin discovery and guide secure connection. Do not claim native creation from the existence of a Drive search tool alone or invent method names/IDs.
3. If native creation/editing is available and authorized by the request, create the specified spreadsheet or update the clearly identified target, then populate actual data/formulas and apply useful formatting. Preserve existing formulas/tabs and unrelated user data. Create a new derivative by default when adapting source material unless an update is requested. Do not change sharing, email or publish without explicit authorization.
4. Validate formulas and references, blanks vs zero, missing/absent observations, denominator zero, duplicated records, totals and source units. Check a few known cases, including an empty row and a real zero. Use the [formula examples](assets/formula-patterns.md) as starting patterns only; adapt to observed column layout/locale. Do not average incompatible measures or hard-code a mastery cutoff without a basis.
5. Open/read back the native sheet to verify populated tabs, key calculated results and target access when tools permit. Return the provider's actual edit URL and clear verification status. If the connector can create but not calculate/render, state the precise unverified part; do not invent cached results or a working link.
6. If native production is unavailable, first check relevant integration availability, then produce an `.xlsx` workbook using the host's spreadsheet-generation skill/tools if available, or CSV for a simple flat table. CSV does not preserve tabs/charts/formatting; disclose that distinction and include an import note. If no file-generation capability exists, provide complete copyable tables and formulas without claiming a file was saved.

## Deliver
Provide the native Sheet link or explicitly labeled local workbook/CSV, a short usage note, source definitions and any capability/verification limit. Fill the requested tracker/schedule rather than only giving a schema. For a reusable blank tracker, provide blank fields plus a clearly separate fictional example; remove examples from populated production data.

## Examples and boundaries
“Put this scope-and-sequence into Google Sheets” → read source documents and preserve order/provenance. “Make a student progress tracker” → define comparable measures and create private individual views/files. “Update this sheet” → read the exact target before editing. Protected/hidden tabs and filtered views are not student-level privacy barriers; never claim they prevent an authorized viewer from accessing other students' data. Use secure authentication, not passwords in chat.
