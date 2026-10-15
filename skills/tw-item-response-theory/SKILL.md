---
name: tw-item-response-theory
description: "Explain and plan defensible IRT analysis: Rasch/1PL, 2PL, 3PL and polytomous models. Use for calibration readiness, model/scale choices, information, precision, linking or DIF; decline unsupported parameter estimates."
---

# Teacher Workbench Item Response Theory

## Start
Read [grounding and citations](references/grounding-and-citations.md) for every invocation. Read [coordination and capabilities](references/coordination.md) for the handoff and host-specific fallback rules. Use the [source directory](references/source-directory.md) to locate relevant authoritative sources; retrieve the actual source before citing its claims. Apply only the foundations relevant to the teacher's decision.

## Inputs
Required for calibration: anonymous item responses with category/missing definitions, scoring, design, purpose and relevant administration conditions. Optional: anchors, groups, sample plan, model theory and prior calibrations. Conceptual requests need no real data.

## Workflow
1. Read references/irt-methods.md. Decide whether the question needs calibration, scoring from a known calibrated bank, a conceptual demonstration or simpler CTT. Never estimate empirical item parameters from item wording or substitute simulated results for unavailable data.
2. Use assets/calibration-readiness.md to assess construct/response model, dimensionality, local independence, coverage, sparse categories, sample/design adequacy and identification. There is no universal adequate N; judge the proposed parameters, model, information and intended precision. Small classroom samples often support descriptive CTT and a future collection plan instead.
3. Specify model and scale explicitly. Distinguish Rasch constraints from a generic equal-slope 1PL parameterization; select 2PL/3PL or polytomous models only with a substantive/statistical rationale. State latent scale constraints, item parameterization and logistic scaling constant.
4. Bind actual estimation to a verified, available psychometric library. The bundled R/mirt recipe is an analysis template requiring R and mirt, not a claimed tested calibration service. Verify its installed API, execute it only with suitable data, and record software/version, estimator, fit specification, convergence, standard errors and warnings. If unavailable, provide the plan and say calibration was not run.
5. Examine global/item fit, residual dependence, dimensionality, boundary estimates, uncertainty and sensitivity before interpreting information or scores. DIF flags require a suitable group/anchor design and substantive fairness review; a flag alone is not proof of bias. Equating/linking needs defensible common-person/item design, invariance and scale checks.
6. Use scripts/irt_known_parameter_demo.py only for labeled known-parameter probability/information illustrations. It does not calibrate items or estimate students' ability. Return a bounded interpretation and data/analysis next steps.

## Deliver
Return either a defensible executed analysis with provenance/diagnostics, or an explicit readiness decision and runnable analysis plan. Separate demonstration parameters from estimated parameters and report uncertainty and scale conventions.

## Limits
Do not infer fixed personal ability, promise model fit, manufacture convergence/DIF findings, or combine unrelated cross-curricular constructs into a unidimensional model by default. More complex psychometrics is not automatically better classroom advice.

## Routing examples
Direct: “Is IRT appropriate for our item bank?” Overlap: a 25-student classroom quiz → CTT if it answers the question. Boundary: “give item difficulty from these stems” → explain why response data and a model are needed.

## Reusable resources
These are editable working formats, not finished teacher deliverables. Fill them with actual task content, examples and keys; remove unused fields. Label authored examples and proposed decision rules.
- [calibration-readiness.md](assets/calibration-readiness.md) — adapt and fill for the requested task.
- [model-analysis-spec.md](assets/model-analysis-spec.md) — adapt and fill for the requested task.

Read [IRT methods](references/irt-methods.md) and [R/mirt recipe](references/mirt-analysis-recipe.md). Run the [known-parameter demonstration](scripts/irt_known_parameter_demo.py) with [synthetic parameters](assets/demo-parameters.json) only to explain curves/information. The demonstration is not calibration.
