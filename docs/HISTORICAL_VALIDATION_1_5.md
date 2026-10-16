# Release 1.5.0 validation

Validated September 29, 2026. This report covers five new skills, routing updates, three new executable helpers, updated creation specifications, and the expanded teacher guide.

- Canonical skill structure was checked in the installed source location. Exported source folders are compared byte-for-byte with the saved files.
- Twenty offline helper tests passed: API pagination and partial coverage, cursor-loop/schema errors, fixed-host and credential-query restrictions, redirect refusal, jurisdiction-specific local matching, schedule timezone/count/weekday/DST behavior, explicit holiday skip semantics, and review blocker/missing-evidence/duplicate-rating behavior.
- Three fresh-context workflow cases exercised all five additions. They produced actual files rather than descriptions of promised artifacts. A rehearsal continuation checked feedback on the teacher's own move and another opportunity to try.
- The review case used an intentionally flawed area ticket: 15 failures, including 11 blockers. The corrected resource passed the same 16 selected criteria. This is a model review and reinspection, not independent educator calibration or proof of effectiveness.
- The teacher guide's 25 rendered pages were visually inspected. Its directory includes all 45 skills. The same PDF, Word and Markdown editions are included in both packages.
- The release packaging check verifies exact catalogs, shared policy consistency, local references, manifest bounds, prompt coverage, guide copies, file hashes and ZIP integrity. See the resulting release record for the final outcome.

## Scope and limits

Learning Commons documentation and current host automation schemas were inspected. A native Learning Commons catalog search did not expose a matching plugin in the author's account. The REST client was tested with mocked transport and the local reader with synthetic records; live authentication and the provider's current server responses were not tested. No key, native connection, personal task, public plugin publication or destination-host installation is bundled or claimed.

The 35 numerical checks recorded for release 1.4.0 remain historical evidence for unchanged calculators. They were not rerun merely for this release. Earlier classroom/resource cases and source logs retain their original scopes and dates. No classroom effectiveness trial, general model comparison or formal teacher-evaluation validity is claimed.

## Reproduce scoped checks

From the package root with Python 3.9+ and a system IANA timezone database:
```
python3 -B tests/v15/test_helpers.py
```
The helper test uses synthetic/mock data and creates no external side effects. Read `tests/v15/README.md` before using the case files: the original review input intentionally contains errors and must not be used as teaching guidance.
