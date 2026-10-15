# Intervention, cognitive demand and grading — Teacher Workbench 1.4.0

Eight added skills extend the full 40-skill suite. Use the orchestrator for combined work or name a specialist directly. The earlier instructional-assistant small-group skill is included. All examples below are hypothetical; supply the actual grade/course, standards, curriculum, evidence and local policies that matter.

| Skill | What it produces |
| --- | --- |
| `tw-intervention-activities` | Actual Tier 1, 2 and 3 activities, models, student tasks, keys, scaffold/error branches and progress checks. |
| `tw-intervention-grouping` | Evidence-based temporary rosters, feasible staffing/schedules, coverage exceptions and regrouping rules. |
| `tw-blooms-taxonomy` | Justified cognitive-demand audits, two-dimensional maps and revised tasks/questions with expected reasoning. |
| `tw-marzano-grading-rubrics` | Original proficiency scales, analytic rubrics, score anchors, grade-profile analysis and moderation guidance. |
| `tw-standards-based-grading` | Local grading-policy maps, evidence/reassessment rules, reporting examples and policy comparisons. |
| `tw-standards-progress-analysis` | Dated standards profiles, status/trend/consistency, coverage, transitions, rollups and sensitivity analyses. |
| `tw-pre-post-growth-analysis` | Matched growth, attrition audit, raw/percentage-point/standardized change and appropriate optional intervals. |
| `tw-grade-calculations` | Reproducible weights, retakes, drops, missing-score policies, extra credit, rounding and advanced calculation support. |

## Start from the evidence you have

Upload diagnostic responses, work samples, a gradebook export, a scope/sequence or an existing rubric; freeform conversation works too. Explain the columns, score meanings, dates and missing-value codes. Use deidentified learner codes for analysis. The skills read the supplied material, separate observed evidence from hypotheses, and ask for missing facts only when those facts change the proposed instruction or calculation. Curriculum-dependent work uses the suite's curriculum reference workflow.

## 1. Create tiered activities and flexible groups

> Use tw-orchestrator with intervention activities and grouping. Here are coded work samples and diagnostic results. Identify specific teachable gaps and strengths, then create Tier 1, Tier 2 and Tier 3 options. Include exact models, student tasks, worked answers, scaffolds, fresh checks and review rules. We have one teacher, one novice assistant, two 15-minute periods and a maximum of four learners per adult. Check feasibility and show unmet needs.

**Expect:** A need/evidence matrix, temporary rosters with individual rationales, a schedule checked for adult/learner conflicts, and actual activity packets. Each packet uses **TW-INT 1.4**: evidence/target; delivery/preparation; complete activity; access/scaffold/extension/fallback; fresh evidence/transfer; implementation/review; and source/change notes. Required local templates take precedence. Assistant-led activities can become the existing ten-section **TW-IA 1.3** packet.

Tier 1 strengthens core instruction and access, Tier 2 adds targeted supplemental instruction, and Tier 3 uses intensive individualized adaptation with the appropriate team and intervention platform. These are levels of support that respond to evidence, not permanent labels attached to students. [CDE MTSS](https://www.cde.ca.gov/ci/cr/ri/mtsscomprti2.asp); [MTSS Center](https://mtss4success.org/essential-components/multi-level-prevention-system); [NCII DBI](https://intensiveintervention.org/data-based-individualization).

Missing or inaccessible evidence goes into a check-needed queue. The same low total can hide different errors, so grouping uses target-specific evidence. An absent learner is not assigned to the lowest group. Required services, accommodations and core instruction remain part of the schedule. Proposed minutes and regrouping thresholds are labeled as local planning choices; validated program conditions are preserved. Generated tasks are not presented as tested intervention programs. Relevant [WWC guidance](https://ies.ed.gov/ncee/wwc/practiceguides) and [NCII intensity/progress guidance](https://intensiveintervention.org/implementation-intervention/taxonomy-intervention-intensity) inform design; actual progress is reviewed with delivery and opportunity data. [NCII monitoring](https://intensiveintervention.org/data-based-individualization/progress-monitoring).

Useful follow-up: “Give the assistant a fully scripted version with a content primer, preparation self-check, error responses, independent check and two-minute teacher handback.”

## 2. Analyze Bloom's taxonomy and create Marzano-style rubrics

> Analyze this lesson and assessment using tw-blooms-taxonomy. Show the actual thinking each task requires, its knowledge dimension and cognitive process. Revise tasks that only appear demanding because of their verbs. Include complete replacement prompts, example responses and scoring evidence.

Bloom analysis uses both cognitive-process and knowledge dimensions; classification depends on the task and expected thinking. It is not a conversion from a verb to a grade or from Bloom to DOK. [Krathwohl's original overview](https://www.chemnet.edu.au/sites/default/files/files/Blooms_taxonomy_2002_Krathwohl.pdf) and [Larsen et al.'s empirical examination](https://escholarship.org/content/qt9087k9x2/qt9087k9x2.pdf) support careful, context-specific use. A unit map may show multiple categories; every lesson need not include every category.

> Use tw-marzano-grading-rubrics. Build an original proficiency scale and an analytic rubric for this standard and task. Define target performance first, then prerequisite/supporting content and a meaningful extension. Include score anchors, nonexamples, accommodation notes and a short moderation exercise. Analyze these existing scores using our stated policy.

**Expect:** Distinct scale and task-rubric purposes, observable descriptors, original examples, a scoring exercise and evidence gaps. In a conventional Marzano-style scale, target content sits at 3, supporting content at 2 and deeper application/transfer at 4; local descriptors still govern. [Marzano Resources' publisher example](https://soltreemrls3.s3-us-west-2.amazonaws.com/marzanoresources.com/media/documents/reproducibles/HDUPSC/proficiencyscalewithsampleactivities.pdf). Required accommodations do not automatically cap proficiency. Missing/not assessed remains distinct from an observed low score. A proficiency label of 3 out of 4 is not automatically 75%; letter/percentage conversion requires an explicit local crosswalk.

## 3. Analyze standards-based grading over time

> Use tw-standards-based-grading and tw-standards-progress-analysis. Here are dated student-by-standard scores and our grading policy. Compare latest, lower median and recent-consistency summaries. Show chronology, missing evidence, recency, stability, mastery transitions and domain rollups. Identify essential-standard gaps and how conclusions change under the alternative rules. Do not change our gradebook.

**Expect:** A policy map, data audit, dated evidence tables/charts when supported, standard profiles, explicit rollup membership/weights, coverage denominators, essential-standard flags and next evidence needs. Other supported workflows include blueprint/coverage audits, reassessment comparisons, prerequisite patterns, rater/form differences and opportunity/missingness checks. Advanced causal, forecasting, multilevel or IRT analysis requires suitable design and a verified runtime; it is not implied by a simple trend line.

The bundled standards calculator supports latest, highest, lower median, mode with a recent tie-break, recent-consistent minimum, and explicitly authorized numeric mean/decaying mean. Rollups support minimum, proportion meeting and authorized weighted means. Ordinal categories use category transitions; descriptive numeric slopes require an explicit comparable interval-like assumption and at least three distinct dates. Incomplete coverage stays visible even when a partial rollup is allowed. Essential-standard flags accompany a numeric rollup rather than silently enforcing an unspecified course-grade rule.

The [WWC April 2026 PARLO review](https://ies.ed.gov/ncee/WWC/Study/94417) concerns a particular secondary mathematics program and meets WWC standards **with reservations** under the version used for that review. It is not an endorsement of every standards-based grading formula or Marzano rubric. The suite checks current studies and separates program evidence from proposed policy. In California district courses, the teacher's grade authority and specified exceptions are addressed by [Education Code §49066](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=EDC&sectionNum=49066); the section does not prescribe one universal grading formula.

## 4. Compare pre/post growth and calculate complex grades

> Use tw-pre-post-growth-analysis. Match these pre/post files by learner code. Audit duplicates, missingness, scale comparability and ceiling effects. Report matched changes, class summaries and clearly labeled standardized changes. Explain whether a paired interval is appropriate and what this design cannot establish.

**Expect:** The matching/exclusion audit, individual changes and matched summaries. Distinguish raw gain, percentage-point gain, relative percentage change, normalized gain and standardized change; they answer different questions. A zero baseline makes relative change undefined. The calculator includes d_z, d_av and baseline-SD standardized change with named denominators. Optional paired-t intervals use SciPy when available and justified. [NIST paired observations](https://www.itl.nist.gov/div898/handbook/prc/section3/prc311.htm); [NIST interval formula](https://www.itl.nist.gov/div898/handbook/prc/section3/prc312.htm); [Lakens on standardizers](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2013.00863/full). A single-group pre/post change is not evidence by itself of intervention causality.

> Use tw-grade-calculations. Apply these category weights, retake rules, exemptions, missing-score rules, drops, extra credit, rounding and thresholds to my export. Show every denominator, policy decision and intermediate result. Compare the stated missing-work policy with an alternative without overwriting source data.

The bundled Decimal calculator supports points or equal-item averaging, category weights, latest/highest attempts, lowest-percentage drops with minimum retained work, exempt/missing distinctions, authorized bonus points, empty-category rules, floors/caps and explicit rounding/threshold order. It rejects unsupported policies rather than silently guessing. Outputs include the exact policy and selection/drop/exclusion audit.

For custom topics such as a required final-exam score, semester blends, credits/GPA, category replacement, nonlinear crosswalks, caps or what-if sensitivity, the skill derives the formula, states policy order, uses an appropriate calculation runtime and checks the result independently. These are supported workflows, not all built-in features of the bundled engine. Example: a current 82 counting 80% plus a final counting 20% needs **97** on the final to reach 85 before rounding: `(85 - 0.8 × 82) / 0.2 = 97`, assuming the current grade excludes the final.

## Worked calculator examples and portability

The package includes three synthetic JSON inputs, three Python scripts and run guides in the relevant skills. Use the run guide before running a calculator. Python 3.9+ is required; only optional paired inference needs SciPy. Without a runtime, the skill can prepare inputs and explain formulas but must label results as unexecuted. Native Sheets/Canva/document production remains conditional on connected host capabilities.

The actual sample checks yielded: standard S1 latest=3 versus lower median=2 with the domain unavailable for missing S2 evidence; three matched pre/post learners with mean raw gain 4; and a weighted grade of 91.33 versus 82.00 when only the missing-work policy changed. See [validation](VALIDATION.md), calculator run guides and the numerical test file for exact synthetic inputs and scope. These demonstrate arithmetic and workflow behavior, not classroom effectiveness.

AI assistance is optional. For chosen AI uses, the suite checks current research and local conditions, distinguishes learner work from generated output, and retains human review of grading. All new skills load the same California/WWC/CSTP/Ed Code/ISTE grounding policy as the existing suite. Source checks here were completed on **2026-09-29 UTC**; current legal, research and platform claims are rechecked when used.
