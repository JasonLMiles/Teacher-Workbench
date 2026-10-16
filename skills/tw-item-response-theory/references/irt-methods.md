# IRT method selection and interpretation

Use the [Testing Standards](https://www.testingstandards.net/open-access-files.html) for score-use quality and the [ETS IRT chapter record](https://www.ets.org/research/policy_research_reports/publications/chapter/2017/jyic.html) as an entry point to the underlying methodology. Read the full relevant methods source before detailed claims. Check [ETS research on alternative/small-sample estimation](https://www.ets.org/research/policy_research_reports/publications/report/2022/keql.html) when the sample is limited. No bibliography substitutes for analysis of the actual design.

## Model and scale
For the known-parameter demonstration, `P(theta) = c + (1-c) * logistic(D*a*(theta-b))`: `a` positive discrimination, `b` location, `c` lower asymptote, and explicit logistic scale `D` (default 1). These supplied numbers are illustrative, not fitted. Equal fixed slopes and c=0 illustrate Rasch-form curves on that chosen scale; a generic equal-slope 1PL can use other identification conventions. State the software's convention rather than treating labels as interchangeable.

Use 2PL for varying slopes or 3PL with a lower asymptote only when design, construct and data support the additional parameters. The 3PL asymptote is a model parameter, not a directly observed individual guessing rate. Ordered-category models such as graded response or partial-credit variants require appropriate category meaning and response processes; do not select from dichotomous examples by convenience.

Choose and report identification (e.g., latent mean/variance constraints and anchors), estimator, priors if used, scale transformation, convergence criteria and uncertainty. A numerical fit is not evidence that substantive assumptions hold. Evaluate dimensionality, local dependence, category use, item/person coverage, boundary estimates, residuals, sensitivity and fit limitations.

## Information and decisions
For a dichotomous item, information is `(dP/dtheta)^2 / (P*(1-P))`. Independent item information on one scale can be summed. The demonstration reports `1/sqrt(information)` as an asymptotic illustration; it is not a calibrated student interval and ignores parameter uncertainty. At extreme numerical saturation it reports zero information and a null inverse-root value.

DIF requires defensible group definitions, sufficient information, anchors/identification and suitable model comparisons, with multiplicity and substantive review as relevant. A statistical flag is not proof of bias, and no flag proves fairness. Linking/equating requires a design and invariance evidence; separate calibrations or raw percent correct do not establish a common scale.

Do not calibrate from item stems, invent parameters, infer fixed traits, or default to a unidimensional model for multiple school subjects. If evidence is insufficient, provide CTT descriptives or a collection plan, stating why that serves the classroom decision.

## Bundled demonstration
Requires standard-library Python 3.9+. Run from the skill directory:

```bash
python3 scripts/irt_known_parameter_demo.py --config assets/demo-parameters.json --output irt-demo-result.json
```

Expected check: for `a=1, b=0, c=0, D=1, theta=0`, probability is 0.5 and item information is 0.25. A second example has `a=1.2,b=0.5,c=0.2`; at theta=b, probability is 0.6 and information is 0.24. All parameters are synthetic and supplied, not estimated. The script does not read student responses, fit models, test DIF, or equate forms.
