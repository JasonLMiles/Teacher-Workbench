# Standards progress and rollup calculator

Run the Python 3.9+ standard-library script from the skill folder:

```bash
python3 scripts/standards_analysis.py assets/standards-input.example.json standards-results.json
```

It reads JSON, makes no network requests and writes JSON. The example is synthetic. Validate source meaning, task alignment and policy before execution; the code checks structure/arithmetic, not educational validity.

## Evidence model

Declare unique `standards` IDs and optionally `students`; otherwise codes come from the records. Each record has student_code, standard_id, task_id, ISO date, status and value. Status is observed, missing, absent, not_assessed or exempt. Nonobserved values are null, not zero. A task ID is unique within learner/standard; reassessments need separate IDs. Multiple same-day records require distinct nonnegative integer `sequence` values. Support/rater/form/source fields may be retained in the chronology. Do not pool incompatible forms or copy an undifferentiated task total into multiple standards.

Required policy: method, window (null or a recent-observation count), min_evidence, scale_type, threshold, as_of date, and stale_days. Ordinal scales need increasing unique numeric `levels` and a threshold at a declared level. Interval scales need scale_min/scale_max and `interval_assumption: true` before numeric means or slopes. Use numeric ordinal labels only as ordered categories unless that assumption is defensible. Records after as_of are excluded with a reason; other missing states remain visible. Staleness is a flag, not an automatic exclusion policy.

## Supported within-standard policies

| Method | Exact behavior |
| --- | --- |
| latest | Last observed value in the selected window. |
| highest | Maximum observed category/value; ignores later declines by design. |
| median_low | Lower middle observed value, preserving an ordinal category for even counts. |
| mode_recent | Most frequent value; tied modes use the latest occurrence among tied categories. |
| recent_consistent_min | Minimum of selected recent observations; a conservative proposed consistency rule, not a validated cutoff. |
| mean | Arithmetic mean, only with explicit interval-like assumption. |
| decaying_mean | Weighted mean with weights decay^(n−1−i), newest weight 1; decay must be >0 and ≤1. Assumes interval-like values and decay by observation order, not elapsed time. |

All require at least min_evidence observed values in the selected window. Report selected task IDs, total count, missing states, actual chronology, category range, consistency fraction and transitions. None is automatically the official grade. A method difference is a sensitivity finding, not proof one learner is more proficient.

For comparable interval-like values, the script calculates a **descriptive** OLS slope using actual days from the first observation, only with at least three observations on three distinct dates. It uses all eligible observed points, not only the summary window; this distinction appears in the interpretation. It supplies no prediction interval, causal estimate or time-series error model. For ordinal values it leaves slope null. Plot individual observations, gaps and phase changes and avoid smoothing away reversals.

## One-level standard-to-domain rollups

Each rollup names an ID, unique leaf members, method, min_coverage >0 to 1, and optional essential members. Nested rollups are intentionally unsupported. Methods: minimum; proportion_meeting (meeting/observed members); or weighted_mean with positive explicit weights summing to one and the interval-like assumption. min_coverage authorizes aggregation of available members when reached; a partial weighted mean then explicitly renormalizes their weights. Use 1 for complete coverage.

Always show observed and all-required denominators, missing standards, coverage, essential standards missing/not meeting, and the essential gate separately. A numeric aggregate cannot silently override an unmet essential requirement. Cross-domain/course rollups, overlapping standards or shared task weights require a separately documented, verified calculation; audit the hierarchy to avoid duplicate influence. Do not convert proficiency labels into percentages without a local crosswalk.

## Other useful analyses

Use actual task/standard maps for coverage, opportunity and item allocation. Use transitions and recency for ordinal histories; conditional reassessment summaries need matched targets/forms. Keep subgroup counts, missingness, supports and exposure visible. Small identifiable cells should not be shared. Class differences cannot identify causes or justify fixed groups.

[NCII progress monitoring](https://intensiveintervention.org/data-based-individualization/progress-monitoring) guides measure-specific goals, graphing and adaptation review; a classroom grading trend is not automatically a validated progress measure. [Testing Standards](https://www.testingstandards.net/open-access-files.html) guide interpretation/fairness evidence. Policy comparisons and this calculator are original analysis choices, not WWC-validated formulas. Sources opened 2026-09-29 UTC.
