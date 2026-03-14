# Retrieval Router

> **The real framework for retrieval isn't "structured vs. unstructured." It's data churn rate vs. indexing cost.**

The Retrieval Router is new in v0.2.0. It classifies every data source by how fast its underlying data changes, then picks the retrieval strategy that matches. No more one-size-fits-all retrieval.

---

## The Problem

Every agent system in the market uses one retrieval strategy for everything. They either embed everything (slow, stale for high-churn data) or do live pulls for everything (expensive, unnecessary for stable data).

This is wrong for the same reason that coding agents abandoned embedding-based RAG: codebases change every time you switch branches. Re-embedding on every checkout kills developer experience. That's why Aider uses Tree-sitter, Codex CLI uses ripgrep, and Cline called semantic RAG "a mind virus" for coding agents.

But for enterprise knowledge bases -- legal docs, compliance policies, customer support libraries -- those don't change every 5 minutes. Embedding them once and using vector search is the right call.

The router makes this distinction operational across every data source an agent touches.

---

## Churn Classes

Every data source registers with one of three churn classes:

### Live (Tier 1)

**Changes:** Constantly (minutes to hours)  
**Strategy:** Direct API pull, no indexing  
**Why:** Any cached answer is already wrong  
**Examples:** Search query reports, auction insights, budget pacing, live performance metrics, stock prices, social media feeds

```python
DataSourceProfile(
    name="search_queries",
    mcp_server="google-ads-mcp",
    churn_class="live",
    index_strategy="none",
)
```

### Warm (Tier 2)

**Changes:** Periodically (days to weeks)  
**Strategy:** BM25 or lightweight embeddings with freshness clock  
**Why:** Index is useful if fresh; stale index is worse than no index  
**Examples:** Keyword lists, ad copy inventory, audience segments, landing page content, pricing sheets

The key: a **freshness threshold** defines how stale the index can be before the router falls back to live pull. No human intervention needed.

```python
DataSourceProfile(
    name="keyword_lists",
    mcp_server="google-ads-mcp",
    churn_class="warm",
    index_strategy="bm25",
    freshness_threshold_seconds=7200,  # 2 hours
)
```

### Cold (Tier 3)

**Changes:** Rarely (months to quarters)  
**Strategy:** Full vector search, embed once  
**Why:** Low churn amortizes indexing cost. Rich semantic search earns its keep.  
**Examples:** Ad policies, account hierarchy, historical benchmarks, strategy docs, legal contracts, compliance libraries

```python
DataSourceProfile(
    name="ad_policies",
    mcp_server="policy-docs-mcp",
    churn_class="cold",
    index_strategy="vector",
    freshness_threshold_seconds=604800,  # 1 week
    embedding_model="all-MiniLM-L6-v2",
)
```

---

## Data Source Registry

Every MCP server self-declares its data profile when registered. The registry stores:

| Field | Purpose |
|---|---|
| `name` | Unique identifier |
| `mcp_server` | Which MCP server provides this data |
| `churn_class` | live / warm / cold |
| `churn_signal` | Event that indicates new data arrived |
| `index_strategy` | none / bm25 / vector / hybrid |
| `embedding_model` | Which model created the current index |
| `freshness_threshold_seconds` | How stale before fallback |
| `schema_fingerprint` | Detects when data shape changes |

---

## Routing Logic

On every retrieval request, the router asks three questions:

1. **What data source is being targeted?**
2. **What's the churn class (declared or learned)?**
3. **Is the current index within its freshness window?**

Then routes:

```
Live source → always live pull (no index needed)

Cold source + healthy index → use index (vector/bm25/hybrid)
Cold source + unhealthy index → fall back to live pull + queue rebuild

Warm source + fresh index → use index
Warm source + stale index → fall back to live pull + trigger re-index
```

---

## Feedback-Driven Reclassification

The router learns from outcomes. Every retrieval is tracked: which source, which strategy, whether the result was used in the agent's output, and whether staleness was detected.

Over time, if a "cold" source keeps producing stale results (its utilization rate drops), the router auto-promotes it to "warm." If a "warm" source's data barely changes and results are always fresh, it gets demoted to "cold" (saving compute on unnecessary live pulls).

```python
# Automatic reclassification
ctx.router().record_retrieval_feedback(
    source_name="client_docs",
    strategy_used="vector",
    result_used_in_output=False,
    staleness_detected=True,
)

# After enough data points:
# "client_docs" reclassified: cold → warm (stale_rate=0.55)
```

---

## Index Health Monitoring

The router continuously monitors index health per source:

| Status | Meaning | Action |
|---|---|---|
| `healthy` | Index exists, fresh, model matches | Use normally |
| `stale` | Index exists but older than threshold | Fallback + queue rebuild |
| `corrupted` | Model drift or schema change | Quarantine + full rebuild |
| `rebuilding` | Rebuild in progress | Use live pull until ready |
| `missing` | No index yet | Full build if strategy requires one |

---

## Data Change Events

When an MCP server pushes new data, the router marks the relevant index as stale and signals the Index Lifecycle Manager to rebuild. The data flow IS the indexing trigger.

```python
# Called automatically when MCP server emits write event
ctx.router().on_data_change("keyword_lists", event_type="write")
# → index marked stale, re-index queued
```

---

## MCP Tools

| Tool | Description |
|---|---|
| `router_register` | Register a data source with churn profile |
| `router_route` | Show routing decision for a query |
| `router_health` | Index health across all sources |
| `router_feedback` | Record retrieval outcome |
| `router_reclassify` | Manual churn class override |
