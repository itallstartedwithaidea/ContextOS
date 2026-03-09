# MCP Tools Reference

ContextOS exposes **47 MCP-compatible tools** across 5 categories. All tools follow the standard MCP schema and are compatible with any MCP client.

---

## Memory Tools (9)

### `memory_store`
Store information with automatic tier assignment based on importance and recency.

```json
{
  "tool": "memory_store",
  "input": {
    "content": "string",
    "tags": ["string"],
    "scope": "user | agent | session",
    "importance": 0.0-1.0,
    "ttl_days": null
  }
}
```

---

### `memory_retrieve`
Semantic search across all memory tiers.

```json
{
  "tool": "memory_retrieve",
  "input": {
    "query": "string",
    "tiers": ["hot", "warm", "cold"],
    "scope": "user | agent | all",
    "limit": 10,
    "min_score": 0.7
  }
}
```

---

### `memory_forget`
Targeted forgetting with cascade to entity graph.

```json
{
  "tool": "memory_forget",
  "input": {
    "memory_id": "string",
    "cascade_graph": true
  }
}
```

---

### `memory_summarize`
Compress a set of memories and promote the summary to the warm tier.

```json
{
  "tool": "memory_summarize",
  "input": {
    "memory_ids": ["string"],
    "target_tier": "warm | cold",
    "preserve_originals": false
  }
}
```

---

### `memory_diff`
Compare two memory snapshots.

```json
{
  "tool": "memory_diff",
  "input": {
    "snapshot_a": "string",
    "snapshot_b": "string"
  }
}
```

---

### `memory_graph_query`
Query the entity relationship graph.

```json
{
  "tool": "memory_graph_query",
  "input": {
    "entity": "string",
    "relationship": "string | null",
    "depth": 2
  }
}
```

---

### `memory_export`
Export full memory state as JSON.

```json
{
  "tool": "memory_export",
  "input": {
    "scope": "user | agent | all",
    "format": "json | markdown"
  }
}
```

---

### `memory_import`
Import / restore memory state.

```json
{
  "tool": "memory_import",
  "input": {
    "data": "string (JSON)",
    "merge_strategy": "replace | merge | skip_conflicts"
  }
}
```

---

### `memory_conflicts`
List and resolve conflicting memories.

```json
{
  "tool": "memory_conflicts",
  "input": {
    "auto_resolve": false,
    "resolution_strategy": "newest | highest_confidence | manual"
  }
}
```

---

## Retrieval Tools (8)

### `retrieve_docs`
Hybrid search (BM25 + dense vector) across your document corpus.

```json
{
  "tool": "retrieve_docs",
  "input": {
    "query": "string",
    "corpus": "internal | web | code | api | all",
    "mode": "hybrid | bm25 | vector",
    "limit": 10,
    "staleness_check": true
  }
}
```

---

### `retrieve_live`
Fetch live documentation via context7 integration.

```json
{
  "tool": "retrieve_live",
  "input": {
    "library": "string",
    "version": "string | latest",
    "topic": "string"
  }
}
```

---

### `retrieve_web`
Web search with source quality scoring.

```json
{
  "tool": "retrieve_web",
  "input": {
    "query": "string",
    "limit": 10,
    "score_sources": true,
    "max_age_days": null
  }
}
```

---

### `retrieve_code`
Codebase search with AST awareness.

```json
{
  "tool": "retrieve_code",
  "input": {
    "query": "string",
    "language": "string | null",
    "search_type": "semantic | exact | ast"
  }
}
```

---

### `retrieve_merge`
Merge and deduplicate results from multiple corpora.

```json
{
  "tool": "retrieve_merge",
  "input": {
    "result_sets": ["array of retrieve results"],
    "dedup_threshold": 0.9,
    "ranking": "score | recency | provenance"
  }
}
```

---

### `retrieve_score`
Re-rank a set of results by provenance quality.

```json
{
  "tool": "retrieve_score",
  "input": {
    "results": ["array"],
    "criteria": ["provenance", "recency", "relevance"]
  }
}
```

---

### `retrieve_feedback`
Log which retrieved results were actually used in final output.

```json
{
  "tool": "retrieve_feedback",
  "input": {
    "result_ids": ["string"],
    "used": true,
    "request_id": "string"
  }
}
```

---

### `retrieve_staleness`
Check content freshness and optionally trigger re-fetch.

```json
{
  "tool": "retrieve_staleness",
  "input": {
    "content_ids": ["string"],
    "ttl_days": 30,
    "auto_refresh": true
  }
}
```

---

## Tool Execution Tools (12)

### `tool_run`
Execute any registered tool.

```json
{
  "tool": "tool_run",
  "input": {
    "tool_name": "string",
    "tool_version": "string | latest",
    "parameters": {},
    "use_cache": true
  }
}
```

---

### `tool_chain`
Execute a DAG pipeline of tools.

```json
{
  "tool": "tool_chain",
  "input": {
    "pipeline": [
      {
        "id": "step_1",
        "tool": "tool_name",
        "parameters": {},
        "depends_on": []
      },
      {
        "id": "step_2",
        "tool": "tool_name",
        "parameters": { "input": "{{step_1.output}}" },
        "depends_on": ["step_1"]
      }
    ],
    "on_failure": "stop | skip | fallback"
  }
}
```

---

### `tool_cache_get`
Retrieve cached tool output.

```json
{
  "tool": "tool_cache_get",
  "input": {
    "tool_name": "string",
    "parameters": {},
    "max_age_seconds": 3600
  }
}
```

---

### `tool_cache_set`
Manually cache a tool result.

```json
{
  "tool": "tool_cache_set",
  "input": {
    "tool_name": "string",
    "parameters": {},
    "result": {},
    "ttl_seconds": 3600
  }
}
```

---

### `tool_register`
Register a new tool at runtime.

```json
{
  "tool": "tool_register",
  "input": {
    "name": "string",
    "description": "string",
    "schema": {},
    "endpoint": "string",
    "version": "string"
  }
}
```

---

### `tool_list`
List all available tools with versions.

```json
{
  "tool": "tool_list",
  "input": {
    "category": "memory | retrieval | execution | planning | orchestration | all",
    "include_deprecated": false
  }
}
```

---

### `tool_schema`
Get the schema for a specific tool.

```json
{
  "tool": "tool_schema",
  "input": {
    "tool_name": "string",
    "version": "string | latest"
  }
}
```

---

### `tool_version_pin`
Pin an agent workflow to a specific tool version.

```json
{
  "tool": "tool_version_pin",
  "input": {
    "tool_name": "string",
    "version": "string",
    "workflow_id": "string"
  }
}
```

---

### `tool_retry_policy`
Configure retry and fallback policy for a tool.

```json
{
  "tool": "tool_retry_policy",
  "input": {
    "tool_name": "string",
    "max_retries": 3,
    "retry_delay_ms": 1000,
    "fallback_tool": "string | null",
    "timeout_ms": 30000
  }
}
```

---

### `tool_cost`
Estimate cost for a tool call before executing.

```json
{
  "tool": "tool_cost",
  "input": {
    "tool_name": "string",
    "parameters": {}
  }
}
```

---

### `tool_sandbox_run`
Execute code in a sandboxed environment.

```json
{
  "tool": "tool_sandbox_run",
  "input": {
    "code": "string",
    "language": "python | javascript | bash",
    "timeout_ms": 10000,
    "capture_output": true
  }
}
```

---

### `tool_composio`
Pass-through to Composio integration for 1000+ API tools.

```json
{
  "tool": "tool_composio",
  "input": {
    "app": "string",
    "action": "string",
    "parameters": {}
  }
}
```

---

## Planning Tools (9)

### `plan_create`
Generate a spec-driven execution plan from a goal.

```json
{
  "tool": "plan_create",
  "input": {
    "goal": "string",
    "context": "string",
    "constraints": ["string"],
    "template": "string | null"
  }
}
```

---

### `plan_revise`
Revise a plan based on mid-execution feedback.

```json
{
  "tool": "plan_revise",
  "input": {
    "plan_id": "string",
    "feedback": "string",
    "failed_step": "string | null",
    "propagate_constraints": true
  }
}
```

---

### `plan_diff`
Compare two versions of a plan.

```json
{
  "tool": "plan_diff",
  "input": {
    "plan_id_a": "string",
    "plan_id_b": "string"
  }
}
```

---

### `plan_evaluate`
Score plan output against the original spec.

```json
{
  "tool": "plan_evaluate",
  "input": {
    "plan_id": "string",
    "output": "string",
    "criteria": ["completeness", "accuracy", "spec_adherence"]
  }
}
```

---

### `plan_spar`
Run the Pre-Response Sparring Hook. See [Pre-Response Sparring Hook](./Pre-Response-Sparring-Hook.md).

```json
{
  "tool": "plan_spar",
  "input": {
    "request": "string",
    "context": "string",
    "prior_actions": ["string"]
  }
}
```

---

### `plan_decompose`
Break a goal into executable subtasks.

```json
{
  "tool": "plan_decompose",
  "input": {
    "goal": "string",
    "max_steps": 10,
    "style": "sequential | parallel | dag"
  }
}
```

---

### `plan_constraints`
Propagate constraint changes through a plan.

```json
{
  "tool": "plan_constraints",
  "input": {
    "plan_id": "string",
    "constraint_change": "string",
    "affected_step": "string"
  }
}
```

---

### `plan_rollback`
Restore a previous plan version.

```json
{
  "tool": "plan_rollback",
  "input": {
    "plan_id": "string",
    "target_version": "string | previous"
  }
}
```

---

### `plan_template`
Load a proven spec template.

```json
{
  "tool": "plan_template",
  "input": {
    "template_name": "string",
    "variables": {}
  }
}
```

---

## Orchestration Tools (9)

### `ctx_route`
Classify and route an incoming request.

```json
{
  "tool": "ctx_route",
  "input": {
    "request": "string",
    "context": "string"
  }
}
```

---

### `ctx_trace`
Get full trace for a request ID.

```json
{
  "tool": "ctx_trace",
  "input": {
    "trace_id": "string",
    "include_costs": true
  }
}
```

---

### `ctx_schema_get`
Get a registered tool schema.

```json
{
  "tool": "ctx_schema_get",
  "input": {
    "tool_name": "string",
    "version": "string | latest"
  }
}
```

---

### `ctx_schema_register`
Register a new tool schema.

```json
{
  "tool": "ctx_schema_register",
  "input": {
    "name": "string",
    "schema": {},
    "version": "string"
  }
}
```

---

### `ctx_cost_summary`
Get cost ledger summary.

```json
{
  "tool": "ctx_cost_summary",
  "input": {
    "workspace": "string",
    "period": "session | day | week | month | all"
  }
}
```

---

### `ctx_workspace_create`
Create a new isolated workspace.

```json
{
  "tool": "ctx_workspace_create",
  "input": {
    "name": "string",
    "config": {}
  }
}
```

---

### `ctx_workspace_list`
List all workspaces.

```json
{
  "tool": "ctx_workspace_list",
  "input": {}
}
```

---

### `ctx_health`
System health check.

```json
{
  "tool": "ctx_health",
  "input": {
    "layers": ["memory", "retrieval", "tools", "planning", "orchestration"]
  }
}
```

---

### `ctx_version`
Get ContextOS version and component info.

```json
{
  "tool": "ctx_version",
  "input": {}
}
```
