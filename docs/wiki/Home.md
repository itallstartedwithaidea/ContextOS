# ContextOS Wiki

Welcome to the ContextOS documentation. This wiki covers everything from quick-start installation to deep architecture internals.

---

## Navigation

| Section | What's Inside |
|---|---|
| [Architecture](./Architecture.md) | How the 8 layers fit together, data flow diagrams |
| **v0.2.0 -- The Cognition Update** | |
| [Cognition Layer](./Cognition-Layer.md) | Six cognitive primitives: forgetting, depth calibration, synthesis detection, unknown unknowns, productive contradiction, gravity |
| [Retrieval Router](./Retrieval-Router.md) | Churn-aware routing, data source registry, feedback-driven reclassification |
| [Index Lifecycle Manager](./Index-Lifecycle-Manager.md) | Self-healing indexes, event-driven re-indexing, circuit breakers, model drift detection |
| **Core Layers** | |
| [Memory Layer](./Memory-Layer.md) | Tiering, entity graph, conflict resolution, persistence |
| [Retrieval Layer](./Retrieval-Layer.md) | Hybrid search, multi-corpus routing, staleness detection |
| [Tool Execution Layer](./Tool-Execution-Layer.md) | DAG pipelines, caching, retry policies, sandboxing |
| [Planning & Spec Layer](./Planning-Spec-Layer.md) | Spec engine, sparring hook, dynamic revision, outcome eval |
| [Orchestration Core](./Orchestration-Core.md) | Intent router, schema registry, cost ledger, tracing |
| **Reference** | |
| [MCP Tools Reference](./MCP-Tools-Reference.md) | All 67 tools, schemas, parameters, examples |
| [Pre-Response Sparring Hook](./Pre-Response-Sparring-Hook.md) | Deep dive on the sparring hook design and usage |
| [Credits & Origins](./Credits-and-Origins.md) | Full credit to all source repos and what each contributed |
| [Configuration](./Configuration.md) | All config options, environment variables, workspace setup |
| [Integrations](./Integrations.md) | Claude Desktop, Cursor, Windsurf, LangChain, OpenAI SDK |
| [Roadmap](./Roadmap.md) | Phase-by-phase build plan with status |
| [Contributing](./Contributing.md) | How to contribute, PR guidelines, code standards |
| [FAQ](./FAQ.md) | Common questions and sharp answers |

---

## In One Paragraph

ContextOS is a unified MCP server that absorbs the capabilities of seven leading open-source AI context projects and builds what none of them had: an orchestration layer, a cognition layer with six cognitive primitives, a churn-aware retrieval router, and a self-healing index lifecycle manager. The result is 67 MCP tools across 8 layers. The industry builds retrieve-then-generate. ContextOS builds retrieve, THINK, then generate. One pip install. `pip install contextos`.

---

## Quick Links

- [GitHub](https://github.com/itallstartedwithaidea/contextOS)
- [PyPI](https://pypi.org/project/contextos)
- [Issue Tracker](https://github.com/itallstartedwithaidea/contextOS/issues)
- [Discussions](https://github.com/itallstartedwithaidea/contextOS/discussions)
