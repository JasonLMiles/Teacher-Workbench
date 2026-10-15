# Teacher Workbench full-suite acceptance checks

These are acceptance requirements for destination installation and use. All 40 implemented portable skills are included. See docs/VALIDATION.md for checks actually run; live provider authentication and browser routes require destination tests.

## Implementation deliverables and acceptance checks

Produce the coordinator and 39 specialist definitions (40 skills total) with exact prefixed names. Each definition must state selection triggers, inputs, workflow, decision rules, references and tool dependencies, outputs, limitations, and examples. Bundle reusable planning templates, assessment blueprints, scoring guides, analysis input schemas, source records, and substitute-packet templates where useful. Explain how shared references are maintained consistently.

Verify the suite against realistic cases, including:

- A short instructional question requiring only a few relevant sources.
- A California standards-aligned lesson with no requested AI use.
- Optional teacher-only AI use and an age-appropriate student AI activity.
- A cross-curricular task requiring separate mathematics, science, and writing evidence.
- A classroom test with a small response sample, omitted items, and an incorrect answer key.
- An IRT request with insufficient data and another with suitable calibration data.
- A scoring rubric needing exemplars and rater consistency checks.
- An emergency substitute day with missing local procedures and no internet access.
- A differentiation request requiring support for SPeD, EL, and varied reading levels while also extending learning for gifted students.
- A source with a broken link, an inaccessible framework page, an outdated standard identifier, and a corrected or conflicting research finding.
- A matter where Education Code is relevant and an ordinary planning question where a legal discussion adds no value.

Accept outputs only when names are consistent; sources actually support claims; links and access status are accurately reported; research currency is stated where material; numeric work is reproducible; the teacher’s AI preference is honored; differentiation preserves intended constructs and documented supports; and the delivered materials are usable in the stated classroom conditions.



## Completion criteria

- All 40 named skills are implemented; each supporting resource exists.
- Shared policy versions agree and standalone invocation works.
- Claimed source checks and numerical analyses were actually performed.
- Tests distinguish definition, resource, behavior, and installation status.
- The destination reports incomplete capabilities accurately.

## Curriculum access acceptance
All 40 skills must use the same grounding policy and retain source IDs/edition/locators across handoffs. Use the curriculum cases in docs/REVIEW_TEST_CASES.md for source intake, actual content retrieval, authentication recovery, read-only assessments, website/folder navigation, ebooks and unavailable capabilities. Report exact read coverage and account restrictions. Never claim that the package alone installs external connections.

## Teaching workflow acceptance — 1.2.0
Execute the W-series cases in docs/REVIEW_TEST_CASES.md. Require uploads plus conversation, accurate source locators/changes, consistent complete plans with required-template precedence, actual aids and separate keys, privacy-aware reflection/tracking, scaffolds that preserve required accommodations, practice-specific PBIS evidence, and honest native/local artifact status. Validate all 40 definitions and shared policy 2026-09-29.2. Native cloud tests must use authorized destination accounts; local XLSX/PPTX production does not count as native success. See docs/VALIDATION.md for performed checks.

## Assistant-led small groups

Implement `tw-instructional-assistant-small-groups` as a complete operational skill for assistant/aide/paraprofessional-led practice, pre-teaching, reteaching, language, intervention or enrichment groups across California K–12. Accept uploaded plans, curriculum references and freeform conversation. Keep teacher responsibility and student access to teacher instruction. Do not assume a grade, person or classroom from unrelated remembered context.

Choose fully scripted, guided or flexible-within-scope support from the assistant's actual content/routine expertise. Unknown expertise may use a clearly labeled fully scripted default. Give a plain-language content primer, exact worked example, vocabulary, likely wrong responses and a short preparation rehearsal/self-check with answers. Match adult support without lowering student learning expectations. Parallel run cards share task IDs and evidence criteria.

Require the **TW-IA 1.3** contract: (1) assignment and quick start; (2) content primer and rehearsal; (3) timed run sheet; (4) actual student tasks and materials; (5) separate adult answer key and response examples; (6) scaffolds and language/access supports; (7) if-this-then-that decisions; (8) individual check and brief record; (9) teacher handback and next-class connection; (10) teacher source/change notes. The run sheet columns are Time/minutes, Say/show/do, What every student does, Look/listen for and Next action/task ID. Honor required school templates. Supply actual fallback, extension and fresh-check content, not just a list of materials the teacher must write.

Populate task-specific visual, language, worked-example and response supports. Model new concepts explicitly; on familiar work allow attempts before escalating prompts. Preserve documented accommodations. Fade temporary cues only after evidence on a fresh comparable opportunity; keep coached answers distinct from independent performance. Include routines for no start, predictable errors, right answer/weak explanation, rapid success, mixed rates, several students stuck, frustration, missing materials and unfamiliar responses. Keep every learner engaged while the assistant helps one student. Specify a short, proposed limit on unproductive prompting and a usable familiar fallback.

Distinguish what the assistant handles now, records for scheduled review, and raises promptly through actual local procedures. Do not invent school contacts or emergency routes, remove required supports, assign grades or alter student plans. Preserve required named-program training, dosage and fidelity; a generated packet is not a validated intervention. Record first attempt, support used, coached retry and fresh response, distinguishing unobserved/missing from incorrect or zero. Separate delivery notes from learning outcomes. Give a concise teacher handback and classroom bridge with proposed next-session choices for teacher review.

Bundle references for support modes/routines, scaffolding/decision routes and evidence/role boundaries; a complete packet template; an assistant readiness/handback template; and a compact observation-record CSV. Apply the common grounding policy unchanged. Route from the orchestrator, lesson planning, differentiation, multilingual and intervention skills. Carry assistant content/routine experience, chosen support mode, group size, prep time, teacher availability/supervision, approved adaptations, required supports and classroom connection; return the packet and handback.

Cold-read and verify actual task/key accuracy, realistic timing, preparation demands, student/adult separation, response branches and all referenced materials. Forward-check a novice assistant with limited preparation/materials and multiple experience levels using common tasks. Treat such checks as workflow validation, not classroom effectiveness evidence. Native artifact production remains conditional on supported host tools.

Primary sources checked 2026-09-29: [EEF teaching-assistant guidance, March 2025](https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/teaching-assistants), [full report](https://d2tic4wvo1iusb.cloudfront.net/production/eef-guidance-reports/teaching-assistants/deployment_of_teaching_assistants_-_guidance_report_v1.1.0.pdf), [scaffolding tool](https://d2tic4wvo1iusb.cloudfront.net/production/eef-guidance-reports/teaching-assistants/scaffolding_framework.pdf) and [partnership tool](https://d2tic4wvo1iusb.cloudfront.net/production/eef-guidance-reports/teaching-assistants/effective_teacher_%E2%80%93_teaching_assistant_partnerships.pdf); [WWC K–6 mathematics intervention guide](https://ies.ed.gov/ncee/wwc/practiceguide/26); and [California Education Code §45344](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=EDC&sectionNum=45344). EEF guidance comes from England, not California law or a WWC rating. Apply recommendation-specific WWC evidence only within its scope. Section 45344(a) retains teacher responsibility for instruction/supervision, permits aide duties outside the teacher's physical presence and excludes grade assignment; (b) addresses district qualifications. Reverify applicable passages and local conditions at use. Current AI research is required when relevant to teacher-selected AI use, not added as a mandatory student activity.


## Intervention, taxonomy and grading

Implement the eight skills, three calculator contracts and full work products specified in the creation prompts. Verify all 40 definitions/resources, 35 numerical checks, actual tier/group activities, cognitive-demand/rubric reasoning, explicit grading policy, source links and new handoff fields. Preserve prior functionality and report unexecuted destination operations honestly.


## Teacher learning guide

Create a guide for teachers who have never used an agentic digital worker. Speak to the teacher in everyday language. Lead with a ten-minute first task and a worked conversation showing the initial request, a useful result, a correction, and the revised result. Explain what the teacher should look for and how to decide whether to use the output. Organize further help around teaching situations: curriculum documents, lessons, scaffolds and language support, assistant/substitute handoffs, intervention groups, assessments, grading, routines, reflection, and optional technology or AI.

Include copyable requests with realistic constraints, short practice activities, troubleshooting language, and a five-session practice path with observable evidence of proficiency. Keep the full 40-skill directory in an optional reference section. Explain unfamiliar terms when needed; do not require readers to know skill routing, orchestration, or tool names. Distinguish native provider documents from importable files and explain access limitations plainly. Keep sources linked beside the claims they support and label fictional examples. Supply an editable edition and a readable PDF when supported, with working navigation and verified page layouts. Retain a portable Markdown edition. The teacher guide is a learning resource, distinct from this builder-facing specification.

Verify all guide skill names against the actual catalog, every source destination and navigation link, the final rendered pages, and matching guide copies in every distributed package. Distinguish document review from a study of usability or classroom effectiveness.

## Release 1.5 additions
Verify 45 complete skills, current routing, the new helper scripts and their bounded behavior. Test a local graph fixture without inferring absent prerequisites, prepare a timezone-specific unscheduled draft, inspect a flawed classroom resource, and exercise a teacher turn in rehearsal. Do not create live user jobs to test package installation. Keep all failed and missing review criteria visible. Verify guide coverage, working citations and final rendered pages.
