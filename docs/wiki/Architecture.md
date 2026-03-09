# Architecture

ContextOS is organized into five layers. Every request enters through the Orchestration Core and is dispatched to the appropriate layer. Layers can call each other but the Orchestration Core is always the entry point.

---

## The Five Layers

```
┌────────────────────────────────────────────────────────────────────┐
│                         CLIENT / AGENT                              │
│              (Claude Desktop · Cursor · Windsurf · SDK)            │
└────────────────────────────┬───────────────────────────────────────┘
                             │  MCP Protocol
┌────────────────────────────▼───────────────────────────────────────┐
│                     ORCHESTRATION CORE                              │
│                                                                     │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐    │
│   │ Intent Router│  │Schema Registry│  │   Cost Ledger         │   │
│   └──────────────┘  └──────────────┘  └──────────────────────┘    │
│   ┌──────────────┐  ┌──────────────┐                               │
│   │Request Tracer│  │  Auth Layer  │                               │
│   └──────────────┘  └──────────────┘                               │
└────┬──────────────┬──────────────┬────────────────┬───────────────┘
     │              │              │                │
┌────▼────┐   ┌─────▼────┐  ┌─────▼─────┐  ┌──────▼──────┐
│ MEMORY  │   │RETRIEVAL │  │   TOOLS   │  │  PLANNING   │
│  LAYER  │   │  LAYER   │  │   LAYER   │  │   LAYER     │
│         │   │          │  │           │  │             │
│ Hot Tier│   │Hybrid    │  │DAG Exec   │  │Spec Engine  │
│Warm Tier│   │Search    │  │Caching    │  │Pre-Response │
│Cold Tier│   │Multi-    │  │Retry/     │  │Sparring Hook│
│Entity   │   │Corpus    │  │Fallback   │  │Dynamic Plan │
│Graph    │   │Routing   │  │Sandboxing │  │Revision     │
│Conflict │   │Staleness │  │Tool       │  │Outcome Eval │
│Resolut. │   │Detection │  │Versioning │  │Constraint   │
│         │   │Feedback  │  │           │  │Propagation  │
│         │   │Loop      │  │           │  │             │
└─────────┘   └──────────┘  └───────────┘  └─────────────┘
     │               │             │               │
     └───────────────┴─────────────┴───────────────┘
                             │
┌────────────────────────────▼───────────────────────────────────────┐
│                      EXTERNAL INTEGRATIONS                          │
│                                                                     │
│   claude-mem     ragflow     context7    composio    MCP Servers   │
│   (memory)     (retrieval) (live docs)   (tools)    (tool proto)   │
└────────────────────────────────────────────────────────────────────┘
```

---

## Layer Responsibilities

### Orchestration Core
The entry point for every request. Responsible for:
- Parsing incoming MCP tool calls
- Classifying intent using semantic routing
- Dispatching to the correct layer(s)
- Recording full request trace
- Tracking costs across all layers
- Enforcing workspace-level auth and rate limits

The Orchestration Core is the only layer that is 100% novel — no existing repo provided this.

### Memory Layer
Responsible for everything the system knows and remembers:
- **Hot tier:** Currently in-context. Zero retrieval latency. Limited to ~8k tokens.
- **Warm tier:** Vector DB (pgvector / sqlite-vec). Millisecond retrieval. Unbounded.
- **Cold tier:** Compressed archive. Used for long-term knowledge that is rarely needed.
- **Entity Graph:** Structured knowledge extracted from unstructured memory.
- **Conflict resolution:** Handles contradictions between memory sources.

### Retrieval Layer
Responsible for finding information across all sources:
- Hybrid search (BM25 + dense vector) for maximum precision-recall
- Multi-corpus routing: internal docs, live web, codebase, API specs
- Staleness detection with configurable TTL per source
- Feedback loop that improves routing over time

### Tool Execution Layer
Responsible for running things:
- Executes any registered MCP-compatible tool
- DAG-based pipeline execution for multi-step workflows
- Output caching by input hash for deterministic calls
- Per-tool retry budgets and fallback tool definitions
- Code sandboxing with output capture

### Planning & Spec Layer
Responsible for thinking before acting:
- Generates spec-driven execution plans from goal descriptions
- Runs the Pre-Response Sparring Hook before any agent output
- Dynamically revises plans when tools fail mid-execution
- Propagates constraint changes through dependent plan steps
- Evaluates final output against original spec

---

## Data Flow: A Complete Request

Here is what happens when an agent sends: `"Find all our Q3 campaign docs and summarize the key decisions"`

```
1. Request enters Orchestration Core
   → Intent Router classifies: RETRIEVAL + PLANNING + MEMORY
   → Request Tracer assigns trace ID: ctx_7f3a9b2
   → Cost Ledger opens billing entry

2. Planning Layer fires first (Pre-Response Sparring Hook)
   → "Is this a solve-it moment or a learn-more moment?"
   → Determines: need retrieval before planning a summary
   → Creates plan: [retrieve_docs → memory_retrieve → plan_decompose → summarize]

3. Memory Layer is checked
   → Hot tier: no recent Q3 campaign context
   → Warm tier: finds 3 relevant memory chunks from past sessions
   → Returns: prior context about Q3 campaigns injected into retrieval query

4. Retrieval Layer executes
   → Multi-corpus route: internal docs + codebase
   → Hybrid search: BM25 finds "Q3 campaign" keyword matches
   → Dense vector: finds semantically related docs
   → Staleness check: 2 docs flagged as >30 days old, re-fetched
   → Results merged and scored by provenance quality

5. Planning Layer generates summary
   → Decomposes: [key decisions by campaign] [budget decisions] [performance notes]
   → Generates structured summary against spec

6. Memory Layer stores result
   → Summary promoted to warm tier
   → Entity graph updated: Q3 → campaigns → decisions (linked)

7. Orchestration Core closes request
   → Trace completed: 1.4s total, 3 tool calls, $0.0034 LLM cost
   → Cost Ledger updated
   → Response returned to agent
```

---

## Configuration

See [Configuration.md](./Configuration.md) for all options.

## Integrations

See [Integrations.md](./Integrations.md) for client setup guides.
