# Connected planning and review in Teacher Workbench 1.5

The five additions fit into everyday planning. Ask in ordinary language; the orchestrator chooses useful specialists. General teaching support continues without a third-party account.

| Need | Skill | What you receive |
| --- | --- | --- |
| Understand a standard and its underlying learning | `tw-learning-commons` | Cited records, relationship direction, read coverage and a proposed instructional implication |
| Practice before class | `tw-lesson-rehearsal` | Internalization brief, one-at-a-time simulated dialogue, feedback and a teaching card |
| Decide the next teaching move | `tw-formative-checks` | Short student check, key, tentative response interpretations and follow-up tasks |
| Repeat useful work | `tw-recurring-workflows` | Tested per-run prompt and an actual native scheduled task only when requested and supported |
| Inspect a lesson or assessment | `tw-pedagogical-review` | Evidence-linked common/subject criteria, corrections and visible unresolved issues |

## Connect Learning Commons

The provider documents a [ChatGPT plugin and Claude connector](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/agent-plugins). Search the destination's catalog and follow its secure connection interface if offered. Availability varies by plan and settings. This release's catalog search did not return a matching Learning Commons integration in the author's account, so no native connection is claimed.

A developer can configure the documented [MCP server](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/mcp-server) in a compatible host, or use the included Python GET client with a key stored in the runtime's approved secret environment. The client does not need an OpenAI API key. Its source and exact commands are in the complete `tw-learning-commons` folder. An authorized JSONL export can be queried locally without an account connection. No server, key or private curriculum is bundled.

CDE remains the source for California standard verification. A graph relationship is a planning reference; actual student evidence is needed before concluding there is a gap. The native documented MCP tools and the broader REST/export datasets have different coverage. Curriculum metadata does not mean that gated lesson pages have been opened. Keep returned license/attribution and edition records.

## Schedule a teacher routine

Use the host's actual scheduler. [ChatGPT documents scheduled work](https://learn.chatgpt.com/docs/automations), but availability, apps and durable file access vary. Teacher Workbench first creates a concrete sample and successfully reads required external sources. It confirms activation only from the scheduler's result. The included weekly planner produces an unscheduled JSON payload; it is not a scheduler. No personal recurring task was activated while building this package.

Each user supplies their own source locations, connections, school calendar, timezone and authorized destination. Account access and personal schedules do not transfer with the shared plugin. Requests to send messages, publish materials or change grades require explicit authorization for those actions.

## Review an actual resource

Ask for a subject-specific review of the student pages and teacher key. The original rubric sets cover common criteria, mathematics, ELA, science, humanities, access/language, formative checks, rehearsal, intervention and grading. The reporting script summarizes supplied judgments and keeps blockers, insufficient evidence and unreviewed criteria visible. It does not independently judge pedagogy or prove classroom effectiveness. A review of an intentionally flawed area check and its corrected version is included among the release examples.

## Use on another system

Copy the complete skill folders, including scripts, templates and references, and follow that system's supported installation method. Bind only real provider tools. Python helpers use the standard library; the timezone planner requires an available IANA timezone database. Without execution tools, the conversational workflows still work but should not claim computed or scheduled results. General native Google Sheets, Canva and curriculum navigation remain dependent on their respective connections.
