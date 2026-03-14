# Changelog

## v0.2.0 -- The Cognition Update (2026-03-14)

**The industry builds: retrieve then generate. ContextOS builds: retrieve, THINK, then generate.**

### New Layers

**Cognition Layer** (`contextOS/cognition.py`)
Six cognitive primitives that model how expert reasoning works between retrieval and output:
- Active Forgetting -- drops retrieved context that degrades output quality
- Reasoning Depth Calibration -- estimates how much thinking a problem deserves
- Synthesis Detection -- determines whether to think or retrieve
- Unknown Unknown Sensing -- detects missing categories of information
- Productive Contradiction -- holds conflicting data as signal, not noise
- Context-Dependent Gravity -- re-weights memory by current question

**Retrieval Router** (`contextOS/router.py`)
Churn-aware routing that selects retrieval strategy per data source:
- Data Source Registry with per-source churn profiles
- Live/warm/cold classification with automatic fallback
- Feedback-driven churn reclassification
- Index freshness checking on every request

**Index Lifecycle Manager** (`contextOS/indexer.py`)
Self-healing index infrastructure:
- Event-driven re-indexing (MCP data events trigger rebuilds)
- Embedding model drift detection and auto-rebuild
- Schema change quarantine
- Circuit breakers (3 failures -> degrade to live pull)
- Heartbeat health checks

### Updated

- `contextOS/core.py` -- expanded from 5 to 8 layers, version bumped to 0.2.0
- `contextOS/__init__.py` -- exports CognitionLayer, RetrievalRouter, IndexLifecycleManager
- `pyproject.toml` -- version 0.2.0, new keywords, optional sentence-transformers/tantivy deps
- `README.md` -- complete rewrite with cognition update documentation, examples, updated architecture
- `docs/wiki/` -- new pages for Cognition Layer, Retrieval Router, Index Lifecycle Manager; updated Architecture, Home, Roadmap

### Architecture

```
v0.1.0: 5 layers, 55 tools
v0.2.0: 8 layers, 67 tools

New tools: cognition_think, cognition_forget, cognition_depth,
cognition_contradictions, cognition_unknowns, cognition_gravity,
router_register, router_route, router_health, router_feedback,
router_reclassify, indexer_status, indexer_rebuild, indexer_heartbeat,
indexer_circuit_reset, indexer_model_update
```

### Origin

The six cognitive primitives were identified by tracing how reasoning actually works in a live conversation analyzing the "Is RAG Dead?" debate. The conversation itself became the spec -- each primitive was practiced before it was named.

---

## v0.1.0 (2025)

Initial release. Five layers: Orchestration, Memory, Retrieval, Tools, Planning. 55 MCP tools. Pre-Response Sparring Hook. MIT license.
