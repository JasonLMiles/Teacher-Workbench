# Teacher Workbench 2.0 source validation

Prepared October 15, 2026. This source distribution retains the 45-skill Teacher Workbench suite and numerical methods. It adds an MIT license, a source-oriented README, six platform installation/usage guides, a focused Gem adaptation, and root-level single-skill ZIPs.

## Executable checks

The repository includes 55 existing offline tests: nine measurement tests, 26 grading/growth tests, and 20 workflow-helper tests. They use synthetic inputs. The structural validator checks all 45 names and routes, source-local links, identical grounding policy copies, and exact archive contents including the license. It verifies archive checksums and conservative upload size/file-count limits.

From the repository root:

```sh
python3 -B tools/build_skill_archives.py
python3 -B tests/test_measurement.py
python3 -B tests/test_grading_growth.py
python3 -B tests/v15/test_helpers.py
python3 -B tests/validate_package.py
```

Use Python 3.9 or later with an IANA timezone database (`tzdata` on systems without one). See `source-release-validation.json` for the recorded results from this source distribution.

## Previously completed checks retained with the suite

All 45 skill definitions passed canonical validation during the renaming release. A fresh workflow loaded `tw-orchestrator` and `tw-grade-calculations`, ran the bundled calculator, and returned 88.67% with a missing quiz excluded and 80.00% with it scored zero for the documented synthetic weighted-category case. The shared grounding policy is revision 2026-10-15.1.

The teacher guide was rendered and all 25 pages were visually reviewed. Its education-source verification date remains September 29, 2026. Historical validation records retain their original dates and scope; current skill names are used for navigation.

## Scope

Platform setup instructions were checked against official vendor documentation on October 15, 2026. Individual ZIP layouts and resource contents are checked offline. Live imports into Google, Copilot Cowork, and OpenAI accounts were not performed for this source distribution. Host tools, permissions, account eligibility, and provider validation still affect availability.

Offline checks and the single workflow case do not establish classroom effectiveness or measured time savings. Current education research and policy should be checked when relevant to a teaching request. Source publication does not activate schedules or connect external accounts.
