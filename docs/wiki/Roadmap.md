# Roadmap

ContextOS is built in three phases. Each phase is designed to compound on the previous one.

---

## Phase 1 — Absorb
*Unify all six source repos into one coherent package.*

- [x] Unified MCP tool schema (47 tools across 5 layers)
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
- [ ] Full composio integration (pass-through to 1000+ tools)
- [ ] ragflow integration (use existing ragflow instance)
- [ ] context7 live doc integration
- [ ] PyPI package publish (`pip install contextos`)
- [ ] Full test suite

---

## Phase 2 — Compound
*Build the feedback loops that make ContextOS self-improving.*

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

## Phase 3 — Platform
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

### v0.1.0 (current)
- Initial architecture and all five layers
- 47 MCP tools defined with full schema
- Pre-Response Sparring Hook
- Orchestration Core
- Full wiki and documentation
- MIT license

---

*Want to influence the roadmap? Open a Discussion on GitHub.*
