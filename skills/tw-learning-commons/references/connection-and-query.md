# Connection and query guide
Documentation checked 2026-09-29. Recheck capabilities before use. No credentials are distributed.

Prefer the native [Learning Commons ChatGPT plugin or Claude connector](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/agent-plugins). Search the host catalog; availability is account-dependent. If it is not offered, say so without inventing an install link. Follow the host's connection UI. The package does not install or authenticate a third-party service.

For a compatible MCP client, the documented [server](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/mcp-server) is `https://kg.mcp.learningcommons.org/mcp`. Configure its key in the client's secret store/header settings (`x-api-key` or the documented bearer route). Never put a real key into a shared manifest. Discover current schemas; returned standard UUIDs feed component/progression tools. Native MCP coverage is narrower than all Knowledge Graph datasets.

For a Python runtime, an authorized administrator may configure only `Teacher_Workbench_LEARNING_COMMONS_API_KEY` in the runtime's secret environment. Do not ask a teacher to paste it into chat. The bundled client makes bounded GET requests to the fixed official [REST base](https://docs.learningcommons.org/api-reference/overview). It refuses redirects and does not print headers, keys or server error bodies. No OpenAI API key is needed by this client.

Examples (replace identifiers with returned values; run from this skill directory):
```
python3 scripts/knowledge_graph.py api --resource standards-frameworks --params '{"jurisdiction":"California","academicSubject":"Mathematics","limit":20}' --out frameworks.json
python3 scripts/knowledge_graph.py api --resource academic-standards --params '{"standardsFrameworkCaseIdentifierUUID":"RETURNED_FRAMEWORK_UUID","limit":100}' --out standards.json
python3 scripts/knowledge_graph.py api --resource academic-standards/RETURNED_STANDARD_UUID/learning-components --out components.json
python3 scripts/knowledge_graph.py api --resource academic-standards/RETURNED_STANDARD_UUID/prerequisites --out prerequisites.json
python3 scripts/knowledge_graph.py local --file supplied-nodes.jsonl --match '{"statementCode":"3.OA.1","jurisdiction":"California"}' --out matches.json
```
The example UUID placeholders are deliberately not executable IDs. Use a returned UUID. The local matcher tests supplied top-level or node `properties` fields by exact value; array fields match a contained value. It preserves full raw records and line numbers. Query relationships only using their actual supplied schema; never infer a missing edge from a node lookup. This is a bounded scan, not an imported graph database.

Supported REST resources: standards-frameworks, academic-standards, courses, plus academic-standards/{UUID}/learning-components and /prerequisites. Other resources must use a discovered supported tool or a deliberately reviewed client extension. Inspect [framework filters and cursor pagination](https://docs.learningcommons.org/api-reference/academic-standards/standards-frameworks), [components](https://docs.learningcommons.org/api-reference/learning-components/learning-components-for-a-standard), [prerequisites](https://docs.learningcommons.org/api-reference/academic-standards/prerequisites-for-a-standard), and [courses](https://docs.learningcommons.org/api-reference/curriculum/courses-in-a-curriculum) for current parameters. The client reports partial results when its page bound is reached. A 401/403 needs authorized connection/access resolution; do not retry by bypassing controls.

For permitted [local exports](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/local-files), ask for a scoped file or use an already authorized download. Do not download an entire graph by default. Retain dataset release, source URLs, node/edge IDs, license and attribution fields. Treat an export's date as its date, not today's content. Consult the [API dataset overview](https://docs.learningcommons.org/api-reference/overview) for coverage and check publisher access conditions at the returned source. Open curriculum metadata does not grant rights to gated lesson content. Verify California standards in [CDE](https://www2.cde.ca.gov/cacs/); WIDA ELD and California ELD are distinct references.

Tests use synthetic records and mocked HTTP transport. They verify client behavior, not account access, live endpoint compatibility or correctness of an external dataset. A successful authorized live read is needed before reporting connected status.
