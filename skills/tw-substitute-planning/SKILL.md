---
name: tw-substitute-planning
description: "Create operational substitute-teacher packets for single-day, emergency or multi-day absences. Use for uploaded lesson-plan conversion, freeform conversational planning, schedules, explicit teaching directions, printable work, keys, supports, offline alternatives and teacher handback."
---

# Teacher Workbench Substitute Planning

## Start
Read [grounding and citations](references/grounding-and-citations.md) for every invocation. Read [coordination and capabilities](references/coordination.md) for the handoff and host-specific fallback rules. Use the [source directory](references/source-directory.md) to locate relevant authoritative sources; retrieve the actual source before citing its claims. Apply only the foundations relevant to the teacher's decision.

## Inputs
Accept uploaded or linked lesson plans, scope-and-sequence, curriculum files, pasted notes, freeform conversation, or any combination. Use `tw-curriculum-document-intake` to read supplied documents; do not ask for retyping or require an upload. Resolve grade/course, absence duration and known schedule/learning goal from those inputs. Optional: school-provided procedures, contacts, materials, technology access, classroom routines and deidentified staff-only supports. Do not require student names.

## Workflow
1. Read supplied plans and extract the schedule, learning tasks and local procedures before designing. Preserve the teacher's sequence, materials and intent; reconcile explicit conversational corrections and flag missing referenced attachments. Record proposed deviations and their reasons. Extract the supplied schedule and local procedures. Mark missing local contacts, attendance/dismissal steps and emergency procedures as teacher-supplied fields; never invent them or substitute generic safety instructions for official procedures.
2. Build a one-page quick start identifying what to teach, materials location if supplied, what to collect and where to return it. Separate confidential staff-only support notes from student handouts; include only necessary deidentified directions.
3. Produce a timed sequence with exact language/directions, student tasks, materials, worked example, answer key/criteria, help route, support and early-finisher options. Choose familiar content for emergency work when appropriate.
4. Include an offline route that teaches the same goal and does not depend on undisclosed passwords, paid accounts, video links or printing that was not arranged. If printing is unavailable, provide board-ready directions and notebook tasks.
5. For multiple days, maintain a clear progression and record where to resume if a class runs behind. Include collection and completion tracking; do not infer mastery solely from completion.
6. Check every minute, handout and key against the schedule. Finish with a handback form for what was taught, evidence, work location and issues for the returning teacher. State any unresolved local fact visibly at the front.

## Deliver
Use [the packet contract](references/output-contract.md), TW-SUB 1.2. Preserve a supplied required format while including the same operational content.
Return a complete usable packet, student work and separate teacher keys, offline alternative, missing local fields, collection list and handback. Do not stop at a planning checklist.

## Limits
Never invent school-specific emergency procedures, contacts, medication directions, login credentials or student plan details. Keep private student information out of general substitute packets.

## Routing examples
Direct: “Make tomorrow’s grade 5 sub plan with no internet.” Overlap: new content → subject/lesson skill first. Boundary: missing local dismissal procedure → marked field requiring school-supplied procedure.

## Reusable resources
These are editable working formats, not finished teacher deliverables. Fill them with actual task content, examples and keys; remove unused fields. Label authored examples and proposed decision rules.
- [single-day-packet.md](assets/single-day-packet.md) — adapt and fill for the requested task.
- [emergency-and-multiday.md](assets/emergency-and-multiday.md) — adapt and fill for the requested task.
- [handback.md](assets/handback.md) — adapt and fill for the requested task.
