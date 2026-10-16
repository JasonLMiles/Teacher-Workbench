# CTT methods and interpretation

Use these as calculation definitions, not evidence that a generated test has been validated. Ground the intended score use in the [AERA/APA/NCME Testing Standards](https://www.testingstandards.net/open-access-files.html); verify the current edition at use. For theory, consult [Holland and Hoskens, ETS RR-02-20](https://www.ets.org/research/policy_research_reports/publications/report/2002/hyek.html). For estimation limits, locate the full [ETS small-sample item-estimation report](https://www.ets.org/research/policy_research_reports/publications/report/2022/keql.html), not just its abstract.

## Definitions implemented by the calculator
- Observed score is modeled as a true-score component plus error; the component concerns expected performance over the model's replications, not a fixed essence of the person.
- Item facility: mean awarded score divided by the maximum; for dichotomous scoring, proportion correct. The denominator is the item's actual scored count under explicit missing rules.
- Corrected item–total relationship: Pearson correlation of an item with the sum of the other items. The script uses the same listwise-complete cases for all such correlations. Constant vectors return null rather than a fabricated zero correlation.
- Coefficient alpha: `k/(k-1) * (1 - sum(sample item variances)/sample total-score variance)`. Item and total variances use the same complete cases and `n-1` denominator. For dichotomous scores this is the alpha/KR-20 equivalent with consistent denominators. At least two items, two complete cases and positive total variance are required for a numerical result; these minimums do not establish interpretive adequacy.
- Conventional SEM: `sample total-score SD * sqrt(1-alpha)` only if alpha is in [0,1]. This is a conventional aggregate approximation under appropriate reliability assumptions, not conditional error for each score. Do not turn it into a high-stakes interval without evaluating assumptions and intended use.

## Decision rules
Inspect the scoring key and item content before acting on a flag. Negative item–rest relationships may reflect a wrong key, ambiguous item, coding, distinct constructs, instruction or chance. Do not automatically reverse scoring, delete items or maximize alpha at the expense of content coverage.

Internal consistency, temporal stability, inter-rater agreement, classification accuracy, dimensionality and validity answer different questions. Alpha alone establishes none of the latter. Consider score structure, dependence, content and administration conditions; report other reliability evidence only if actually analyzed with a suitable method.

Use small classroom samples to describe this administration and guide review. Do not use a convenience warning threshold as a universal adequate sample size, a passing rule or a justification for an item bank. No automatic pass/fail or mastery rule is implemented.

Per-item available-case statistics may involve different students, while reliability uses complete cases. Report both counts and why omissions, invalid responses and items not administered were handled differently. A total based on different available items is not automatically comparable; the script does not rank incomplete totals.
