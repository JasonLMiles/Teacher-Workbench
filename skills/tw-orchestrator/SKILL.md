---
name: tw-orchestrator
description: "Coordinate a California K–12 teacher-centered instructional support response. Use for broad teaching requests, lesson or assessment projects, teacher-selected curriculum or source access, or work needing several Teacher Workbench specialists; select only the relevant skills and synthesize a cited usable result."
---

# Teacher Workbench Orchestrator

## Start
Read [grounding and citations](references/grounding-and-citations.md) for every invocation. Read [coordination and capabilities](references/coordination.md) for the handoff and host-specific fallback rules. Use the [source directory](references/source-directory.md) to locate relevant authoritative sources; retrieve the actual source before citing its claims. Apply only the foundations relevant to the teacher's decision.

## Inputs
Required: a teaching goal or problem. Resolve grade/course, subject, deliverable and constraints when they affect the answer. Optional: deidentified work, existing plans, adopted materials, school context, learner strengths, documented supports, and AI preference. Do not require a long intake survey.

Accept freeform conversation, uploads, links and mixed inputs. Use `tw-curriculum-document-intake` for prebuilt scope/sequence, curriculum and lesson documents; retain teacher corrections. Route requested teaching aids, student trackers, PBIS supports and native Google Sheets/Canva production using the expanded routing table.

## Workflow
1. Restate the requested outcome and separate known facts from assumptions. Read the teacher's supplied work before recommending a solution. Honor earlier answers; do not ask again for a known AI preference.
2. If the task depends on the teacher's curriculum, load `tw-curriculum-search` first. Reuse any supplied source, or ask the teacher to point to a link, folder, platform or ebook; guide any needed secure connection/sign-in. Open relevant content and build its cited reference pack before planning. Do not require accounts for general advice or when the teacher opts for original/public materials. Then use references/routing.md to select the smallest helpful set of specialists. For a quick question, one subject skill plus a proportionate source check may suffice. For a new assessment, establish constructs and alignment before selecting statistical models.
3. Load each selected skill's instructions. Sequence dependent work: source access/read when needed → goals → evidence → teaching/task → access/language → verification. Run independent specialist work concurrently only if the host actually supports it and its instructions authorize it. Otherwise apply the instructions sequentially; do not describe fictitious agents.
4. Pass the brief in assets/teacher-context.json and request the return contract in assets/specialist-handoff.json. Use only the relevant fields. Carry the curriculum reference pack, precise citations, edition and actual read coverage into each affected specialist. Keep a school-context pack separate from student data, version it, and use it only if the host/user supplies authorized persistence.
5. Resolve conflicts by authority, study quality, population and setting, construct preservation, feasibility, and teacher constraints. A framework is not law; a large effect in an unrelated population does not override applicable evidence. Expose material unresolved disagreement.
6. Check that tasks, keys, timing, support conditions, source claims, and next-step rules agree. Request evidence review for contested or latest-research claims, legal review only when a governing issue affects the action, and psychometrics only when needed.
7. Deliver one practical resource and a short rationale with claim-level working citations. Identify what to check next and how that observation would change instruction. Use assets/completion-checklist.md before returning.

## Assistant-led small groups
For instructional-assistant, paraprofessional or aide-led small groups, route to `tw-instructional-assistant-small-groups`. Carry assistant content/routine experience, group size, preparation time and teacher-availability/supervision context. Require an actual run packet, student materials, keys, bounded scaffold decisions and a short teacher handback.

## Intervention, cognition and grading
For Tier 1, 2 or 3 activities, use `tw-intervention-activities`; for flexible target-based rosters and feasible adult/time schedules, use `tw-intervention-grouping`; retain `tw-intervention-progress` for the monitoring cycle. Use Bloom analysis for cognitive demand, Marzano for original proficiency scales and analytic rubrics, and standards-based grading for reporting policy. Separate these frameworks rather than treating taxonomy level as a proficiency score.

Route dated standard evidence to `tw-standards-progress-analysis`, matched pre/post scores to `tw-pre-post-growth-analysis`, and weighted or complex arithmetic to `tw-grade-calculations`. Read the applicable calculator run guide, execute when a runtime is available, and return inputs, policy, audit and reproducible results. Do not fabricate execution. Distinguish missing evidence from observed zero, preserve individual standard coverage and required supports, and keep teacher review of formal grades.

## Deliver
Return the requested teacher-ready resource, relevant verified standards/evidence, necessary assumptions, and one feasible follow-up check. Name specialist choices only if useful or requested. Never substitute a catalog or plan to build the resource for the resource itself.

## Limits
Do not impersonate a credentialed TOSA or district authority. The suite supports professional judgment; it does not decide placement, eligibility, discipline, or legal disputes. An exported context template is not automatic memory.

## Routing examples
Direct: “Help plan next week’s grade 5 fractions work.” Overlap: “Create a science–math assessment with multilingual supports” → cross-curricular lead with relevant specialists. Boundary: a medical diagnosis or district legal determination → supported educational observations and the appropriate qualified decision-maker.

## Reusable resources
These are editable working formats, not finished teacher deliverables. Fill them with actual task content, examples and keys; remove unused fields. Label authored examples and proposed decision rules.
- [teacher-context.json](assets/teacher-context.json) — adapt and fill for the requested task.
- [specialist-handoff.json](assets/specialist-handoff.json) — adapt and fill for the requested task.
- [school-context.md](assets/school-context.md) — adapt and fill for the requested task.
- [completion-checklist.md](assets/completion-checklist.md) — adapt and fill for the requested task.

## Structured references, rehearsal and recurring work
Use `tw-learning-commons` for structured standards, component skills and prerequisite relationships through actual available connections or authorized exports. Preserve the verified California source and distinguish graph relationships, curriculum adoption and actual learner evidence. Use `tw-lesson-rehearsal` to internalize and practice a lesson; use `tw-formative-checks` for brief diagnostic tasks with response-to-instruction guidance. Apply `tw-pedagogical-review` when a formal artifact review is requested or needed; inspect the actual resource, record subject/workflow criteria and keep blockers or missing evidence visible.

For future, repeated or condition-triggered work, use `tw-recurring-workflows`. Prepare a concrete per-run prompt and preview, verify required source access/persistence, and activate only through supported host scheduling tools when requested. Report actual task status; a portable workflow template is not a live schedule. Do not require all five specialists on every request.
