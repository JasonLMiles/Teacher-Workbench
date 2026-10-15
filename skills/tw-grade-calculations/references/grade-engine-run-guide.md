# Grade calculation engine and advanced recipes

Run the Python 3.9+ standard-library calculator from the skill folder:

```bash
python3 scripts/grade_engine.py assets/grade-input.example.json grade-results.json
```

Inputs are synthetic in the bundled example. Actual calculations require the teacher's policy and deidentified records. The script uses exact decimal arithmetic, makes no network requests and writes JSON; numeric results are strings to preserve precision. No grades are posted.

## Supported policy and input

Copy the example policy and replace every rule deliberately. Unknown policy keys are rejected. Required rules: aggregation (points/equal_items), missing (error/exclude/zero), attempts (error/latest/highest), drop_lowest (nonnegative integer per category, or category mapping), drop_min_keep (at least 1), drop_missing_zeros (boolean), category_weights (null or positive weights summing exactly to 1), empty_categories (error/renormalize), extra_credit (forbid/points_bonus), allow_scores_above_max, floor_pct/cap_pct (null or numeric), round_digits, rounding (half_up/half_even), threshold_basis (raw/rounded), and thresholds (possibly empty).

Each record supplies student_code, assignment_id, positive integer attempt_order, category, earned, positive possible, and status (observed/missing/exempt). Missing/exempt earned values must be null; observed zero is retained. Optional extra_credit=true requires possible=0, points aggregation and points_bonus policy. A bonus adds earned points to a retained regular numerator; it never creates a denominator. Additional score above an ordinary maximum requires allow_scores_above_max=true. Negative scores are unsupported.

Multiple attempts require retake_comparable=true after reviewing the actual forms/targets. Latest selects the greatest attempt_order before applying missing exclusion; a latest missing submission can therefore leave the assignment ungraded under exclude. Highest ranks observed percentages (or explicit missing-zero values), with later attempt_order breaking ties; it excludes nonobserved attempts from ranking. An exempt assignment must be represented consistently across its attempts. Review these semantics against local policy rather than assuming they fit every gradebook.

## Calculation order

1. Validate records/policy. Select attempts; log each unselected record. Apply missing/exempt rule, retaining its reason.
2. Within each category (or the whole course when category_weights is null), drop the requested number of lowest-percentage eligible regular items, retaining at least drop_min_keep. Assignment ID breaks tied percentages. Missing-zero eligibility follows drop_missing_zeros. This rule is not an optimization to maximize final grade. Report requested versus actual drops.
3. Points aggregation = (sum retained earned + bonus)/(sum retained possible) ×100. Equal-items aggregation = mean of each retained earned/possible ×100. Equal-items plus point bonuses is unsupported. These methods differ when task maxima differ.
4. With categories, combine category percentages with declared weights. Empty categories either leave that learner's result unavailable or explicitly renormalize available weights. All categories empty never produces a grade. Report missing categories and denominators.
5. Apply a final overall floor/cap, then declared display rounding. Determine labels using the explicitly selected unrounded or rounded value and descending minimum thresholds. Do not round every item unless a separately verified local procedure requires it.

Every learner receives an audit trail and intermediate category totals. A final floor is not a per-item minimum; a final cap is not a score correction. No unsupported late penalty, grade replacement, custom drop optimization or external score is silently approximated.

## Advanced topics outside the bundled engine

For a requested extra policy, write a transparent equation or a small verified calculation/workbook and label it custom. Examples below are mathematical illustrations, not recommended grading rules.

- **Term/final blend:** G=(1−w)C+wF. If C=82 and the final has weight .20, reaching 85 before rounding requires F=97. If w=0, the final cannot change G. Check reachable score ranges and the policy's actual rounding/threshold stage.
- **Credit-weighted GPA:** sum(grade points × included credits)/sum(included credits). With 3 included credits at 4.0 and 1 at 3.0, GPA=3.75. The institution must supply letter/plus-minus mappings, weighted-course bonuses, repeated-course handling and which credits belong in the denominator.
- **Several term weights:** verify they sum to one and that term grades already include or exclude the final correctly. Do not count an exam twice.
- **What-if sensitivity:** recompute the same source under explicitly named alternatives such as missing excluded versus zero, raw versus rounded thresholds, or latest versus highest reassessment. Preserve source data; explain the policy consequence instead of choosing a rule to reach a desired grade.

For standards-based conversions use the actual local crosswalk. Neither 3/4 nor a rubric mean automatically means 75 percent. Arithmetic correctness does not establish fairness or validity. [California Education Code §49066](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=EDC&sectionNum=49066) addresses teacher determination and specified grade-change exceptions/procedures in school districts, not a universal formula. Opened 2026-09-29 UTC; verify current local policy and applicable requirements for the actual question.
