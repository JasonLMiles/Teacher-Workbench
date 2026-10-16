# Connections case result

The exact California record is `synthetic-a` on line 1. Its `SYN.3.A` code is explicitly a synthetic fixture, not a real standard. The second line shares the code but has jurisdiction `Other`. Both lines were read. No prerequisite edges or relationship schema are supplied, so prerequisites are unknown from this file; no-prerequisite and learner-gap claims would be unsupported. See `reference-pack.md` and `california-match.json`.

## Concrete unscheduled draft

- Title: Review supplied California SYN.3.A example.
- Cadence: weekly Friday at 3:30 PM, IANA zone `America/Los_Angeles`.
- Start: 2026-10-02.
- End condition: four occurrences, ending 2026-10-23.
- Status: draft only; no task ID exists, no next live run is confirmed, no account was connected.
- Proposed delivery: a private task result; no destination or persistent run state has been verified.
- Files: `workflow-brief.json` is the reusable input; `workflow-draft.json` is the local planner's validated draft; `one-run-prompt.txt` is the execution prompt; `sample-review.md` is a preview made from the actual supplied input.

| Occurrence | Local date (Friday) | Local time | UTC |
| --- | --- | --- | --- |
| 1 | 2026-10-02 | 3:30 PM PDT | 2026-10-02 22:30 UTC |
| 2 | 2026-10-09 | 3:30 PM PDT | 2026-10-09 22:30 UTC |
| 3 | 2026-10-16 | 3:30 PM PDT | 2026-10-16 22:30 UTC |
| 4 | 2026-10-23 | 3:30 PM PDT | 2026-10-23 22:30 UTC |

The four planned dates use PDT (UTC−07:00). These are planned occurrence times, not a scheduler's returned next-run times. No school-calendar exclusions were supplied or inferred.

The proposed VEVENT has `DTSTART;TZID=America/Los_Angeles:20261002T153000` and `RRULE:FREQ=WEEKLY;BYDAY=FR;COUNT=4`; it is only data in a draft file. The local planner does not contact a scheduler.

## Access and persistence needed before a future activation

1. A durable, authorized source locator or host-attached resource must replace the temporary scratch path. Preserve its content/version, provenance and any relationship schema. A cloud task cannot rely on this local path surviving.
2. Verify a harmless read through every external app actually required by the future task. The supplied local read does not verify any app connection. The example-file review itself needs no Learning Commons account; a future live graph review needs a supported connection and a successful authorized read of the real standard/relationships. Do not request credentials in chat.
3. Confirm a private output destination and durable minimal run-state location if change comparison or duplicate-output checks are desired. No prior-run comparison should be claimed without readable prior state.
4. If school-calendar skipping is desired, supply an actual calendar or explicit dates. Runtime skipping still consumes one of the four scheduled invocations unless the teacher later authorizes a different schedule.
5. Activation would require a separate request, discovery of the current scheduler schema/capabilities, a successful preview from the intended persistent sources, and validation of the scheduler's actual returned ID/status/next run. This request authorized preparation only, so no create/update/run-now action was taken.

Available automation metadata was discovered read-only; no native Learning Commons tool appeared in the available tool registry. This is not a claim that any catalog integration is unavailable or that an account is authenticated. No installation or connection flow was started.

## Validation

The Learning Commons local matcher returned one match and `complete: true` after scanning both lines. The weekly planner validates the exact IANA timezone, first weekday and count; its emitted status must be `draft_not_scheduled`. All report claims come from the supplied fixture or the local draft computation; no empirical instructional conclusion or official standards verification is asserted.
