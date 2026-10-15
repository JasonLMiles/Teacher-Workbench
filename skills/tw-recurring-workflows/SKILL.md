---
name: tw-recurring-workflows
description: "Prepare and, when supported and requested, schedule recurring teacher planning and evidence-review work. Use for weekly lesson preparation, periodic curriculum updates, repeated deidentified progress reviews, scheduled reminders, or pausing/updating an existing teaching workflow."
---

# Teacher Workbench Recurring Workflows

Read [grounding and citations](references/grounding-and-citations.md) and [host and scheduling rules](references/host-and-scheduling.md). Use [the workflow brief](assets/workflow-brief.json). A skill is not itself a background service.

## Make the job concrete
Reuse the user's requested outcome, source locations, delivery destination, cadence and timezone. Ask only for material missing scheduling details. Resolve ambiguous school days with the actual school calendar; weekdays do not establish holidays. Separate a reusable template request from a request to activate a task. Building this skill or its package does not authorize a live personal task.

Write a prompt for one execution: relevant Teacher Workbench skills, stable source IDs/links and scope, inputs to reread, required output, destination, limits, missing-data behavior and stop/escalation conditions. Keep credentials and unnecessary student identifiers out. For a simple reminder, source access may be unnecessary. For data/lesson generation, make a sample output using actual available inputs before scheduling; a preview is not a successful scheduled run.

## Activate only through actual host capabilities
1. Discover the native scheduling tools and read their current schemas/instructions. Check existing tasks privately when needed to avoid duplicates; preserve an existing task ID when updating. Do not use a displayed task list unless the user asks to see it.
2. For every required external app, perform a successful harmless read in this conversation before creation. A catalog listing or connection badge is insufficient. If blocked, offer the exact connection/approval step, continue preparing the reviewable prompt, and report blocked activation. Do not create a task assuming access will work later.
3. Verify persistent inputs and output access. A cloud task cannot depend on a temporary local scratch path. Use an authorized stable file/project/service or attach a durable resource through the host. Never promise that a shared skill transfers an account connection, district policy, private folder or personal schedule to another user.
4. Translate the requested time using an IANA timezone. Use exact scheduling for a stated clock time and flexible scheduling only when appropriate and supported. The bundled `scripts/workflow_plan.py` validates a weekly time-based draft; it does not schedule anything. Inspect returned next-run times after activation. Use native facilities for monthly, one-off, event or condition triggers.
5. For event triggers, discover supported events and schemas and verify app access. Do not silently substitute polling. Follow current host limits, required channel membership and permission rules. Keep time-based and event-based payloads separate where required. For condition polling, obey the actual minimum interval.
6. Create/update only the authorized scope. Do not send family messages, publish files, change grades or share access without explicit authorization for that action. Follow permission already supplied; do not repeatedly ask to approve harmless authorized setup.
7. Confirm only the scheduler's actual returned ID, status, cadence/timezone and next run. Report failures honestly. If the host cannot schedule, provide the finished reusable prompt and manual routine; label it unscheduled. Never imply a timer is running because a JSON or calendar file exists.

## Each run
Read current sources and versions, check calendar exclusions, use the task's relevant specialist and produce a dated draft with citations. Record coverage and changes since the last successful run if authorized durable state exists. If no new evidence or a source is unavailable, state that; do not invent results or overwrite a previous valid output. Treat missing work as missing evidence. Keep formal grading and placement decisions with the teacher. Prevent duplicate outputs using the run ID/date and existing destination when supported, without claiming exactly-once execution.

For a requested pause, change or cancellation, use the host's task tool and verify its result. Explain how the teacher can inspect the first runs and adjust the routine.
