---
name: tw-classical-test-theory
description: "Analyze classroom test scores and items using classical/traditional test theory (CTT). Use for item facility, corrected item-total relationships, distractors, internal consistency, SEM and reproducible response-data audits."
---

# Teacher Workbench Classical Test Theory

## Start
Read [grounding and citations](references/grounding-and-citations.md) for every invocation. Read [coordination and capabilities](references/coordination.md) for the handoff and host-specific fallback rules. Use the [source directory](references/source-directory.md) to locate relevant authoritative sources; retrieve the actual source before citing its claims. Apply only the foundations relevant to the teacher's decision.

## Inputs
Required for analysis: anonymous response CSV, scoring key/categories and purpose. Resolve omitted, invalid and not-administered codes. Optional: item/standard map, administration/support conditions and reporting needs. For explanation only, no data are required.

## Workflow
1. Read references/measurement-methods.md and inspect the dataset/configuration before calculation. Preserve the raw file. Check anonymous IDs, item columns, scoring rules, missing codes, administration conditions and construct map. Show suspected key issues; never silently correct a key.
2. Explain observed score = true-score component + error within the model. Select statistics suited to the question, scoring and sample. Item facility is sample/test dependent; difficulty and discrimination are not inherent constants of a classroom item.
3. When Python is available, run scripts/ctt_analyze.py with an explicit config and output path. It handles raw keyed or scored items, per-item descriptives and listwise-complete corrected item-total/alpha calculations. Read its warnings and denominators; do not hide exclusions. Use another verified method if the purpose needs rater agreement, stability or classification consistency.
4. Interpret facility, distractor counts and corrected item-total relationships with the actual item and teaching context. A negative relationship can signal a key/problem, multidimensionality, sparse data or other causes; inspect rather than automatically discard.
5. Explain internal consistency separately from validity, test–retest stability and rater agreement. Report alpha and conventional SEM only when their assumptions and computation are appropriate; do not portray them as individual conditional precision. Small classroom samples permit descriptive analysis but unstable population estimates.
6. Provide an actionable item/curriculum review and a reproducible audit: files/hashes, scoring/missing rules, counts, software/version and warnings. Do not assign mastery cutoffs from alpha or item facility.

## Deliver
Return a data/scoring audit, relevant item/test results with sample counts, limitations, key-review flags, practical next steps and the executable/reproducible artifact. Label bundled examples synthetic.

## Limits
No score report without actual execution when calculations are claimed. Do not equate high alpha with unidimensionality or validity, or a small class with a calibrated item bank. If tools/data are absent, supply the script/configuration and a bounded plan.

## Routing examples
Direct: “Analyze this quiz CSV and answer key.” Overlap: explain misconceptions → student-work/subject specialist. Boundary: compare scores across different forms without design evidence → no unsupported equating.

## Reusable resources
These are editable working formats, not finished teacher deliverables. Fill them with actual task content, examples and keys; remove unused fields. Label authored examples and proposed decision rules.
- [analysis-report.md](assets/analysis-report.md) — adapt and fill for the requested task.

Read [measurement methods](references/measurement-methods.md) and [data/run guide](references/data-and-run-guide.md) before analysis. Use [synthetic response data](assets/synthetic-responses.csv), [scoring configuration](assets/scoring-config.json), and [the tested calculator](scripts/ctt_analyze.py) for a reproducible demonstration. Never report the synthetic results as real students.
