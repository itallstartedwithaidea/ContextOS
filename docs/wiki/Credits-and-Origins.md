# Credits & Origins

ContextOS was built on top of — and with deep respect for — six open-source projects that each solved a real problem. This page gives full credit to every one of them, explains exactly what they contributed, and is honest about what they were missing. Without these projects, ContextOS would not exist.

---

## The Six Pillars

---

### 1. modelcontextprotocol/servers
**Repository:** https://github.com/modelcontextprotocol/servers  
**Stars:** 80,500+  
**Language:** TypeScript  
**Maintainer:** Anthropic + Community  

#### What They Built
The Model Context Protocol (MCP) is the TCP/IP of AI tool execution. It defines the standard schema for how AI models call tools, receive results, and manage context across turns. The servers repo provides the reference implementations. At 80k stars, it is the most-starred project in the AI context space for a reason: it defined the protocol that everyone else follows.

#### What ContextOS Took From It
- The MCP protocol itself as the native schema for all ContextOS tools
- 100% compatibility — every ContextOS tool is a valid MCP tool
- The concept of a tool registry as the foundation of the execution layer
- Reference server implementations as the baseline for ContextOS's tool execution layer

#### What Was Missing
MCP defines the protocol but provides no higher-level capabilities. There is no memory system, no retrieval engine, no planning layer, no orchestration. It is intentionally a low-level standard. ContextOS is what you build on top of it.

**Gap summary:** Protocol only. No memory, retrieval, planning, or orchestration.

---

### 2. infiniflow/ragflow
**Repository:** https://github.com/infiniflow/ragflow  
**Stars:** 74,400+  
**Language:** Python  
**Maintainer:** InfiniFlow  

#### What They Built
RAGFlow is one of the most production-ready open-source RAG engines available. It handles the full pipeline: document ingestion, chunking, embedding, indexing, retrieval, and generation. Its "Deep Document Understanding" approach handles complex layouts, tables, and mixed-format documents far better than naive chunking approaches. The agent capabilities allow it to reason across retrieval steps.

#### What ContextOS Took From It
- The RAG engine architecture as the foundation of ContextOS's Retrieval Layer
- Deep document understanding pipeline for complex document types
- Agent-aware retrieval execution patterns
- The chunking and embedding strategies

#### What Was Missing
RAGFlow is an excellent retrieval system but it lives in isolation. It has no memory layer — every session starts fresh. There is no staleness detection on retrieved content, so stale chunks silently poison responses. There is no multi-corpus routing — you either search one corpus or you manage multiple instances yourself. Most critically, there is no feedback loop: RAGFlow has no way to learn which retrieved chunks were actually useful versus which were noise.

**Gap summary:** Excellent retrieval, but stateless, single-corpus, and non-learning.

---

### 3. dair-ai/Prompt-Engineering-Guide
**Repository:** https://github.com/dair-ai/Prompt-Engineering-Guide  
**Stars:** 71,300+  
**Language:** MDX  
**Maintainer:** Elvis Saravia / DAIR.AI  

#### What They Built
The most comprehensive corpus of prompt engineering knowledge available in any single place. 71k stars. Covers chain-of-thought, few-shot learning, ReAct agents, RAG prompting, prompt injection defenses, evaluation frameworks, and hundreds of research paper summaries. An essential reference for anyone building AI systems seriously.

#### What ContextOS Took From It
- The prompt pattern library powering ContextOS's Planning Layer spec templates
- Chain-of-thought and ReAct patterns used in the agent instruction layer
- Evaluation frameworks referenced in the Outcome Evaluation tool
- The taxonomy of prompt engineering techniques used in the Pre-Response Sparring Hook design

#### What Was Missing
The Prompt Engineering Guide is documentation — exceptional documentation, but static. There is no runtime integration, no way to automatically apply the right prompt pattern to the right situation, no versioning of prompts in production, and no measurement of which patterns actually work for your specific use case. You read it and implement manually.

**Gap summary:** Invaluable knowledge corpus. Zero runtime applicability.

---

### 4. upstash/context7
**Repository:** https://github.com/upstash/context7  
**Stars:** 48,200+  
**Language:** TypeScript  
**Maintainer:** Upstash  

#### What They Built
Context7 solves a specific and painful problem: LLMs get trained on old library docs and generate code for deprecated APIs. Context7 fetches live, version-specific documentation for the exact library version you're using and injects it into your LLM context. It works as an MCP server and integrates cleanly into Claude Desktop, Cursor, and other editors.

#### What ContextOS Took From It
- The live documentation fetching pattern as a tool in the Retrieval Layer
- Version-aware context injection strategy
- The staleness-awareness concept (extended significantly in ContextOS)
- MCP integration pattern for documentation tools

#### What Was Missing
Context7 is stateless by design — each call fetches fresh docs and that's it. There is no memory: it doesn't remember which libraries you've been working with across sessions. There is no integration with a retrieval layer — it can't combine live docs with your own codebase or internal docs. There is no learning: if you query the same library 100 times, call 101 is exactly as expensive as call 1 with no caching.

**Gap summary:** Stateless doc fetching. No memory, no caching, no integration with other context sources.

---

### 5. thedotmack/claude-mem
**Repository:** https://github.com/thedotmack/claude-mem  
**Stars:** 33,500+  
**Language:** TypeScript  
**Maintainer:** thedotmack  

#### What They Built
Claude-mem captures everything Claude does during coding sessions and compresses it using AI, storing the result in SQLite with embeddings. It was one of the first practical demonstrations that AI agents need persistent memory, and that 33k stars represents developer pain — people starred it because they've been burned by agents that forget everything.

#### What ContextOS Took From It
- The session capture + AI compression pattern
- SQLite + embeddings as the warm memory store architecture
- The concept of memory as a first-class citizen in agent infrastructure
- The embedding-based retrieval approach for memory search

#### What Was Missing
Claude-mem's fundamental limitation is that memory is session-scoped. When the process stops, everything is lost unless you've manually exported it. There is no cross-session persistence layer. There is no memory tiering — everything lives at the same priority level with no concept of hot (in-context), warm (vector DB), or cold (archive). There is no entity graph: relationships between things you remember are not structured. There is no conflict resolution: if you remember something different about a topic from two different sessions, there is no mechanism to reconcile the contradiction. And there is no separation between what the user told the system versus what agents learned during execution.

**Gap summary:** In-session only. Dies on restart. No tiering, entity graph, or conflict resolution.

---

### 6. ComposioHQ/composio
**Repository:** https://github.com/ComposioHQ/composio  
**Stars:** 27,300+  
**Language:** TypeScript / Python  
**Maintainer:** ComposioHQ  

#### What They Built
Composio powers 1000+ tool integrations with managed authentication, tool search, and a sandboxed workbench. It removes the OAuth headache and provides a clean interface for AI agents to call external APIs. It's the best solution available for the "how does my agent call Salesforce / GitHub / Slack" problem.

#### What ContextOS Took From It
- The 1000+ tool integration catalog via the composio pass-through tool
- The OAuth and auth management patterns
- The sandboxed execution workbench concept
- Tool search and discovery patterns

#### What Was Missing
Composio treats every tool call as an independent one-shot operation. There is no tool chaining — no way to define a DAG where the output of tool A flows into the input of tool B with branching logic. There is no output caching — if your agent calls the same deterministic API endpoint 50 times with the same parameters, you make 50 API calls and pay for all of them. There are no retry and fallback policies per tool. There is no tool versioning — upgrades can silently break production agents. There is no cross-tool cost tracking.

**Gap summary:** Excellent integrations, but every call is isolated. No pipelines, no caching, no policies.

---

### 7. gsd-build/get-shit-done
**Repository:** https://github.com/gsd-build/get-shit-done  
**Stars:** 26,500+  
**Language:** JavaScript  
**Maintainer:** gsd-build  

#### What They Built
GSD (get-shit-done) is a lightweight meta-prompting and spec-driven development system for Claude Code using TÂCHES. It enforces a structured spec before any code is written, preventing the most common failure mode: generating code that doesn't match what was actually needed.

#### What ContextOS Took From It
- The spec-driven execution model as the foundation of the Planning Layer
- Meta-prompting patterns for task decomposition
- The TÂCHES task structure adapted into ContextOS plan templates
- The principle that agents should plan before executing

#### What Was Missing
GSD creates specs upfront but they are static — if a tool fails midway through execution, the plan doesn't update. There is no constraint propagation: if step 3 fails, steps 4–7 that depended on step 3 are not automatically revised. There is no spec versioning — you can't diff two versions of a plan or roll back to a prior version that performed better. There is no outcome evaluation loop: GSD doesn't measure whether the final output actually matched the original spec.

Most importantly, there is no Pre-Response Sparring Hook — a forced reflection step before any agent output that distinguishes "I should solve this now" from "I need more information before I act." This single missing feature is responsible for a large share of AI agent failures in production.

**Gap summary:** Good upfront spec. No dynamic revision, no versioning, no evaluation, no reflection before acting.

---

## The Gap Summary

| Gap | Severity | Layer |
|---|---|---|
| No orchestration layer — anywhere | 🔴 Critical | Orchestration |
| Memory dies with session | 🔴 Critical | Memory |
| No retrieval feedback loop | 🔴 Critical | Retrieval |
| No tool DAG execution | 🔴 Critical | Tools |
| No pre-response sparring hook | 🔴 Critical | Planning |
| No cross-session entity graph | 🟠 High | Memory |
| No staleness detection | 🟠 High | Retrieval |
| No tool output caching | 🟠 High | Tools |
| No spec versioning + diff | 🟠 High | Planning |
| No cost ledger | 🟠 High | Orchestration |
| No memory conflict resolution | 🟡 Medium | Memory |
| No multi-corpus routing | 🟡 Medium | Retrieval |
| No tool retry + fallback policies | 🟡 Medium | Tools |
| No outcome evaluation | 🟡 Medium | Planning |
| No schema registry | 🟡 Medium | Orchestration |

ContextOS builds all of them.

---

*This page will be kept up to date as ContextOS evolves. If you maintain any of these projects and want to collaborate or discuss integration, open a Discussion on GitHub.*
