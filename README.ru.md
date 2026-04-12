# ContextOS

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [中文](README.zh.md) | [Nederlands](README.nl.md) | [Русский](README.ru.md) | [한국어](README.ko.md)

> **Единый слой контекстного интеллекта для ИИ-агентов.**  
> Одна установка через pip. Все возможности. Ничего не упущено.

[![PyPI version](https://badge.fury.io/py/contextos.svg)](https://badge.fury.io/py/contextos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![GitHub Stars](https://img.shields.io/github/stars/itallstartedwithaidea/contextOS?style=social)](https://github.com/itallstartedwithaidea/contextOS)

```
pip install contextos
```

---

## Что такое ContextOS?

ContextOS — это **слой операционной системы для контекста ИИ**: единый MCP-сервер и CLI, который поглощает, расширяет и превосходит возможности семи ведущих открытых репозиториев в экосистеме ИИ-агентов и управления контекстом.

Он создан потому, что ни один проект не покрывал весь стек. Каждый существующий инструмент блестел в одном и не хватало всего остального. ContextOS собирает их вместе, закрывает каждый пробел и добавляет слой оркестрации, которого нигде не было.

**ContextOS — не обёртка. Это платформа.** Каждый инструмент, который вы использовали раньше, становится модулем, работающим поверх неё.

---

## v0.2.0 — обновление Cognition

**Индустрия строит: извлечь, затем сгенерировать.**  
**ContextOS строит: извлечь, ПОДУМАТЬ, затем сгенерировать.**

Все фреймворки агентов на рынке пропускают самый важный шаг. Они извлекают контекст, запихивают его в промпт и генерируют вывод. Мышление между извлечением и выводом — та часть, где эксперт рассуждает о противоречиях, взвешивает ограничения, чувствует недостающую информацию и решает, насколько глубоко копать — этой части нигде нет.

До сих пор.

v0.2.0 добавляет три новых слоя и фреймворк, моделирующий то, как на самом деле работает экспертное рассуждение:

### Слой Cognition — шесть когнитивных примитивов

Это операции рассуждения между извлечением и генерацией. Ни один фреймворк агентов не строил их как полноценный слой.

| Примитив | Что делает | Почему это важно |
|---|---|---|
| **Активное забывание** | Отбрасывает извлечённый контекст, ухудшающий качество вывода | Больше контекста не всегда лучше. 20 извлечённых фрагментов, из которых важны 3, создают шум, сбивающий рассуждение. |
| **Калибровка глубины рассуждения** | Оценивает, сколько размышления заслуживает задача до траты вычислений | Быстрое сопоставление с образцом и цепочка из 10 шагов рассуждения оба допустимы — для разных задач. Агенты должны понимать, в какой ситуации они находятся. |
| **Детекция синтеза** | Определяет, должен ли агент ДУМАТЬ над тем, что есть, или ИДТИ за большим | Вся индустрия трактует каждую задачу как проблему извлечения. Некоторые задачи — синтез, аналогия или реляционное рассуждение. Больше данных им вредит. |
| **Чувствование неизвестного неизвестного** | Обнаруживает отсутствие целой КАТЕГОРИИ информации | Известные неизвестные просты. Неизвестные неизвестные убивают. «Я не знал, что данные Salesforce здесь релевантны» — иной режим отказа, чем «у меня нет сегодняшних данных». |
| **Продуктивное противоречие** | Держит конфликтующие данные как сигнал вместо разрешения | «Google Ads говорит, что конверсии растут, CRM — что воронка плоская» — ответ не «выбрать одно». Разрыв измерений И есть инсайт. |
| **Контекстно-зависимая гравитация** | Перевзвешивает важность памяти по текущему вопросу | Воспоминание «никогда не запускать branded без одобрения» даёт низкую схожесть с запросом PMax, но кардинально меняет рекомендацию. Статические оценки важности это упускают. |

### Retrieval Router — маршрутизация с учётом churn

Настоящий каркас извлечения — не «структурированные vs неструктурированные данные». Это **скорость изменения данных vs стоимость индексации.**

Кодовые базы меняются при каждом переключении ветки — эмбеддинг мгновенно даёт устаревшие индексы. Юридические документы меняются ежеквартально — один раз эмбеддить окупается месяцами. Retrieval Router классифицирует каждый источник данных по скорости изменения нижележащих данных и выбирает стратегию извлечения.

| Класс churn | Пример данных | Стратегия | Почему |
|---|---|---|---|
| **Live** | Отчёты по поисковым запросам, аукционные данные, темп бюджета | Прямой API-pull, без индекса | Любой кэшированный ответ уже неверен |
| **Warm** | Списки ключевых слов, сегменты аудитории, инвентарь текстов объявлений | BM25 или векторный индекс с часами свежести | Меняется еженедельно; индекс полезен, если свеж |
| **Cold** | Политики рекламы, иерархия аккаунта, стратегические документы | Полный векторный поиск, embed один раз | Меняется не чаще квартала; имеет смысл глубокая индексация |

Роутер проверяет свежесть индекса на каждый запрос. Если индекс warm-источника устарел, автоматически откатывается к live pull. Без вмешательства человека.

### Index Lifecycle Manager — самовосстанавливающиеся индексы

Событийно-управляемая переиндексация с предохранителями и детекцией дрейфа модели эмбеддингов.

- **Переиндексация по записи:** когда MCP-сервер пушит новые данные, индекс перестраивается автоматически. Без cron. Поток данных И есть триггер индексации.
- **Детекция дрейфа модели эмбеддингов:** обновили модель? Каждый векторный индекс тихо невалиден. Менеджер жизненного цикла ловит несоответствия версий модели и запускает полные пересборки.
- **Карантин при смене схемы:** если меняется форма входящих данных, существующие индексы карантинятся до пересборки. Никаких тихо неверных результатов.
- **Предохранители:** если переиндексация падает 3 раза подряд, система перестаёт пытаться и деградирует к live pull. Алерты. Ручной сброс доступен.
- **Пульс-проверки:** периодические сканы ловят устаревшие индексы, которые не были затронуты событиями.

---

## Как это работает: пример из рекламы

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

## На плечах гигантов

ContextOS не существовал бы без выдающейся работы этих проектов. Мы формально благодарим и чтим каждый:

### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

**80,5k stars — TypeScript**  
Фундаментальный стандарт выполнения инструментов и протокола контекста. ContextOS принимает MCP как нативную схему и на 100% совместим со всеми существующими MCP-серверами.  
**Что дало нам:** протокол. Стандарт. Экосистему.  
**Чего не хватало:** нет слоя оркестрации, памяти, извлечения, планирования — только транспортный протокол.

---

### [infiniflow/ragflow](https://github.com/infiniflow/ragflow)

**74,4k stars — Python**  
Промышленный RAG-движок с возможностями агента и глубоким разбором документов.  
**Что дало нам:** движок извлечения, пайплайн загрузки документов, выполнение RAG с учётом агента.  
**Чего не хватало:** нет межслойной интеграции памяти, детекции устаревания, маршрутизации по нескольким корпусам, петли обратной связи, нативной MCP-схемы инструментов.

---

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

**71,3k stars — MDX**  
Авторитетный корпус паттернов prompt engineering, статей и техник.  
**Что дало нам:** базу знаний планирования и промптинга, питающую шаблоны спецификаций и паттерны инструкций агентов в ContextOS.  
**Чего не хватало:** только статическая документация — нет интеграции в рантайм, версионирования промптов, отслеживания результатов.

---

### [upstash/context7](https://github.com/upstash/context7)

**48,2k stars — TypeScript**  
Актуальная документация кода для LLM и AI-редакторов кода.  
**Что дало нам:** живую выдачу документации, инъекцию контекста с учётом версий для LLM.  
**Чего не хватало:** нет слоя памяти, интеграции извлечения, непрерывности сессии — чисто stateless выборка доков.

---

### [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)

**33,5k stars — TypeScript**  
Плагин Claude Code, захватывающий и сжимающий сессии кодирования с ИИ и SQLite + эмбеддинги.  
**Что дало нам:** паттерн сжатия памяти в сессии, архитектуру SQLite + эмбеддинги.  
**Чего не хватало:** память умирает с сессией. Нет межсессионной персистентности, графа сущностей, уровней, разрешения конфликтов.

---

### [ComposioHQ/composio](https://github.com/ComposioHQ/composio)

**27,3k stars — TypeScript**  
Питает 1000+ наборов инструментов с auth, поиском инструментов и песочницей для сборки ИИ-агентов.  
**Что дало нам:** слой внешней интеграции API — OAuth, песочница инструментов, контекст выполнения.  
**Чего не хватало:** нет выполнения DAG инструментов, кэширования выводов, политик retry/fallback, версионирования инструментов.

---

### [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)

**26,5k stars — JavaScript**  
Лёгкая система мета-промптинга и разработки на спецификациях для Claude Code.  
**Что дало нам:** модель выполнения на спеках, паттерны мета-промптинга, шаблоны декомпозиции задач.  
**Чего не хватало:** нет динамической пересмотра планов, распространения ограничений, версионирования спеков, петли оценки результатов.

---

### [andrewyng/context-hub](https://github.com/andrewyng/context-hub)

**47 stars — JavaScript**  
Курируемое версионируемое хранилище документов с CLI (`chub`) для кодовых агентов.  
**Что дало нам:** паттерн doc intelligence: курируемый контент + инкрементальная выборка + локальные аннотации + петли обратной связи сообщества.  
**Чего не хватало:** нет слоя памяти, интеграции извлечения, MCP-схемы инструментов, поддержки Python.

> **ContextOS полностью поглощает context-hub.** Каждая команда `chub` отображается на команду `ctx docs`.

---

## Чего не хватало — и что строит ContextOS

После поглощения всех семи проектов оставались пробелы, которые ни один репозиторий не закрывал целиком:

### Ядро оркестрации *(полностью новое)*

| Возможность | Почему важно |
|---|---|
| **Семантический маршрутизатор намерений** | Классифицирует каждый входящий запрос и автоматически направляет в нужный слой. |
| **Трассировка запросов / наблюдаемость** | Полная линейка на вызов инструмента: какой слой сработал, задержка, стоимость токенов, оценка качества. |
| **Реестр схем** | Версионированные схемы инструментов с обратной совместимостью. |
| **Аутентификация нескольких workspace** | API-ключи, лимиты и аудит-логи на workspace. |
| **Книга затрат** | Учёт расходов LLM + API по сессии, workspace и инструменту. |

### Слой Cognition *(полностью новый в v0.2.0)*

| Возможность | Почему важно |
|---|---|
| **Активное забывание** | Убирает извлечённый контекст, создающий шум. Больше — не лучше. |
| **Калибровка глубины рассуждения** | Понимать, сколько размышления стоит задача до траты вычислений. |
| **Детекция синтеза** | Отличать задачи извлечения от задач рассуждения. |
| **Чувствование неизвестного неизвестного** | Обнаруживать отсутствующие категории информации, а не только факты. |
| **Продуктивное противоречие** | Держать конфликтующие сигналы как инсайт, а не сводить к одному ответу. |
| **Контекстно-зависимая гравитация** | Перевзвешивать память по текущему вопросу. Ограничения важнее косинусной схожести. |
| **Бюджет контекста** | Ограничивать токены извлечённого контекста. «Окно контекста = RAM» Карпати сделано операционным. |

### Retrieval Router *(полностью новый в v0.2.0)*

| Возможность | Почему важно |
|---|---|
| **Реестр источников данных** | Каждый MCP-сервер декларирует профиль churn, стратегию индекса и порог свежести. |
| **Маршрутизация с учётом churn** | Классификация live/warm/cold по источнику. Стратегия соответствует волатильности данных. |
| **Автоматический откат** | Индекс устарел? Откат к live pull. Без ручного вмешательства. |
| **Переклассификация по обратной связи** | Если «cold»-источник постоянно устаревает, система автоматически повышает его до «warm». |

### Index Lifecycle Manager *(полностью новый в v0.2.0)*

| Возможность | Почему важно |
|---|---|
| **Событийно-управляемая переиндексация** | События данных MCP запускают пересборку. Без cron. |
| **Детекция дрейфа модели эмбеддингов** | Обновление модели = все векторные индексы невалидны. Автообнаружение и пересборка. |
| **Карантин при смене схемы** | Меняется форма данных? Индекс в карантине до пересборки. |
| **Предохранители** | 3 последовательных сбоя индекса = деградация к live pull + алерт. |
| **Пульс-проверки здоровья** | Периодические сканы ловят то, что события пропустили. |

### Слой памяти *(расширяет claude-mem)*

| Возможность | Почему важно |
|---|---|
| **Межсессионная персистентность** | Память переживает перезапуски процессов. |
| **Уровни памяти (Hot/Warm/Cold)** | Автоповышение/понижение по свежести + релевантности. |
| **Граф сущностей** | Извлекает сущности и связывает их как структурированные знания. |
| **Разрешение конфликтов** | Разрешает противоречивые источники памяти по времени + уверенности. |
| **Память пользователя vs агента** | Что сказал пользователь системе и что выучили агенты — раздельно. |

### Слой извлечения *(расширяет ragflow + context7)*

| Возможность | Почему важно |
|---|---|
| **Гибридный поиск** | BM25 по ключевым словам + плотный векторный поиск вместе. |
| **Оценка атрибуции источника** | Ранжирует фрагменты по качеству происхождения, не только по косинусу. |
| **Детекция устаревания** | Помечает контент старше настраиваемого TTL и запускает повторную выборку. |
| **Маршрутизация по нескольким корпусам** | Параллельно направляет запросы к докам, живому вебу, кодовой базе или спецификации API. |
| **Петля обратной связи извлечения** | Отслеживает, какие фрагменты попали в итоговый вывод. Маршрутизация улучшается со временем. |

### Слой выполнения инструментов *(расширяет composio + MCP servers)*

| Возможность | Почему важно |
|---|---|
| **Цепочки инструментов / выполнение DAG** | Многошаговые пайплайны с ветвлением. |
| **Песочничное выполнение кода** | Безопасное выполнение с захватом вывода и восстановлением после ошибок. |
| **Кэширование выводов инструментов** | Кэширует детерминированные результаты по хэшу входа. |
| **Политики retry + fallback** | SLA на инструмент: бюджет повторов, запасной инструмент, graceful degradation. |
| **Версионирование инструментов** | Фиксирует рабочие процессы агентов на конкретные версии инструментов. |

### Слой планирования и спеков *(расширяет GSD + Prompt-Engineering-Guide)*

| Возможность | Почему важно |
|---|---|
| **Динамическая пересмотр планов** | Планы обновляются в ходе выполнения по выводу инструментов. |
| **Распространение ограничений** | Если инструмент X падает, нижестоящие шаги пересматриваются автоматически. |
| **Версионирование спеков + diff** | Отслеживает эволюцию спеков задач. Откат, если новая спека хуже. |
| **Хук спарринга перед ответом** | Обязательная рефлексия перед любым выводом агента. Пауза перед действием. |
| **Оценка результата** | Оценивает итоговый вывод относительно исходной спеки. Сигнал обратно в планирование. |

### Слой doc intelligence *(полностью поглощает context-hub)*

| Возможность | Почему важно |
|---|---|
| **Реестр курируемых доков** | Сообществом поддерживаемые версионируемые markdown-доки для API, фреймворков и инструментов. |
| **Выборка под язык** | Получает доки на целевом языке. Без лишних фрагментов. |
| **Инкрементальная выборка** | Берёт только нужное. Без лишних токенов. |
| **Постоянные аннотации** | Локальные заметки агентов к докам. Переживают перезапуск сессии. |
| **Петля обратной связи сообщества** | Голоса за/против по доку возвращаются мейнтейнерам. |
| **Оценка устаревания доков** | Устаревшие доки помечаются и автоматически перезагружаются. |

---

## Архитектура

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

**Критический поток данных (v0.2.0):**

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

## Быстрый старт

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

### Регистрация источников данных

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

### Запуск прохода Cognition

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

### Команды docs *(паритет с context-hub + расширения)*

```bash
ctx docs search openai                     # find available docs
ctx docs get openai/chat --lang py         # fetch current docs, Python variant
ctx docs get stripe/api --file webhooks    # incremental fetch
ctx docs annotate stripe/api "Note here"   # attach a persistent note
ctx docs feedback stripe/api up            # upvote a doc
```

### Команды памяти

```bash
ctx memory store "key insight about X"
ctx memory retrieve "what do I know about stripe webhooks"
ctx memory forget "session notes from project Y"
ctx memory graph query "entity:OpenAI"
ctx memory conflicts --resolve auto
```

### Команды извлечения

```bash
ctx retrieve docs "stripe payment intents python"
ctx retrieve live "openai assistants api latest"
ctx retrieve web "LLM context window best practices 2026"
ctx retrieve code "webhook verification pattern"
```

### Команды роутера *(новое в v0.2.0)*

```bash
ctx router register --name google_ads --churn live --index none
ctx router register --name policies --churn cold --index vector
ctx router health                          # index health across all sources
ctx router route "what queries triggered ads today"  # show routing decision
```

### Команды cognition *(новое в v0.2.0)*

```bash
ctx cognition think --query "should I pause branded" --domain advertising
ctx cognition budget --tokens 4000         # set context budget
ctx cognition contradictions --last        # show last detected contradictions
ctx cognition unknowns --last              # show unknown-unknown alerts
```

### Команды планирования

```bash
ctx plan create "build a stripe checkout integration"
ctx plan spar                              # pre-response sparring hook
ctx plan revise --feedback "tool X failed"
ctx plan evaluate --against-spec spec.md
```

### Команды оркестрации

```bash
ctx health                                 # all 8 layers
ctx cost summary --workspace my-agent
ctx trace --id req_abc123
```

---

## Экспонируемые инструменты MCP

ContextOS экспонирует **67 инструментов** в 8 категориях через протокол MCP.

### Инструменты памяти (9)
`memory_store` `memory_retrieve` `memory_forget` `memory_summarize` `memory_diff` `memory_graph_query` `memory_export` `memory_import` `memory_conflicts`

### Инструменты извлечения (8)
`retrieve_docs` `retrieve_live` `retrieve_web` `retrieve_code` `retrieve_merge` `retrieve_score` `retrieve_feedback` `retrieve_staleness`

### Инструменты cognition (6) *(новое в v0.2.0)*
`cognition_think` `cognition_forget` `cognition_depth` `cognition_contradictions` `cognition_unknowns` `cognition_gravity`

### Инструменты роутера (5) *(новое в v0.2.0)*
`router_register` `router_route` `router_health` `router_feedback` `router_reclassify`

### Инструменты индексатора (5) *(новое в v0.2.0)*
`indexer_status` `indexer_rebuild` `indexer_heartbeat` `indexer_circuit_reset` `indexer_model_update`

### Выполнение инструментов (12)
`tool_run` `tool_chain` `tool_cache_get` `tool_cache_set` `tool_register` `tool_list` `tool_schema` `tool_version_pin` `tool_retry_policy` `tool_cost` `tool_sandbox_run` `tool_composio`

### Инструменты планирования (9)
`plan_create` `plan_revise` `plan_diff` `plan_evaluate` `plan_spar` `plan_decompose` `plan_constraints` `plan_rollback` `plan_template`

### Инструменты оркестрации (9)
`ctx_route` `ctx_trace` `ctx_schema_get` `ctx_schema_register` `ctx_cost_summary` `ctx_workspace_create` `ctx_workspace_list` `ctx_health` `ctx_version`

### Инструменты doc intelligence (8)
`docs_search` `docs_get` `docs_get_file` `docs_annotate` `docs_annotate_clear` `docs_annotate_list` `docs_feedback` `docs_contribute`

---

## Петля самосовершенствования агента

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

## Дорожная карта

### Фаза 1 — Поглощение *(завершена)*
- [x] Единая схема инструментов MCP
- [x] Слой памяти с межсессионной персистентностью
- [x] Гибридный движок извлечения
- [x] Реестр инструментов с выполнением DAG
- [x] Движок планирования + спеков с хуком спарринга
- [x] Orchestration Core
- [x] Слой doc intelligence (context-hub поглощён)

### Фаза 1.5 — Обновление Cognition *(v0.2.0 — текущая)*
- [x] **Слой Cognition** с 6 когнитивными примитивами
- [x] **Retrieval Router** с churn-aware маршрутизацией
- [x] **Index Lifecycle Manager** с самовосстановлением
- [x] Реестр источников данных с профилями на источник
- [x] Соблюдение бюджета контекста
- [x] Предохранители для операций с индексом
- [x] Детекция дрейфа модели эмбеддингов
- [x] Переклассификация churn по обратной связи
- [ ] Продакшен-интеграции (sentence-transformers, rank-bm25, tantivy)
- [ ] Полный набор тестов для примитивов cognition
- [ ] Бенчмарк: влияние слоя cognition на качество вывода

### Фаза 2 — Накопление эффекта
- [ ] Петля обратной связи извлечения (автоулучшение маршрутизации)
- [ ] Граф сущностей с запросами по связям
- [ ] Движок разрешения конфликтов памяти
- [ ] Слой кэширования выводов инструментов
- [ ] Оценка результата + скоринг спеков
- [ ] Backend PostgreSQL + pgvector для масштаба
- [ ] Docker-образ + docker-compose

### Фаза 3 — Платформа
- [ ] ContextOS Cloud (хостинг, мультитенантность)
- [ ] Визуальный конструктор workflow
- [ ] Маркетплейс схем инструментов
- [ ] Enterprise SSO + аудит-логи
- [ ] Адаптеры LangChain + CrewAI + AutoGen

---

## Происхождение слоя Cognition

Шесть когнитивных примитивов в v0.2.0 были выявлены, прослеживая, как рассуждение работает в живом диалоге решения проблем, и называя каждую операцию по мере её практики.

Точкой отсчёта был пост Cole Medin в LinkedIn «Is RAG Dead?» с диаграммой, разделяющей структурированные данные (где RAG был оставлен кодовыми агентами) и неструктурированные (где RAG процветает). Комментатор указал на два момента: RAG смешивали с семантическим поиском (RAG можно делать с BM25), и настоящая причина, почему кодовые агенты используют grep, в том, что переиндексация при каждом checkout ветки убивает DX.

Этот инсайт — скорость изменения данных vs стоимость индексации — стал Retrieval Router. Но возник более глубокий вопрос: что происходит между извлечением и выводом, чего никто не строит? Ответом стал набор когнитивных примитивов, неявно практикуемых в самом разговоре:

- Активное забывание происходило каждый ход (отбрасывая нерелевантные детали поста)
- Калибровка глубины шла естественно (знать, когда углубиться vs дать быстрый ответ)
- Детекция синтеза присутствовала (некоторым вопросам нужно рассуждение, не извлечение)
- Чувствование неизвестного неизвестного всплыло (комментатор нашёл слепую зону, о существовании которой Cole не знал)
- Продуктивное противоречие стало ключевым инсайтом (Cole одновременно утверждал, что RAG мёртв И что агентный поиск — будущее, что является RAG)
- Контекстно-зависимая гравитация появилась при анализе кодовой базы ContextOS (память важности 0,3 о «никогда не паузить branded» стала 0,95, когда текущий вопрос был о паузе branded-кампаний)

Разговор стал спеком. Каждый примитив практиковался до того, как был назван. Этот раздел — запись того происхождения.

---

## Участие

PR приветствуются и для **кода**, и для **доков**. См. [CONTRIBUTING.md](docs/CONTRIBUTING.md).

Создано под [IASAWI](https://github.com/itallstartedwithaidea) — It All Started With A Idea.

---

## Лицензия

MIT — см. [LICENSE](LICENSE)

---

## Цитирование

Если вы используете ContextOS в исследовании или продакшене, пожалуйста, процитируйте:

```
@software{contextos2026,
  title = {ContextOS: The Unified Context Intelligence Layer},
  author = {Williams, John and IASAWI Contributors},
  year = {2026},
  url = {https://github.com/itallstartedwithaidea/contextOS}
}
```

---

*Создано с уважением к каждому репозиторию, который был раньше.*
