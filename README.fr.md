# ContextOS

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [中文](README.zh.md) | [Nederlands](README.nl.md) | [Русский](README.ru.md) | [한국어](README.ko.md)

> **La couche unifiée d’intelligence contextuelle pour les agents IA.**  
> Une installation pip. Toutes les capacités. Rien ne manque.

[![PyPI version](https://badge.fury.io/py/contextos.svg)](https://badge.fury.io/py/contextos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![GitHub Stars](https://img.shields.io/github/stars/itallstartedwithaidea/contextOS?style=social)](https://github.com/itallstartedwithaidea/contextOS)

```
pip install contextos
```

---

## Qu’est-ce que ContextOS ?

ContextOS est la **couche système d’exploitation du contexte pour l’IA** — un serveur MCP et une CLI unifiés qui absorbent, étendent et dépassent les capacités de sept dépôts open source majeurs dans l’écosystème des agents IA et de la gestion du contexte.

Il a été créé parce qu’aucun projet ne couvrait toute la pile. Chaque outil existant excellait sur un point et manquait le reste. ContextOS les réunit, comble chaque lacune et ajoute une couche d’orchestration qui n’existait nulle part ailleurs.

**ContextOS n’est pas un simple wrapper. C’est une plateforme.** Chaque outil que vous utilisiez avant devient un module qui s’exécute au-dessus.

---

## v0.2.0 — La mise à jour Cognition

**L’industrie construit : récupérer puis générer.**  
**ContextOS construit : récupérer, RÉFLÉCHIR, puis générer.**

Tous les frameworks d’agents sur le marché sautent l’étape la plus importante. Ils récupèrent du contexte, le fourrent dans un prompt et génèrent une sortie. La réflexion entre la récupération et la sortie — là où un expert raisonne sur les contradictions, pèse les contraintes, sent les informations manquantes et décide de la profondeur nécessaire — cette partie n’existe nulle part.

Jusqu’à présent.

La v0.2.0 ajoute trois nouvelles couches et un framework qui modélise la façon dont le raisonnement d’expert fonctionne réellement :

### La couche Cognition — six primitives cognitives

Ce sont les opérations de raisonnement qui se situent entre la récupération et la génération. Aucun framework d’agents ne les a construites.

| Primitive | Rôle | Pourquoi c’est important |
|---|---|---|
| **Oubli actif** | Écarte le contexte récupéré qui dégrade la qualité de sortie | Plus de contexte n’est pas toujours mieux. 20 extraits dont 3 comptent créent du bruit qui dévie le raisonnement. |
| **Calibration de la profondeur de raisonnement** | Estime combien de réflexion un problème mérite avant d’engager du calcul | Un rapide pattern matching et une chaîne de raisonnement en 10 étapes sont tous deux valides — pour des problèmes différents. Les agents doivent savoir dans quelle situation ils sont. |
| **Détection de synthèse** | Détermine si l’agent doit RÉFLÉCHIR à ce qu’il a ou ALLER CHERCHER davantage | Toute l’industrie traite chaque tâche comme un problème de récupération. Certaines tâches sont de la synthèse, de l’analogie ou du raisonnement relationnel. Plus de données leur nuisent. |
| **Détection d’inconnues inconnues** | Détecte quand il manque une CATÉGORIE entière d’information | Les inconnues connues sont faciles. Les inconnues inconnues tuent. « Je ne savais pas que les données Salesforce étaient pertinentes ici » est un mode d’échec différent de « Je n’ai pas les données du jour ». |
| **Contradiction productive** | Conserve des données contradictoires comme signal plutôt que de les trancher | « Google Ads dit conversions en hausse, le CRM dit pipeline plat » — la réponse n’est pas « en choisir une ». L’écart de mesure EST l’insight. |
| **Gravité dépendante du contexte** | Repondère l’importance de la mémoire selon la question actuelle | Un souvenir « ne jamais lancer du branded sans approbation » score faible en similarité avec une requête PMax mais change fondamentalement la recommandation. Des scores d’importance statiques ratent cela. |

### Le routeur de récupération — routage sensible au churn

Le vrai cadre pour la récupération n’est pas « données structurées vs non structurées ». C’est **taux de churn des données vs coût d’indexation.**

Les bases de code changent à chaque changement de branche — les embedder crée des index périmés instantanément. Les documents juridiques changent trimestriellement — les embedder une fois est rentable pendant des mois. Le Retrieval Router classe chaque source selon la vitesse de changement des données sous-jacentes, puis choisit la stratégie de récupération adaptée.

| Classe de churn | Exemple de données | Stratégie | Pourquoi |
|---|---|---|---|
| **Live** | Rapports de requêtes de recherche, données d’enchères, rythme du budget | Appel API direct, pas d’index | Toute réponse en cache est déjà fausse |
| **Warm** | Listes de mots-clés, segments d’audience, inventaire de textes d’annonce | Index BM25 ou vectoriel avec horloge de fraîcheur | Change chaque semaine, l’index est utile s’il est à jour |
| **Cold** | Politiques d’annonces, hiérarchie de compte, docs de stratégie | Recherche vectorielle complète, embed une fois | Change au plus trimestriellement, investir dans un index profond |

Le routeur vérifie la fraîcheur de l’index à chaque requête. Si l’index d’une source « warm » est périmé, il bascule automatiquement sur un pull live. Sans intervention humaine.

### Le gestionnaire de cycle de vie des index — index auto-réparateurs

Ré-indexation pilotée par événements, avec disjoncteurs et détection de dérive du modèle d’embedding.

- **Ré-indexation déclenchée par écriture :** quand un serveur MCP pousse de nouvelles données, l’index se reconstruit automatiquement. Pas de cron. Le flux de données EST le déclencheur d’indexation.
- **Détection de dérive du modèle d’embedding :** vous mettez à jour votre modèle d’embedding ? Chaque index vectoriel devient silencieusement invalide. Le gestionnaire de cycle de vie détecte les incohérences de version de modèle et déclenche des reconstructions complètes.
- **Quarantaine en cas de changement de schéma :** si la forme des données entrantes change, les index existants sont mis en quarantaine jusqu’à reconstruction. Pas de résultats silencieusement faux.
- **Disjoncteurs :** si la ré-indexation échoue 3 fois de suite, le système arrête d’essayer et se dégrade en pull live. Alertes. Réinitialisation manuelle possible.
- **Contrôles de heartbeat :** des scans de santé périodiques attrapent les index périmés non déclenchés par les événements.

---

## Fonctionnement : un exemple publicitaire

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

## Sur les épaules des géants

ContextOS n’existerait pas sans le travail extraordinaire de ces projets. Nous créditons et honorons formellement chacun :

### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

**80,5 k stars — TypeScript**  
Le standard fondateur pour l’exécution d’outils et le protocole de contexte. ContextOS adopte MCP comme schéma natif et est 100 % compatible avec tous les serveurs MCP existants.  
**Ce qu’il nous a apporté :** le protocole. Le standard. L’écosystème.  
**Ce qui manquait :** pas de couche d’orchestration, pas de mémoire, pas de récupération, pas de planification — seulement le protocole de transport.

---

### [infiniflow/ragflow](https://github.com/infiniflow/ragflow)

**74,4 k stars — Python**  
Moteur RAG de niveau production avec capacités d’agent et analyse profonde de documents.  
**Ce qu’il nous a apporté :** le moteur de récupération, le pipeline d’ingestion, l’exécution RAG consciente des agents.  
**Ce qui manquait :** pas d’intégration mémoire cross-couches, pas de détection de péremption, pas de routage multi-corpus, pas de boucle de retour, pas de schéma d’outils natif MCP.

---

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

**71,3 k stars — MDX**  
Le corpus de référence des patterns, articles et techniques de prompt engineering.  
**Ce qu’il nous a apporté :** la base de connaissances planification / prompting qui alimente les modèles de spec et les patterns d’instructions des agents dans ContextOS.  
**Ce qui manquait :** documentation statique uniquement — pas d’intégration runtime, pas de versioning des prompts, pas de suivi des résultats.

---

### [upstash/context7](https://github.com/upstash/context7)

**48,2 k stars — TypeScript**  
Documentation de code à jour pour les LLM et éditeurs de code IA.  
**Ce qu’il nous a apporté :** récupération de documentation live, injection de contexte versionnée pour les LLM.  
**Ce qui manquait :** pas de couche mémoire, pas d’intégration récupération, pas de continuité de session — récupération de docs purement sans état.

---

### [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)

**33,5 k stars — TypeScript**  
Plugin Claude Code qui capture et compresse les sessions de code avec IA et SQLite + embeddings.  
**Ce qu’il nous a apporté :** le pattern de compression mémoire en session, l’architecture SQLite + embeddings.  
**Ce qui manquait :** la mémoire meurt avec la session. Pas de persistance cross-session, pas de graphe d’entités, pas de niveaux, pas de résolution de conflits.

---

### [ComposioHQ/composio](https://github.com/ComposioHQ/composio)

**27,3 k stars — TypeScript**  
Alimente 1000+ toolkits avec auth, recherche d’outils et banc d’essai sandboxé pour construire des agents IA.  
**Ce qu’il nous a apporté :** la couche d’intégration API externe — flux OAuth, sandboxing d’outils, contexte d’exécution.  
**Ce qui manquait :** pas d’exécution DAG d’outils, pas de cache de sorties, pas de politiques retry/fallback, pas de versioning d’outils.

---

### [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)

**26,5 k stars — JavaScript**  
Système léger de méta-prompting et de développement piloté par les specs pour Claude Code.  
**Ce qu’il nous a apporté :** le modèle d’exécution piloté par spec, les patterns de méta-prompting, les templates de décomposition de tâches.  
**Ce qui manquait :** pas de révision dynamique de plan, pas de propagation de contraintes, pas de versioning de spec, pas de boucle d’évaluation des résultats.

---

### [andrewyng/context-hub](https://github.com/andrewyng/context-hub)

**47 stars — JavaScript**  
Dépôt de documents curés et versionnés avec une CLI (`chub`) pour les agents de code.  
**Ce qu’il nous a apporté :** le pattern doc intelligence : contenu curé + fetch incrémental + annotations locales + boucles de feedback communautaire.  
**Ce qui manquait :** pas de couche mémoire, pas d’intégration récupération, pas de schéma d’outils MCP, pas de support Python.

> **ContextOS absorbe context-hub entièrement.** Chaque commande `chub` correspond à une commande `ctx docs`.

---

## Ce qui manquait — et ce que ContextOS construit

Après absorption des sept projets, voici les lacunes qu’aucun dépôt seul ne couvrait :

### Cœur d’orchestration *(entièrement nouveau)*

| Fonctionnalité | Pourquoi c’est important |
|---|---|
| **Routeur d’intention sémantique** | Classe chaque requête entrante et dispatch vers la bonne couche automatiquement. |
| **Traçage des requêtes / observabilité** | Lignée complète par appel d’outil : quelle couche a réagi, latence, coût tokens, score qualité. |
| **Registre de schémas** | Schémas d’outils versionnés avec rétrocompatibilité. |
| **Auth multi-workspace** | Clés API par workspace, limites de débit et journaux d’audit. |
| **Grand livre des coûts** | Suivi des dépenses LLM + API par session, workspace et outil. |

### Couche Cognition *(entièrement nouvelle en v0.2.0)*

| Fonctionnalité | Pourquoi c’est important |
|---|---|
| **Oubli actif** | Écarte le contexte récupéré qui crée du bruit. Plus n’est pas mieux. |
| **Calibration profondeur de raisonnement** | Savoir combien de réflexion un problème mérite avant d’investir du calcul. |
| **Détection de synthèse** | Distinguer tâches de récupération et tâches de raisonnement. |
| **Détection d’inconnues inconnues** | Détecter des catégories d’information manquantes, pas seulement des faits manquants. |
| **Contradiction productive** | Tenir des signaux contradictoires comme insight au lieu de trancher sur une réponse. |
| **Gravité dépendante du contexte** | Repondérer la mémoire selon la question actuelle. Les contraintes priment sur les scores de similarité. |
| **Budget de contexte** | Appliquer des limites de tokens au contexte récupéré. Le « Context Window = RAM » de Karpathy rendu opérationnel. |

### Routeur de récupération *(entièrement nouveau en v0.2.0)*

| Fonctionnalité | Pourquoi c’est important |
|---|---|
| **Registre des sources de données** | Chaque serveur MCP déclare son profil de churn, stratégie d’index et seuil de fraîcheur. |
| **Routage sensible au churn** | Classification live/warm/cold par source. La stratégie suit la volatilité des données. |
| **Repli automatique** | Index périmé ? Repli sur pull live. Pas d’intervention manuelle. |
| **Reclassification pilotée par le feedback** | Si une source « cold » devient souvent périmée, le système la promeut automatiquement en « warm ». |

### Gestionnaire de cycle de vie des index *(entièrement nouveau en v0.2.0)*

| Fonctionnalité | Pourquoi c’est important |
|---|---|
| **Ré-indexation pilotée par événements** | Les événements de données MCP déclenchent des reconstructions. Pas de cron. |
| **Détection de dérive du modèle d’embedding** | Mise à jour du modèle = tous les index vectoriels invalides. Détecté et reconstruit automatiquement. |
| **Quarantaine changement de schéma** | La forme des données change ? Index mis en quarantaine jusqu’à reconstruction. |
| **Disjoncteurs** | 3 échecs d’index consécutifs = dégradation en pull live + alerte. |
| **Contrôles de santé heartbeat** | Scans périodiques pour ce que les événements ont manqué. |

### Couche mémoire *(étend claude-mem)*

| Fonctionnalité | Pourquoi c’est important |
|---|---|
| **Persistance cross-session** | La mémoire survit aux redémarrages de processus. |
| **Niveaux de mémoire (Hot/Warm/Cold)** | Promotion/rétrogradation auto par récence + pertinence. |
| **Graphe d’entités** | Extrait des entités et les relie comme connaissance structurée. |
| **Résolution de conflits** | Résout les sources mémoire contradictoires via horodatage + confiance. |
| **Mémoire utilisateur vs agent** | Ce que l’utilisateur a dit au système vs ce que les agents ont appris — séparé. |

### Couche de récupération *(étend ragflow + context7)*

| Fonctionnalité | Pourquoi c’est important |
|---|---|
| **Recherche hybride** | BM25 mots-clés + recherche vectorielle dense combinées. |
| **Score d’attribution de source** | Classe les extraits par qualité de provenance, pas seulement similarité cosinus. |
| **Détection de péremption** | Signale le contenu plus vieux qu’un TTL configurable et déclenche un re-fetch. |
| **Routage multi-corpus** | Route les requêtes vers docs, web live, base de code ou spec API — en parallèle. |
| **Boucle de feedback récupération** | Suit quels extraits sont apparus dans la sortie finale. Le routage s’améliore avec le temps. |

### Couche d’exécution d’outils *(étend composio + serveurs MCP)*

| Fonctionnalité | Pourquoi c’est important |
|---|---|
| **Chaînage d’outils / exécution DAG** | Pipelines multi-étapes avec logique de branchement. |
| **Exécution de code sandboxée** | Exécution sûre avec capture de sortie et récupération d’erreurs. |
| **Cache des sorties d’outil** | Met en cache les résultats déterministes par hash d’entrée. |
| **Politiques retry + fallback** | SLA par outil : budget de retry, outil de secours, dégradation gracieuse. |
| **Versioning d’outils** | Épingle les workflows d’agent sur des versions d’outils précises. |

### Couche planification & spec *(étend GSD + Prompt-Engineering-Guide)*

| Fonctionnalité | Pourquoi c’est important |
|---|---|
| **Révision dynamique du plan** | Les plans se mettent à jour en cours d’exécution selon les sorties d’outils. |
| **Propagation de contraintes** | Si l’outil X échoue, les étapes en aval sont révisées automatiquement. |
| **Versioning de spec + diff** | Suit l’évolution des specs de tâche. Retour arrière si la nouvelle spec sous-performe. |
| **Hook de sparring pré-réponse** | Réflexion obligatoire avant toute sortie d’agent. Force une pause avant d’agir. |
| **Évaluation des résultats** | Note la sortie finale par rapport à la spec d’origine. Remonte du signal vers la planification. |

### Couche doc intelligence *(absorbe entièrement context-hub)*

| Fonctionnalité | Pourquoi c’est important |
|---|---|
| **Registre de docs curés** | Markdown versionné et maintenu par la communauté pour APIs, frameworks et outils. |
| **Fetch spécifique à la langue** | Récupère les docs dans votre langue cible. Pas d’extraits hors sujet. |
| **Fetch incrémental** | Ne récupère que le nécessaire. Pas de tokens gaspillés. |
| **Annotations persistantes** | Notes locales que les agents attachent aux docs. Survient aux redémarrages de session. |
| **Boucle de feedback communautaire** | Votes pour/contre par doc remontent aux mainteneurs. |
| **Score de péremption des docs** | Les docs périmés sont signalés et re-fetchés automatiquement. |

---

## Architecture

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

**Flux de données critique (v0.2.0) :**

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

## Démarrage rapide

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

### Enregistrer des sources de données

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

### Exécuter une passe Cognition

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

## CLI : `ctx`

### Commandes docs *(parité context-hub + extensions)*

```bash
ctx docs search openai                     # find available docs
ctx docs get openai/chat --lang py         # fetch current docs, Python variant
ctx docs get stripe/api --file webhooks    # incremental fetch
ctx docs annotate stripe/api "Note here"   # attach a persistent note
ctx docs feedback stripe/api up            # upvote a doc
```

### Commandes mémoire

```bash
ctx memory store "key insight about X"
ctx memory retrieve "what do I know about stripe webhooks"
ctx memory forget "session notes from project Y"
ctx memory graph query "entity:OpenAI"
ctx memory conflicts --resolve auto
```

### Commandes de récupération

```bash
ctx retrieve docs "stripe payment intents python"
ctx retrieve live "openai assistants api latest"
ctx retrieve web "LLM context window best practices 2026"
ctx retrieve code "webhook verification pattern"
```

### Commandes routeur *(nouveau en v0.2.0)*

```bash
ctx router register --name google_ads --churn live --index none
ctx router register --name policies --churn cold --index vector
ctx router health                          # index health across all sources
ctx router route "what queries triggered ads today"  # show routing decision
```

### Commandes cognition *(nouveau en v0.2.0)*

```bash
ctx cognition think --query "should I pause branded" --domain advertising
ctx cognition budget --tokens 4000         # set context budget
ctx cognition contradictions --last        # show last detected contradictions
ctx cognition unknowns --last              # show unknown-unknown alerts
```

### Commandes de planification

```bash
ctx plan create "build a stripe checkout integration"
ctx plan spar                              # pre-response sparring hook
ctx plan revise --feedback "tool X failed"
ctx plan evaluate --against-spec spec.md
```

### Commandes d’orchestration

```bash
ctx health                                 # all 8 layers
ctx cost summary --workspace my-agent
ctx trace --id req_abc123
```

---

## Outils MCP exposés

ContextOS expose **67 outils** dans 8 catégories via le protocole MCP.

### Outils mémoire (9)
`memory_store` `memory_retrieve` `memory_forget` `memory_summarize` `memory_diff` `memory_graph_query` `memory_export` `memory_import` `memory_conflicts`

### Outils de récupération (8)
`retrieve_docs` `retrieve_live` `retrieve_web` `retrieve_code` `retrieve_merge` `retrieve_score` `retrieve_feedback` `retrieve_staleness`

### Outils cognition (6) *(nouveau en v0.2.0)*
`cognition_think` `cognition_forget` `cognition_depth` `cognition_contradictions` `cognition_unknowns` `cognition_gravity`

### Outils routeur (5) *(nouveau en v0.2.0)*
`router_register` `router_route` `router_health` `router_feedback` `router_reclassify`

### Outils indexer (5) *(nouveau en v0.2.0)*
`indexer_status` `indexer_rebuild` `indexer_heartbeat` `indexer_circuit_reset` `indexer_model_update`

### Exécution d’outils (12)
`tool_run` `tool_chain` `tool_cache_get` `tool_cache_set` `tool_register` `tool_list` `tool_schema` `tool_version_pin` `tool_retry_policy` `tool_cost` `tool_sandbox_run` `tool_composio`

### Outils de planification (9)
`plan_create` `plan_revise` `plan_diff` `plan_evaluate` `plan_spar` `plan_decompose` `plan_constraints` `plan_rollback` `plan_template`

### Outils d’orchestration (9)
`ctx_route` `ctx_trace` `ctx_schema_get` `ctx_schema_register` `ctx_cost_summary` `ctx_workspace_create` `ctx_workspace_list` `ctx_health` `ctx_version`

### Outils doc intelligence (8)
`docs_search` `docs_get` `docs_get_file` `docs_annotate` `docs_annotate_clear` `docs_annotate_list` `docs_feedback` `docs_contribute`

---

## Boucle d’auto-amélioration de l’agent

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

## Feuille de route

### Phase 1 — Absorber *(terminée)*
- [x] Schéma d’outils MCP unifié
- [x] Couche mémoire avec persistance cross-session
- [x] Moteur de récupération hybride
- [x] Registre d’outils avec exécution DAG
- [x] Moteur de planification + spec avec hook de sparring
- [x] Orchestration Core
- [x] Couche doc intelligence (context-hub absorbé)

### Phase 1.5 — Mise à jour Cognition *(v0.2.0 — actuelle)*
- [x] **Couche Cognition** avec 6 primitives cognitives
- [x] **Retrieval Router** avec routage sensible au churn
- [x] **Index Lifecycle Manager** avec auto-réparation
- [x] Registre des sources de données avec profils par source
- [x] Application du budget de contexte
- [x] Disjoncteurs pour les opérations d’index
- [x] Détection de dérive du modèle d’embedding
- [x] Reclassification du churn pilotée par le feedback
- [ ] Intégrations production (sentence-transformers, rank-bm25, tantivy)
- [ ] Suite de tests complète pour les primitives cognition
- [ ] Benchmark : impact de la couche cognition sur la qualité de sortie

### Phase 2 — Composer
- [ ] Boucle de feedback récupération (améliore automatiquement le routage)
- [ ] Graphe d’entités avec requêtes de relations
- [ ] Moteur de résolution des conflits mémoire
- [ ] Couche de cache des sorties d’outil
- [ ] Évaluation des résultats + scoring de spec
- [ ] Backend PostgreSQL + pgvector pour l’échelle
- [ ] Image Docker + docker-compose

### Phase 3 — Plateforme
- [ ] ContextOS Cloud (hébergé, multi-tenant)
- [ ] Constructeur de workflows visuel
- [ ] Marketplace pour schémas d’outils
- [ ] SSO entreprise + journaux d’audit
- [ ] Adaptateurs LangChain + CrewAI + AutoGen

---

## L’origine de la couche Cognition

Les six primitives cognitives de la v0.2.0 ont été identifiées en suivant comment le raisonnement fonctionne réellement dans une conversation de résolution de problèmes en direct, puis en nommant chaque opération au fur et à mesure de sa pratique.

Le point de départ était un post LinkedIn de Cole Medin demandant « Is RAG Dead ? » avec un diagramme séparant données structurées (où le RAG a été abandonné par les agents de code) et données non structurées (où le RAG prospère). Un commentateur a souligné deux choses : le RAG était confondu avec la recherche sémantique (on peut faire du RAG avec BM25), et la vraie raison pour laquelle les agents de code utilisent grep est que la ré-indexation à chaque checkout de branche tue l’expérience développeur.

Cette intuition — taux de churn des données vs coût d’indexation — est devenue le Retrieval Router. Mais une question plus profonde est apparue : que se passe-til entre la récupération et la sortie que personne ne construit ? La réponse était un ensemble de primitives cognitives pratiquées implicitement dans la conversation elle-même :

- L’oubli actif se produisait à chaque tour (en laissant tomber les détails non pertinents du post)
- La calibration de profondeur était naturelle (savoir quand aller en profondeur vs donner une réponse rapide)
- La détection de synthèse était présente (certaines questions demandaient du raisonnement, pas de la récupération)
- La détection d’inconnues inconnues est apparue (le commentateur a trouvé un angle mort que Cole ne savait pas exister)
- La contradiction productive était l’insight central (Cole soutenait à la fois que le RAG est mort ET que la recherche agentique est l’avenir — ce qui est du RAG)
- La gravité dépendante du contexte est apparue en analysant la base ContextOS (une mémoire d’importance 0,3 sur « ne jamais mettre en pause le branded » est passée à 0,95 quand la question actuelle concernait la mise en pause des campagnes branded)

La conversation est devenue la spec. Chaque primitive a été pratiquée avant d’être nommée. Cette section existe pour en garder la trace.

---

## Contribuer

Les PR sont les bienvenues pour le **code** et la **documentation**. Voir [CONTRIBUTING.md](docs/CONTRIBUTING.md) pour les lignes directrices.

Construit sous [IASAWI](https://github.com/itallstartedwithaidea) — It All Started With A Idea.

---

## Licence

MIT — voir [LICENSE](LICENSE)

---

## Citation

Si vous utilisez ContextOS en recherche ou en production, veuillez citer :

```
@software{contextos2026,
  title = {ContextOS: The Unified Context Intelligence Layer},
  author = {Williams, John and IASAWI Contributors},
  year = {2026},
  url = {https://github.com/itallstartedwithaidea/contextOS}
}
```

---

*Construit avec respect pour chaque dépôt qui l’a précédé.*
