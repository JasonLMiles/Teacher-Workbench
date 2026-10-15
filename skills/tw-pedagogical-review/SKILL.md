---
name: tw-pedagogical-review
description: "Review actual teaching materials against explicit common and subject-specific pedagogical criteria. Use for lesson or assessment quality checks, output evaluations, rubric-based comparisons, checking revisions, and identifying content, alignment, accessibility or evidence problems before classroom use."
---

# Teacher Workbench Pedagogical Review

Read [grounding and citations](references/grounding-and-citations.md) and [review method](references/review-method.md). Load `assets/rubrics.json`; these are original Teacher Workbench operational criteria, not a validated instrument or a reproduction of another provider's evaluation set.

## Review the artifact
1. Obtain the actual lesson, check, packet or student materials and intended target/use. Inspect all relevant pages, keys, diagrams and source passages. Do not rate a promise in a chat as if the promised artifact existed. Mark unavailable material as insufficient evidence and continue checking what is present.
2. Select common criteria plus applicable subject/workflow sets. Record exclusions with reasons. Require a subject set for subject instruction and a workflow set when reviewing a formative check, rehearsal, intervention or grading resource. Multi-subject work needs each applicable subject set. Preserve the full criterion list; do not select only easy passes.
3. Apply one criterion at a time. Use pass, fail, not_applicable or insufficient_evidence; distinguish unreviewed criteria automatically in the report. A pass/fail needs an exact artifact locator and reason, with supporting source when external. A not_applicable judgment needs a real applicability reason; difficulty or missing content is not a reason to omit a criterion.
4. Recompute examples, keys, totals and grade calculations independently. Verify standards and externally grounded claims against opened authoritative sources. Judge cognitive demand from what students must do, not verbs alone; verify whether scaffolds preserve the construct and individual evidence.
5. Prioritize material content/key errors, harmful/inappropriate directions, misrepresented sources and invalid score interpretations as blockers. Explain the smallest correction and produce it when requested. Required accommodations must not be removed to make a score appear more independent.
6. For rubric-based evaluation, create ratings in the schema in `assets/review-example.json`, then run `scripts/review_report.py` when a runtime exists. This script checks record completeness and summarizes judgments; it cannot determine pedagogical quality. Keep failed, insufficient and unreviewed criteria visible. A high pass percentage never overrides a blocker. Do not label an untested artifact validated.
7. Reinspect the revised artifact against the original criteria; attach new evidence, retain previous ratings and show unresolved issues. For consequential or comparative evaluation, have a qualified educator review and calibrate a sample independently; show disagreement rather than averaging it away. Simulated examples and model review are not classroom outcome evidence.

## Deliver
Lead with usable, revise before use, or incomplete review, scoped to the material actually checked. List blocker fixes first, then a few useful refinements with page/task evidence, source links and a corrected example. Supply the completed rubric table or machine-readable report when requested. State review coverage and any missing sources. Avoid a decorative score unsupported by the artifact.

For a quick classroom request, apply a proportionate subset of the workflow while checking all relevant content; do not force a lengthy evaluation report. Route research disputes to evidence review, psychometrics to CTT/IRT and governing policy to Ed Code support.
