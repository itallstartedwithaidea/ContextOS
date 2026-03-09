# ContextOS

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

ContextOS is the **operating system layer for AI context** — a single, unified MCP server and CLI that absorbs, extends, and surpasses the capabilities of seven leading open-source repositories in the AI agent and context management ecosystem.

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
A production-grade RAG engine with agent capabilities and deep document parsing.  
**What it gave us:** The retrieval engine, document ingestion pipeline, agent-aware RAG execution.  
**What was missing:** No cross-layer memory integration, no staleness detection, no multi-corpus routing, no feedback loop, no MCP-native tool schema.

---

### 🔴 [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

**⭐ 71.3k stars · MDX**  
The definitive corpus of prompt engineering patterns, papers, and techniques.  
**What it gave us:** The planning and prompting knowledge base powering ContextOS's spec templates and agent instruction patterns.  
**What was missing:** Static documentation only — no runtime integration, no prompt versioning, no outcome tracking.

---

### 🟢 [upstash/context7](https://github.com/upstash/context7)

**⭐ 48.2k stars · TypeScript**  
Up-to-date code documentation for LLMs and AI code editors.  
**What it gave us:** Live documentation fetching, version-aware context injection for LLMs.  
**What was missing:** No memory layer, no retrieval integration, no session continuity — purely stateless doc fetching.

---

### 🟣 [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)

**⭐ 33.5k stars · TypeScript**  
A Claude Code plugin that captures and compresses coding sessions using AI and SQLite + embeddings.  
**What it gave us:** The in-session memory compression pattern, SQLite + embeddings architecture.  
**What was missing:** Memory dies with the session. No cross-session persistence, no entity graph, no tiering, no conflict resolution.

---

### 🔵 [ComposioHQ/composio](https://github.com/ComposioHQ/composio)

**⭐ 27.3k stars · TypeScript**  
Powers 1000+ toolkits with auth, tool search, and a sandboxed workbench for building AI agents.  
**What it gave us:** The external API integration layer — OAuth flows, tool sandboxing, execution context.  
**What was missing:** No tool DAG execution, no output caching, no retry/fallback policies, no tool versioning.

---

### 🟡 [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)

**⭐ 26.5k stars · JavaScript**  
A lightweight meta-prompting and spec-driven development system for Claude Code.  
**What it gave us:** The spec-driven execution model, meta-prompting patterns, task decomposition templates.  
**What was missing:** No dynamic plan revision, no constraint propagation, no spec versioning, no outcome evaluation loop.

---

### 🟤 [andrewyng/context-hub](https://github.com/andrewyng/context-hub)

**⭐ 47 stars · JavaScript**  
A curated, versioned doc store with a CLI (`chub`) for coding agents — designed to stop agents from hallucinating APIs by giving them the right docs at the right time.  
**What it gave us:** The doc intelligence pattern: curated content + incremental fetch + local annotations + community feedback loops + SKILL.md agent integration.  
**What was missing:** No memory layer, no retrieval integration, no MCP tool schema, no cross-session persistence of annotations, no Python support, no connection to the broader agent context stack.

> **ContextOS absorbs context-hub completely.** Every `chub` command maps to a `ctx docs` command. Every feature context-hub ships — and everything it planned but never built — is in ContextOS.

---

## What Was Missing — And What ContextOS Builds

After absorbing all seven projects, these were the gaps that no single repo addressed:

### 🔴 Orchestration Core *(entirely new)*

| Feature | Why It Matters |
|---|---|
| **Semantic Intent Router** | Classifies every incoming request and dispatches to the correct layer automatically. |
| **Request Tracing / Observability** | Full lineage per tool call: which layer fired, latency, token cost, quality score. |
| **Schema Registry** | Versioned tool schemas with backward compatibility. |
| **Multi-Workspace Auth** | Per-workspace API keys, rate limits, and audit logs. |
| **Cost Ledger** | Track LLM + API spend per session, per workspace, per tool. |

### 🟣 Memory Layer *(extends claude-mem)*

| Feature | Why It Matters |
|---|---|
| **Cross-Session Persistence** | Memory survives process restarts. |
| **Memory Tiering (Hot/Warm/Cold)** | Auto-promote/demote by recency + relevance. |
| **Entity Graph** | Extracts entities and links them as structured knowledge. |
| **Conflict Resolution** | Resolve contradicting memory sources using timestamp + confidence. |
| **User-Scoped vs Agent-Scoped Memory** | What the user told the system vs what agents learned — kept separate. |

### 🔵 Retrieval Layer *(extends ragflow + context7)*

| Feature | Why It Matters |
|---|---|
| **Hybrid Search** | BM25 keyword + dense vector search combined. |
| **Source Attribution Scoring** | Rank chunks by provenance quality, not just cosine similarity. |
| **Staleness Detection** | Flags content older than a configurable TTL and triggers re-fetch. |
| **Multi-Corpus Routing** | Route queries to docs, live web, codebase, or API spec — in parallel. |
| **Retrieval Feedback Loop** | Tracks which chunks appeared in final output. Routes better over time. |

### 🟢 Tool Execution Layer *(extends composio + MCP servers)*

| Feature | Why It Matters |
|---|---|
| **Tool Chaining / DAG Execution** | Multi-step tool pipelines with branching logic. |
| **Sandboxed Code Execution** | Safe execution with output capture and error recovery. |
| **Tool Output Caching** | Cache deterministic results by input hash. |
| **Retry + Fallback Policies** | Per-tool SLA: retry budget, fallback tool, graceful degradation. |
| **Tool Versioning** | Pin agent workflows to specific tool versions. |

### 🟡 Planning & Spec Layer *(extends GSD + Prompt-Engineering-Guide)*

| Feature | Why It Matters |
|---|---|
| **Dynamic Plan Revision** | Plans update mid-execution based on tool output. |
| **Constraint Propagation** | If tool X fails, downstream steps are automatically revised. |
| **Spec Versioning + Diff** | Track how task specs evolve. Roll back if new spec underperforms. |
| **Pre-Response Sparring Hook** | Mandatory reflection before any agent output. Forces pause before firing. |
| **Outcome Evaluation** | Scores final output against original spec. Feeds signal back to planning. |

### 🟤 Doc Intelligence Layer *(absorbs context-hub entirely)*

| Feature | Why It Matters |
|---|---|
| **Curated Doc Registry** | Community-maintained, versioned markdown docs for APIs, frameworks, and tools — exactly what context-hub built, natively inside ContextOS. |
| **Language-Specific Fetch** | Fetch docs in your target language (`--lang py`, `--lang js`, `--lang ts`). No irrelevant snippets. |
| **Incremental Fetch** | Fetch only what you need — main entry point, specific `--file` references, or `--full` for everything. No wasted tokens. |
| **Persistent Annotations** | Local notes that agents attach to docs. Survive session restarts. Appear automatically on future fetches. Cross-session by default — unlike context-hub's session-scoped annotations. |
| **Community Feedback Loop** | Up/down votes per doc flow back to maintainers. Docs get better for everyone. |
| **SKILL.md Agent Integration** | Drop-in skill file for Claude Code, Cursor, Windsurf. Prompt your agent to use it once — it knows how forever. |
| **Doc Staleness Scoring** | Every fetched doc is scored against the live source. Stale docs are flagged and re-fetched automatically — not a manual `chub` command. |
| **Annotation Cross-Session Sync** | Annotations sync across machines via your ContextOS workspace. context-hub annotations are local-only. |
| **Doc Contribution Pipeline** | Submit new docs via `ctx docs contribute` — generates the correct markdown + YAML frontmatter and opens a draft PR. No manual formatting. |

---

## CLI: `ctx`

ContextOS ships a full CLI. Every `chub` command from context-hub works as a `ctx docs` subcommand — plus the full ContextOS capability surface.

### Doc Commands *(context-hub parity + extensions)*

```bash
# --- context-hub parity ---
ctx docs search openai                     # find available docs (replaces: chub search openai)
ctx docs get openai/chat --lang py         # fetch current docs, Python variant (replaces: chub get)
ctx docs get openai/chat --lang js         # JavaScript variant
ctx docs get stripe/api --file webhooks    # incremental fetch — specific reference file
ctx docs get openai/chat --full            # fetch everything including all reference files
ctx docs annotate stripe/api "Note here"  # attach a persistent note (replaces: chub annotate)
ctx docs annotate stripe/api --clear       # remove annotation
ctx docs annotate --list                   # list all annotations
ctx docs feedback stripe/api up            # upvote a doc (replaces: chub feedback)
ctx docs feedback stripe/api down          # downvote with optional label

# --- ContextOS extensions (not in context-hub) ---
ctx docs contribute openai/embeddings      # generate draft doc + open PR
ctx docs diff openai/chat v1.2 v1.3       # diff two doc versions
ctx docs staleness openai/chat             # check if doc is stale vs live source
ctx docs sync --annotations               # sync annotations across workspaces
ctx docs import chub                       # import all existing chub annotations + feedback
```

### Memory Commands

```bash
ctx memory store "key insight about X"
ctx memory retrieve "what do I know about stripe webhooks"
ctx memory forget "session notes from project Y"
ctx memory summarize --tier warm
ctx memory diff snapshot-a snapshot-b
ctx memory graph query "entity:OpenAI"
ctx memory export --format json
ctx memory import backup.json
ctx memory conflicts --resolve auto
```

### Retrieval Commands

```bash
ctx retrieve docs "stripe payment intents python"
ctx retrieve live "openai assistants api latest"
ctx retrieve web "LLM context window best practices 2025"
ctx retrieve code "webhook verification pattern"
ctx retrieve merge --sources docs,web,code
ctx retrieve score --rerank provenance
ctx retrieve feedback --session last
ctx retrieve staleness --corpus my-docs
```

### Planning Commands

```bash
ctx plan create "build a stripe checkout integration"
ctx plan spar                               # pre-response sparring hook
ctx plan revise --feedback "tool X failed"
ctx plan evaluate --against-spec spec.md
ctx plan decompose "goal: migrate to new API"
ctx plan diff v1 v2
ctx plan rollback v1
ctx plan template stripe-integration
```

### Orchestration Commands

```bash
ctx route "classify and dispatch this request"
ctx trace --id req_abc123
ctx schema get stripe/api
ctx schema register --file my-tool.json
ctx cost summary --workspace my-agent
ctx workspace create production
ctx workspace list
ctx health
ctx version
```

---

## Claude Code / Cursor / Windsurf Integration

Drop the ContextOS skill into your agent's skill directory and it knows how to use docs, memory, retrieval, and planning automatically.

**Claude Code:**
```bash
mkdir -p ~/.claude/skills/contextos
# Copy the ContextOS SKILL.md there
```

**MCP Config (Claude Desktop, Cursor, Windsurf):**
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

## Quick Start

```python
from contextos import ContextOS

ctx = ContextOS(
    workspace="my-agent",
    memory_tier="warm",        # hot | warm | cold
    retrieval_mode="hybrid",   # vector | bm25 | hybrid
    tools=["composio", "mcp"], # tool backends
    sparring_hook=True,        # pre-response reflection
    docs_registry="community"  # curated doc registry (context-hub content + ContextOS extensions)
)

# Use as MCP server
ctx.serve(port=8080)
```

---

## Agent Self-Improvement Loop

ContextOS is designed for a compounding loop where agents get smarter over time — across every layer simultaneously.

```
Without ContextOS                          With ContextOS
─────────────────                          ──────────────
Search the web                             Fetch curated docs (Doc Layer)
Noisy results                              Stale docs auto-refreshed
Code breaks                                Agent annotates gaps locally
Knowledge forgotten next session           Annotations persist cross-session
Hallucinated APIs                          Versioned, language-specific docs
No memory of past decisions                Hot/warm/cold memory with entity graph
No plan when tools fail                    Constraint propagation + dynamic revision
Output not evaluated                       Sparring hook + outcome scoring
Effort wasted repeating the same mistakes  ↗ Compounds with every run
↻ Repeat next session
```

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         CONTEXTOS                                │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  ORCHESTRATION CORE                       │   │
│  │   Intent Router · Schema Registry · Cost Ledger          │   │
│  │   Request Tracing · Multi-Workspace Auth                 │   │
│  └──────┬──────────┬──────────┬──────────┬──────────────────┘   │
│         │          │          │          │                       │
│  ┌──────▼──┐  ┌────▼─────┐  ┌▼────────┐ ┌▼──────────┐         │
│  │ MEMORY  │  │RETRIEVAL │  │  TOOLS  │ │ PLANNING  │         │
│  │         │  │          │  │         │ │           │         │
│  │Hot/Warm/│  │Hybrid    │  │DAG Exec │ │Spec Engine│         │
│  │Cold     │  │Search    │  │Caching  │ │Pre-Resp   │         │
│  │Entity   │  │Multi-    │  │Retry    │ │Sparring   │         │
│  │Graph    │  │Corpus    │  │Policies │ │Hook       │         │
│  │Conflict │  │Staleness │  │Version  │ │Outcome    │         │
│  │Resolve  │  │Detection │  │Pinning  │ │Eval       │         │
│  └─────────┘  └──────────┘  └─────────┘ └───────────┘         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  DOC INTELLIGENCE LAYER                   │   │
│  │   (absorbs context-hub entirely)                         │   │
│  │                                                          │   │
│  │  Curated Registry · Language-Specific Fetch             │   │
│  │  Incremental Fetch · Persistent Annotations             │   │
│  │  Community Feedback · SKILL.md Integration              │   │
│  │  Staleness Scoring · Cross-Session Annotation Sync      │   │
│  │  Doc Contribution Pipeline · chub import                │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
       ▲            ▲           ▲          ▲          ▲
  claude-mem    ragflow     composio      GSD     context-hub
  (absorbed)  (absorbed)  (absorbed)  (absorbed)  (absorbed)
               context7      MCP        Prompt
             (absorbed)    Servers      Guide
                          (absorbed)  (absorbed)
```

---

## MCP Tools Exposed

ContextOS exposes **55 tools** across 6 categories via the MCP protocol.

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

### Doc Intelligence Tools (8) *(new — absorbs context-hub)*
- `docs_search` — Search curated doc registry by query or ID
- `docs_get` — Fetch versioned, language-specific doc (`--lang py|js|ts`)
- `docs_get_file` — Incremental fetch of a specific reference file within a doc
- `docs_annotate` — Attach a persistent cross-session annotation to a doc
- `docs_annotate_clear` — Remove annotation from a doc
- `docs_annotate_list` — List all annotations across all docs
- `docs_feedback` — Submit up/down vote on a doc (flows to maintainers)
- `docs_contribute` — Generate draft doc + YAML frontmatter for community submission

---

## Migration from `chub`

Already using context-hub? Every command maps directly:

```bash
# context-hub → ContextOS
chub search openai           →  ctx docs search openai
chub get openai/chat --lang py  →  ctx docs get openai/chat --lang py
chub annotate stripe/api "x" →  ctx docs annotate stripe/api "x"
chub annotate --list         →  ctx docs annotate --list
chub feedback stripe/api up  →  ctx docs feedback stripe/api up
```

Import your existing annotations in one command:

```bash
ctx docs import chub
# Imports all local chub annotations into ContextOS cross-session storage
```

---

## Roadmap

### Phase 1 — Absorb *(current)*
- Unified MCP tool schema
- Memory layer with cross-session persistence
- Hybrid retrieval engine
- Tool registry with DAG execution
- Planning + spec engine with sparring hook
- Full composio integration
- Doc intelligence layer (context-hub absorbed)
- `ctx docs import chub` migration path
- PyPI package publish

### Phase 2 — Compound
- Retrieval feedback loop (auto-improves routing)
- Entity graph with relationship queries
- Memory conflict resolution engine
- Tool output caching layer
- Outcome evaluation + spec scoring
- Doc annotation cross-workspace sync
- Community doc registry (open PRs)

### Phase 3 — Platform
- ContextOS Cloud (hosted, multi-tenant)
- Visual workflow builder
- Marketplace for tool schemas + doc registries
- Enterprise SSO + audit logs
- LangChain + OpenAI Agents SDK adapters
- `chub`-compatible npm shim (alias for teams using context-hub today)

---

## Contributing

PRs welcome for both **code** and **docs**. The doc registry is plain markdown with YAML frontmatter — if you know an API well, you can contribute in 10 minutes.

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for both tracks.

Built under [IASAWI](https://github.com/itallstartedwithaidea) — It All Started With A Idea.

---

## License

MIT — see [LICENSE](LICENSE)

---

## Citation

If you use ContextOS in research or production, please cite:

```
@software{contextos2025,
  title = {ContextOS: The Unified Context Intelligence Layer},
  author = {Williams, John and IASAWI Contributors},
  year = {2025},
  url = {https://github.com/itallstartedwithaidea/contextOS}
}
```

---

*Built with respect for every repo that came before it.*
