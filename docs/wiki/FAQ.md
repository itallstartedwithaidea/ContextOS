# FAQ

---

**Q: Is ContextOS a fork of any of the six source repos?**

No. ContextOS is an original implementation that absorbs the *architecture and patterns* of those repos, not their code. Every line is written fresh. The source repos are credited because they shaped how ContextOS thinks about the problem space, not because their code was copied.

---

**Q: Does ContextOS replace composio / ragflow / claude-mem?**

It can, but it doesn't have to. ContextOS can run as an orchestration layer on top of your existing composio or ragflow instance. Or it can absorb those responsibilities entirely using its own implementations. The choice is yours per deployment.

---

**Q: What is the Pre-Response Sparring Hook and why does it matter?**

It is a mandatory reflection step that runs before any agent output, asking: "Do I have enough information to act on this correctly, or am I pattern-matching?" Every other repo in this space fires before thinking. ContextOS thinks before firing. See the [dedicated wiki page](./Pre-Response-Sparring-Hook.md).

---

**Q: Is the MCP protocol required?**

ContextOS is MCP-native but not MCP-exclusive. You can use the Python API directly without any MCP client. MCP is the recommended interface because it integrates cleanly with Claude Desktop, Cursor, and Windsurf.

---

**Q: Why Python and not TypeScript like most MCP servers?**

The retrieval and memory layers benefit heavily from the Python ML ecosystem (numpy, sentence-transformers, rank-bm25, pgvector). The orchestration and tool layers could be either language, but Python wins on ecosystem breadth for AI agent infrastructure. A TypeScript adapter is on the roadmap.

---

**Q: How does ContextOS handle costs?**

The Cost Ledger tracks every LLM call and API call, attributed to workspace, session, and tool. You can query the ledger at any granularity. No other repo in this space had this — you were flying blind on cost.

---

**Q: What databases does ContextOS use?**

By default: SQLite for lightweight deployments (memory + traces). For production: pgvector for vector search, PostgreSQL for persistent state. Configurable via `memory_db_path` and the `full` extras install.

---

**Q: Can I contribute?**

Yes. See [Contributing.md](./Contributing.md). We especially welcome contributions that improve the integration with the six source repos we credit.

---

**Q: What is IASAWI?**

It All Started With A Idea — John Williams's consultancy and product studio. [GitHub](https://github.com/itallstartedwithaidea).
