# Coordination and host capabilities

Use the host's available web search and page/PDF reading tools to verify sources; use its file reader for authorized supplied files and its calculation runtime for numerical work. Tool names differ by host: discover available capabilities rather than inventing API names. General coaching works without an external account. Referencing private curriculum requires a suitable authorized connector or browser supplied by the host; the package does not bundle those connections. Do not claim to have run a tool, another agent, or a calculation that did not run.

When another skill is needed, resolve its exact name in the host catalog or the plugin's sibling skills folders. Read its SKILL.md and the resources it names. If separate agents are unavailable, apply the skills in sequence yourself. If a named skill cannot be found, perform the supported portion and state the gap; do not pretend it ran. Respect all higher-priority host instructions.

## Brief
Record task_id; teacher_goal; grade/course; subjects; supplied materials and observations; learner strengths/needs; documented supports; time/resources; technology/AI preference; supplied local procedures; required deliverable; unresolved facts; currency needs. Ask only for facts that change a material decision. For the rest, state assumptions and produce a useful first version.

## Specialist return
Record skill_name; findings; observed versus inferred evidence; proposed action; usable artifact; verified alignment; source records with supported claims; evidence strength and transfer limits; assumptions; assessment/access implications; capability gaps; follow-up measure and decision rule. Use labeled prose if JSON adds no value. Give the teacher one coherent answer rather than internal handoff traffic.

## Fallbacks
- No web: use supplied authoritative sources, mark currency and link verification as unconfirmed, and avoid invented standard codes or legal conclusions.
- No code: explain the calculation and provide the bundled script or data plan; do not invent computed results.
- No files/export: provide complete copyable content with filenames suggested, without claiming it was saved.
- Missing local facts: mark a precise field for the teacher; never invent school contacts, procedures, account permissions, or student plans.
- Existing AI preference governs the entire task. Without a requested student-AI route, do not add one.

## Curriculum handoff
Use `tw-curriculum-search` when the task depends on teacher-selected curriculum. Pass the reference pack and source records (identity, edition, locators, actual read coverage and access restrictions) with the brief; preserve those citations in the return. Reuse verified content rather than asking for login again. If sources are missing or blocked, distinguish proposed original work from curriculum-based work and retain the smallest next action. Do not silently substitute editions or transfer teacher-only assessment material into student-facing outputs.

## Document and artifact handoff
Pass source_document_brief, curriculum_reference_pack, requested_output_format, audience, artifact_destination (if supplied), and existing_supports as relevant. Use document intake for uploaded/pasted plans, teaching aids for new resources, reflection-tracking for student progress tools, behavior-PBIS for framework support, and the Google Sheets/Canva specialists for native production. Report artifact_status as content_only, local_file_created or native_created; separately report verification and sharing. Do not imply installation/authentication or a successful external write without evidence.
