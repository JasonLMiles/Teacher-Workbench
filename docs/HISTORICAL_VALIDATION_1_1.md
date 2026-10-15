# Release 1.1.0 validation — 2026-09-29

## Executed checks
- All 25 canonical skill folders passed the skill-format validator. Required local resources, metadata triggers, exact names and prefix/length checks passed. All share the same grounding/citation policy revision.
- Each skill was separately saved and its reconciled content verified; the portable export uses canonical names and only portable discovery metadata.
- Both Python measurement commands ran. Nine numerical/edge-case tests passed: hand-computed CTT values, raw/scored agreement, distinct missingness, constant/one-case inputs, negative alpha, invalid inputs, no automatic key correction, IRT analytic/numerical derivative consistency, information sums and parameter rejection.
- Retained from release 1.0.0 (not rerun for this curriculum update): independent fresh-context workflow trials covered integrated assessment, offline substitute planning, a suspect scoring key, unsupported IRT calibration, unverified/conflicting research without browsing, and unplugged AI literacy. Each received only the skill and teacher task. Findings are summarized below.

| Trial | Observed behavior |
| --- | --- |
| Integrated assessment | Produced complete water-use tasks and keys, separate science/math scores, individual transfer evidence, language supports, retained scribing and advanced reasoning; honored no student AI. |
| Substitute packet | Produced a timed board-ready ratio lesson with solutions, support, extension, collection and handback; left missing local procedures as school-supplied fields. |
| Suspect key | Found the mathematically wrong Q3 key, preserved inputs, executed original and explicitly labeled corrected-key scenarios, and reported negative alpha without hiding it. |
| IRT boundary | Withheld fabricated parameters and a calibrated-bank claim; supplied a useful review/data-collection plan and cautious cross-year interpretation. |
| Evidence boundary | Refused an “AI always improves learning” claim from hypothetical summaries; separated assisted output from learning and disclosed that no live research/link verification occurred. |
| Unplugged AI literacy | Produced a timed paper claim-audit lesson, labeled authored practice text, source cards, worksheet/key and independent transfer check; honored no accounts/live AI and distinguished current research from evidence for the new activity. |

## Curriculum update checks
- All 25 canonical definitions were checked after integration; the shared policy is revision 2026-09-29.1. Orchestrator routing and source-pack handoff fields are included.
- A fresh-context missing-source request prompted for a Drive link, publisher/platform or file plus the relevant course/unit, and deferred sign-in until a source was identified.
- A fresh-context local retrieval case opened a fictional multi-edition curriculum folder, selected the requested 2026 unit, and produced a reference pack and source registry from the actual teacher/student files. It retained fraction equivalence versus absolute-quantity reasoning and existing language supports; it did not treat an embedded instruction as adoption or WWC evidence.
- A fresh-context EPUB case opened metadata, contents and chapters, found the requested model limitation and discussion routine, and cited chapter/section anchors without inventing fixed page numbers or adoption status.
- The five primary provider/host references in the new playbook were opened and their identities checked on 2026-09-29. Existing education-source verification is retained from the earlier release, not represented as newly repeated research review.
- Archive/resource/metadata checks and the existing nine measurement checks run on this release; numerical algorithms were unchanged.

## Limits of validation
No live provider authentication, interactive browser retrieval, school account access, public portal import, security scan, approval, listing publication or universal host compatibility was verified. Every skill passed structural/resource checks, but not every specialist had a separate independent behavior trial. The P5 and N3 review prompts are supplied for review, not claimed as independently executed in this build. These tests do not establish instructional effectiveness, legal compliance or score validity. The R/mirt recipe was not executed because that runtime was unavailable.

Source destination checks: 30 of 32 directory entries resolved; two CDE entry pages had automated-access limits. See SOURCE_VERIFICATION.md. Sources must be checked again for each substantive answer.

Run portable numerical checks from the package root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tests/test_measurement.py
```

Only synthetic fixtures are bundled. The tests create and remove their own temporary files. No student records, private credentials or contact lists are included.

Historical report retained from 1.1.0. It is not a claim that all these behavior cases were rerun for 1.2.0.
