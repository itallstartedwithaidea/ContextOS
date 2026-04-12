# ContextOS

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [中文](README.zh.md) | [Nederlands](README.nl.md) | [Русский](README.ru.md) | [한국어](README.ko.md)

> **面向 AI 智能体的统一上下文智能层。**  
> 一次 pip 安装。全部能力。无一遗漏。

[![PyPI version](https://badge.fury.io/py/contextos.svg)](https://badge.fury.io/py/contextos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![GitHub Stars](https://img.shields.io/github/stars/itallstartedwithaidea/contextOS?style=social)](https://github.com/itallstartedwithaidea/contextOS)

```
pip install contextos
```

---

## 什么是 ContextOS？

ContextOS 是 **AI 上下文的操作系统层**——单一的统一 MCP 服务器与 CLI，吸收、扩展并超越 AI 智能体与上下文管理生态中七个领先开源仓库的能力。

它的诞生是因为没有一个项目覆盖全栈。现有工具往往只擅长一件事而缺少其余部分。ContextOS 将它们合在一起，填补每一处空白，并加入此前任何地方都不存在的编排层。

**ContextOS 不是包装器，而是平台。** 你过去使用的每一种工具都会变成运行在其上的模块。

---

## v0.2.0 — Cognition 更新

**行业做法：检索再生成。**  
**ContextOS 做法：检索，思考，再生成。**

市面上的智能体框架都跳过了最关键的一步。它们检索上下文，塞进提示词，然后生成输出。介于检索与输出之间的思考——专家会权衡矛盾、约束、感知信息缺口并决定思考深度——这一部分在任何地方都不存在。

直到现在。

v0.2.0 新增三层与一个框架，用来建模专家推理的真实工作方式：

### Cognition 层 — 六种认知原语

这些是介于检索与生成之间的推理操作。没有任何智能体框架把它们做成一等能力。

| 原语 | 作用 | 为何重要 |
|---|---|---|
| **主动遗忘** | 丢弃降低输出质量的已检索上下文 | 更多上下文并不总是更好。检索到 20 段而只有 3 段真正有用会产生噪声，把推理带偏。 |
| **推理深度校准** | 在投入算力前估计问题值得多少思考 | 快速模式匹配与十步推理链都合理——但适用于不同问题。智能体应知道自己处于哪种情境。 |
| **综合检测** | 判断智能体应对已有信息**思考**还是**再去获取** | 整个行业把每个任务都当检索问题。有些任务是综合、类比或关系推理，更多数据反而有害。 |
| **未知未知感知** | 检测智能体是否缺失**整类**信息 | 已知未知容易处理。未知未知会致命。「我不知道 Salesforce 数据在这里相关」与「我没有今天的数据」是不同失败模式。 |
| **建设性矛盾** | 把冲突数据当作信号而非强行消解 | 「Google Ads 说转化上升，CRM 说管道持平」——答案不是「选一个」。测量鸿沟**就是**洞察。 |
| **上下文相关引力** | 按当前问题重新加权记忆重要性 | 关于「未经批准绝不投放品牌词」的记忆在与 PMax 查询的相似度上得分很低，却会根本改变建议。静态重要性分数捕捉不到这一点。 |

### 检索路由器 — 面向变更感知的路由

检索的真正框架不是「结构化 vs 非结构化数据」，而是 **数据变更率 vs 索引成本。**

代码库每次切换分支都会变——一嵌入索引立刻过时。法律文档每季度才变——嵌入一次可受益数月。Retrieval Router 按底层数据变化速度为每个数据源分类，再选择匹配的检索策略。

| 变更类别 | 示例数据 | 策略 | 原因 |
|---|---|---|---|
| **Live** | 搜索词报告、竞价数据、预算节奏 | 直接 API 拉取，不建索引 | 任何缓存答案都已错误 |
| **Warm** | 关键词列表、受众细分、广告文案库 | BM25 或向量索引 + 新鲜度时钟 | 每周变化，索引在新鲜时有用 |
| **Cold** | 广告政策、账户层级、策略文档 | 全向量检索，嵌入一次 | 最多每季度变化，值得深度索引 |

路由器在每次请求时检查索引新鲜度。若 warm 源索引过期，会自动回退到实时拉取，无需人工干预。

### 索引生命周期管理器 — 自愈合索引

事件驱动重索引，带断路器与嵌入模型漂移检测。

- **写入触发重索引：** MCP 服务器推送新数据时，索引自动重建。无定时任务。数据流**就是**索引触发器。
- **嵌入模型漂移检测：** 更新嵌入模型？所有向量索引在静默中失效。生命周期管理器捕获模型版本不匹配并触发全量重建。
- **模式变更隔离：** 若入站数据形状变化，现有索引在重建前被隔离。不会出现静默错误结果。
- **断路器：** 若连续 3 次重索引失败，系统停止重试并降级为实时拉取。发出告警。可手动复位。
- **心跳检查：** 定期健康扫描捕获事件未触发的陈旧索引。

---

## 工作原理：广告示例

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

## 站在巨人的肩膀上

没有这些项目的杰出工作，就不会有 ContextOS。我们正式致谢并致敬每一个项目：

### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

**80.5k stars — TypeScript**  
工具执行与上下文协议的基础标准。ContextOS 以 MCP 为原生模式，与所有现有 MCP 服务器 100% 兼容。  
**它给予我们：** 协议。标准。生态。  
**缺失之处：** 无编排层、无记忆、无检索、无规划——仅有传输协议本身。

---

### [infiniflow/ragflow](https://github.com/infiniflow/ragflow)

**74.4k stars — Python**  
生产级 RAG 引擎，具备智能体能力与深度文档解析。  
**它给予我们：** 检索引擎、文档摄入流水线、面向智能体的 RAG 执行。  
**缺失之处：** 无跨层记忆集成、无陈旧检测、无多语料路由、无反馈闭环、无 MCP 原生工具模式。

---

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

**71.3k stars — MDX**  
提示工程模式、论文与技术的权威语料库。  
**它给予我们：** 支撑 ContextOS 规格模板与智能体指令模式的规划与提示知识库。  
**缺失之处：** 仅静态文档——无运行时集成、无提示版本管理、无结果追踪。

---

### [upstash/context7](https://github.com/upstash/context7)

**48.2k stars — TypeScript**  
面向 LLM 与 AI 代码编辑器的最新代码文档。  
**它给予我们：** 实时文档获取、面向 LLM 的版本感知上下文注入。  
**缺失之处：** 无记忆层、无检索集成、无会话连续性——纯无状态文档拉取。

---

### [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)

**33.5k stars — TypeScript**  
使用 AI 与 SQLite + 嵌入捕获并压缩编码会话的 Claude Code 插件。  
**它给予我们：** 会话内记忆压缩模式、SQLite + 嵌入架构。  
**缺失之处：** 记忆随会话结束而消失。无跨会话持久化、无实体图、无分层、无冲突解决。

---

### [ComposioHQ/composio](https://github.com/ComposioHQ/composio)

**27.3k stars — TypeScript**  
为 1000+ 工具包提供认证、工具搜索与沙箱工作台以构建 AI 智能体。  
**它给予我们：** 外部 API 集成层——OAuth 流程、工具沙箱、执行上下文。  
**缺失之处：** 无工具 DAG 执行、无输出缓存、无重试/回退策略、无工具版本管理。

---

### [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)

**26.5k stars — JavaScript**  
面向 Claude Code 的轻量元提示与规格驱动开发系统。  
**它给予我们：** 规格驱动执行模型、元提示模式、任务分解模板。  
**缺失之处：** 无动态计划修订、无约束传播、无规格版本管理、无结果评估闭环。

---

### [andrewyng/context-hub](https://github.com/andrewyng/context-hub)

**47 stars — JavaScript**  
带 CLI（`chub`）的策展、版本化文档库，面向编码智能体。  
**它给予我们：** 文档智能模式：策展内容 + 增量获取 + 本地注释 + 社区反馈闭环。  
**缺失之处：** 无记忆层、无检索集成、无 MCP 工具模式、无 Python 支持。

> **ContextOS 完整吸收 context-hub。** 每个 `chub` 命令都映射为 `ctx docs` 命令。

---

## 曾经缺失的部分 — ContextOS 的构建

在吸收全部七个项目后，这些是单个仓库都未覆盖的缺口：

### 编排核心 *(全新)*

| 能力 | 为何重要 |
|---|---|
| **语义意图路由器** | 分类每个入站请求并自动分发到正确层。 |
| **请求追踪 / 可观测性** | 每次工具调用的完整血缘：哪一层触发、延迟、token 成本、质量分。 |
| **模式注册表** | 带向后兼容的版本化工具模式。 |
| **多工作区认证** | 每工作区 API 密钥、速率限制与审计日志。 |
| **成本账本** | 按会话、工作区、工具追踪 LLM + API 支出。 |

### Cognition 层 *(v0.2.0 全新)*

| 能力 | 为何重要 |
|---|---|
| **主动遗忘** | 丢弃制造噪声的检索上下文。多不一定好。 |
| **推理深度校准** | 在投入算力前知道问题值得多少思考。 |
| **综合检测** | 区分检索任务与推理任务。 |
| **未知未知感知** | 检测缺失的信息类别，而非仅缺失事实。 |
| **建设性矛盾** | 将冲突信号作为洞察持有，而非消解为单一答案。 |
| **上下文相关引力** | 按当前问题重加权记忆。约束覆盖相似度分数。 |
| **上下文预算** | 对检索上下文强制执行 token 限制。将 Karpathy 的「上下文窗口 = RAM」落地为操作能力。 |

### 检索路由器 *(v0.2.0 全新)*

| 能力 | 为何重要 |
|---|---|
| **数据源注册表** | 每个 MCP 服务器自声明变更画像、索引策略与新鲜度阈值。 |
| **变更感知路由** | 每源 live/warm/cold 分类。策略匹配数据波动。 |
| **自动回退** | 索引陈旧？回退到实时拉取。无需人工干预。 |
| **反馈驱动重分类** | 若「cold」源持续变旧，系统自动提升为「warm」。 |

### 索引生命周期管理器 *(v0.2.0 全新)*

| 能力 | 为何重要 |
|---|---|
| **事件驱动重索引** | MCP 数据事件触发重建。无 cron。 |
| **嵌入模型漂移检测** | 模型更新 = 所有向量索引无效。自动检测并重建。 |
| **模式变更隔离** | 数据形状变化？索引隔离至重建完成。 |
| **断路器** | 连续 3 次索引失败 = 降级实时拉取 + 告警。 |
| **心跳健康检查** | 定期扫描捕获事件遗漏的陈旧索引。 |

### 记忆层 *(扩展 claude-mem)*

| 能力 | 为何重要 |
|---|---|
| **跨会话持久化** | 记忆在进程重启后仍存在。 |
| **记忆分层（Hot/Warm/Cold）** | 按新近度 + 相关性自动升降级。 |
| **实体图** | 提取实体并链接为结构化知识。 |
| **冲突解决** | 使用时间戳 + 置信度解决矛盾记忆源。 |
| **用户范围 vs 智能体范围记忆** | 用户告知系统的内容与智能体学到的内容——分开展示。 |

### 检索层 *(扩展 ragflow + context7)*

| 能力 | 为何重要 |
|---|---|
| **混合检索** | BM25 关键词 + 稠密向量检索组合。 |
| **来源归因评分** | 按出处质量排序片段，而非仅余弦相似度。 |
| **陈旧检测** | 标记超过可配置 TTL 的内容并触发重新获取。 |
| **多语料路由** | 将查询并行路由到文档、实时网页、代码库或 API 规范。 |
| **检索反馈闭环** | 追踪哪些片段出现在最终输出中。路由随时间改进。 |

### 工具执行层 *(扩展 composio + MCP servers)*

| 能力 | 为何重要 |
|---|---|
| **工具链 / DAG 执行** | 多步工具流水线与分支逻辑。 |
| **沙箱代码执行** | 安全执行、捕获输出与错误恢复。 |
| **工具输出缓存** | 按输入哈希缓存确定性结果。 |
| **重试 + 回退策略** | 每工具 SLA：重试预算、回退工具、优雅降级。 |
| **工具版本管理** | 将智能体工作流固定到特定工具版本。 |

### 规划与规格层 *(扩展 GSD + Prompt-Engineering-Guide)*

| 能力 | 为何重要 |
|---|---|
| **动态计划修订** | 计划随工具输出在执行中更新。 |
| **约束传播** | 若工具 X 失败，下游步骤自动修订。 |
| **规格版本 + diff** | 追踪任务规格如何演变。新规格表现差时可回滚。 |
| **响应前对练钩子** | 任何智能体输出前的强制反思。在行动前强制停顿。 |
| **结果评估** | 将最终输出相对原始规格打分。将信号反馈给规划。 |

### 文档智能层 *(完整吸收 context-hub)*

| 能力 | 为何重要 |
|---|---|
| **策展文档注册表** | 社区维护、版本化的 API、框架与工具 Markdown 文档。 |
| **语言特定获取** | 按目标语言获取文档。无不相关片段。 |
| **增量获取** | 只取所需。不浪费 token。 |
| **持久注释** | 智能体附加在文档上的本地笔记。跨会话重启保留。 |
| **社区反馈闭环** | 每文档上下投票反馈给维护者。 |
| **文档陈旧评分** | 陈旧文档被标记并自动重新获取。 |

---

## 架构

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

**关键数据流（v0.2.0）：**

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

## 快速开始

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

### 注册数据源

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

### 运行 Cognition 通道

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

## CLI：`ctx`

### 文档命令 *(与 context-hub 对等 + 扩展)*

```bash
ctx docs search openai                     # find available docs
ctx docs get openai/chat --lang py         # fetch current docs, Python variant
ctx docs get stripe/api --file webhooks    # incremental fetch
ctx docs annotate stripe/api "Note here"   # attach a persistent note
ctx docs feedback stripe/api up            # upvote a doc
```

### 记忆命令

```bash
ctx memory store "key insight about X"
ctx memory retrieve "what do I know about stripe webhooks"
ctx memory forget "session notes from project Y"
ctx memory graph query "entity:OpenAI"
ctx memory conflicts --resolve auto
```

### 检索命令

```bash
ctx retrieve docs "stripe payment intents python"
ctx retrieve live "openai assistants api latest"
ctx retrieve web "LLM context window best practices 2026"
ctx retrieve code "webhook verification pattern"
```

### 路由器命令 *(v0.2.0 新增)*

```bash
ctx router register --name google_ads --churn live --index none
ctx router register --name policies --churn cold --index vector
ctx router health                          # index health across all sources
ctx router route "what queries triggered ads today"  # show routing decision
```

### Cognition 命令 *(v0.2.0 新增)*

```bash
ctx cognition think --query "should I pause branded" --domain advertising
ctx cognition budget --tokens 4000         # set context budget
ctx cognition contradictions --last        # show last detected contradictions
ctx cognition unknowns --last              # show unknown-unknown alerts
```

### 规划命令

```bash
ctx plan create "build a stripe checkout integration"
ctx plan spar                              # pre-response sparring hook
ctx plan revise --feedback "tool X failed"
ctx plan evaluate --against-spec spec.md
```

### 编排命令

```bash
ctx health                                 # all 8 layers
ctx cost summary --workspace my-agent
ctx trace --id req_abc123
```

---

## 暴露的 MCP 工具

ContextOS 通过 MCP 协议在 8 个类别中暴露 **67** 个工具。

### 记忆工具 (9)
`memory_store` `memory_retrieve` `memory_forget` `memory_summarize` `memory_diff` `memory_graph_query` `memory_export` `memory_import` `memory_conflicts`

### 检索工具 (8)
`retrieve_docs` `retrieve_live` `retrieve_web` `retrieve_code` `retrieve_merge` `retrieve_score` `retrieve_feedback` `retrieve_staleness`

### Cognition 工具 (6) *(v0.2.0 新增)*
`cognition_think` `cognition_forget` `cognition_depth` `cognition_contradictions` `cognition_unknowns` `cognition_gravity`

### 路由器工具 (5) *(v0.2.0 新增)*
`router_register` `router_route` `router_health` `router_feedback` `router_reclassify`

### 索引器工具 (5) *(v0.2.0 新增)*
`indexer_status` `indexer_rebuild` `indexer_heartbeat` `indexer_circuit_reset` `indexer_model_update`

### 工具执行 (12)
`tool_run` `tool_chain` `tool_cache_get` `tool_cache_set` `tool_register` `tool_list` `tool_schema` `tool_version_pin` `tool_retry_policy` `tool_cost` `tool_sandbox_run` `tool_composio`

### 规划工具 (9)
`plan_create` `plan_revise` `plan_diff` `plan_evaluate` `plan_spar` `plan_decompose` `plan_constraints` `plan_rollback` `plan_template`

### 编排工具 (9)
`ctx_route` `ctx_trace` `ctx_schema_get` `ctx_schema_register` `ctx_cost_summary` `ctx_workspace_create` `ctx_workspace_list` `ctx_health` `ctx_version`

### 文档智能工具 (8)
`docs_search` `docs_get` `docs_get_file` `docs_annotate` `docs_annotate_clear` `docs_annotate_list` `docs_feedback` `docs_contribute`

---

## 智能体自改进闭环

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

## 路线图

### 阶段 1 — 吸收 *(已完成)*
- [x] 统一 MCP 工具模式
- [x] 带跨会话持久化的记忆层
- [x] 混合检索引擎
- [x] 带 DAG 执行的工具注册表
- [x] 带对练钩子的规划 + 规格引擎
- [x] Orchestration Core
- [x] 文档智能层（已吸收 context-hub）

### 阶段 1.5 — Cognition 更新 *(v0.2.0 — 当前)*
- [x] **Cognition 层**与 6 种认知原语
- [x] **Retrieval Router**与变更感知路由
- [x] **Index Lifecycle Manager**与自愈合
- [x] 带每源画像的数据源注册表
- [x] 上下文预算强制执行
- [x] 索引操作断路器
- [x] 嵌入模型漂移检测
- [x] 反馈驱动的变更重分类
- [ ] 生产集成（sentence-transformers、rank-bm25、tantivy）
- [ ] 认知原语的完整测试套件
- [ ] 基准：认知层对输出质量的影响

### 阶段 2 — 复合
- [ ] 检索反馈闭环（自动改进路由）
- [ ] 带关系查询的实体图
- [ ] 记忆冲突解决引擎
- [ ] 工具输出缓存层
- [ ] 结果评估 + 规格评分
- [ ] 用于规模的 PostgreSQL + pgvector 后端
- [ ] Docker 镜像 + docker-compose

### 阶段 3 — 平台
- [ ] ContextOS Cloud（托管、多租户）
- [ ] 可视化工作流构建器
- [ ] 工具模式市场
- [ ] 企业 SSO + 审计日志
- [ ] LangChain + CrewAI + AutoGen 适配器

---

## Cognition 层的起源

v0.2.0 的六种认知原语来自追踪实时问题解决对话中推理的真实运作方式，并在实践中为每个操作命名。

起点是 Cole Medin 在 LinkedIn 上的帖子「Is RAG Dead?」，配图将结构化数据（编码智能体放弃 RAG 之处）与非结构化数据（RAG 兴盛之处）分开。评论者指出两点：RAG 被与语义搜索混为一谈（可用 BM25 做 RAG），以及编码智能体使用 grep 的真正原因是每次切换分支都重新索引会毁掉开发者体验。

这一洞察——数据变更率 vs 索引成本——演化为 Retrieval Router。但更深层的问题是：检索与输出之间发生了什么却无人构建？答案是一组在对话本身中被隐式实践的认知原语：

- 每轮都在发生主动遗忘（丢弃帖子里无关细节）
- 深度校准自然发生（知道何时深入 vs 快速回应）
- 综合检测存在（有些问题需要推理而非检索）
- 未知未知感知浮现（评论者发现了 Cole 不知道自己存在的盲点）
- 建设性矛盾是核心洞察（Cole 同时主张 RAG 已死**且**智能体搜索是未来——这仍是 RAG）
- 在分析 ContextOS 代码库时出现上下文相关引力（关于「未经批准绝不暂停品牌」的 0.3 重要性记忆，在当前问题是暂停品牌活动时升至 0.95）

对话成了规格。每个原语在命名前已被实践。本节记录其起源。

---

## 贡献

欢迎为 **代码** 与 **文档** 提交 PR。准则见 [CONTRIBUTING.md](docs/CONTRIBUTING.md)。

在 [IASAWI](https://github.com/itallstartedwithaidea) 下构建 — It All Started With A Idea。

---

## 许可证

MIT — 见 [LICENSE](LICENSE)

---

## 引用

若在研究或生产中使用 ContextOS，请引用：

```
@software{contextos2026,
  title = {ContextOS: The Unified Context Intelligence Layer},
  author = {Williams, John and IASAWI Contributors},
  year = {2026},
  url = {https://github.com/itallstartedwithaidea/contextOS}
}
```

---

*怀着对所有先行仓库的敬意而构建。*
