---
name: tw-lesson-unit-planning
description: "Create usable California K–12 lessons and units with aligned goals, evidence, models, practice, supports and teacher keys. Use for daily plans, learning sequences, backward design or revising an existing plan."
---

# Teacher Workbench Lesson Unit Planning

## Start
Read [grounding and citations](references/grounding-and-citations.md) for every invocation. Read [coordination and capabilities](references/coordination.md) for the handoff and host-specific fallback rules. Use the [source directory](references/source-directory.md) to locate relevant authoritative sources; retrieve the actual source before citing its claims. Apply only the foundations relevant to the teacher's decision.

## Inputs
Required: grade/course, subject/goal, available time and deliverable. Accept uploaded/linked lesson plans, scope-and-sequence and curriculum files, pasted text, freeform conversation or a mixture; use `tw-curriculum-document-intake` for document reconciliation. Optional: existing materials, prior work, learner needs, documented supports, resources and AI preference. Make a reasonable labeled default if nonessential facts are missing.

## Workflow
1. Verify relevant standards and framework guidance. Define learning goals and student-facing success criteria, then choose evidence that actually shows the goal. Identify prerequisites and a brief check.
2. Build a feasible sequence within the supplied minutes/days. Include a launch, explicit modeling or purposeful inquiry, guided practice, application, discussion and an independent check as appropriate to the content; do not force every phase into every lesson.
3. Write teacher moves, student tasks, questions, expected responses, misconception hypotheses and contingent responses to evidence. Provide actual task text, examples and keys—not just instructions to create them later.
4. Plan access, language rehearsal and extension around the same core learning. Create actual models, prompts, organizers and practice supports; use the differentiation scaffold ladder to define help and fading criteria. Coordinate with the differentiation/multilingual skills for substantial needs. Preserve documented supports; identify construct changes explicitly.
5. For units, show progression, spaced opportunities to revisit learning, formative checkpoints and a culminating task. Specify how the next lesson changes after each checkpoint.
6. Check timings, material availability, preparation burden, numerical accuracy and scoring consistency. Honor the teacher’s AI preference; include an equivalent route when a requested technology is unavailable.

## Assistant-led small groups
When the teacher wants an instructional assistant to lead a group or rotation, use `tw-instructional-assistant-small-groups` to translate the selected lesson segment into a packet matched to the assistant’s content/routine experience, with actual tasks, keys, decision branches and handback. Preserve the lesson target and independent evidence.

## Deliver
Use [the output contract](references/output-contract.md), TW-LP 1.2, with fixed default headings/order and table columns for every complete lesson. Preserve a teacher-supplied required format with a content crosswalk. Conversational revisions retain the chosen format.
Return a complete plan plus student resources and teacher key/criteria, materials/preparation, supports and extensions, sources in teacher notes, and an evidence-based next step.

## Limits
Do not claim a generated lesson is empirically validated. Do not invent supplied curriculum pages, student responses or district requirements. Mark assumptions and copyrighted text needs precisely.

## Routing examples
Direct: “Create a 45-minute grade 6 ratio lesson.” Overlap: teacher absent → substitute planning makes procedures operational. Boundary: unknown school emergency routines → request/supply marked local fields rather than inventing them.

## Reusable resources
These are editable working formats, not finished teacher deliverables. Fill them with actual task content, examples and keys; remove unused fields. Label authored examples and proposed decision rules.
- [single-lesson.md](assets/single-lesson.md) — adapt and fill for the requested task.
- [unit-plan.md](assets/unit-plan.md) — adapt and fill for the requested task.
- [student-resource-and-key.md](assets/student-resource-and-key.md) — adapt and fill for the requested task.

## Preparation and response to evidence
For teacher practice before instruction, pass the actual lesson, worked task/key and supports to `tw-lesson-rehearsal`; preserve the default lesson format when incorporating revisions. For one to three diagnostic checks with actionable follow-up, use `tw-formative-checks`. When requested, use `tw-pedagogical-review` to inspect actual student materials and teacher notes against common and relevant subject criteria. For recurring planning, hand the confirmed sources and lesson format to `tw-recurring-workflows`; do not imply the plan schedules itself.
