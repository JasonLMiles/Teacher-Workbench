# Supplied-export reference pack

Teaching question: Find the California `SYN.3.A` record and determine what the supplied file establishes about prerequisites.

Route actually used: authorized supplied-file read plus the Learning Commons skill's bounded `local` JSONL matcher. It scanned both lines and returned one exact match. `complete: true` means this file scan completed; it does not establish graph or dataset completeness. No live Learning Commons connection or API read was used.

| Record / relationship | Source ID and locator | What was actually read | Attribution / license | Coverage limits |
| --- | --- | --- | --- | --- |
| California match | `synthetic-a`; supplied `nodes.jsonl`, line 1 | Label `Standard`; `statementCode: SYN.3.A`; `jurisdiction: California`; `gradeLevel: ["3"]`; description `Synthetic fixture, not a real standard.` | License field: `synthetic test fixture`; no publisher/author attribution supplied | No framework ID/title, official edition, adoption/current status, source URL or dataset release provided |
| Same code, other jurisdiction | `synthetic-b`; supplied `nodes.jsonl`, line 2 | `statementCode: SYN.3.A`; `jurisdiction: Other`; description `Different synthetic record.` | None supplied | Excluded by the jurisdiction match; not an equivalent California record |
| Prerequisite relationships | No edge/relationship IDs or relationship records supplied in either line | Both complete raw node records inspected; no relationship schema or edge direction present | Not supplied | Prerequisite coverage is unknown; this file cannot support a graph traversal |

CDE confirmation: not established. The file itself identifies the matching record as synthetic, so it is not evidence of an adopted California standard and no official standard statement is claimed. CDE was not queried for this fictional identifier. If a real standard is intended, its framework/edition and exact California record must first be supplied or retrieved and verified; do not silently substitute another code or framework.

## What can be inferred

The file establishes only a synthetic node labeled as a California grade-3 record and a second, different-jurisdiction node sharing its code. An exact jurisdiction filter matters. It does not establish prerequisite existence, nonexistence, direction, sequence, component mastery or learner gaps. The absence of edge records from this two-node export is missing relationship evidence, not proof that the standard has no prerequisites. Node order and the shared code do not establish any relationship.

## Instructional implications

No instructional prerequisite task or learner-gap inference is justified by this fixture. For real instructional use, first obtain the intended genuine standard/framework and a scoped relationship export with its schema, or an authorized successful read using a genuine returned standard identifier. Only then can an instructional prerequisite hypothesis be paired with a brief student task; no student evidence is supplied here.

## Provenance

- Supplied file: `../cases/nodes.jsonl`.
- Exact-match output: `california-match.json`, retaining line number and full raw record.
- File SHA-256: `5a9924068d6380b5871699e84eaf0272da5323a0f1a401290b5f234ffe60f61e`.
- Retrieved: `2026-09-29T15:31:38.782751+00:00`.
- Coverage: two JSONL lines; one California exact match; no malformed or unread records in this supplied file.
- Dataset release/version, export date, framework edition, upstream source URLs and adoption status: unprovided.
- This review verifies a local fixture read, not account access, a comprehensive index, live endpoint compatibility or a curriculum lesson read.
