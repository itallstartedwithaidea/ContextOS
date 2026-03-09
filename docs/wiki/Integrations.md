# Integrations

ContextOS works with every major MCP client and AI agent framework.

---

## Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "contextos": {
      "command": "contextos",
      "args": ["serve"],
      "env": {
        "CONTEXTOS_WORKSPACE": "claude-desktop",
        "CONTEXTOS_MEMORY_PERSIST": "true",
        "CONTEXTOS_SPARRING_HOOK": "true"
      }
    }
  }
}
```

---

## Cursor

Add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "contextos": {
      "command": "contextos",
      "args": ["serve", "--port", "8080"]
    }
  }
}
```

---

## Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "contextos": {
      "serverUrl": "http://localhost:8080/mcp"
    }
  }
}
```

Start the server first: `contextos serve`

---

## Python SDK (direct)

```python
from contextos import ContextOS

ctx = ContextOS(workspace="my-project", sparring_hook=True)

# Store memory
ctx.memory().store("User prefers concise responses", scope="user", importance=0.8)

# Retrieve
results = ctx.retrieval().retrieve("concise responses", corpus="internal")

# Run a tool
result = ctx.tools().run("web_search", {"query": "MCP server Python"})

# Create and execute a plan
plan = ctx.planning().create_plan("Analyze Q3 campaign performance")
verdict = ctx.planning().spar("Delete all low-ROAS campaigns", context="Q4 planning")

# Check costs
print(ctx.cost_summary())
```

---

## LangChain

```python
from langchain.tools import Tool
from contextos import ContextOS

ctx = ContextOS(workspace="langchain-agent")

tools = [
    Tool(
        name=t["name"],
        description=t.get("description", ""),
        func=lambda params, name=t["name"]: ctx.tools().run(name, params).output
    )
    for t in ctx.tools().list_tools()
]
```

---

## OpenAI Agents SDK

```python
from agents import Agent, Tool
from contextos import ContextOS

ctx = ContextOS(workspace="openai-agent")

agent = Agent(
    name="ContextOS Agent",
    tools=[
        Tool(
            name="memory_retrieve",
            description="Retrieve from persistent memory",
            function=lambda q: ctx.memory().retrieve(q)
        ),
        Tool(
            name="retrieve_docs",
            description="Search documentation",
            function=lambda q: ctx.retrieval().retrieve(q)
        ),
    ]
)
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `CONTEXTOS_WORKSPACE` | `default` | Workspace name |
| `CONTEXTOS_PORT` | `8080` | MCP server port |
| `CONTEXTOS_HOST` | `0.0.0.0` | MCP server host |
| `CONTEXTOS_MEMORY_PERSIST` | `true` | Persist memory across sessions |
| `CONTEXTOS_MEMORY_DB` | `./contextos_memory.db` | SQLite path |
| `CONTEXTOS_SPARRING_HOOK` | `true` | Enable Pre-Response Sparring Hook |
| `CONTEXTOS_SPARRING_THRESHOLD` | `medium` | low / medium / high / always |
| `CONTEXTOS_RETRIEVAL_MODE` | `hybrid` | vector / bm25 / hybrid |
| `CONTEXTOS_TOOL_CACHING` | `true` | Enable tool output caching |
| `CONTEXTOS_TRACING` | `true` | Enable request tracing |
| `CONTEXTOS_COST_LEDGER` | `true` | Enable cost tracking |
| `ANTHROPIC_API_KEY` | — | Required for LLM-powered features |
| `OPENAI_API_KEY` | — | Optional, for OpenAI-backed features |
| `COMPOSIO_API_KEY` | — | Required for Composio integrations |
