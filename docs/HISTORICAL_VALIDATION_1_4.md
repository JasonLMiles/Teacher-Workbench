# Release 1.4.0 validation — 2026-09-29 UTC

- All 40 canonical skills passed the format validator. Eight new skills and three integrations were saved and reconciled for this increment, following the assistant-group skill and five saved integrations. Shared grounding policy revision 2026-09-29.2 is identical across all skills.
- Three fresh-context trials were reviewed: evidence-based intervention grouping plus usable tier activities/assistant handoff; Bloom analysis plus a Marzano scale, rubric and standards-reporting policy comparison; and six actual calculator runs plus an independently checked custom final-exam calculation. See [detailed review](intervention-grading-validation.json). The earlier two assistant-packet trials are retained in [their report](assistant-behavior-validation.json).
- 26 new numerical/edge checks passed for standards, growth and grade calculations. The first test pass needed a test-only floating-point comparison tolerance; the calculation was correct. Subsequent checks passed. The nine existing measurement checks also passed: 35 numerical tests in the release gate.
- Export checks cover exact names, metadata, local resources, identical shared policy, manifest limits, archives, canonical authored-content equality and independent checksums for all 40 skills. Prompts, guide, catalogs and completion records cover the full suite.
- [Primary-source verification](SOURCE_VERIFICATION.md) records exactly which pages were opened and their scope. Current claims must still be reverified at use.

These are synthetic calculation, generated-output and structural checks, not classroom effectiveness studies. The intervention trial does not establish a validated dosage or program. Taxonomy and rubric examples do not validate a grading system. The growth script received an input-validation hardening after the fresh-context run; the final numerical gate covers the revised code and valid example calculations remain unchanged.

No live gradebook writes, Google Sheets/Canva creation, private-provider sign-in, interactive private-browser retrieval, public portal import or public publication was performed for this release. Not every prior skill received a new independent trial. Historical 1.2 and earlier checks retain their original dates/scope. The optional R/mirt calibration recipe remains unexecuted; full IRT calibration was not performed.

Run from the extracted package root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tests/test_measurement.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/test_grading_growth.py
```

Python 3.9+ is needed for the new calculators. SciPy is optional for paired-t inference; the inferential test reports a skip if it is unavailable. Runtime versions for the fresh calculation demonstration were Python 3.12.14 and SciPy 1.17.0. All 35 numerical tests ran without skips in the build environment.
