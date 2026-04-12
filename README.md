# ContextOS

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [中文](README.zh.md) | [Nederlands](README.nl.md) | [Русский](README.ru.md) | [한국어](README.ko.md)

> **The unified context intelligence layer for AI agents.**  
> One pip install. Every capability. Nothing missing.

[![PyPI version](https://badge.fury.io/py/contextos.svg)](https://badge.fury.io/py/contextos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![GitHub Stars](https://img.shields.io/github/stars/itallstartedwithaidea/contextOS?style=social)](https://github.com/itallstartedwithaidea/contextOS)

```
pip install contextos
```

---

## What Is ContextOS?

ContextOS is the **operating system layer for AI context** -- a single, unified MCP server and CLI that absorbs, extends, and surpasses the capabilities of seven leading open-source repositories in the AI agent and context management ecosystem.

It was built because no single project covered the full stack. Every existing tool was excellent at one thing and missing everything else. ContextOS brings them all together, fills every gap, and adds an orchestration layer that didn't exist anywhere.

**ContextOS is not a wrapper. It is a platform.** Every tool you were using before becomes a module that runs on top of it.

---

## v0.2.0 -- The Cognition Update

**The industry builds: retrieve then generate.**  
**ContextOS builds: retrieve, THINK, then generate.**

Every agent framework in the market skips the most important step. They retrieve context, stuff it into a prompt, and generate output. The thinking that happens between retrieval and output -- the part where an expert would reason about contradictions, weigh constraints, sense missing information, and decide how deep to go -- that part doesn't exist anywhere.

Until now.

v0.2.0 adds three new layers and a framework that models how expert reasoning actually works:

### The Cognition Layer -- Six Cognitive Primitives

These are the reasoning operations that happen between retrieval and generation. No agent framework has built them.

| Primitive | What It Does | Why It Matters |
|---|---|---|
| **Active Forgetting** | Drops retrieved context that degrades output quality | More context isn't always better. 20 retrieved chunks where 3 matter creates noise that pulls reasoning off course. |
| **Reasoning Depth Calibration** | Estimates how much thinking a problem deserves before committing compute | A fast pattern match and a 10-step chain of reasoning are both valid -- for different problems. Agents should know which situation they're in. |
| **Synthesis Detection** | Determines whether the agent needs to THINK about what it has or GO GET more | The entire industry treats every task as a retrieval problem. Some tasks are synthesis, analogy, or relational reasoning. More data hurts them. |
| **Unknown Unknown Sensing** | Detects when the agent is missing an entire CATEGORY of information | Known unknowns are easy. Unknown unknowns kill. "I didn't know Salesforce data was relevant here" is a different failure mode than "I don't have today's data." |
| **Productive Contradiction** | Holds conflicting data as signal instead of resolving it | "Google Ads says conversions up, CRM says pipeline flat" -- the answer isn't "pick one." The measurement gap IS the insight. |
| **Context-Dependent Gravity** | Re-weights memory importance based on the current question | A memory about "never run branded without approval" scores low on similarity to a PMax query but fundamentally changes the recommendation. Static importance scores miss this. |

### The Retrieval Router -- Churn-Aware Routing

The real framework for retrieval isn't "structured vs. unstructured data." It's **data churn rate vs. indexing cost.**

Codebases change every time you switch branches -- embedding them creates stale indexes instantly. Legal documents change quarterly -- embedding them once pays off for months. The Retrieval Router classifies every data source by how fast its underlying data changes, then picks the retrieval strategy that matches.

| Churn Class | Example Data | Strategy | Why |
|---|---|---|---|
| **Live** | Search query reports, auction data, budget pacing | Direct API pull, no index | Any cached answer is already wrong |
| **Warm** | Keyword lists, audience segments, ad copy inventory | BM25 or vector index with freshness clock | Changes weekly, index is useful if fresh |
| **Cold** | Ad policies, account hierarchy, strategy docs | Full vector search, embed once | Changes quarterly at most, invest in deep indexing |

The router checks index freshness on every request. If a warm source's index is stale, it automatically falls back to live pull. No human intervention.

### The Index Lifecycle Manager -- Self-Healing Indexes

Event-driven re-indexing with circuit breakers and embedding model drift detection.

- **Write-triggered re-indexing:** When an MCP server pushes new data, the index rebuilds automatically. No cron jobs. The data flow IS the indexing trigger.
- **Embedding model drift detection:** Update your embedding model? Every vector index is silently invalid. The lifecycle manager catches model version mismatches and triggers full rebuilds.
- **Schema change quarantine:** If the shape of incoming data changes, existing indexes are quarantined until rebuilt. No silently wrong results.
- **Circuit breakers:** If re-indexing fails 3 times consecutively, the system stops trying and degrades to live pull. Alerts fire. Manual reset available.
- **Heartbeat checks:** Periodic health scans catch stale indexes that weren't triggered by events.

---

## How It Works: An Advertising Example

```python
from contextos import ContextOS
from contextos.router import DataSourceProfile

ctx = ContextOS(workspace="ad-agent", cognition_enabled=True)

# Register data sources with churn profiles
ctx.router().register_source(DataSourceProfile(
    name="search_queries",
    mcp_server="google-ads-mcp",
    churn_class="live",         # changes every hour
    index_strategy="none",       # always pull fresh
))

ctx.router().register_source(DataSourceProfile(
    name="keyword_lists",
    mcp_server="google-ads-mcp",
    churn_class="warm",          # changes weekly
    index_strategy="bm25",
    freshness_threshold_seconds=7200,
))

ctx.router().register_source(DataSourceProfile(
    name="ad_policies",
    mcp_server="policy-docs-mcp",
    churn_class="cold",          # changes quarterly
    index_strategy="vector",
    freshness_threshold_seconds=604800,
))

# The cognition layer runs automatically between retrieval and output.
# Given "should I pause branded campaigns given declining ROAS", it:
#
# 1. Active Forgetting: drops irrelevant chunks, keeps signal
# 2. Unknown Unknown Sensing: flags that budget data and analytics
#    were available but not queried
# 3. Gravity Reweighting: finds a constraint at importance 0.3
#    saying "never pause branded without approval" and boosts it
#    to 0.95 because it's a constraint that overrides the analysis
# 4. Synthesis Detection: identifies this as a reasoning problem,
#    not a retrieval problem -- the agent has contradictory data
#    (ROAS down, pipeline up) and needs to reason about what
#    the contradiction means
```

---

## Standing on the Shoulders of Giants

ContextOS would not exist without the extraordinary work of these projects. We formally credit and honor each one:

### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

**80.5k stars -- TypeScript**  
The foundational standard for tool execution and context protocol. ContextOS adopts MCP as its native schema and is 100% compatible with all existing MCP servers.  
**What it gave us:** The protocol. The standard. The ecosystem.  
**What was missing:** No orchestration layer, no memory, no retrieval, no planning -- just the transport protocol itself.

---

### [infiniflow/ragflow](https://github.com/infiniflow/ragflow)

**74.4k stars -- Python**  
A production-grade RAG engine with agent capabilities and deep document parsing.  
**What it gave us:** The retrieval engine, document ingestion pipeline, agent-aware RAG execution.  
**What was missing:** No cross-layer memory integration, no staleness detection, no multi-corpus routing, no feedback loop, no MCP-native tool schema.

---

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

**71.3k stars -- MDX**  
The definitive corpus of prompt engineering patterns, papers, and techniques.  
**What it gave us:** The planning and prompting knowledge base powering ContextOS's spec templates and agent instruction patterns.  
**What was missing:** Static documentation only -- no runtime integration, no prompt versioning, no outcome tracking.

---

### [upstash/context7](https://github.com/upstash/context7)

**48.2k stars -- TypeScript**  
Up-to-date code documentation for LLMs and AI code editors.  
**What it gave us:** Live documentation fetching, version-aware context injection for LLMs.  
**What was missing:** No memory layer, no retrieval integration, no session continuity -- purely stateless doc fetching.

---

### [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)

**33.5k stars -- TypeScript**  
A Claude Code plugin that captures and compresses coding sessions using AI and SQLite + embeddings.  
**What it gave us:** The in-session memory compression pattern, SQLite + embeddings architecture.  
**What was missing:** Memory dies with the session. No cross-session persistence, no entity graph, no tiering, no conflict resolution.

---

### [ComposioHQ/composio](https://github.com/ComposioHQ/composio)

**27.3k stars -- TypeScript**  
Powers 1000+ toolkits with auth, tool search, and a sandboxed workbench for building AI agents.  
**What it gave us:** The external API integration layer -- OAuth flows, tool sandboxing, execution context.  
**What was missing:** No tool DAG execution, no output caching, no retry/fallback policies, no tool versioning.

---

### [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)

**26.5k stars -- JavaScript**  
A lightweight meta-prompting and spec-driven development system for Claude Code.  
**What it gave us:** The spec-driven execution model, meta-prompting patterns, task decomposition templates.  
**What was missing:** No dynamic plan revision, no constraint propagation, no spec versioning, no outcome evaluation loop.

---

### [andrewyng/context-hub](https://github.com/andrewyng/context-hub)

**47 stars -- JavaScript**  
A curated, versioned doc store with a CLI (`chub`) for coding agents.  
**What it gave us:** The doc intelligence pattern: curated content + incremental fetch + local annotations + community feedback loops.  
**What was missing:** No memory layer, no retrieval integration, no MCP tool schema, no Python support.

> **ContextOS absorbs context-hub completely.** Every `chub` command maps to a `ctx docs` command.

---

## What Was Missing -- And What ContextOS Builds

After absorbing all seven projects, these were the gaps that no single repo addressed:

### Orchestration Core *(entirely new)*

| Feature | Why It Matters |
|---|---|
| **Semantic Intent Router** | Classifies every incoming request and dispatches to the correct layer automatically. |
| **Request Tracing / Observability** | Full lineage per tool call: which layer fired, latency, token cost, quality score. |
| **Schema Registry** | Versioned tool schemas with backward compatibility. |
| **Multi-Workspace Auth** | Per-workspace API keys, rate limits, and audit logs. |
| **Cost Ledger** | Track LLM + API spend per session, per workspace, per tool. |

### Cognition Layer *(entirely new in v0.2.0)*

| Feature | Why It Matters |
|---|---|
| **Active Forgetting** | Drop retrieved context that creates noise. More isn't better. |
| **Reasoning Depth Calibration** | Know how much thinking a problem deserves before investing compute. |
| **Synthesis Detection** | Distinguish retrieval tasks from reasoning tasks. |
| **Unknown Unknown Sensing** | Detect missing categories of information, not just missing facts. |
| **Productive Contradiction** | Hold conflicting signals as insight instead of resolving to one answer. |
| **Context-Dependent Gravity** | Re-weight memory by current question. Constraints override similarity scores. |
| **Context Budget** | Enforce token limits on retrieved context. Karpathy's "Context Window = RAM" made operational. |

### Retrieval Router *(entirely new in v0.2.0)*

| Feature | Why It Matters |
|---|---|
| **Data Source Registry** | Every MCP server self-declares its churn profile, index strategy, and freshness threshold. |
| **Churn-Aware Routing** | Live/warm/cold classification per source. Strategy matches data volatility. |
| **Automatic Fallback** | Stale index? Fall back to live pull. No manual intervention. |
| **Feedback-Driven Reclassification** | If a "cold" source keeps going stale, the system auto-promotes it to "warm." |

### Index Lifecycle Manager *(entirely new in v0.2.0)*

| Feature | Why It Matters |
|---|---|
| **Event-Driven Re-indexing** | MCP data events trigger rebuilds. No cron jobs. |
| **Embedding Model Drift Detection** | Model update = all vector indexes invalid. Auto-detected, auto-rebuilt. |
| **Schema Change Quarantine** | Data shape changes? Index quarantined until rebuilt. |
| **Circuit Breakers** | 3 consecutive index failures = degrade to live pull + alert. |
| **Heartbeat Health Checks** | Periodic scans catch anything events missed. |

### Memory Layer *(extends claude-mem)*

| Feature | Why It Matters |
|---|---|
| **Cross-Session Persistence** | Memory survives process restarts. |
| **Memory Tiering (Hot/Warm/Cold)** | Auto-promote/demote by recency + relevance. |
| **Entity Graph** | Extracts entities and links them as structured knowledge. |
| **Conflict Resolution** | Resolve contradicting memory sources using timestamp + confidence. |
| **User-Scoped vs Agent-Scoped Memory** | What the user told the system vs what agents learned -- kept separate. |

### Retrieval Layer *(extends ragflow + context7)*

| Feature | Why It Matters |
|---|---|
| **Hybrid Search** | BM25 keyword + dense vector search combined. |
| **Source Attribution Scoring** | Rank chunks by provenance quality, not just cosine similarity. |
| **Staleness Detection** | Flags content older than a configurable TTL and triggers re-fetch. |
| **Multi-Corpus Routing** | Route queries to docs, live web, codebase, or API spec -- in parallel. |
| **Retrieval Feedback Loop** | Tracks which chunks appeared in final output. Routes better over time. |

### Tool Execution Layer *(extends composio + MCP servers)*

| Feature | Why It Matters |
|---|---|
| **Tool Chaining / DAG Execution** | Multi-step tool pipelines with branching logic. |
| **Sandboxed Code Execution** | Safe execution with output capture and error recovery. |
| **Tool Output Caching** | Cache deterministic results by input hash. |
| **Retry + Fallback Policies** | Per-tool SLA: retry budget, fallback tool, graceful degradation. |
| **Tool Versioning** | Pin agent workflows to specific tool versions. |

### Planning & Spec Layer *(extends GSD + Prompt-Engineering-Guide)*

| Feature | Why It Matters |
|---|---|
| **Dynamic Plan Revision** | Plans update mid-execution based on tool output. |
| **Constraint Propagation** | If tool X fails, downstream steps are automatically revised. |
| **Spec Versioning + Diff** | Track how task specs evolve. Roll back if new spec underperforms. |
| **Pre-Response Sparring Hook** | Mandatory reflection before any agent output. Forces pause before firing. |
| **Outcome Evaluation** | Scores final output against original spec. Feeds signal back to planning. |

### Doc Intelligence Layer *(absorbs context-hub entirely)*

| Feature | Why It Matters |
|---|---|
| **Curated Doc Registry** | Community-maintained, versioned markdown docs for APIs, frameworks, and tools. |
| **Language-Specific Fetch** | Fetch docs in your target language. No irrelevant snippets. |
| **Incremental Fetch** | Fetch only what you need. No wasted tokens. |
| **Persistent Annotations** | Local notes that agents attach to docs. Survive session restarts. |
| **Community Feedback Loop** | Up/down votes per doc flow back to maintainers. |
| **Doc Staleness Scoring** | Stale docs are flagged and re-fetched automatically. |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
|                          CLIENT / AGENT                               |
|               (Claude Desktop - Cursor - Windsurf - SDK)             |
└───────────────────────────────┬──────────────────────────────────────┘
                                | MCP Protocol
┌───────────────────────────────▼──────────────────────────────────────┐
|                       ORCHESTRATION CORE                              |
|    Intent Router - Schema Registry - Cost Ledger - Request Tracing   |
└──┬──────────┬──────────┬──────────┬──────────┬──────────┬────────────┘
   |          |          |          |          |          |
┌──▼───┐ ┌───▼────┐ ┌───▼───┐ ┌───▼────┐ ┌───▼────┐ ┌───▼─────┐
|MEMORY| |RETRIEV.| | TOOLS | |PLANNING| |COGNIT. | | ROUTER  |
|      | |        | |       | |        | |        | |         |
|Hot   | |Hybrid  | |DAG    | |Spec    | |Active  | |Churn    |
|Warm  | |Search  | |Exec   | |Engine  | |Forget  | |Classes  |
|Cold  | |Multi-  | |Cache  | |Sparring| |Depth   | |Data Src |
|Entity| |Corpus  | |Retry  | |Hook    | |Calibr. | |Registry |
|Graph | |Stale-  | |Sand-  | |Dynamic | |Synth.  | |Freshness|
|Confl.| |ness    | |box    | |Revis.  | |Detect  | |Clock    |
|Resol.| |Feed-   | |Version| |Outcome | |Unknown | |Feedback |
|      | |back    | |Pin    | |Eval    | |Unknown | |Learn    |
|      | |        | |       | |        | |Contra- | |         |
|      | |        | |       | |        | |diction | |         |
|      | |        | |       | |        | |Gravity | |         |
└──────┘ └────────┘ └───────┘ └────────┘ └────────┘ └────┬────┘
                                                          |
                                                   ┌──────▼──────┐
                                                   |   INDEXER    |
                                                   |             |
                                                   |Event-Driven |
                                                   |Re-index     |
                                                   |Model Drift  |
                                                   |Detection    |
                                                   |Circuit      |
                                                   |Breakers     |
                                                   |Heartbeat    |
                                                   └─────────────┘
```

**The critical data flow (v0.2.0):**

```
Request → Orchestration → Router (pick strategy per source)
                            ↓
                        Retrieval (execute strategy)
                            ↓
                        Cognition (THINK before generating)
                          - forget noise
                          - calibrate depth
                          - sense unknown unknowns
                          - detect contradictions
                          - reweight constraints
                            ↓
                        Planning (Sparring Hook + plan)
                            ↓
                        Generation (finally, produce output)
                            ↓
                        Feedback (did the output use the context?)
                            ↓
                        Router learns → Indexer heals → Cognition calibrates
```

---

## Quick Start

```python
from contextos import ContextOS

ctx = ContextOS(
    workspace="my-agent",
    memory_tier="warm",
    retrieval_mode="hybrid",
    tools=["composio", "mcp"],
    sparring_hook=True,
    cognition_enabled=True,        # v0.2.0: thinking layer
    churn_aware_routing=True,      # v0.2.0: per-source routing
)

# Use as MCP server
ctx.serve(port=8080)
```

### Register Data Sources

```python
from contextos.router import DataSourceProfile

ctx.router().register_source(DataSourceProfile(
    name="google_ads",
    mcp_server="google-ads-mcp",
    churn_class="live",
    index_strategy="none",
))

ctx.router().register_source(DataSourceProfile(
    name="client_docs",
    mcp_server="google-drive-mcp",
    churn_class="cold",
    index_strategy="vector",
    freshness_threshold_seconds=604800,
))
```

### Run a Cognition Pass

```python
report = ctx.cognition().think(
    query="should we shift budget from search to pmax",
    retrieved_context=[...],
    memories=[...],
    available_sources=["google_ads", "analytics", "crm", "budget"],
    retrieved_from=["google_ads", "analytics"],
    domain="advertising",
)

print(report.unknown_unknowns)   # sources you forgot to check
print(report.gravity_shifts)     # constraints that override the analysis
print(report.contradictions)     # conflicting signals worth investigating
print(report.depth_estimate)     # how much thinking this deserves
```

---

## CLI: `ctx`

### Doc Commands *(context-hub parity + extensions)*

```bash
ctx docs search openai                     # find available docs
ctx docs get openai/chat --lang py         # fetch current docs, Python variant
ctx docs get stripe/api --file webhooks    # incremental fetch
ctx docs annotate stripe/api "Note here"   # attach a persistent note
ctx docs feedback stripe/api up            # upvote a doc
```

### Memory Commands

```bash
ctx memory store "key insight about X"
ctx memory retrieve "what do I know about stripe webhooks"
ctx memory forget "session notes from project Y"
ctx memory graph query "entity:OpenAI"
ctx memory conflicts --resolve auto
```

### Retrieval Commands

```bash
ctx retrieve docs "stripe payment intents python"
ctx retrieve live "openai assistants api latest"
ctx retrieve web "LLM context window best practices 2026"
ctx retrieve code "webhook verification pattern"
```

### Router Commands *(new in v0.2.0)*

```bash
ctx router register --name google_ads --churn live --index none
ctx router register --name policies --churn cold --index vector
ctx router health                          # index health across all sources
ctx router route "what queries triggered ads today"  # show routing decision
```

### Cognition Commands *(new in v0.2.0)*

```bash
ctx cognition think --query "should I pause branded" --domain advertising
ctx cognition budget --tokens 4000         # set context budget
ctx cognition contradictions --last        # show last detected contradictions
ctx cognition unknowns --last              # show unknown-unknown alerts
```

### Planning Commands

```bash
ctx plan create "build a stripe checkout integration"
ctx plan spar                              # pre-response sparring hook
ctx plan revise --feedback "tool X failed"
ctx plan evaluate --against-spec spec.md
```

### Orchestration Commands

```bash
ctx health                                 # all 8 layers
ctx cost summary --workspace my-agent
ctx trace --id req_abc123
```

---

## MCP Tools Exposed

ContextOS exposes **67 tools** across 8 categories via the MCP protocol.

### Memory Tools (9)
`memory_store` `memory_retrieve` `memory_forget` `memory_summarize` `memory_diff` `memory_graph_query` `memory_export` `memory_import` `memory_conflicts`

### Retrieval Tools (8)
`retrieve_docs` `retrieve_live` `retrieve_web` `retrieve_code` `retrieve_merge` `retrieve_score` `retrieve_feedback` `retrieve_staleness`

### Cognition Tools (6) *(new in v0.2.0)*
`cognition_think` `cognition_forget` `cognition_depth` `cognition_contradictions` `cognition_unknowns` `cognition_gravity`

### Router Tools (5) *(new in v0.2.0)*
`router_register` `router_route` `router_health` `router_feedback` `router_reclassify`

### Indexer Tools (5) *(new in v0.2.0)*
`indexer_status` `indexer_rebuild` `indexer_heartbeat` `indexer_circuit_reset` `indexer_model_update`

### Tool Execution (12)
`tool_run` `tool_chain` `tool_cache_get` `tool_cache_set` `tool_register` `tool_list` `tool_schema` `tool_version_pin` `tool_retry_policy` `tool_cost` `tool_sandbox_run` `tool_composio`

### Planning Tools (9)
`plan_create` `plan_revise` `plan_diff` `plan_evaluate` `plan_spar` `plan_decompose` `plan_constraints` `plan_rollback` `plan_template`

### Orchestration Tools (9)
`ctx_route` `ctx_trace` `ctx_schema_get` `ctx_schema_register` `ctx_cost_summary` `ctx_workspace_create` `ctx_workspace_list` `ctx_health` `ctx_version`

### Doc Intelligence Tools (8)
`docs_search` `docs_get` `docs_get_file` `docs_annotate` `docs_annotate_clear` `docs_annotate_list` `docs_feedback` `docs_contribute`

---

## Agent Self-Improvement Loop

```
Without ContextOS                          With ContextOS v0.2.0
-----------------                          ---------------------
Search the web                             Churn-aware retrieval per source
Noisy results                              Active forgetting drops noise
17 chunks, 3 useful                        Context budget enforces quality
Code breaks                                Agent annotates gaps locally
No idea what's missing                     Unknown-unknown sensing flags gaps
Contradictions ignored                     Productive contradiction finds insight
Static memory importance                   Gravity reweighting by current question
Knowledge forgotten next session           Hot/warm/cold memory with entity graph
No plan when tools fail                    Constraint propagation + dynamic revision
Output not evaluated                       Sparring hook + outcome scoring
Stale indexes silently wrong               Self-healing indexes with circuit breakers
Effort wasted repeating mistakes           Compounds with every run
```

---

## Roadmap

### Phase 1 -- Absorb *(complete)*
- [x] Unified MCP tool schema
- [x] Memory layer with cross-session persistence
- [x] Hybrid retrieval engine
- [x] Tool registry with DAG execution
- [x] Planning + spec engine with sparring hook
- [x] Orchestration Core
- [x] Doc intelligence layer (context-hub absorbed)

### Phase 1.5 -- Cognition Update *(v0.2.0 -- current)*
- [x] **Cognition Layer** with 6 cognitive primitives
- [x] **Retrieval Router** with churn-aware routing
- [x] **Index Lifecycle Manager** with self-healing
- [x] Data Source Registry with per-source profiles
- [x] Context Budget enforcement
- [x] Circuit breakers for index operations
- [x] Embedding model drift detection
- [x] Feedback-driven churn reclassification
- [ ] Production integrations (sentence-transformers, rank-bm25, tantivy)
- [ ] Full test suite for cognition primitives
- [ ] Benchmark: cognition layer impact on output quality

### Phase 2 -- Compound
- [ ] Retrieval feedback loop (auto-improves routing)
- [ ] Entity graph with relationship queries
- [ ] Memory conflict resolution engine
- [ ] Tool output caching layer
- [ ] Outcome evaluation + spec scoring
- [ ] PostgreSQL + pgvector backend for scale
- [ ] Docker image + docker-compose

### Phase 3 -- Platform
- [ ] ContextOS Cloud (hosted, multi-tenant)
- [ ] Visual workflow builder
- [ ] Marketplace for tool schemas
- [ ] Enterprise SSO + audit logs
- [ ] LangChain + CrewAI + AutoGen adapters

---

## The Origin of the Cognition Layer

The six cognitive primitives in v0.2.0 were identified by tracing how reasoning actually works in a live problem-solving conversation, then naming each operation as it was practiced.

The starting point was a LinkedIn post by Cole Medin asking "Is RAG Dead?" with a diagram separating structured data (where RAG was abandoned by coding agents) from unstructured data (where RAG thrives). A commenter pointed out two things: RAG was being conflated with semantic search (you can do RAG with BM25), and the real reason coding agents use grep is that re-indexing on every branch checkout kills developer experience.

That insight -- data churn rate vs. indexing cost -- became the Retrieval Router. But the deeper question emerged: what happens between retrieval and output that nobody's building for? The answer was a set of cognitive primitives that were being practiced implicitly in the conversation itself:

- Active forgetting was happening every turn (dropping irrelevant details from the post)
- Depth calibration was happening naturally (knowing when to go deep vs. give a quick take)
- Synthesis detection was present (some questions needed reasoning, not retrieval)
- Unknown-unknown sensing surfaced (the commenter found a blind spot Cole didn't know existed)
- Productive contradiction was the core insight (Cole simultaneously argued RAG is dead AND that agentic search is the future -- which is RAG)
- Context-dependent gravity appeared when analyzing the ContextOS codebase (a 0.3 importance memory about "never pause branded" became 0.95 when the current question was about pausing branded campaigns)

The conversation became the spec. Each primitive was practiced before it was named. This section exists as a record of that origin.

---

## Contributing

PRs welcome for both **code** and **docs**. See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

Built under [IASAWI](https://github.com/itallstartedwithaidea) -- It All Started With A Idea.

---

## License

MIT -- see [LICENSE](LICENSE)

---

## Citation

If you use ContextOS in research or production, please cite:

```
@software{contextos2026,
  title = {ContextOS: The Unified Context Intelligence Layer},
  author = {Williams, John and IASAWI Contributors},
  year = {2026},
  url = {https://github.com/itallstartedwithaidea/contextOS}
}
```

---

*Built with respect for every repo that came before it.*
