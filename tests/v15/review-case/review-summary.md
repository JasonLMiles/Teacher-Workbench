# Review of the Grade 3 area exit ticket

**Revise before use: the original resource has 11 blocker failures.** Its area key is wrong, and it makes unsupported disability, tier-placement, and mastery claims. The corrected resource passes the selected design checks and is usable as a proposed brief formative check within the scope below.

Review date: 2026-09-29. Reviewer: Codex model review. The same reviewer reinspected the revision; no independent educator calibration occurred.

## Blockers and corrections

1. **Wrong mathematical key — original line 5.** The 3-by-5 rectangle has area **15 square units (B)** and perimeter **16 units**. The original calls the perimeter calculation area. Corrected S1/T2 elicit and explain both quantities. This matches the distinction in [CA 3.MD.7.b](https://www2.cde.ca.gov/cacs/id/web/359) and [CA 3.MD.8](https://www2.cde.ca.gov/cacs/id/web/362).
2. **Unsupported diagnosis and automatic Tier 3 placement — original line 5.** One selection supplies no diagnosis or placement history. Corrected T4 treats possible misconceptions as hypotheses to probe and keeps decisions with the established problem-solving process. [CDE's MTSS guidance](https://www.cde.ca.gov/ci//cr/ri/) describes data gathering, teams, and continuous improvement; it supplies no one-answer placement rule.
3. **Unjustified response-mode restriction — original line 5.** The written-only rule conflates handwriting/access help with mathematical reasoning. Corrected T1 preserves documented supports and permits the learner's own explanation through suitable modes. T3 distinguishes support that provides an answer or method. This design choice is consistent with [CAST UDL 3.0, consideration 5.1](https://udlguidelines.cast.org/action-expression/expression-communication/multiple-media/).
4. **Invalid individual mastery inference and missingness rule — original line 5.** A class percentage cannot demonstrate each learner's understanding. Excluding unanswered papers hides coverage. Corrected T3 records each learner, retains offered-but-blank responses as no evidence, exposes absence/not-offered counts, and keeps prompted success separate.
5. **Incomplete evidence for the stated target — original lines 2–4.** Selecting an area answer with all choices already labeled square units does not fully elicit the area/perimeter distinction. Corrected item 2 asks for perimeter and its unit; item 3 asks what both measures count. The notes limit the alignment claim to the sampled parts of the standards.

Useful refinements also supplied: administration timing, accepted strategies, an explanation frame, response-specific next moves, a fresh recheck/key, and a same-area/different-perimeter extension. Original line 6's move to “volume” is unsupported by the ticket, but volume is not categorically outside grade 3: [3.MD.2](https://www2.cde.ca.gov/cacs/id/web/352) includes liquid-volume measurement. Geometric volume is a different target.

## Scope and criterion selection

All six lines of the actual supplied resource were inspected, including the key and teacher directions. The revised S1 and T1–T7 were then read, their arithmetic recomputed, and all selected criteria reapplied.

Selected sets: common, mathematics, access/language, formative, intervention, and grading. Intervention applies because the original makes a Tier 3 placement decision; grading applies because it assigns full credit and a class rollup. Both remain in the reinspection to check the replacement scoring and support rules. Access/language applies because the original restricts oral assistance.

Excluded sets: ELA (no literacy score construct), science (no science/NGSS target), humanities (no disciplinary source interpretation), and rehearsal (no teacher rehearsal or simulated dialogue). These exclusions are preserved in both machine-readable ratings files.

The optional A2 language-scaffold criterion is not applicable to the original, which promises no language-development scaffold and supplies no learner language profile requiring one. It becomes applicable and passes in the revision because an actual optional explanation frame is supplied. No selected criterion was silently dropped.

## Completed rubric summary

The full reason and exact artifact locator for every judgment are retained in the ratings and script reports. These are original Teacher Workbench operational criteria, **not a validated instrument**.

| Criterion | Original | Revised | Evidence of correction |
| --- | --- | --- | --- |
| C1 Target and evidence agree | Fail | Pass | S1 asks for both measures and their meanings; T7 limits alignment. |
| C2 Content and keys accurate | Fail | Pass | T2, T5, T6 have recomputed values and correct units. |
| C3 Claims/sources honest | Fail | Pass | Authored examples and hypotheses are labeled; T7 and sources.json record checked sources and limits. |
| C4 Materials usable | Fail | Pass | T1 administration, S1 tasks, and T2–T6 keys/follow-up are present. |
| C5 Evidence supports inference | Fail | Pass | T3 separates individual evidence, prompts, blanks, absence, and rates. |
| C6 Participation/support appropriate | Fail | Pass | T1 preserves supports and response modes; T4 removes labels and automatic placement. |
| M1 Mathematical meaning | Fail | Pass | T2/T5 distinguish square coverage from boundary length. |
| M2 Student reasoning | Fail | Pass | S1 item 3/T2 accept defensible models and explanations. |
| A1 Construct-preserving access | Fail | Pass | T1/T3 distinguish access assistance from supplied math and retain required supports. |
| A2 Usable language support | Not applicable | Pass | T1/T5 provide a frame; optional fading preserves required supports. |
| F1 Diagnostic interpretation | Fail | Pass | T4 treats patterns tentatively and checks ambiguous/blank work. |
| F2 Actionable follow-up | Fail | Pass | T4/T5 connect a teaching move to a fresh recheck. |
| I1 Need and intensity | Fail | Pass | T4/T5 remove single-answer diagnosis/placement and keep support decisions bounded. |
| I2 Implementation/monitoring | Fail | Pass | T5 supplies a model, key, scaffold boundary, and follow-up decision. |
| G1 Policy and arithmetic | Fail | Pass | T3 gives categorical rules and explicit denominators; no invented class counts. |
| G2 Defensible interpretation | Fail | Pass | T3/T4 retain coverage and support conditions without grade/mastery claims. |

| Script result | Original | Revised |
| --- | --- | --- |
| Disposition | revise_before_use | selected_checks_passed |
| Pass | 0 | 16 |
| Fail | 15 | 0 |
| Not applicable | 1 | 0 |
| Insufficient evidence | 0 | 0 |
| Unreviewed | 0 | 0 |
| Blocker failures | 11 | 0 |

Original blocker IDs: C1, C2, C3, C5, C6, M1, A1, F1, I1, G1, G2. There are no unresolved selected criteria in the revision. The counts summarize supplied judgments; they are not a quality score, student score, or proof of efficacy.

## Evidence and verification

The installed skill's report script ran successfully on both ratings files:

```bash
python3 ../../../skills/tw-pedagogical-review/scripts/review_report.py original-ratings.json --out original-report.json
python3 ../../../skills/tw-pedagogical-review/scripts/review_report.py revised-ratings.json --out revised-report.json
```

The commands were run with the actual absolute ratings/output paths in this directory. The script checks rating completeness and summarizes reviewer judgments; it does not independently judge pedagogy.

Independent arithmetic verification counted unit squares and summed four side lengths for every rectangle used: 3×5, 3×4, 2×5, 2×6, and 1×12. Results and the original-source hash are in verification.json. The original is preserved unchanged in original-resource.md.

The reteaching representation is consistent with the [CDE Mathematics Framework, chapter 6, printed pp. 83–84](https://www.cde.ca.gov/ci/ma/cf/documents/mathframeworkch6.pdf). [WWC mathematics intervention recommendations 2 and 3](https://ies.ed.gov/ncee/wwc/PracticeGuide/26) are each rated **Strong Evidence**; [WWC's data-use recommendation 1](https://ies.ed.gov/ncee/wwc/practiceguide/12) is rated **Minimal Evidence**. These ratings belong to the recommendations, not to the authored tasks. The current WWC guide index was checked; this was a targeted source check, not a systematic research review.

No student work, response counts, individual accommodation plan, adopted curriculum, local pacing plan, or implementation data was provided. The design preserves required supports but cannot verify the delivery of an unseen plan. CDE landing pages encountered access errors on some requests; the relevant official chapter PDF and standards pages were actually opened. The full source ledger records version/date, section, claim, evidence type, limits, and verification date.

A qualified educator should independently calibrate a sample before this model-only review is used for a consequential or comparative evaluation. No classroom outcome, empirical validation, or general model-quality claim is made here.

## Files

- corrected-resource.md — student ticket plus teacher key, evidence profile, teaching moves, recheck, extension, and citations.
- original-ratings.json / original-report.json — preserved original judgments and script output.
- revised-ratings.json / revised-report.json — full reinspection judgments and script output.
- sources.json — claim-specific source ledger and retrieval limits.
- verification.json — independent arithmetic and original-file provenance.
- original-resource.md — unchanged snapshot of the supplied six-line artifact.

