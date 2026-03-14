# Architecture

ContextOS is organized into eight layers. Every request enters through the Orchestration Core and is dispatched to the appropriate layer. The Cognition Layer sits between retrieval and output, adding reasoning that no other framework provides.

---

## The Eight Layers

```
┌──────────────────────────────────────────────────────────────────────┐
|                          CLIENT / AGENT                               |
|               (Claude Desktop - Cursor - Windsurf - SDK)             |
└───────────────────────────────┬──────────────────────────────────────┘
                                | MCP Protocol
┌───────────────────────────────▼──────────────────────────────────────┐
|                       ORCHESTRATION CORE                              |
|                                                                       |
|    Intent Router   Schema Registry   Cost Ledger   Request Tracing   |
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

The Orchestration Core is 100% novel -- no existing repo provided this.

### Cognition Layer *(new in v0.2.0)*
The thinking layer between retrieval and output. Responsible for:
- **Active Forgetting:** Drop retrieved context that creates noise
- **Reasoning Depth Calibration:** Estimate how much thinking a problem deserves
- **Synthesis Detection:** Determine whether to think about existing context or retrieve more
- **Unknown Unknown Sensing:** Detect missing categories of information
- **Productive Contradiction:** Hold conflicting signals as insight
- **Context-Dependent Gravity:** Re-weight memories by current question

This layer is entirely new. No open-source agent framework has built it. See [Cognition Layer](./Cognition-Layer.md) for deep documentation.

### Retrieval Router *(new in v0.2.0)*
Churn-aware routing that sits before the retrieval layer. Responsible for:
- Classifying data sources by churn rate (live/warm/cold)
- Selecting retrieval strategy per source
- Checking index freshness on every request
- Falling back to live pull when indexes are stale
- Learning from outcomes to reclassify churn classes

See [Retrieval Router](./Retrieval-Router.md) for full documentation.

### Index Lifecycle Manager *(new in v0.2.0)*
Self-healing index infrastructure behind the router. Responsible for:
- Event-driven re-indexing triggered by MCP data events
- Embedding model drift detection and auto-rebuild
- Schema change quarantine
- Circuit breakers for failed index operations
- Periodic heartbeat health checks

See [Index Lifecycle Manager](./Index-Lifecycle-Manager.md) for full documentation.

### Memory Layer
Responsible for everything the system knows and remembers:
- **Hot tier:** Currently in-context. Zero retrieval latency.
- **Warm tier:** Vector DB (pgvector / sqlite-vec). Millisecond retrieval.
- **Cold tier:** Compressed archive. Rarely needed.
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

## Data Flow: A Complete Request (v0.2.0)

Here is what happens when an agent sends: `"Should I pause branded search campaigns given declining ROAS?"`

```
1. Request enters Orchestration Core
   → Intent Router classifies: RETRIEVAL + COGNITION + PLANNING
   → Request Tracer assigns trace ID: ctx_8b4c2f1
   → Cost Ledger opens billing entry

2. Retrieval Router fires
   → Checks registered sources for "advertising" domain
   → google_ads: live → direct API pull
   → keyword_lists: warm, index stale → fallback to live pull + queue re-index
   → ad_policies: cold, index healthy → use vector search

3. Retrieval Layer executes per router decisions
   → Live pull: fresh search query data, auction insights
   → Vector search: policy docs, historical benchmarks
   → BM25: (skipped, index stale)
   → Results merged and scored by provenance quality

4. Cognition Layer fires (THE NEW STEP)
   → Active Forgetting: 20 chunks in, 12 kept, 8 dropped (noise, redundancy, budget)
   → Depth Calibration: "moderate" (4 steps, high stakes due to "pause" keyword)
   → Synthesis Detection: "synthesize" (contradictory data needs reasoning, not more data)
   → Unknown Unknown Sensing: "budget" and "crm" data available but not queried (!)
   → Productive Contradiction: ROAS down + pipeline up = measurement gap (the insight)
   → Gravity Reweighting: "never pause without approval" boosted 0.3 → 0.95

5. Planning Layer fires (Pre-Response Sparring Hook)
   → Receives CognitionReport (knows retrieval quality AND thinking quality)
   → Verdict: HOLD — constraint detected + 2 sources not queried
   → Recommended action: query CRM and budget data, then re-evaluate

6. Agent pauses, queries missing sources, re-runs
   → Now has full picture: ROAS declining but pipeline growing,
     budget data shows room, constraint requires client approval
   → Generates recommendation: don't pause, investigate attribution gap,
     present options to client for decision

7. Orchestration Core closes request
   → Trace: 2.1s total, 5 tool calls, $0.0047 LLM cost
   → Cognition metrics logged for calibration learning
   → Retrieval feedback logged for router reclassification
```

---

## Configuration

See [Configuration.md](./Configuration.md) for all options.

## Integrations

See [Integrations.md](./Integrations.md) for client setup guides.
