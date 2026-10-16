# Scheduling across hosts
Check the current host's scheduling capability, tool schemas and permissions. [ChatGPT scheduled tasks documentation](https://learn.chatgpt.com/docs/automations) was checked 2026-09-29. Availability and allowed integrations vary. A portable skill supplies the job instructions; the host supplies execution, durable storage and connections.

For ChatGPT's exposed automation tools, use current metadata as the operational contract. Before creation, successfully read every required external service. Discover a suitable integration if absent. Use native secret/connection UI; do not embed credentials in a task. Exact clock-time requests use exact scheduling, an IANA timezone and the native schedule fields. Use relative-offset fields only where supported. Current VEVENT tooling requires no SUMMARY or DTEND; use RRULE COUNT/UNTIL for a supported end condition. Event-based jobs require supported trigger schema and app access; do not add a time schedule to that payload. Consult host limits before polling a condition.

The included planner supports weekly schedules only:
```
python3 scripts/workflow_plan.py assets/workflow-brief.json --out workflow-draft.json
```
Edit the template first. The planner rejects invalid dates/zones, nonexistent DST times, ambiguous local times and weekly times in the 01:00–02:59 DST window, mismatched first weekday and invalid repeat counts. Its output says `draft_not_scheduled`. It does not contact a scheduler, test an external connection or verify school holidays. For exclusions, the runtime prompt checks an explicit date list/calendar and may skip work while a scheduled invocation still occurs. Do not describe that as suppressing the scheduler's invocation.

Before live activation, run the workflow once using authorized sources and review the result. Confirm the scheduler's returned ID/status and next-run time after creation. Preserve those for requested changes; a copied job brief has no live task ID. Review early runs and adjust. Store a small run record only where authorized: task ID, run date, source IDs/version, coverage, output locator, status, unresolved issue. No-input and failed-read runs must not become invented student progress. Gradebook writes, public sharing and person-directed messages require their own explicit authorization.

Examples: prepare next week's draft lessons from a stable unit folder; review a deidentified tracker every Friday; periodically check for relevant new research and report search date/coverage. Do not assume school holidays from California residency or infer a teacher's school schedule.
