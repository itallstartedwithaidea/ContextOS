# ContextOS

> **The unified context intelligence layer for AI agents.**  
> One pip install. Every capability. Nothing missing.

[![PyPI version](https://badge.fury.io/py/contextos.svg)](https://badge.fury.io/py/contextos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![GitHub Stars](https://img.shields.io/github/stars/itallstartedwithaidea/contextOS?style=social)](https://github.com/itallstartedwithaidea/contextOS)

```bash
pip install contextos
```

---

## What Is ContextOS?

ContextOS is the **operating system layer for AI context** — a single, unified MCP server that absorbs, extends, and surpasses the capabilities of six leading open-source repositories in the AI agent and context management ecosystem.

It was built because no single project covered the full stack. Every existing tool was excellent at one thing and missing everything else. ContextOS brings them all together, fills every gap, and adds an orchestration layer that didn't exist anywhere.

**ContextOS is not a wrapper. It is a platform.** Every tool you were using before becomes a module that runs on top of it.

---

## Standing on the Shoulders of Giants

ContextOS would not exist without the extraordinary work of these projects. We formally credit and honor each one:

### 🔵 [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
**⭐ 80.5k stars · TypeScript**  
The foundational standard for tool execution and context protocol. ContextOS adopts MCP as its native schema and is 100% compatible with all existing MCP servers.  
**What it gave us:** The protocol. The standard. The ecosystem.  
**What was missing:** No orchestration layer, no memory, no retrieval, no planning — just the transport protocol itself.

---

### 🟠 [infiniflow/ragflow](https://github.com/infiniflow/ragflow)
**⭐ 74.4k stars · Python**  
A production-grade RAG engine with agent capabilities and deep document parsing. The best open-source RAG implementation available.  
**What it gave us:** The retrieval engine, document ingestion pipeline, agent-aware RAG execution.  
**What was missing:** No cross-layer memory integration, no staleness detection, no multi-corpus routing, no feedback loop back into the retrieval ranker, no MCP-native tool schema.

---

### 🔴 [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)
**⭐ 71.3k stars · MDX**  
The definitive corpus of prompt engineering patterns, papers, and techniques. 71k stars for a reason.  
**What it gave us:** The planning and prompting knowledge base powering ContextOS's spec templates and agent instruction patterns.  
**What was missing:** Static documentation only — no runtime integration, no prompt versioning, no outcome tracking, no way to measure which patterns actually work in production.

---

### 🟢 [upstash/context7](https://github.com/upstash/context7)
**⭐ 48.2k stars · TypeScript**  
Up-to-date code documentation for LLMs and AI code editors. Solves the stale-docs problem elegantly.  
**What it gave us:** Live documentation fetching, version-aware context injection for LLMs.  
**What was missing:** No memory layer, no retrieval integration, no session continuity — purely stateless doc fetching with no learning across calls.

---

### 🟣 [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)
**⭐ 33.5k stars · TypeScript**  
A Claude Code plugin that captures and compresses coding sessions using AI and SQLite + embeddings.  
**What it gave us:** The in-session memory compression pattern, SQLite + embeddings architecture, and the proof that agents need memory badly enough to get 33k stars.  
**What was missing:** Memory dies with the session. No cross-session persistence, no entity graph, no memory tiering (hot/warm/cold), no user-scoped vs agent-scoped separation, no conflict resolution.

---

### 🔵 [ComposioHQ/composio](https://github.com/ComposioHQ/composio)
**⭐ 27.3k stars · TypeScript**  
Powers 1000+ toolkits with auth, tool search, and a sandboxed workbench for building AI agents.  
**What it gave us:** The external API integration layer — OAuth flows, tool sandboxing, execution context.  
**What was missing:** No tool DAG execution (pipelines, not one-shots), no output caching, no retry/fallback policies, no tool versioning, no cross-tool cost tracking.

---

### 🟡 [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)
**⭐ 26.5k stars · JavaScript**  
A lightweight meta-prompting and spec-driven development system for Claude Code via TÂCHES.  
**What it gave us:** The spec-driven execution model, meta-prompting patterns, task decomposition templates.  
**What was missing:** No dynamic plan revision, no constraint propagation when tools fail mid-plan, no spec versioning + diff, no outcome evaluation loop.

---

## What Was Missing — And What ContextOS Builds

After absorbing all six projects, these were the gaps that no single repo addressed. ContextOS builds every one of them:

### 🔴 Orchestration Core *(entirely new — no existing repo covers this)*
| Feature | Why It Matters |
|---|---|
| **Semantic Intent Router** | Classifies every incoming request and dispatches to the correct layer automatically. No hard-coded routing rules. |
| **Request Tracing / Observability** | Full lineage per tool call: which layer fired, latency, token cost, quality score. Know exactly what your agent spent and why. |
| **Schema Registry** | Versioned tool schemas with backward compatibility. Upgrades never silently break production agents. |
| **Multi-Workspace Auth** | Per-workspace API keys, rate limits, and audit logs. Production-safe from day one. |
| **Cost Ledger** | Track LLM + API spend per session, per workspace, per tool. Stop flying blind on cost. |

### 🟣 Memory Layer *(extends claude-mem)*
| Feature | Why It Matters |
|---|---|
| **Cross-Session Persistence** | Memory survives process restarts. Your agent doesn't forget everything when the server bounces. |
| **Memory Tiering (Hot/Warm/Cold)** | Hot = in-context, Warm = vector DB, Cold = archive. Auto-promote/demote by recency + relevance. |
| **Entity Graph** | Extracts entities from memory and links them as structured knowledge — not just text blobs. |
| **Conflict Resolution** | When two memory sources contradict, resolve using timestamp + confidence scoring. |
| **User-Scoped vs Agent-Scoped Memory** | What the user told the system vs what agents learned during execution — kept separate. |

### 🔵 Retrieval Layer *(extends ragflow + context7)*
| Feature | Why It Matters |
|---|---|
| **Hybrid Search** | BM25 keyword + dense vector search combined. Neither alone gives sufficient precision-recall. |
| **Source Attribution Scoring** | Rank retrieved chunks by provenance quality, not just cosine similarity. |
| **Staleness Detection** | Flags retrieved content older than a configurable TTL and triggers automatic re-fetch. |
| **Multi-Corpus Routing** | Route queries to your docs, live web, codebase, or API spec — in parallel, then merge. |
| **Retrieval Feedback Loop** | Tracks which retrieved chunks actually appeared in final output. Routes better over time. |

### 🟢 Tool Execution Layer *(extends composio + MCP servers)*
| Feature | Why It Matters |
|---|---|
| **Tool Chaining / DAG Execution** | Define multi-step tool pipelines with branching logic. Not every tool call is a one-shot. |
| **Sandboxed Code Execution** | Safe execution environment for generated code with output capture and error recovery. |
| **Tool Output Caching** | Cache deterministic results by input hash. Stop re-calling the same API for the same data. |
| **Retry + Fallback Policies** | Per-tool SLA: retry budget, fallback tool, graceful degradation path. |
| **Tool Versioning** | Pin agent workflows to specific tool versions. |

### 🟡 Planning & Spec Layer *(extends GSD + Prompt-Engineering-Guide)*
| Feature | Why It Matters |
|---|---|
| **Dynamic Plan Revision** | Plans update mid-execution based on tool output — not just static upfront decomposition. |
| **Constraint Propagation** | If tool X fails, downstream steps that depended on it are automatically revised. |
| **Spec Versioning + Diff** | Track how task specs evolve. Roll back to a prior version if new spec underperforms. |
| **Pre-Response Sparring Hook** | A mandatory reflection step before any agent output — distinguishes solve-it from learn-more moments. Forces the agent to pause before firing. |
| **Outcome Evaluation** | Scores final output against original spec. Feeds signal back to planning prompts. |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTEXTOS                                 │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ORCHESTRATION CORE                      │   │
│  │   Intent Router · Schema Registry · Cost Ledger     │   │
│  │   Request Tracing · Multi-Workspace Auth            │   │
│  └──────────┬──────────┬──────────┬──────────┬─────────┘   │
│             │          │          │          │              │
│    ┌────────▼──┐  ┌────▼─────┐  ┌▼────────┐ ┌▼──────────┐ │
│    │  MEMORY   │  │RETRIEVAL │  │  TOOLS  │ │ PLANNING  │ │
│    │           │  │          │  │         │ │           │ │
│    │Hot/Warm/  │  │Hybrid    │  │DAG Exec │ │Spec Engine│ │
│    │Cold Tiers │  │Search    │  │Caching  │ │Pre-Resp   │ │
│    │Entity     │  │Multi-    │  │Retry    │ │Sparring   │ │
│    │Graph      │  │Corpus    │  │Policies │ │Hook       │ │
│    │Conflict   │  │Staleness │  │Version  │ │Outcome    │ │
│    │Resolution │  │Detection │  │Pinning  │ │Eval       │ │
│    └───────────┘  └──────────┘  └─────────┘ └───────────┘ │
└─────────────────────────────────────────────────────────────┘
         ▲               ▲              ▲              ▲
    claude-mem        ragflow       composio          GSD
    (absorbed)     (absorbed)     (absorbed)     (absorbed)
                    context7        MCP            Prompt
                  (absorbed)      Servers          Guide
                               (absorbed)       (absorbed)
```

---

## Installation

```bash
pip install contextos
```

### Quick Start

```python
from contextos import ContextOS

ctx = ContextOS(
    workspace="my-agent",
    memory_tier="warm",        # hot | warm | cold
    retrieval_mode="hybrid",   # vector | bm25 | hybrid
    tools=["composio", "mcp"], # tool backends
    sparring_hook=True         # pre-response reflection
)

# Use as MCP server
ctx.serve(port=8080)
```

### Claude Desktop / Cursor / Windsurf

Add to your MCP config:

```json
{
  "mcpServers": {
    "contextos": {
      "command": "contextos",
      "args": ["serve"],
      "env": {
        "CONTEXTOS_WORKSPACE": "my-agent",
        "CONTEXTOS_API_KEY": "your-key"
      }
    }
  }
}
```

---

## MCP Tools Exposed

ContextOS exposes **47 tools** across 5 categories via the MCP protocol:

### Memory Tools (9)
- `memory_store` — Store with automatic tiering
- `memory_retrieve` — Semantic search across all tiers
- `memory_forget` — Targeted forgetting with cascade
- `memory_summarize` — Compress + promote to warm tier
- `memory_diff` — Compare two memory snapshots
- `memory_graph_query` — Query the entity relationship graph
- `memory_export` — Export full memory state
- `memory_import` — Import / restore memory state
- `memory_conflicts` — List and resolve conflicting memories

### Retrieval Tools (8)
- `retrieve_docs` — Hybrid search across your corpus
- `retrieve_live` — Fetch live docs via context7 integration
- `retrieve_web` — Web search with source scoring
- `retrieve_code` — Codebase search with AST awareness
- `retrieve_merge` — Merge results from multiple corpora
- `retrieve_score` — Re-rank results by provenance quality
- `retrieve_feedback` — Log which results were actually used
- `retrieve_staleness` — Check and refresh stale content

### Tool Execution (12)
- `tool_run` — Execute any registered tool
- `tool_chain` — Execute a DAG pipeline of tools
- `tool_cache_get` — Retrieve cached tool output
- `tool_cache_set` — Manually cache a tool result
- `tool_register` — Register a new tool at runtime
- `tool_list` — List all available tools + versions
- `tool_schema` — Get schema for a specific tool
- `tool_version_pin` — Pin a tool to a specific version
- `tool_retry_policy` — Configure retry/fallback for a tool
- `tool_cost` — Get cost estimate for a tool call
- `tool_sandbox_run` — Execute code in sandboxed environment
- `tool_composio` — Pass-through to Composio integration

### Planning Tools (9)
- `plan_create` — Generate a spec-driven execution plan
- `plan_revise` — Revise plan based on mid-execution feedback
- `plan_diff` — Diff two versions of a plan
- `plan_evaluate` — Score plan output against original spec
- `plan_spar` — Run pre-response sparring hook
- `plan_decompose` — Break goal into executable subtasks
- `plan_constraints` — Propagate constraint changes through plan
- `plan_rollback` — Restore previous plan version
- `plan_template` — Load a proven spec template

### Orchestration Tools (9)
- `ctx_route` — Classify and route a request
- `ctx_trace` — Get full trace for a request ID
- `ctx_schema_get` — Get registered tool schema
- `ctx_schema_register` — Register a new tool schema
- `ctx_cost_summary` — Get cost ledger summary
- `ctx_workspace_create` — Create a new workspace
- `ctx_workspace_list` — List all workspaces
- `ctx_health` — System health check
- `ctx_version` — Get ContextOS version info

---

## Roadmap

### Phase 1 — Absorb *(current)*
- [x] Unified MCP tool schema
- [x] Memory layer with cross-session persistence
- [x] Hybrid retrieval engine
- [x] Tool registry with DAG execution
- [x] Planning + spec engine with sparring hook
- [ ] Full composio integration
- [ ] PyPI package publish

### Phase 2 — Compound
- [ ] Retrieval feedback loop (auto-improves routing)
- [ ] Entity graph with relationship queries
- [ ] Memory conflict resolution engine
- [ ] Tool output caching layer
- [ ] Outcome evaluation + spec scoring

### Phase 3 — Platform
- [ ] ContextOS Cloud (hosted, multi-tenant)
- [ ] Visual workflow builder
- [ ] Marketplace for tool schemas
- [ ] Enterprise SSO + audit logs
- [ ] LangChain + OpenAI Agents SDK adapters

---

## Contributing

PRs welcome. Please read [CONTRIBUTING.md](./docs/CONTRIBUTING.md) first.

Built under [IASAWI](https://github.com/itallstartedwithaidea) — It All Started With A Idea.

---

## License

MIT — see [LICENSE](./LICENSE)

---

## Citation

If you use ContextOS in research or production, please cite:

```bibtex
@software{contextos2025,
  title = {ContextOS: The Unified Context Intelligence Layer},
  author = {Williams, John and IASAWI Contributors},
  year = {2025},
  url = {https://github.com/itallstartedwithaidea/contextOS}
}
```

---

*Built with respect for every repo that came before it.*
