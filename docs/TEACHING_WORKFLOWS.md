# Documents, teaching resources and behavior support

Teacher Workbench 1.2.0 includes 31 skills. You can start from conversation, uploads, links or any combination. Tell it your grade/course, learning goal, time, available materials and requested output; reuse context already supplied. Uploaded documents are read as references rather than treated as instructions to override your request.

| Request | Workflow and deliverable |
| --- | --- |
| Turn my uploaded lesson into a substitute packet | Document intake reads the plan and any pacing map; substitute planning preserves your intent and corrections, then writes timed directions, actual student tasks, separate keys, supports, an offline option and handback. Freeform chat works too. |
| Use my scope and sequence, curriculum or lesson documents | Curriculum search handles needed source access; document intake extracts sequence, goals, assessments, supports and precise source locations, resolves versions and identifies missing attachments. File formats depend on available host readers. |
| Make a Google Sheet | The production skill creates and checks a native Sheet if connected write tools are available. Otherwise it creates an editable XLSX, or a simpler CSV, with its status clearly stated. Each user needs an authorized account for native creation. |
| Make a Canva resource | The production skill creates/edits supported native designs when Canva tools are connected. Otherwise it can supply an editable PPTX/DOCX for import plus a preview. Import fidelity still needs checking in Canva. |
| Create teaching aids and student reflection/data sheets | Dedicated skills make complete anchor charts, worked examples, organizers, cards, practice tasks, reflection prompts, goal/evidence/action records and private progress logs or graphs. Teacher keys and source notes stay separate. |
| Add scaffolding | Existing differentiation and multilingual skills supply models, guided practice, cues, language support, accessible response options and extension. Each temporary scaffold has evidence for adjustment/fading; required accommodations remain. |
| Support behavior with PBIS or other frameworks | The behavior skill produces explicitly taught routines, expectation matrices, teacher language, private observations/reflections and implementation checks using appropriate PBIS/MTSS, SEL or restorative guidance. It distinguishes evidence for practices from claims about whole frameworks. |
| Keep lesson output consistent | Complete lessons use the ten-section TW-LP 1.2 format below. Uploaded required templates take precedence, with essential information retained. Narrow edits return only the requested section. |

## Default full lesson format
1. Overview
2. Sources and alignment
3. Learning goals and success criteria
4. Preparation and prerequisites
5. Lesson sequence — Time/minutes; Teacher moves/model; Student task; Evidence/check; Response/next step
6. Scaffolds, language supports and extension
7. Assessment and next instruction
8. Student materials
9. Teacher key and use notes
10. Reflection, sources and changes

Complete substitute packets use TW-SUB 1.2: quick start and missing local facts; schedule/materials/source; timed directions; student work; separate keys; offline/early finish; staff-only notes; handback; sources/changes. Missing emergency, contact or dismissal information is flagged for school completion.

## Try these prompts
> Use my uploaded scope-and-sequence and lesson plan. Keep my objective and scribing accommodation, shorten it to 30 minutes, and create a lesson plus a substitute packet using only the board and notebooks.

> Create an anchor chart and two scaffolded practice tasks for this learning target, with a separate answer key. Use my attached school template.

> Create a private student reflection and progress workbook. Distinguish an observed zero from an absence, include evidence and next-step prompts, and make an editable XLSX for later Google Sheets import. Do not connect an account.

> Make this two-page teaching aid as an editable Canva design if connected tools are available; otherwise create an editable import-ready PPTX with a preview and separate teacher key.

> Use our PBIS expectations to teach the return-from-recess routine. Give me a teaching script, visual sequence, private paper reflection and a way to check whether my supports were delivered.

## How production is reported
- `content_only`: usable text/content supplied, with any file-production limitation stated.
- `local_file_created`: an actual checked file is linked; an XLSX or PPTX is not described as a native Google Sheet or Canva design.
- `native_created`: the connected provider confirmed creation and relevant content was checked; an actual provider link is returned.

Do not place multiple students' private records in a workbook shared with all students. Hidden/protected tabs and filter views are not student privacy boundaries. Student confidence, work completion, behavior and demonstrated learning remain distinct measures.

## Research and host requirements
All skills retain the California standards/frameworks, Education Code, CSTP, WWC, ISTE, research-currency and claim-level citation rules. For these additions, see [checked primary sources](SOURCE_VERIFICATION.md). PBIS guidance includes current [classroom MTSS guidance](https://www.pbis.org/resource/multi-tiered-system-of-supports-mtss-in-the-classroom) and the [WWC K–5 behavior guide](https://ies.ed.gov/ncee/WWC/PracticeGuide/31/Published); reflection design consults [EEF's updated metacognition guidance](https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/metacognition). These sources inform practice; they do not validate a newly generated worksheet or local decision threshold.

The package supplies workflows and resources. The destination supplies file readers, production tools, browser access, provider integrations and account permissions. Private sources may require secure connection/sign-in. Native Sheets/Canva creation requires sufficient connected write capabilities; prompts alone cannot add those tools. No live Google/Canva account writes were tested in this release. See [validation](VALIDATION.md) for the exact checks performed and [curriculum access](CURRICULUM_ACCESS.md) for source setup.
