# ContextOS

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [中文](README.zh.md) | [Nederlands](README.nl.md) | [Русский](README.ru.md) | [한국어](README.ko.md)

> **De uniforme contextintelligentielaag voor AI-agents.**  
> Eén pip-installatie. Elke capability. Niets ontbreekt.

[![PyPI version](https://badge.fury.io/py/contextos.svg)](https://badge.fury.io/py/contextos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![GitHub Stars](https://img.shields.io/github/stars/itallstartedwithaidea/contextOS?style=social)](https://github.com/itallstartedwithaidea/contextOS)

```
pip install contextos
```

---

## Wat is ContextOS?

ContextOS is de **besturingssysteemlaag voor AI-context** — één uniforme MCP-server en CLI die de mogelijkheden van zeven toonaangevende open-source repositories in het AI-agent- en contextbeheer-ecosysteem absorbeert, uitbreidt en overtreft.

Het is gebouwd omdat geen enkel project de volledige stack dekte. Elke bestaande tool was uitstekend in één ding en miste de rest. ContextOS brengt ze samen, vult elke kloof en voegt een orchestratielaag toe die nergens bestond.

**ContextOS is geen wrapper. Het is een platform.** Elke tool die je eerder gebruikte wordt een module die erbovenop draait.

---

## v0.2.0 — De Cognition-update

**De industrie bouwt: ophalen en dan genereren.**  
**ContextOS bouwt: ophalen, DENKEN en dan genereren.**

Elk agentframework op de markt slaat de belangrijkste stap over. Ze halen context op, proppen die in een prompt en genereren output. Het denken tussen ophalen en output — het deel waar een expert redeneert over tegenstrijdigheden, afwegingen maakt, ontbrekende informatie voelt en bepaalt hoe diep te gaan — dat deel bestaat nergens.

Tot nu.

v0.2.0 voegt drie nieuwe lagen en een framework toe dat modelleert hoe expertredenering werkelijk functioneert:

### De Cognition-laag — zes cognitieve primitieven

Dit zijn de redeneerbewerkingen tussen retrieval en generatie. Geen enkel agentframework heeft ze gebouwd.

| Primitief | Wat het doet | Waarom het telt |
|---|---|---|
| **Actief vergeten** | Laat opgehaalde context vallen die de outputkwaliteit vermindert | Meer context is niet altijd beter. 20 opgehaalde brokken waarvan er 3 ertoe doen maken ruis die het redeneren uit koers haalt. |
| **Diepte-calibratie van redeneren** | Schat hoeveel denken een probleem waard is voordat je rekenkracht inzet | Snel patroonherkennen en een tienstaps redeneerketen zijn allebei geldig — voor verschillende problemen. Agents moeten weten in welke situatie ze zitten. |
| **Synthese-detectie** | Bepaalt of de agent moet DENKEN over wat hij heeft of MEER moet HALEN | De hele industrie behandelt elke taak als een retrievalprobleem. Sommige taken zijn synthese, analogie of relationeel redeneren. Meer data schaadt ze. |
| **Onbekend-onbekend waarnemen** | Detecteert wanneer een hele CATEGORIE informatie ontbreekt | Bekende onbekenden zijn makkelijk. Onbekende onbekenden doden. «Ik wist niet dat Salesforce-data hier relevant was» is een andere foutmodus dan «ik heb de data van vandaag niet». |
| **Productieve contradictie** | Houdt conflicterende data als signaal vast in plaats van ze op te lossen | «Google Ads zegt conversies omhoog, CRM zegt pipeline vlak» — het antwoord is niet «kies één». De meetkloof IS de insight. |
| **Contextafhankelijke zwaartekracht** | Weegt geheugenbelang opnieuw op basis van de huidige vraag | Een herinnering over «nooit branded zonder goedkeuring» scoort laag op gelijkenis met een PMax-query maar verandert fundamenteel de aanbeveling. Statische belangrijkheidsscores missen dit. |

### De Retrieval Router — churn-bewuste routing

Het echte framework voor retrieval is niet «gestructureerd vs ongestructureerde data». Het is **datachurn vs indexeringkosten.**

Codebases veranderen elke keer dat je van branch wisselt — embedden maakt indexen direct verouderd. Juridische documenten veranderen per kwartaal — één keer embedden betaalt zich maandenlang uit. De Retrieval Router classificeert elke databron op hoe snel de onderliggende data verandert en kiest dan de passende retrievalstrategie.

| Churn-klasse | Voorbeelddata | Strategie | Waarom |
|---|---|---|---|
| **Live** | Zoekqueryrapporten, veilingdata, budgettempo | Directe API-pull, geen index | Elk gecached antwoord is al fout |
| **Warm** | Keywordlijsten, doelgroepsegmenten, advertentieteksten | BM25- of vectorindex met versheidklok | Verandert wekelijks; index is nuttig als hij vers is |
| **Cold** | Advertentiebeleid, accounthiërarchie, strategiedocumenten | Volledige vectorsearch, één keer embedden | Verandert hoogstens per kwartaal; investeer in diepe indexering |

De router controleert bij elke request de indexversheid. Als de index van een warme bron verouderd is, valt hij automatisch terug op live pull. Geen menselijke tussenkomst.

### De Index Lifecycle Manager — zelfherstellende indexen

Event-gedreven herindexering met circuitbreakers en embeddingmodel-drift-detectie.

- **Schrijf-getriggerde herindexering:** wanneer een MCP-server nieuwe data pusht, wordt de index automatisch herbouwd. Geen cronjobs. De datastroom IS de indexeringstrigger.
- **Embeddingmodel-drift-detectie:** update je embeddingmodel? Elke vectorindex is stilletjes ongeldig. De lifecycle manager vangt modelversiemismatches en triggert volledige rebuilds.
- **Schema-wijziging-quarantaine:** verandert de vorm van inkomende data, dan worden bestaande indexen in quarantaine gezet tot herbouw. Geen stilzwijgend foute resultaten.
- **Circuitbreakers:** faalt herindexering 3 keer achter elkaar, dan stopt het systeem met proberen en degradeert naar live pull. Alerts. Handmatige reset mogelijk.
- **Heartbeat-checks:** periodieke gezondheidsscans vangen verouderde indexen die niet door events werden getriggerd.

---

## Hoe het werkt: een advertentievoorbeeld

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

## Op de schouders van reuzen

ContextOS zou niet bestaan zonder het buitengewone werk van deze projecten. We erkennen en eren elk project formeel:

### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

**80,5k stars — TypeScript**  
De fundamentele standaard voor tool-uitvoering en contextprotocol. ContextOS adopteert MCP als nativeschema en is 100% compatibel met alle bestaande MCP-servers.  
**Wat het ons gaf:** het protocol. De standaard. Het ecosysteem.  
**Wat ontbrak:** geen orchestratielaag, geen geheugen, geen retrieval, geen planning — alleen het transportprotocol zelf.

---

### [infiniflow/ragflow](https://github.com/infiniflow/ragflow)

**74,4k stars — Python**  
Een productieklare RAG-engine met agentmogelijkheden en diepe documentparsing.  
**Wat het ons gaf:** de retrieval-engine, de document-ingest-pipeline, agent-bewuste RAG-uitvoering.  
**Wat ontbrak:** geen cross-laag geheugenintegratie, geen verouderingsdetectie, geen multi-corpus routing, geen feedbacklus, geen MCP-native toolschema.

---

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

**71,3k stars — MDX**  
Het definitieve corpus van promptengineering-patronen, papers en technieken.  
**Wat het ons gaf:** de plannings- en promptkennisbank die de spectemplates en agentinstructiepatronen van ContextOS voedt.  
**Wat ontbrak:** alleen statische documentatie — geen runtime-integratie, geen promptversiebeheer, geen outcometracking.

---

### [upstash/context7](https://github.com/upstash/context7)

**48,2k stars — TypeScript**  
Actuele codedocumentatie voor LLM’s en AI-code-editors.  
**Wat het ons gaf:** live documentatie ophalen, versiebewuste contextinjectie voor LLM’s.  
**Wat ontbrak:** geen geheugenlaag, geen retrieval-integratie, geen sessiecontinuïteit — puur stateless doc-fetching.

---

### [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)

**33,5k stars — TypeScript**  
Een Claude Code-plugin die codeersessies vastlegt en comprimeert met AI en SQLite + embeddings.  
**Wat het ons gaf:** het in-sessie geheugencompressiepatroon, de SQLite + embeddings-architectuur.  
**Wat ontbrak:** geheugen sterft met de sessie. Geen cross-sessie persistentie, geen entiteitsgraaf, geen tiering, geen conflictresolutie.

---

### [ComposioHQ/composio](https://github.com/ComposioHQ/composio)

**27,3k stars — TypeScript**  
Voedt 1000+ toolkits met auth, toolzoekfunctie en een gesandboxte werkbank voor AI-agents.  
**Wat het ons gaf:** de externe API-integratielaag — OAuth-flows, tool-sandboxing, uitvoeringscontext.  
**Wat ontbrak:** geen tool-DAG-uitvoering, geen outputcaching, geen retry/fallback-beleid, geen toolversiebeheer.

---

### [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)

**26,5k stars — JavaScript**  
Een lichtgewicht meta-prompting- en spec-gedreven ontwikkelsysteem voor Claude Code.  
**Wat het ons gaf:** het spec-gedreven uitvoeringsmodel, meta-promptingpatronen, taakdecompositietemplates.  
**Wat ontbrak:** geen dynamische planrevisie, geen constraintpropagatie, geen specversiebeheer, geen outcome-evaluatielus.

---

### [andrewyng/context-hub](https://github.com/andrewyng/context-hub)

**47 stars — JavaScript**  
Een gecureerde, versioned doc store met een CLI (`chub`) voor codeeragents.  
**Wat het ons gaf:** het doc-intelligentiepatroon: gecureerde content + incrementele fetch + lokale annotaties + communityfeedbacklussen.  
**Wat ontbrak:** geen geheugenlaag, geen retrieval-integratie, geen MCP-toolschema, geen Python-ondersteuning.

> **ContextOS absorbeert context-hub volledig.** Elk `chub`-commando mapt naar een `ctx docs`-commando.

---

## Wat ontbrak — en wat ContextOS bouwt

Na absorptie van alle zeven projecten waren dit de hiaten die geen enkele repo alleen adresseed:

### Orchestration Core *(volledig nieuw)*

| Feature | Waarom het telt |
|---|---|
| **Semantische intent-router** | Classificeert elk inkomend verzoek en dispatcht automatisch naar de juiste laag. |
| **Request tracing / observability** | Volledige lineage per toolcall: welke laag vuurde, latency, tokencost, kwaliteitsscore. |
| **Schema Registry** | Versioned toolschemas met backward compatibility. |
| **Multi-workspace auth** | API-keys, rate limits en auditlogs per workspace. |
| **Cost Ledger** | Volg LLM- + API-uitgaven per sessie, workspace en tool. |

### Cognition-laag *(volledig nieuw in v0.2.0)*

| Feature | Waarom het telt |
|---|---|
| **Actief vergeten** | Laat opgehaalde context vallen die ruis maakt. Meer is niet beter. |
| **Diepte-calibratie van redeneren** | Weten hoeveel denken een probleem waard is voordat je rekenkracht investeert. |
| **Synthese-detectie** | Retrievaltaken onderscheiden van redeneertaken. |
| **Onbekend-onbekend waarnemen** | Ontbrekende informatiecategorieën detecteren, niet alleen ontbrekende feiten. |
| **Productieve contradictie** | Conflicterende signalen vasthouden als insight in plaats van tot één antwoord te reduceren. |
| **Contextafhankelijke zwaartekracht** | Geheugen opnieuw wegen naar de huidige vraag. Constraints overrulen gelijkenisscores. |
| **Contextbudget** | Tokenlimieten op opgehaalde context afdwingen. Karpathy’s «Context Window = RAM» operationeel gemaakt. |

### Retrieval Router *(volledig nieuw in v0.2.0)*

| Feature | Waarom het telt |
|---|---|
| **Data Source Registry** | Elke MCP-server declareert zijn churnprofiel, indexstrategie en versheiddrempel. |
| **Churn-bewuste routing** | Live/warm/cold-classificatie per bron. Strategie matcht datavolatiliteit. |
| **Automatische fallback** | Verouderde index? Terugval op live pull. Geen handmatige tussenkomst. |
| **Feedback-gedreven herclassificatie** | Als een «cold»-bron steeds veroudert, promoot het systeem hem automatisch naar «warm». |

### Index Lifecycle Manager *(volledig nieuw in v0.2.0)*

| Feature | Waarom het telt |
|---|---|
| **Event-gedreven herindexering** | MCP-data-events triggeren rebuilds. Geen cronjobs. |
| **Embeddingmodel-drift-detectie** | Modelupdate = alle vectorindexen ongeldig. Automatisch gedetecteerd en herbouwd. |
| **Schema-wijziging-quarantaine** | Verandert de datavorm? Index in quarantaine tot herbouw. |
| **Circuitbreakers** | 3 opeenvolgende indexfalen = degradatie naar live pull + alert. |
| **Heartbeat-gezondheidschecks** | Periodieke scans vangen wat events misten. |

### Geheugenlaag *(breidt claude-mem uit)*

| Feature | Waarom het telt |
|---|---|
| **Cross-sessie persistentie** | Geheugen overleeft procesherstarts. |
| **Geheugen-tiering (Hot/Warm/Cold)** | Auto-promotie/demotie op recency + relevantie. |
| **Entiteitsgraaf** | Extraheert entiteiten en koppelt ze als gestructureerde kennis. |
| **Conflictresolutie** | Lost tegenstrijdige geheugenbronnen op met timestamp + confidence. |
| **User-scoped vs agent-scoped geheugen** | Wat de gebruiker het systeem vertelde vs wat agents leerden — gescheiden. |

### Retrieval-laag *(breidt ragflow + context7 uit)*

| Feature | Waarom het telt |
|---|---|
| **Hybrid Search** | BM25-keyword + dense vectorsearch gecombineerd. |
| **Source Attribution Scoring** | Rangschikt brokken op provenancekwaliteit, niet alleen cosinusgelijkenis. |
| **Staleness Detection** | Markeert content ouder dan configureerbare TTL en triggert re-fetch. |
| **Multi-Corpus Routing** | Routeert queries parallel naar docs, live web, codebase of API-spec. |
| **Retrieval Feedback Loop** | Volgt welke brokken in de uiteindelijke output zaten. Routing verbetert over tijd. |

### Tool Execution-laag *(breidt composio + MCP servers uit)*

| Feature | Waarom het telt |
|---|---|
| **Tool Chaining / DAG Execution** | Multi-step toolpipelines met vertakkingslogica. |
| **Sandboxed Code Execution** | Veilige uitvoer met output capture en error recovery. |
| **Tool Output Caching** | Cache deterministische resultaten op input-hash. |
| **Retry + Fallback Policies** | Per-tool SLA: retry budget, fallback tool, graceful degradation. |
| **Tool Versioning** | Pin agentworkflows op specifieke toolversies. |

### Planning & Spec-laag *(breidt GSD + Prompt-Engineering-Guide uit)*

| Feature | Waarom het telt |
|---|---|
| **Dynamic Plan Revision** | Plannen updaten midden in uitvoering op basis van tooloutput. |
| **Constraint Propagation** | Als tool X faalt, worden downstream stappen automatisch herzien. |
| **Spec Versioning + Diff** | Volg hoe taakspecs evolueren. Rollback als nieuwe spec onderpresteert. |
| **Pre-Response Sparring Hook** | Verplichte reflectie vóór elke agentoutput. Pauzeert vóór het vuren. |
| **Outcome Evaluation** | Scoret uiteindelijke output tegen oorspronkelijke spec. Voedt signaal terug naar planning. |

### Doc Intelligence-laag *(absorbeert context-hub volledig)*

| Feature | Waarom het telt |
|---|---|
| **Curated Doc Registry** | Community-onderhouden, versioned markdown-docs voor API’s, frameworks en tools. |
| **Language-Specific Fetch** | Haal docs op in je doeltaal. Geen irrelevante snippets. |
| **Incremental Fetch** | Haal alleen op wat je nodig hebt. Geen verspilde tokens. |
| **Persistent Annotations** | Lokale notities die agents aan docs hangen. Overleven sessieherstarts. |
| **Community Feedback Loop** | Up/downvotes per doc stromen terug naar maintainers. |
| **Doc Staleness Scoring** | Verouderde docs worden gemarkeerd en automatisch opnieuw opgehaald. |

---

## Architectuur

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

**De kritieke datastroom (v0.2.0):**

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

## Quick Start

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

### Dataregistreren

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

### Een Cognition-pass uitvoeren

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

## CLI: `ctx`

### Doc-commando’s *(context-hub-pariteit + extensies)*

```bash
ctx docs search openai                     # find available docs
ctx docs get openai/chat --lang py         # fetch current docs, Python variant
ctx docs get stripe/api --file webhooks    # incremental fetch
ctx docs annotate stripe/api "Note here"   # attach a persistent note
ctx docs feedback stripe/api up            # upvote a doc
```

### Geheugencommando’s

```bash
ctx memory store "key insight about X"
ctx memory retrieve "what do I know about stripe webhooks"
ctx memory forget "session notes from project Y"
ctx memory graph query "entity:OpenAI"
ctx memory conflicts --resolve auto
```

### Retrieval-commando’s

```bash
ctx retrieve docs "stripe payment intents python"
ctx retrieve live "openai assistants api latest"
ctx retrieve web "LLM context window best practices 2026"
ctx retrieve code "webhook verification pattern"
```

### Router-commando’s *(nieuw in v0.2.0)*

```bash
ctx router register --name google_ads --churn live --index none
ctx router register --name policies --churn cold --index vector
ctx router health                          # index health across all sources
ctx router route "what queries triggered ads today"  # show routing decision
```

### Cognition-commando’s *(nieuw in v0.2.0)*

```bash
ctx cognition think --query "should I pause branded" --domain advertising
ctx cognition budget --tokens 4000         # set context budget
ctx cognition contradictions --last        # show last detected contradictions
ctx cognition unknowns --last              # show unknown-unknown alerts
```

### Planningscommando’s

```bash
ctx plan create "build a stripe checkout integration"
ctx plan spar                              # pre-response sparring hook
ctx plan revise --feedback "tool X failed"
ctx plan evaluate --against-spec spec.md
```

### Orchestratiecommando’s

```bash
ctx health                                 # all 8 layers
ctx cost summary --workspace my-agent
ctx trace --id req_abc123
```

---

## Blootgestelde MCP-tools

ContextOS blootstelt **67 tools** in 8 categorieën via het MCP-protocol.

### Geheugentools (9)
`memory_store` `memory_retrieve` `memory_forget` `memory_summarize` `memory_diff` `memory_graph_query` `memory_export` `memory_import` `memory_conflicts`

### Retrieval-tools (8)
`retrieve_docs` `retrieve_live` `retrieve_web` `retrieve_code` `retrieve_merge` `retrieve_score` `retrieve_feedback` `retrieve_staleness`

### Cognition-tools (6) *(nieuw in v0.2.0)*
`cognition_think` `cognition_forget` `cognition_depth` `cognition_contradictions` `cognition_unknowns` `cognition_gravity`

### Router-tools (5) *(nieuw in v0.2.0)*
`router_register` `router_route` `router_health` `router_feedback` `router_reclassify`

### Indexer-tools (5) *(nieuw in v0.2.0)*
`indexer_status` `indexer_rebuild` `indexer_heartbeat` `indexer_circuit_reset` `indexer_model_update`

### Tool Execution (12)
`tool_run` `tool_chain` `tool_cache_get` `tool_cache_set` `tool_register` `tool_list` `tool_schema` `tool_version_pin` `tool_retry_policy` `tool_cost` `tool_sandbox_run` `tool_composio`

### Planning-tools (9)
`plan_create` `plan_revise` `plan_diff` `plan_evaluate` `plan_spar` `plan_decompose` `plan_constraints` `plan_rollback` `plan_template`

### Orchestratie-tools (9)
`ctx_route` `ctx_trace` `ctx_schema_get` `ctx_schema_register` `ctx_cost_summary` `ctx_workspace_create` `ctx_workspace_list` `ctx_health` `ctx_version`

### Doc Intelligence-tools (8)
`docs_search` `docs_get` `docs_get_file` `docs_annotate` `docs_annotate_clear` `docs_annotate_list` `docs_feedback` `docs_contribute`

---

## Agent self-improvement loop

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

## Roadmap

### Fase 1 — Absorberen *(afgerond)*
- [x] Uniform MCP-toolschema
- [x] Geheugenlaag met cross-sessie persistentie
- [x] Hybrid retrieval-engine
- [x] Toolregistry met DAG-uitvoering
- [x] Planning + spec-engine met sparring hook
- [x] Orchestration Core
- [x] Doc intelligence-laag (context-hub geabsorbeerd)

### Fase 1.5 — Cognition-update *(v0.2.0 — huidig)*
- [x] **Cognition-laag** met 6 cognitieve primitieven
- [x] **Retrieval Router** met churn-bewuste routing
- [x] **Index Lifecycle Manager** met zelfherstellend gedrag
- [x] Data Source Registry met profielen per bron
- [x] Contextbudget-afhandhaving
- [x] Circuitbreakers voor indexoperaties
- [x] Embeddingmodel-drift-detectie
- [x] Feedback-gedreven churn-herclassificatie
- [ ] Productie-integraties (sentence-transformers, rank-bm25, tantivy)
- [ ] Volledige testsuite voor cognition-primitieven
- [ ] Benchmark: impact van cognition-laag op outputkwaliteit

### Fase 2 — Compound
- [ ] Retrieval feedback loop (verbetert routing automatisch)
- [ ] Entiteitsgraaf met relatiequeries
- [ ] Geheugenconflictresolutie-engine
- [ ] Tool output caching-laag
- [ ] Outcome evaluation + spec scoring
- [ ] PostgreSQL + pgvector-backend voor schaal
- [ ] Docker image + docker-compose

### Fase 3 — Platform
- [ ] ContextOS Cloud (gehost, multi-tenant)
- [ ] Visuele workflow builder
- [ ] Marketplace voor toolschemas
- [ ] Enterprise SSO + auditlogs
- [ ] LangChain + CrewAI + AutoGen adapters

---

## De oorsprong van de Cognition-laag

De zes cognitieve primitieven in v0.2.0 zijn geïdentificeerd door te traceren hoe redenering werkelijk verloopt in een live probleemoplossingsgesprek, en elke bewerking te benoemen zoals die werd uitgevoerd.

Het startpunt was een LinkedIn-post van Cole Medin met de vraag «Is RAG Dead?» en een diagram dat gestructureerde data (waar RAG door codeeragents werd verlaten) scheidde van ongestructureerde data (waar RAG bloeit). Een reageerder wees op twee dingen: RAG werd verward met semantische zoeken (je kunt RAG met BM25 doen), en de echte reden dat codeeragents grep gebruiken is dat herindexeren bij elke branch-checkout de developer experience doodt.

Dat inzicht — datachurn vs indexeringkosten — werd de Retrieval Router. Maar er kwam een diepere vraam: wat gebeurt er tussen retrieval en output dat niemand bouwt? Het antwoord was een set cognitieve primitieven die impliciet in het gesprek zelf werden uitgevoerd:

- Actief vergeten gebeurde elke beurt (irrelevante details uit de post laten vallen)
- Diepte-calibratie gebeurde vanzelf (weten wanneer diep te gaan vs een snelle take)
- Synthese-detectie was aanwezig (sommige vragen vroegen om redenering, niet retrieval)
- Onbekend-onbekend waarnemen kwam boven (de reageerder vond een blinde vlek die Cole niet wist te bestaan)
- Productieve contradictie was de kerninzicht (Cole beargumenteerde tegelijk dat RAG dood is EN dat agentic search de toekomst is — wat RAG is)
- Contextafhankelijke zwaartekracht verscheen bij het analyseren van de ContextOS-codebase (een geheugen met belang 0,3 over «nooit branded pauzeren» werd 0,95 toen de huidige vraag ging over branded campagnes pauzeren)

Het gesprek werd de spec. Elke primitief werd geoefend voordat hij werd benoemd. Deze sectie bestaat als verslag van die oorsprong.

---

## Bijdragen

PR’s zijn welkom voor zowel **code** als **docs**. Zie [CONTRIBUTING.md](docs/CONTRIBUTING.md) voor richtlijnen.

Gebouwd onder [IASAWI](https://github.com/itallstartedwithaidea) — It All Started With A Idea.

---

## Licentie

MIT — zie [LICENSE](LICENSE)

---

## Citeren

Als je ContextOS in onderzoek of productie gebruikt, citeer dan:

```
@software{contextos2026,
  title = {ContextOS: The Unified Context Intelligence Layer},
  author = {Williams, John and IASAWI Contributors},
  year = {2026},
  url = {https://github.com/itallstartedwithaidea/contextOS}
}
```

---

*Gebouwd met respect voor elke repo die eraan voorafging.*
