# ContextOS

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [中文](README.zh.md) | [Nederlands](README.nl.md) | [Русский](README.ru.md) | [한국어](README.ko.md)

> **La capa unificada de inteligencia de contexto para agentes de IA.**  
> Un solo `pip install`. Todas las capacidades. Nada falta.

[![PyPI version](https://badge.fury.io/py/contextos.svg)](https://badge.fury.io/py/contextos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![GitHub Stars](https://img.shields.io/github/stars/itallstartedwithaidea/contextOS?style=social)](https://github.com/itallstartedwithaidea/contextOS)

```
pip install contextos
```

---

## ¿Qué es ContextOS?

ContextOS es la **capa de sistema operativo para el contexto de la IA**: un único servidor MCP y CLI unificados que absorben, amplían y superan las capacidades de siete repositorios líderes de código abierto en el ecosistema de agentes de IA y gestión del contexto.

Se construyó porque ningún proyecto cubría toda la pila. Cada herramienta existente destacaba en una cosa y carecía del resto. ContextOS las reúne, cierra cada brecha y añade una capa de orquestación que no existía en ningún sitio.

**ContextOS no es un envoltorio. Es una plataforma.** Cada herramienta que usabas antes se convierte en un módulo que se ejecuta encima.

---

## v0.2.0 — La actualización Cognition

**La industria construye: recuperar y luego generar.**  
**ContextOS construye: recuperar, PENSAR y luego generar.**

Todos los frameworks de agentes del mercado omiten el paso más importante. Recuperan contexto, lo meten en un prompt y generan salida. El pensamiento entre la recuperación y la salida —donde un experto razona sobre contradicciones, pondera restricciones, intuye información faltante y decide qué profundidad merece el problema— esa parte no existe en ningún sitio.

Hasta ahora.

La v0.2.0 añade tres capas nuevas y un marco que modela cómo funciona realmente el razonamiento experto:

### La capa Cognition — seis primitivas cognitivas

Son las operaciones de razonamiento que ocurren entre la recuperación y la generación. Ningún framework de agentes las ha construido.

| Primitiva | Qué hace | Por qué importa |
|---|---|---|
| **Olvido activo** | Descarta contexto recuperado que degrada la calidad de salida | Más contexto no siempre es mejor. 20 fragmentos recuperados donde solo importan 3 generan ruido que desvía el razonamiento. |
| **Calibración de profundidad de razonamiento** | Estima cuánto pensar merece un problema antes de gastar cómputo | Un emparejamiento rápido de patrones y una cadena de razonamiento de 10 pasos son ambos válidos —para problemas distintos. Los agentes deberían saber en qué situación están. |
| **Detección de síntesis** | Determina si el agente debe PENSAR en lo que tiene o IR A BUSCAR más | Toda la industria trata cada tarea como un problema de recuperación. Algunas tareas son síntesis, analogía o razonamiento relacional. Más datos las perjudican. |
| **Sensado de desconocidos desconocidos** | Detecta cuando falta una CATEGORÍA entera de información | Los conocidos desconocidos son fáciles. Los desconocidos desconocidos matan. «No sabía que los datos de Salesforce eran relevantes aquí» es un modo de fallo distinto de «no tengo los datos de hoy». |
| **Contradicción productiva** | Mantiene datos en conflicto como señal en lugar de resolverlos | «Google Ads dice conversiones arriba, el CRM dice pipeline plano» —la respuesta no es «elegir uno». La brecha de medición ES el insight. |
| **Gravedad dependiente del contexto** | Repondera la importancia de la memoria según la pregunta actual | Un recuerdo sobre «nunca lanzar branded sin aprobación» puntúa bajo en similitud con una consulta PMax pero cambia por completo la recomendación. Las puntuaciones de importancia estáticas pierden esto. |

### El enrutador de recuperación — enrutamiento consciente del churn

El marco real de recuperación no es «datos estructurados frente a no estructurados». Es **tasa de rotación de datos frente a coste de indexación.**

Las bases de código cambian cada vez que cambias de rama —incrustarlas crea índices obsoletos al instante. Los documentos legales cambian trimestralmente —incrustarlos una vez compensa durante meses. El Retrieval Router clasifica cada fuente de datos por qué tan rápido cambian los datos subyacentes y luego elige la estrategia de recuperación adecuada.

| Clase de churn | Datos de ejemplo | Estrategia | Por qué |
|---|---|---|---|
| **Live** | Informes de consultas de búsqueda, datos de subasta, ritmo del presupuesto | Pull directo por API, sin índice | Cualquier respuesta en caché ya es incorrecta |
| **Warm** | Listas de palabras clave, segmentos de audiencia, inventario de textos de anuncio | Índice BM25 o vectorial con reloj de frescura | Cambia semanalmente; el índice sirve si está fresco |
| **Cold** | Políticas de anuncios, jerarquía de cuenta, documentos de estrategia | Búsqueda vectorial completa, embed una vez | Cambia como mucho trimestralmente; merece indexación profunda |

El enrutador comprueba la frescura del índice en cada petición. Si el índice de una fuente «warm» está obsoleto, hace fallback automático a pull en vivo. Sin intervención humana.

### El gestor del ciclo de vida del índice — índices auto-reparadores

Reindexación dirigida por eventos, con disyuntores y detección de deriva del modelo de embedding.

- **Reindexación disparada por escritura:** cuando un servidor MCP envía datos nuevos, el índice se reconstruye solo. Sin cron. El flujo de datos ES el disparador de indexación.
- **Detección de deriva del modelo de embedding:** ¿actualizas tu modelo de embedding? Cada índice vectorial queda inválido en silencio. El gestor del ciclo de vida detecta discrepancias de versión de modelo y dispara reconstrucciones completas.
- **Cuarentena por cambio de esquema:** si cambia la forma de los datos entrantes, los índices existentes quedan en cuarentena hasta reconstruirse. Sin resultados silenciosamente incorrectos.
- **Disyuntores:** si la reindexación falla 3 veces seguidas, el sistema deja de intentar y se degrada a pull en vivo. Alertas. Reinicio manual disponible.
- **Comprobaciones de latido:** exploraciones periódicas de salud detectan índices obsoletos no disparados por eventos.

---

## Cómo funciona: un ejemplo de publicidad

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

## Sobre los hombros de gigantes

ContextOS no existiría sin el trabajo extraordinario de estos proyectos. Acreditamos y honramos formalmente a cada uno:

### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

**80,5k stars — TypeScript**  
El estándar fundacional para ejecución de herramientas y protocolo de contexto. ContextOS adopta MCP como esquema nativo y es 100% compatible con todos los servidores MCP existentes.  
**Lo que nos dio:** el protocolo. El estándar. El ecosistema.  
**Lo que faltaba:** sin capa de orquestación, sin memoria, sin recuperación, sin planificación —solo el protocolo de transporte.

---

### [infiniflow/ragflow](https://github.com/infiniflow/ragflow)

**74,4k stars — Python**  
Motor RAG de grado producción con capacidades de agente y análisis profundo de documentos.  
**Lo que nos dio:** el motor de recuperación, el pipeline de ingesta, la ejecución RAG consciente del agente.  
**Lo que faltaba:** sin integración de memoria entre capas, sin detección de obsolescencia, sin enrutamiento multi-corpus, sin bucle de feedback, sin esquema de herramientas nativo MCP.

---

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

**71,3k stars — MDX**  
El corpus definitivo de patrones, papers y técnicas de prompt engineering.  
**Lo que nos dio:** la base de conocimiento de planificación y prompting que alimenta las plantillas de spec y los patrones de instrucción de agentes en ContextOS.  
**Lo que faltaba:** solo documentación estática —sin integración en runtime, sin versionado de prompts, sin seguimiento de resultados.

---

### [upstash/context7](https://github.com/upstash/context7)

**48,2k stars — TypeScript**  
Documentación de código actualizada para LLM y editores de código con IA.  
**Lo que nos dio:** obtención de documentación en vivo, inyección de contexto consciente de versión para LLM.  
**Lo que faltaba:** sin capa de memoria, sin integración de recuperación, sin continuidad de sesión —solo obtención de docs sin estado.

---

### [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)

**33,5k stars — TypeScript**  
Plugin de Claude Code que captura y comprime sesiones de código con IA y SQLite + embeddings.  
**Lo que nos dio:** el patrón de compresión de memoria en sesión, la arquitectura SQLite + embeddings.  
**Lo que faltaba:** la memoria muere con la sesión. Sin persistencia entre sesiones, sin grafo de entidades, sin niveles, sin resolución de conflictos.

---

### [ComposioHQ/composio](https://github.com/ComposioHQ/composio)

**27,3k stars — TypeScript**  
Impulsa más de 1000 toolkits con auth, búsqueda de herramientas y un banco de trabajo aislado para construir agentes de IA.  
**Lo que nos dio:** la capa de integración de API externas —flujos OAuth, sandboxing de herramientas, contexto de ejecución.  
**Lo que faltaba:** sin ejecución DAG de herramientas, sin caché de salidas, sin políticas de reintento/fallback, sin versionado de herramientas.

---

### [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)

**26,5k stars — JavaScript**  
Sistema ligero de meta-prompting y desarrollo guiado por specs para Claude Code.  
**Lo que nos dio:** el modelo de ejecución guiado por spec, patrones de meta-prompting, plantillas de descomposición de tareas.  
**Lo que faltaba:** sin revisión dinámica de planes, sin propagación de restricciones, sin versionado de specs, sin bucle de evaluación de resultados.

---

### [andrewyng/context-hub](https://github.com/andrewyng/context-hub)

**47 stars — JavaScript**  
Almacén de documentos curados y versionados con una CLI (`chub`) para agentes de código.  
**Lo que nos dio:** el patrón de inteligencia documental: contenido curado + fetch incremental + anotaciones locales + bucles de feedback comunitario.  
**Lo que faltaba:** sin capa de memoria, sin integración de recuperación, sin esquema de herramientas MCP, sin soporte Python.

> **ContextOS absorbe context-hub por completo.** Cada comando `chub` se mapea a un comando `ctx docs`.

---

## Qué faltaba — y qué construye ContextOS

Tras absorber los siete proyectos, estos eran los huecos que ningún repo abordaba solo:

### Núcleo de orquestación *(totalmente nuevo)*

| Característica | Por qué importa |
|---|---|
| **Enrutador de intención semántica** | Clasifica cada petición entrante y despacha a la capa correcta automáticamente. |
| **Trazado de peticiones / observabilidad** | Linaje completo por llamada a herramienta: qué capa actuó, latencia, coste en tokens, puntuación de calidad. |
| **Registro de esquemas** | Esquemas de herramientas versionados con compatibilidad hacia atrás. |
| **Auth multi-workspace** | Claves API por workspace, límites de tasa y registros de auditoría. |
| **Libro mayor de costes** | Seguimiento del gasto LLM + API por sesión, workspace y herramienta. |

### Capa Cognition *(totalmente nueva en v0.2.0)*

| Característica | Por qué importa |
|---|---|
| **Olvido activo** | Descarta contexto recuperado que genera ruido. Más no es mejor. |
| **Calibración de profundidad de razonamiento** | Saber cuánto pensar merece un problema antes de invertir cómputo. |
| **Detección de síntesis** | Distinguir tareas de recuperación de tareas de razonamiento. |
| **Sensado de desconocidos desconocidos** | Detectar categorías faltantes de información, no solo hechos faltantes. |
| **Contradicción productiva** | Mantener señales en conflicto como insight en lugar de resolver a una sola respuesta. |
| **Gravedad dependiente del contexto** | Reponderar la memoria según la pregunta actual. Las restricciones superan las puntuaciones de similitud. |
| **Presupuesto de contexto** | Aplicar límites de tokens al contexto recuperado. El «Context Window = RAM» de Karpathy hecho operativo. |

### Enrutador de recuperación *(totalmente nuevo en v0.2.0)*

| Característica | Por qué importa |
|---|---|
| **Registro de fuentes de datos** | Cada servidor MCP declara su perfil de churn, estrategia de índice y umbral de frescura. |
| **Enrutamiento consciente del churn** | Clasificación live/warm/cold por fuente. La estrategia sigue la volatilidad de los datos. |
| **Fallback automático** | ¿Índice obsoleto? Fallback a pull en vivo. Sin intervención manual. |
| **Reclasificación guiada por feedback** | Si una fuente «cold» sigue quedando obsoleta, el sistema la promueve automáticamente a «warm». |

### Gestor del ciclo de vida del índice *(totalmente nuevo en v0.2.0)*

| Característica | Por qué importa |
|---|---|
| **Reindexación dirigida por eventos** | Los eventos de datos MCP disparan reconstrucciones. Sin cron. |
| **Detección de deriva del modelo de embedding** | Actualización del modelo = todos los índices vectoriales inválidos. Detectado y reconstruido automáticamente. |
| **Cuarentena por cambio de esquema** | ¿Cambia la forma de los datos? Índice en cuarentena hasta reconstruir. |
| **Disyuntores** | 3 fallos de índice consecutivos = degradación a pull en vivo + alerta. |
| **Comprobaciones de salud por latido** | Exploraciones periódicas capturan lo que los eventos no dispararon. |

### Capa de memoria *(extiende claude-mem)*

| Característica | Por qué importa |
|---|---|
| **Persistencia entre sesiones** | La memoria sobrevive a reinicios de proceso. |
| **Niveles de memoria (Hot/Warm/Cold)** | Promoción/degradación automática por recencia + relevancia. |
| **Grafo de entidades** | Extrae entidades y las enlaza como conocimiento estructurado. |
| **Resolución de conflictos** | Resuelve fuentes de memoria contradictorias usando marca temporal + confianza. |
| **Memoria por usuario vs por agente** | Lo que el usuario dijo al sistema frente a lo que aprendieron los agentes —separado. |

### Capa de recuperación *(extiende ragflow + context7)*

| Característica | Por qué importa |
|---|---|
| **Búsqueda híbrida** | BM25 por palabras clave + búsqueda vectorial densa combinadas. |
| **Puntuación de atribución de fuente** | Ordena fragmentos por calidad de procedencia, no solo similitud coseno. |
| **Detección de obsolescencia** | Marca contenido más viejo que un TTL configurable y dispara re-fetch. |
| **Enrutamiento multi-corpus** | Enruta consultas a docs, web en vivo, base de código o spec de API —en paralelo. |
| **Bucle de feedback de recuperación** | Rastrea qué fragmentos aparecieron en la salida final. El enrutamiento mejora con el tiempo. |

### Capa de ejecución de herramientas *(extiende composio + servidores MCP)*

| Característica | Por qué importa |
|---|---|
| **Encadenamiento de herramientas / ejecución DAG** | Pipelines multi-paso con lógica de ramificación. |
| **Ejecución de código en sandbox** | Ejecución segura con captura de salida y recuperación de errores. |
| **Caché de salida de herramientas** | Cachea resultados deterministas por hash de entrada. |
| **Políticas de reintento + fallback** | SLA por herramienta: presupuesto de reintento, herramienta alternativa, degradación elegante. |
| **Versionado de herramientas** | Fija flujos de agente a versiones concretas de herramientas. |

### Capa de planificación y spec *(extiende GSD + Prompt-Engineering-Guide)*

| Característica | Por qué importa |
|---|---|
| **Revisión dinámica del plan** | Los planes se actualizan a mitad de ejecución según la salida de herramientas. |
| **Propagación de restricciones** | Si la herramienta X falla, los pasos posteriores se revisan automáticamente. |
| **Versionado de spec + diff** | Rastrea cómo evolucionan las specs de tarea. Revierte si la nueva spec rinde peor. |
| **Hook de sparring pre-respuesta** | Reflexión obligatoria antes de cualquier salida del agente. Obliga a pausar antes de actuar. |
| **Evaluación de resultados** | Puntúa la salida final frente a la spec original. Devuelve señal a la planificación. |

### Capa de inteligencia documental *(absorbe context-hub por completo)*

| Característica | Por qué importa |
|---|---|
| **Registro de docs curados** | Markdown versionado mantenido por la comunidad para APIs, frameworks y herramientas. |
| **Fetch específico de lenguaje** | Obtiene docs en tu idioma objetivo. Sin fragmentos irrelevantes. |
| **Fetch incremental** | Obtiene solo lo necesario. Sin tokens desperdiciados. |
| **Anotaciones persistentes** | Notas locales que los agentes adjuntan a los docs. Sobreviven a reinicios de sesión. |
| **Bucle de feedback comunitario** | Votos arriba/abajo por doc vuelven a los mantenedores. |
| **Puntuación de obsolescencia de docs** | Los docs obsoletos se marcan y se vuelven a obtener automáticamente. |

---

## Arquitectura

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

**Flujo de datos crítico (v0.2.0):**

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

## Inicio rápido

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

### Registrar fuentes de datos

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

### Ejecutar un pase de Cognition

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

### Comandos de docs *(paridad context-hub + extensiones)*

```bash
ctx docs search openai                     # find available docs
ctx docs get openai/chat --lang py         # fetch current docs, Python variant
ctx docs get stripe/api --file webhooks    # incremental fetch
ctx docs annotate stripe/api "Note here"   # attach a persistent note
ctx docs feedback stripe/api up            # upvote a doc
```

### Comandos de memoria

```bash
ctx memory store "key insight about X"
ctx memory retrieve "what do I know about stripe webhooks"
ctx memory forget "session notes from project Y"
ctx memory graph query "entity:OpenAI"
ctx memory conflicts --resolve auto
```

### Comandos de recuperación

```bash
ctx retrieve docs "stripe payment intents python"
ctx retrieve live "openai assistants api latest"
ctx retrieve web "LLM context window best practices 2026"
ctx retrieve code "webhook verification pattern"
```

### Comandos del enrutador *(nuevo en v0.2.0)*

```bash
ctx router register --name google_ads --churn live --index none
ctx router register --name policies --churn cold --index vector
ctx router health                          # index health across all sources
ctx router route "what queries triggered ads today"  # show routing decision
```

### Comandos de cognition *(nuevo en v0.2.0)*

```bash
ctx cognition think --query "should I pause branded" --domain advertising
ctx cognition budget --tokens 4000         # set context budget
ctx cognition contradictions --last        # show last detected contradictions
ctx cognition unknowns --last              # show unknown-unknown alerts
```

### Comandos de planificación

```bash
ctx plan create "build a stripe checkout integration"
ctx plan spar                              # pre-response sparring hook
ctx plan revise --feedback "tool X failed"
ctx plan evaluate --against-spec spec.md
```

### Comandos de orquestación

```bash
ctx health                                 # all 8 layers
ctx cost summary --workspace my-agent
ctx trace --id req_abc123
```

---

## Herramientas MCP expuestas

ContextOS expone **67 herramientas** en 8 categorías vía el protocolo MCP.

### Herramientas de memoria (9)
`memory_store` `memory_retrieve` `memory_forget` `memory_summarize` `memory_diff` `memory_graph_query` `memory_export` `memory_import` `memory_conflicts`

### Herramientas de recuperación (8)
`retrieve_docs` `retrieve_live` `retrieve_web` `retrieve_code` `retrieve_merge` `retrieve_score` `retrieve_feedback` `retrieve_staleness`

### Herramientas de cognition (6) *(nuevo en v0.2.0)*
`cognition_think` `cognition_forget` `cognition_depth` `cognition_contradictions` `cognition_unknowns` `cognition_gravity`

### Herramientas del enrutador (5) *(nuevo en v0.2.0)*
`router_register` `router_route` `router_health` `router_feedback` `router_reclassify`

### Herramientas del indexador (5) *(nuevo en v0.2.0)*
`indexer_status` `indexer_rebuild` `indexer_heartbeat` `indexer_circuit_reset` `indexer_model_update`

### Ejecución de herramientas (12)
`tool_run` `tool_chain` `tool_cache_get` `tool_cache_set` `tool_register` `tool_list` `tool_schema` `tool_version_pin` `tool_retry_policy` `tool_cost` `tool_sandbox_run` `tool_composio`

### Herramientas de planificación (9)
`plan_create` `plan_revise` `plan_diff` `plan_evaluate` `plan_spar` `plan_decompose` `plan_constraints` `plan_rollback` `plan_template`

### Herramientas de orquestación (9)
`ctx_route` `ctx_trace` `ctx_schema_get` `ctx_schema_register` `ctx_cost_summary` `ctx_workspace_create` `ctx_workspace_list` `ctx_health` `ctx_version`

### Herramientas de inteligencia documental (8)
`docs_search` `docs_get` `docs_get_file` `docs_annotate` `docs_annotate_clear` `docs_annotate_list` `docs_feedback` `docs_contribute`

---

## Bucle de auto-mejora del agente

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

## Hoja de ruta

### Fase 1 — Absorber *(completada)*
- [x] Esquema unificado de herramientas MCP
- [x] Capa de memoria con persistencia entre sesiones
- [x] Motor de recuperación híbrido
- [x] Registro de herramientas con ejecución DAG
- [x] Motor de planificación + spec con hook de sparring
- [x] Orchestration Core
- [x] Capa de inteligencia documental (context-hub absorbido)

### Fase 1.5 — Actualización Cognition *(v0.2.0 — actual)*
- [x] **Capa Cognition** con 6 primitivas cognitivas
- [x] **Retrieval Router** con enrutamiento consciente del churn
- [x] **Index Lifecycle Manager** con auto-reparación
- [x] Registro de fuentes de datos con perfiles por fuente
- [x] Aplicación del presupuesto de contexto
- [x] Disyuntores para operaciones de índice
- [x] Detección de deriva del modelo de embedding
- [x] Reclasificación de churn guiada por feedback
- [ ] Integraciones de producción (sentence-transformers, rank-bm25, tantivy)
- [ ] Suite de pruebas completa para primitivas de cognition
- [ ] Benchmark: impacto de la capa cognition en la calidad de salida

### Fase 2 — Componer
- [ ] Bucle de feedback de recuperación (mejora el enrutamiento automáticamente)
- [ ] Grafo de entidades con consultas de relaciones
- [ ] Motor de resolución de conflictos de memoria
- [ ] Capa de caché de salidas de herramientas
- [ ] Evaluación de resultados + puntuación de specs
- [ ] Backend PostgreSQL + pgvector para escala
- [ ] Imagen Docker + docker-compose

### Fase 3 — Plataforma
- [ ] ContextOS Cloud (alojado, multi-inquilino)
- [ ] Constructor visual de workflows
- [ ] Marketplace de esquemas de herramientas
- [ ] SSO empresarial + registros de auditoría
- [ ] Adaptadores LangChain + CrewAI + AutoGen

---

## El origen de la capa Cognition

Las seis primitivas cognitivas de la v0.2.0 se identificaron rastreando cómo funciona realmente el razonamiento en una conversación viva de resolución de problemas, y nombrando cada operación a medida que se practicaba.

El punto de partida fue una publicación en LinkedIn de Cole Medin preguntando «Is RAG Dead?» con un diagrama que separaba datos estructurados (donde el RAG fue abandonado por agentes de código) de datos no estructurados (donde el RAG prospera). Un comentarista señaló dos cosas: el RAG se confundía con búsqueda semántica (se puede hacer RAG con BM25), y la razón real por la que los agentes de código usan grep es que reindexar en cada checkout de rama arruina la experiencia del desarrollador.

Esa intuición —tasa de rotación de datos frente a coste de indexación— se convirtió en el Retrieval Router. Pero surgió una pregunta más profunda: ¿qué ocurre entre la recuperación y la salida que nadie está construyendo? La respuesta fue un conjunto de primitivas cognitivas que se practicaban implícitamente en la propia conversación:

- El olvido activo ocurría en cada turno (dejando caer detalles irrelevantes del post)
- La calibración de profundidad ocurría de forma natural (saber cuándo profundizar vs dar una respuesta rápida)
- La detección de síntesis estaba presente (algunas preguntas necesitaban razonamiento, no recuperación)
- El sensado de desconocidos desconocidos apareció (el comentarista encontró un punto ciego que Cole no sabía que existía)
- La contradicción productiva fue el insight central (Cole argumentó a la vez que el RAG está muerto Y que la búsqueda agéntica es el futuro —lo cual es RAG)
- La gravedad dependiente del contexto apareció al analizar la base de código de ContextOS (una memoria de importancia 0,3 sobre «nunca pausar branded» pasó a 0,95 cuando la pregunta actual era pausar campañas branded)

La conversación se convirtió en la spec. Cada primitiva se practicó antes de nombrarse. Esta existe como registro de ese origen.

---

## Contribuir

Se aceptan PRs tanto de **código** como de **docs**. Consulta [CONTRIBUTING.md](docs/CONTRIBUTING.md) para las pautas.

Construido bajo [IASAWI](https://github.com/itallstartedwithaidea) — It All Started With A Idea.

---

## Licencia

MIT — ver [LICENSE](LICENSE)

---

## Cita

Si usas ContextOS en investigación o producción, por favor cita:

```
@software{contextos2026,
  title = {ContextOS: The Unified Context Intelligence Layer},
  author = {Williams, John and IASAWI Contributors},
  year = {2026},
  url = {https://github.com/itallstartedwithaidea/contextOS}
}
```

---

*Construido con respeto por cada repositorio que lo precedió.*
