# Index Lifecycle Manager

> **Self-healing indexes that rebuild on data events, detect embedding model drift, and degrade gracefully when things break.**

The Index Lifecycle Manager is new in v0.2.0. It sits behind the Retrieval Router and ensures that indexes are always ready when the router needs them. No cron jobs. No manual refresh. The data pipeline IS the indexing trigger.

---

## Why This Exists

The old constraint was that re-embedding is expensive and slow. That forced coding agents toward grep-only approaches -- they couldn't afford to re-index on every branch checkout.

What changed: local embedding models (sentence-transformers, Nomic, BGE) run on commodity hardware. BM25 indexes rebuild in seconds via rank_bm25 or tantivy. The cost barrier collapsed.

The lifecycle manager makes the new economics operational: continuous background re-indexing triggered by data events, with automatic detection when indexes go bad and graceful degradation when rebuilds fail.

---

## Core Behaviors

### 1. Event-Driven Re-indexing

When an MCP server pushes new data (a write event), the lifecycle manager queues an index rebuild for that source. BM25 rebuilds run inline because they're sub-second. Vector rebuilds queue for async processing.

```python
# Triggered automatically by MCP data events
ctx.indexer().on_data_change("keyword_lists", change_type="write")
# → IndexJob queued: incremental rebuild, bm25, trigger=data_change
```

No scheduled jobs. No polling. The data flow is the trigger.

### 2. Heartbeat Health Checks

Every N seconds (configurable, default 300), the manager scans all registered sources. This catches:

- Indexes that went stale without a write event (data changed upstream but no event was emitted)
- Corrupted indexes (model drift, schema changes)
- Missing indexes (source was registered but never indexed)

```python
results = ctx.indexer().heartbeat()
# {checked: 5, stale: 1, rebuilt: 1, circuit_breaker_open: 0}
```

### 3. Embedding Model Drift Detection

This is subtle and critical. If you update your embedding model (e.g., from `all-MiniLM-L6-v2` to `all-MiniLM-L12-v2`), every vector index is silently invalid. Old embeddings and new embeddings aren't in the same vector space. Similarity searches produce garbage results with no obvious error.

The lifecycle manager catches this:

- Every index stores which model and version created it
- When the active model changes, all vector indexes with mismatched models are flagged as `corrupted`
- Full rebuilds are queued automatically

```python
jobs = ctx.indexer().on_model_change(
    new_model="all-MiniLM-L12-v2",
    new_version="2.0.0",
)
# 3 vector indexes queued for full rebuild
```

### 4. Schema Change Quarantine

If the shape of incoming data changes (new fields, removed fields, restructured nesting), existing indexes may be indexing the wrong thing. The manager:

- Computes a schema fingerprint from data samples
- Compares against the fingerprint at index time
- If they differ: quarantines the index (status = `corrupted`), queues full rebuild
- No results served from a quarantined index

```python
new_fingerprint = ctx.indexer().compute_schema_fingerprint(data_sample)
ctx.indexer().on_schema_change("keyword_lists", new_fingerprint)
# If fingerprint changed: index quarantined, rebuild queued
```

### 5. Circuit Breakers

If re-indexing fails 3 consecutive times for a source, the circuit breaker trips. The system stops trying to rebuild and degrades to live-pull-only for that source. This prevents:

- Wasted compute on a fundamentally broken data source
- Cascade failures from one bad source affecting the whole system
- Silent retry storms

After the cooldown period (default 300s), the breaker enters `half_open` state and allows one retry. If it succeeds, the breaker resets. If it fails, it trips again.

```python
# Check circuit breaker state
health = ctx.indexer().health()
# {circuit_breakers_open: 1, ...}

# Manual reset after fixing the underlying issue
ctx.indexer().reset_circuit_breaker("keyword_lists")
```

---

## Index Jobs

Every index operation is tracked as a job:

| Field | Purpose |
|---|---|
| `id` | Unique job identifier |
| `source_name` | Which data source |
| `job_type` | `full_build`, `incremental`, `rebuild_model_change`, `rebuild_schema_change` |
| `strategy` | `bm25`, `vector`, `hybrid` |
| `status` | `queued`, `running`, `completed`, `failed` |
| `trigger` | What caused this job: `data_change`, `model_change`, `heartbeat_stale`, etc. |
| `documents_processed` | How many documents were indexed |
| `duration_ms` | How long it took |

---

## Configuration

```python
ctx = ContextOS(
    index_heartbeat_interval_seconds=300,        # how often heartbeat runs
    index_circuit_breaker_threshold=3,            # failures before trip
    index_circuit_breaker_cooldown_seconds=300,   # wait before retry after trip
    active_embedding_model="all-MiniLM-L6-v2",   # current model
    active_embedding_model_version="1.0.0",
)
```

---

## Production Integration Points

The lifecycle manager stubs are designed for drop-in replacement with production backends:

| Strategy | Production Backend | Rebuild Speed |
|---|---|---|
| BM25 | `rank_bm25` or `tantivy` | Sub-second for most corpora |
| Vector | `sentence-transformers` (local) | Minutes for large corpora |
| Hybrid | Both | BM25 inline, vector async |

Local embedding means no API calls, no per-token cost, no rate limits. The cost barrier that made re-indexing impractical for high-churn data is gone.

---

## MCP Tools

| Tool | Description |
|---|---|
| `indexer_status` | Health and job status across all sources |
| `indexer_rebuild` | Manually trigger index rebuild for a source |
| `indexer_heartbeat` | Run heartbeat check now |
| `indexer_circuit_reset` | Reset a tripped circuit breaker |
| `indexer_model_update` | Register new embedding model (triggers rebuilds) |
