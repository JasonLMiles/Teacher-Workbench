# Curriculum references and handoff

Use the registry and reference-pack templates only for fields that matter to this task. Empty template fields mean unknown, not verified. Keep the final response readable rather than exposing internal routing.

## Access states
- `candidate`: seen in a result/list; contents not read.
- `metadata_only`: identity/metadata checked; lesson text not opened.
- `login_required`: blocked by an observed sign-in requirement.
- `permission_denied`: an authenticated read was refused.
- `read_partial`: actual relevant content read with explicit missing sections/pages.
- `read_verified`: relevant cited content opened and checked; this does not mean the whole book was read.
- `unavailable`: missing, unreadable or unsupported after the attempted route.

Only read_partial/read_verified sources may support curriculum-content claims, and only for passages actually read. State exactly what was retrieved; never fabricate tool calls, page numbers, checks, dates or provider IDs. A login page verifies a restriction, not lesson content. Use unknown/null for unavailable revision or modification information; do not infer an edition from a filename alone.

## Minimal source records
For each used source retain a local source ID, title/issuer, provider, stable observed URL or supplied-file reference, file/item ID when exposed, edition/version/revision, course/grade, unit/lesson, exact page/section/slide/sheet/location, access date, access state, what was read and what was missing, supported claim/use, reuse restrictions and teacher/student visibility. Record only necessary private path metadata. Do not retain account identifiers unless needed to distinguish user-selected connections; never retain authentication secrets, temporary signed downloads, student records or assessment responses.

Link claim-specific citations to the actual referenced file/page. For restricted sources use “requires your account”; test in the current authorized session when possible and report if only a filename/locator can be verified. Do not synthesize a URL from an opaque ID. For local uploads give a host-supported file citation or filename + page/section; do not publish the upload to create a public link. Keep quotations limited and respect applicable reuse limits even when the source is licensed to the teacher.

## Reference pack for specialists
Include purpose and scope, chosen curriculum/edition, authoritative selection reason (teacher-selected/adopted status as supplied), a short content synopsis, relevant instructional sequence/prerequisites, target/task/assessment demand, existing support resources, materials/time constraints, citations, gaps and proposed adaptations. Link each finding to source IDs and precise locators. Pass excerpts only where necessary; never make the pack a substitute copy of a licensed book or secure item bank.

Send this pack to `tw-orchestrator` and the relevant lead: alignment, lesson/unit, substitute, assessment, cross-curricular assessment, differentiation, multilingual, subject instruction, intervention or enrichment. Preserve each subject's source-to-target mapping for cross-curricular work. Keep answer keys and secure teacher resources out of student-facing handoffs. Assessment analytics require separate deidentified response data; curriculum access alone does not authorize roster or grade access.

Downstream skills must distinguish: source content; teacher's adoption/context claims; verified California standards/frameworks; research evidence; and original proposed additions. Publisher metadata is a starting point for alignment, not proof. Do not override an adopted edition solely because a public website is newer; flag material conflicts and resolve the teacher's intended source. Do not silently merge different editions, student/teacher versions or languages.

## Reuse and refresh
Within the task, reuse verified records instead of repeating intake/login. For a later task, check available access and version/modified metadata, reopen cited content when changed or uncertain, and note the date. A changed version or revoked access invalidates an earlier assumption; it does not erase the prior record. Save a minimal pointer registry only through authorized host persistence and only when requested or permitted by the artifact workflow. Do not store private school pointers in these distributable skill files. No background crawl or automatic durable memory is implied.
