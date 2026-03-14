# Roadmap

ContextOS is built in phases. Each phase compounds on the previous one.

---

## Phase 1 -- Absorb *(complete)*
*Unify all seven source repos into one coherent package.*

- [x] Unified MCP tool schema (55 tools across 6 layers)
- [x] Memory layer architecture with hot/warm/cold tiering
- [x] Cross-session memory persistence (extending claude-mem)
- [x] Hybrid retrieval engine (extending ragflow)
- [x] Multi-corpus routing (internal + web + code + API)
- [x] Tool DAG execution (extending composio)
- [x] Spec-driven planning engine (extending GSD)
- [x] **Pre-Response Sparring Hook** (entirely new)
- [x] Orchestration Core with intent router (entirely new)
- [x] Cost Ledger (entirely new)
- [x] Request tracing (entirely new)
- [x] Doc intelligence layer (context-hub absorbed)

---

## Phase 1.5 -- The Cognition Update *(v0.2.0 -- current)*
*Add the thinking layer between retrieval and output.*

- [x] **Cognition Layer** with 6 cognitive primitives
  - [x] Active Forgetting (drop noise, enforce context budget)
  - [x] Reasoning Depth Calibration (estimate compute investment)
  - [x] Synthesis Detection (think vs. retrieve decision)
  - [x] Unknown Unknown Sensing (detect missing categories)
  - [x] Productive Contradiction (hold tension as signal)
  - [x] Context-Dependent Gravity (re-weight by current question)
- [x] **Retrieval Router** with churn-aware routing
  - [x] Data Source Registry (per-source profiles)
  - [x] Live / warm / cold classification
  - [x] Automatic fallback on stale indexes
  - [x] Feedback-driven churn reclassification
- [x] **Index Lifecycle Manager**
  - [x] Event-driven re-indexing
  - [x] Embedding model drift detection
  - [x] Schema change quarantine
  - [x] Circuit breakers (3 failures → degrade + alert)
  - [x] Heartbeat health checks
- [x] Context Budget enforcement
- [x] CognitionReport → Sparring Hook integration
- [x] Updated tool count: 67 tools across 8 layers
- [ ] Production integrations (sentence-transformers, rank-bm25, tantivy)
- [ ] Full test suite for cognition primitives
- [ ] Benchmark: cognition layer impact on output quality
- [ ] Full composio integration (pass-through to 1000+ tools)
- [ ] ragflow integration (use existing ragflow instance)
- [ ] context7 live doc integration
- [ ] PyPI package publish (`pip install contextos`)

---

## Phase 2 -- Compound
*Build the feedback loops that make ContextOS self-improving.*

- [ ] Cognition self-learning loop (depth calibration from outcomes)
- [ ] Retrieval feedback loop (track which chunks were used, improve routing)
- [ ] Entity graph with relationship queries (NER + knowledge graph)
- [ ] Memory conflict resolution engine (timestamp + confidence scoring)
- [ ] Tool output caching layer (Redis-backed for distributed deployments)
- [ ] Outcome evaluation + spec scoring (measure plan success rate)
- [ ] Constraint propagation in planning (when step fails, update dependents)
- [ ] Spec versioning + diff UI
- [ ] TypeScript adapter for MCP clients
- [ ] Docker image + docker-compose for production deployment
- [ ] PostgreSQL + pgvector backend for scale

---

## Phase 3 -- Platform
*Make ContextOS a platform others build on.*

- [ ] ContextOS Cloud (hosted, multi-tenant, no self-hosting required)
- [ ] Visual workflow builder for DAG pipelines
- [ ] Tool schema marketplace (publish + discover schemas)
- [ ] Enterprise SSO + workspace audit logs
- [ ] LangGraph integration
- [ ] CrewAI integration
- [ ] AutoGen integration
- [ ] Billing dashboard with per-workspace cost breakdowns
- [ ] ContextOS Pro: managed retrieval corpus hosting
- [ ] ContextOS Enterprise: on-premise deployment with SLA

---

## Version History

### v0.2.0 (current) -- The Cognition Update
- **Cognition Layer** with 6 cognitive primitives (active forgetting, depth calibration, synthesis detection, unknown-unknown sensing, productive contradiction, context-dependent gravity)
- **Retrieval Router** with churn-aware routing and data source registry
- **Index Lifecycle Manager** with self-healing indexes, circuit breakers, and model drift detection
- Architecture expanded from 5 to 8 layers
- Tool count expanded from 55 to 67
- The industry builds: retrieve → generate. ContextOS builds: retrieve → THINK → generate.

### v0.1.0
- Initial architecture and all five layers
- 55 MCP tools defined with full schema
- Pre-Response Sparring Hook
- Orchestration Core
- Doc Intelligence Layer (context-hub absorbed)
- Full wiki and documentation
- MIT license

---

*Want to influence the roadmap? Open a Discussion on GitHub.*
