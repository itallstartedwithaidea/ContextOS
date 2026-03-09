# ContextOS Wiki

Welcome to the ContextOS documentation. This wiki covers everything from quick-start installation to deep architecture internals.

---

## Navigation

| Section | What's Inside |
|---|---|
| [Architecture](./Architecture.md) | How the 5 layers fit together, data flow diagrams |
| [Memory Layer](./Memory-Layer.md) | Tiering, entity graph, conflict resolution, persistence |
| [Retrieval Layer](./Retrieval-Layer.md) | Hybrid search, multi-corpus routing, staleness detection |
| [Tool Execution Layer](./Tool-Execution-Layer.md) | DAG pipelines, caching, retry policies, sandboxing |
| [Planning & Spec Layer](./Planning-Spec-Layer.md) | Spec engine, sparring hook, dynamic revision, outcome eval |
| [Orchestration Core](./Orchestration-Core.md) | Intent router, schema registry, cost ledger, tracing |
| [MCP Tools Reference](./MCP-Tools-Reference.md) | All 47 tools, schemas, parameters, examples |
| [Credits & Origins](./Credits-and-Origins.md) | Full credit to all 6 source repos and what each contributed |
| [Configuration](./Configuration.md) | All config options, environment variables, workspace setup |
| [Integrations](./Integrations.md) | Claude Desktop, Cursor, Windsurf, LangChain, OpenAI SDK |
| [Roadmap](./Roadmap.md) | Phase-by-phase build plan with status |
| [Contributing](./Contributing.md) | How to contribute, PR guidelines, code standards |
| [FAQ](./FAQ.md) | Common questions and sharp answers |

---

## In One Paragraph

ContextOS is a unified MCP server that absorbs the capabilities of six leading open-source AI context projects — modelcontextprotocol/servers, ragflow, Prompt-Engineering-Guide, context7, claude-mem, composio, and get-shit-done — and builds the orchestration layer that none of them had. The result is 47 MCP tools across 5 layers: Memory, Retrieval, Tool Execution, Planning, and Orchestration. One pip install. pip install contextos.

---

## Quick Links

- [GitHub](https://github.com/itallstartedwithaidea/contextOS)
- [PyPI](https://pypi.org/project/contextos)
- [Issue Tracker](https://github.com/itallstartedwithaidea/contextOS/issues)
- [Discussions](https://github.com/itallstartedwithaidea/contextOS/discussions)
