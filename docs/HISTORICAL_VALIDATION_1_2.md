# Release 1.2.0 validation — 2026-09-29

## Executed for this release
- All 31 canonical definitions passed the skill-format validator; each was saved separately and reconciled content was verified. Shared policy revision 2026-09-29.2 is identical across the suite.
- Portable export checks cover exact names, discovery metadata, relative resources, manifest fields and lengths, archive paths, checksums and consistency with canonical authored content.
- Four fresh-context behavior trials exercised source-document intake and fixed-format lesson/substitute output; an offline student reflection/progress XLSX; a Canva-importable editable teaching aid; and a PBIS teaching routine. See the detailed [behavior report](workflow-behavior-validation.json).
- The unchanged measurement tools passed the existing nine numerical/edge-case checks as a release packaging gate. This does not imply full IRT calibration was run.
- Primary references for behavior, reflection and provider production were retrieved on 2026-09-29. The California MTSS entry was access-limited and is not counted as full-text verified. See [source verification](SOURCE_VERIFICATION.md).

## Scope of the behavior trials
| Trial | Observed result |
| --- | --- |
| Document intake, lesson and substitute | Read actual supplied scope and lesson fixtures; preserved objectives, task order and scribing; applied a conversation correction from 45 to 30 minutes; produced the ten-section lesson and nine-section substitute packet with board-ready tasks, separate keys and missing local procedures marked. External retrieval was explicitly disabled for this trial; the plans disclosed unverified official alignment. |
| Student tracking and Sheets fallback | Created an actual editable XLSX with student prompts, data, graph and teacher notes; preserved an observed zero separately from missing/absent data; checked rate calculations and their limits. No Google account was connected or native Sheet created. |
| Teaching aid and Canva fallback | Created actual editable PPTX resources with native text/shapes, separate teacher key and rendered previews; inspected layout and fraction representations. No Canva account was connected and import fidelity inside Canva was not tested. |
| PBIS routine | Produced an expectation matrix, weekly routine-teaching plan, scripts, private paper reflection, teacher observation record and proposed adaptation rules; distinguished early implementation checks from a full self-monitoring evaluation and preserved supplied supports. |

## Unperformed destination checks
No native Google Sheets or Canva account creation/import/readback, live provider authentication, interactive private browser retrieval, public portal import, approval, listing publication or universal-host compatibility test was performed. These skills depend on actual destination capabilities and user permissions. Every definition passed structural checks; not every specialist received a new independent trial. Local outputs and realistic fixtures do not establish instructional effectiveness, legal compliance, score validity or cloud integration success.

Historical 1.0/1.1 workflow checks remain available in [the prior report](HISTORICAL_VALIDATION_1_1.md) and are not described as rerun. The optional R/mirt recipe remains unexecuted. Current sources must be rechecked for substantive answers, especially law, AI research and changing provider features. No student records, private curriculum, credentials or account data are bundled.

Run the portable numerical gate from the package root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tests/test_measurement.py
```
