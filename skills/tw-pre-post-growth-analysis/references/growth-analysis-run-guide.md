# Matched pre/post calculation guide

The bundled Python 3.9+ script is `scripts/growth_analysis.py`. It uses the standard library for descriptive results; optional inference requires an installed SciPy. It makes no network requests and writes only the requested output file.

```bash
python3 scripts/growth_analysis.py assets/growth-input.example.json growth-results.json
```

The example is synthetic. Run from the skill folder, or pass absolute paths in the host. Load the actual input and output; do not claim a calculation from reading this guide alone.

## Input and audit

Provide `pre` and `post` arrays with stable `student_code`, `status` and `score`. Valid statuses: observed, missing, absent, not_administered, exempt. Nonobserved scores must be null; an observed zero remains zero. IDs must be unique within each wave. Order can differ; matching uses IDs. The script reports union, pre/post-observed, matched and excluded counts and each excluded learner's status. Only matched observed pairs enter growth summaries. Validate the actual design and measure outside the script.

Policy requires `comparable: true` and a substantive `comparability_note`; these attestations are not statistical equating. `analysis_scale` is raw with a common `score_min`/`score_max`, or percentage with positive `pre_max` and `post_max`. Percentage conversion does not itself make two tests equivalent. `direction` is higher or lower. Use interval-like scores only; ordinal levels should use transitions. Optional `inference` and `normalized_gain` are booleans. `confidence` is between 0 and 1 when inference is requested. Numeric scores must be finite and within their declared ranges.

## Definitions and interpretation

Change is post − pre; improvement reverses its sign for lower-is-better measures. Matched means use exactly the same learners. Sample SD uses n−1. The output reports mean/median/range/SD of changes and improved/unchanged/declined counts. Relative percent change is 100 × change/pre and is null when pre is zero; distinguish it from percentage-point change. This ratio can be inappropriate on scales without a meaningful zero.

Named standardized changes: `d_z` = mean change / SD of changes; `d_av` = mean change / arithmetic mean of pre and post SDs; baseline-standardized change uses pre SD. Each answers a different question. Undefined denominators return null, not zero or infinity. Do not apply generic small/medium/large thresholds to judge teaching effectiveness. See [Lakens (2013), correlated-samples section](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2013.00863/full).

If requested for higher-is-better bounded scores, normalized gain is change/(maximum−pre). The script excludes individual pretest-ceiling cases from that ratio, retains negative gains, and separately reports the mean of eligible individual ratios and the ratio of matched means. Neither is a causal effect estimate. Show eligible/excluded counts and discuss baseline/ceiling dependence.

Optional paired inference uses t = mean change / (SD change/√n), df=n−1, and a two-sided t interval. It requires at least two pairs with nonzero change variance; otherwise returns unavailable. SciPy version and assumptions are reported. [NIST paired observations](https://www.itl.nist.gov/div898/handbook/prc/section3/prc311.htm) and [paired-difference interval formula](https://www.itl.nist.gov/div898/handbook/prc/section3/prc312.htm) support the arithmetic. A confidence interval containing zero does not demonstrate equivalence. A class convenience sample, clustering, attrition, repeated testing and nonnormal differences need design-specific judgment.

## Beyond this calculator

No ANCOVA, comparison-group effect, multilevel model, causal inference, vertical scaling, reliable-change index or forecast is implemented. When requested, inspect the design and use a verified appropriate runtime, reporting methods and assumptions. Preserve dates, forms, exposure and supports; inspect missingness and ceiling/floor effects. [Current WWC handbooks](https://ies.ed.gov/ncee/wwc/Handbooks) govern specific study reviews; an ordinary classroom pre/post analysis does not acquire a WWC rating. Sources opened 2026-09-29 UTC.
