# ContextOS

[English](README.md) | [Français](README.fr.md) | [Español](README.es.md) | [中文](README.zh.md) | [Nederlands](README.nl.md) | [Русский](README.ru.md) | [한국어](README.ko.md)

> **AI 에이전트를 위한 통합 컨텍스트 인텔리전스 레이어.**  
> pip 한 번이면 됩니다. 모든 기능을 갖춥니다. 빠짐없이.

[![PyPI version](https://badge.fury.io/py/contextos.svg)](https://badge.fury.io/py/contextos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![GitHub Stars](https://img.shields.io/github/stars/itallstartedwithaidea/contextOS?style=social)](https://github.com/itallstartedwithaidea/contextOS)

```
pip install contextos
```

---

## ContextOS란?

ContextOS는 **AI 컨텍스트를 위한 운영체제 레이어**로, AI 에이전트와 컨텍스트 관리 생태계의 선도적인 오픈소스 저장소 일곱 개의 역량을 흡수·확장·능가하는 단일 통합 MCP 서버와 CLI입니다.

어느 한 프로젝트도 전체 스택을 다루지 못했기 때문에 만들어졌습니다. 기존 도구는 한 가지에는 뛰어났지만 나머지는 부족했습니다. ContextOS는 이를 한데 모으고 모든 공백을 메우며, 어디에도 없었던 오케스트레이션 레이어를 추가합니다.

**ContextOS는 래퍼가 아니라 플랫폼입니다.** 이전에 쓰던 모든 도구는 그 위에서 동작하는 모듈이 됩니다.

---

## v0.2.0 — Cognition 업데이트

**업계는: 검색한 뒤 생성합니다.**  
**ContextOS는: 검색하고, 생각한 뒤, 생성합니다.**

시중의 에이전트 프레임워크는 가장 중요한 단계를 건너뜁니다. 컨텍스트를 검색해 프롬프트에 넣고 출력을 만듭니다. 검색과 출력 사이의 사고—전문가가 모순을 따지고, 제약을 저울질하고, 빠진 정보를 감지하며, 얼마나 깊이 들어갈지 결정하는 부분—그 부분은 어디에도 없었습니다.

지금까지는 그랬습니다.

v0.2.0은 세 개의 새 레이어와, 전문가 추론이 실제로 작동하는 방식을 모델링하는 프레임워크를 추가합니다:

### Cognition 레이어 — 여섯 가지 인지 원시(primitive)

검색과 생성 사이에서 일어나는 추론 연산입니다. 어떤 에이전트 프레임워크도 이를 일급으로 구축하지 않았습니다.

| 원시(primitive) | 하는 일 | 중요한 이유 |
|---|---|---|
| **능동적 망각(Active Forgetting)** | 출력 품질을 떨어뜨리는 검색된 컨텍스트를 버립니다 | 컨텍스트가 많을수록 항상 좋은 것은 아닙니다. 20개 청크 중 3개만 의미 있으면 노이즈가 되어 추론을 빗나가게 합니다. |
| **추론 깊이 보정(Reasoning Depth Calibration)** | 연산을 쓰기 전에 문제가 얼마나 많은 사고를 할 가치가 있는지 추정합니다 | 빠른 패턴 매칭과 10단계 추론 사슬은 모두 유효합니다—다른 문제에 대해서입니다. 에이전트는 자신이 어떤 상황인지 알아야 합니다. |
| **종합 감지(Synthesis Detection)** | 에이전트가 가진 것에 대해 **생각**해야 할지, 더 **가져와야** 할지 판단합니다 | 업계는 모든 작업을 검색 문제로 취급합니다. 일부 작업은 종합·유추·관계 추론입니다. 데이터가 많을수록 해가 됩니다. |
| **모르는 것의 모름 감지(Unknown Unknown Sensing)** | 정보의 **전체 범주**가 빠졌는지 감지합니다 | 아는 모름은 쉽습니다. 모르는 모름은 치명적입니다. «Salesforce 데이터가 여기 관련 있는 줄 몰랐다»는 «오늘 데이터가 없다»와 다른 실패 모드입니다. |
| **생산적 모순(Productive Contradiction)** | 충돌하는 데이터를 하나로 해소하지 않고 신호로 유지합니다 | «Google Ads는 전환 상승, CRM은 파이프라인 평탄»—답은 «하나 고르기»가 아닙니다. 측정 간극 **자체가** 인사이트입니다. |
| **맥락 의존적 중력(Context-Dependent Gravity)** | 현재 질문에 따라 메모리 중요도를 다시 가중합니다 | «승인 없이는 브랜디드 절대 안 돌린다»는 기억은 PMax 질의와의 유사도는 낮지만 권고를 근본적으로 바꿉니다. 정적 중요도 점수는 이를 놓칩니다. |

### Retrieval Router — churn 인지 라우팅

검색의 진짜 프레임은 «구조화 vs 비구조화 데이터»가 아니라 **데이터 변동률(churn) vs 인덱싱 비용**입니다.

코드베이스는 브랜치를 바꿀 때마다 변합니다—임베딩하면 즉시 오래된 인덱스가 됩니다. 법률 문서는 분기마다 바뀝니다—한 번 임베딩하면 수개월간 이득입니다. Retrieval Router는 각 데이터 소스의 기저 데이터가 얼마나 빨리 바뀌는지로 분류한 뒤 맞는 검색 전략을 고릅니다.

| Churn 등급 | 예시 데이터 | 전략 | 이유 |
|---|---|---|---|
| **Live** | 검색어 보고서, 경매 데이터, 예산 페이싱 | 직접 API pull, 인덱스 없음 | 캐시된 답은 이미 틀렸습니다 |
| **Warm** | 키워드 목록, 오디언스 세그먼트, 광고 카피 인벤토리 | BM25 또는 벡터 인덱스 + 신선도 시계 | 주간 변동, 신선하면 인덱스가 유용합니다 |
| **Cold** | 광고 정책, 계정 계층, 전략 문서 | 전체 벡터 검색, 한 번 임베딩 | 분기 이상으로 드물게 변함, 깊은 인덱싱에 투자 |

라우터는 매 요청마다 인덱스 신선도를 확인합니다. warm 소스의 인덱스가 오래되면 자동으로 live pull로 대체합니다. 사람 개입이 필요 없습니다.

### Index Lifecycle Manager — 자가 치유 인덱스

회구동 재인덱싱, 서킷 브레이커, 임베딩 모델 드리프트 감지.

- **쓰기 트리거 재인덱싱:** MCP 서버가 새 데이터를 푸시하면 인덱스가 자동으로 재구축됩니다. cron 없음. 데이터 흐름 **곧** 인덱싱 트리거입니다.
- **임베딩 모델 드리프트 감지:** 임베딩 모델을 업데이트하면? 모든 벡터 인덱스는 조용히 무효가 됩니다. 라이프사이클 매니저가 모델 버전 불일치를 잡아 전체 재구축을 트리거합니다.
- **스키마 변경 격리:** 들어오는 데이터 형태가 바뀌면 기존 인덱스는 재구축 전까지 격리됩니다. 조용히 틀린 결과는 없습니다.
- **서킷 브레이커:** 재인덱싱이 연속 3회 실패하면 시스템은 시도를 멈추고 live pull로 저하합니다. 알림이 울립니다. 수동 리셋 가능합니다.
- **하트비트 점검:** 주기적 헬스 스캔이 이벤트로 잡히지 않은 오래된 인덱스를 잡습니다.

---

## 동작 방식: 광고 예시

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

## 거인의 어깨 위에서

이 프로젝트들의 탁월한 작업 없이는 ContextOS가 없었을 것입니다. 각 저장소에 공식적으로 감사와 경의를 표합니다:

### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

**80.5k stars — TypeScript**  
도구 실행과 컨텍스트 프로토콜의 기초 표준입니다. ContextOS는 MCP를 네이티브 스키마로 채택하며 기존 모든 MCP 서버와 100% 호환됩니다.  
**준 것:** 프로토콜. 표준. 생태계.  
**부족했던 것:** 오케스트레이션 레이어, 메모리, 검색, 계획 없음—전송 프로토콜 자체만 있었습니다.

---

### [infiniflow/ragflow](https://github.com/infiniflow/ragflow)

**74.4k stars — Python**  
에이전트 기능과 깊은 문서 파싱을 갖춘 프로덕션급 RAG 엔진입니다.  
**준 것:** 검색 엔진, 문서 수집 파이프라인, 에이전트 인지 RAG 실행.  
**부족했던 것:** 레이어 간 메모리 통합, 오래됨 감지, 다중 코퍼스 라우팅, 피드백 루프, MCP 네이티브 도구 스키마 없음.

---

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

**71.3k stars — MDX**  
프롬프트 엔지니어링 패턴, 논문, 기법의 결정적 코퍼스입니다.  
**준 것:** ContextOS의 스펙 템플릿과 에이전트 지시 패턴을 뒷받침하는 계획·프롬프팅 지식 베이스.  
**부족했던 것:** 정적 문서만—런타임 통합, 프롬프트 버전 관리, 결과 추적 없음.

---

### [upstash/context7](https://github.com/upstash/context7)

**48.2k stars — TypeScript**  
LLM과 AI 코드 에디터를 위한 최신 코드 문서입니다.  
**준 것:** 라이브 문서 가져오기, LLM을 위한 버전 인지 컨텍스트 주입.  
**부족했던 것:** 메모리 레이어, 검색 통합, 세션 연속성 없음—순수 무상태 문서 fetch.

---

### [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)

**33.5k stars — TypeScript**  
AI와 SQLite + 임베딩으로 코딩 세션을 캡처·압축하는 Claude Code 플러그인입니다.  
**준 것:** 세션 내 메모리 압축 패턴, SQLite + 임베딩 아키텍처.  
**부족했던 것:** 메모리는 세션과 함께 사라짐. 세션 간 지속성, 엔티티 그래프, 티어링, 충돌 해결 없음.

---

### [ComposioHQ/composio](https://github.com/ComposioHQ/composio)

**27.3k stars — TypeScript**  
1000+ 툴킷에 인증, 도구 검색, 샌드박스된 작업대를 제공해 AI 에이전트를 만듭니다.  
**준 것:** 외부 API 통합 레이어—OAuth 흐름, 도구 샌드박싱, 실행 컨텍스트.  
**부족했던 것:** 도구 DAG 실행, 출력 캐싱, 재시도/폴백 정책, 도구 버전 관리 없음.

---

### [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)

**26.5k stars — JavaScript**  
Claude Code를 위한 경량 메타 프롬프팅·스펙 기반 개발 시스템입니다.  
**준 것:** 스펙 기반 실행 모델, 메타 프롬프팅 패턴, 작업 분해 템플릿.  
**부족했던 것:** 동적 계획 수정, 제약 전파, 스펙 버전 관리, 결과 평가 루프 없음.

---

### [andrewyng/context-hub](https://github.com/andrewyng/context-hub)

**47 stars — JavaScript**  
코딩 에이전트를 위한 CLI(`chub`)가 있는 큐레이션·버전 관리 문서 저장소입니다.  
**준 것:** 문서 인텔리전스 패턴: 큐레이션 콘텐츠 + 증분 fetch + 로컬 주석 + 커뮤니티 피드백 루프.  
**부족했던 것:** 메모리 레이어, 검색 통합, MCP 도구 스키마, Python 지원 없음.

> **ContextOS는 context-hub를 완전히 흡수합니다.** 모든 `chub` 명령은 `ctx docs` 명령에 매핑됩니다.

---

## 무엇이 빠졌는가 — ContextOS가 무엇을 짓는가

일곱 프로젝트를 모두 흡수한 뒤에도 단일 저장소가 다루지 못한 공백은 다음과 같았습니다:

### 오케스트레이션 코어 *(완전히 새로움)*

| 기능 | 중요한 이유 |
|---|---|
| **시맨틱 인텐트 라우터** | 들어오는 모든 요청을 분류해 올바른 레이어로 자동 디스패치합니다. |
| **요청 추적 / 관측 가능성** | 도구 호출마다 전체 계보: 어떤 레이어가 동작했는지, 지연, 토큰 비용, 품질 점수. |
| **스키마 레지스트리** | 하위 호환을 갖춘 버전 관리 도구 스키마. |
| **다중 워크스페이스 인증** | 워크스페이스별 API 키, 속도 제한, 감사 로그. |
| **비용 원장** | 세션·워크스페이스·도구별 LLM + API 지출 추적. |

### Cognition 레이어 *(v0.2.0에서 완전히 새로움)*

| 기능 | 중요한 이유 |
|---|---|
| **능동적 망각** | 노이즈를 만드는 검색 컨텍스트를 버립니다. 많다고 좋은 것은 아닙니다. |
| **추론 깊이 보정** | 연산을 쓰기 전에 문제가 얼마나 많은 사고를 할 가치가 있는지 압니다. |
| **종합 감지** | 검색 작업과 추론 작업을 구분합니다. |
| **모르는 것의 모름 감지** | 빠진 사실뿐 아니라 빠진 정보 **범주**를 감지합니다. |
| **생산적 모순** | 충돌 신호를 한 답으로 줄이지 않고 인사이트로 유지합니다. |
| **맥락 의존적 중력** | 현재 질문으로 메모리를 다시 가중합니다. 제약이 유사도 점수를 덮어씁니다. |
| **컨텍스트 예산** | 검색된 컨텍스트에 토큰 한도를 강제합니다. Karpathy의 «컨텍스트 윈도우 = RAM»을 운영 가능하게 만듭니다. |

### Retrieval Router *(v0.2.0에서 완전히 새로움)*

| 기능 | 중요한 이유 |
|---|---|
| **데이터 소스 레지스트리** | 각 MCP 서버가 churn 프로필, 인덱스 전략, 신선도 임계값을 스스로 선언합니다. |
| **Churn 인지 라우팅** | 소스별 live/warm/cold 분류. 전략이 데이터 변동성과 맞습니다. |
| **자동 폴백** | 인덱스가 오래됐나요? live pull로 폴백합니다. 수동 개입 없음. |
| **피드백 기반 재분류** | «cold» 소스가 계속 오래되면 시스템이 자동으로 «warm»으로 승격합니다. |

### Index Lifecycle Manager *(v0.2.0에서 완전히 새로움)*

| 기능 | 중요한 이유 |
|---|---|
| **이벤트 구동 재인덱싱** | MCP 데이터 이벤트가 재구축을 트리거합니다. cron 없음. |
| **임베딩 모델 드리프트 감지** | 모델 업데이트 = 모든 벡터 인덱스 무효. 자동 감지·자동 재구축. |
| **스키마 변경 격리** | 데이터 형태가 바뀌었나요? 재구축 전까지 인덱스 격리. |
| **서킷 브레이커** | 연속 인덱스 실패 3회 = live pull로 저하 + 알림. |
| **하트비트 헬스 체크** | 주기적 스캔이 이벤트가 놓친 것을 잡습니다. |

### 메모리 레이어 *(claude-mem 확장)*

| 기능 | 중요한 이유 |
|---|---|
| **세션 간 지속성** | 메모리가 프로세스 재시작 후에도 남습니다. |
| **메모리 티어링 (Hot/Warm/Cold)** | 최근성 + 관련성으로 자동 승격/강등. |
| **엔티티 그래프** | 엔티티를 추출해 구조화된 지식으로 연결합니다. |
| **충돌 해결** | 타임스탬프 + 신뢰도로 모순되는 메모리 소스를 해결합니다. |
| **사용자 범위 vs 에이전트 범위 메모리** | 사용자가 시스템에 말한 것과 에이전트가 배운 것—분리 보관. |

### 검색 레이어 *(ragflow + context7 확장)*

| 기능 | 중요한 이유 |
|---|---|
| **하이브리드 검색** | BM25 키워드 + 밀집 벡터 검색 결합. |
| **출처 귀속 점수** | 코사인 유사도뿐 아니라 출처 품질로 청크 순위. |
| **오래됨 감지** | 설정 가능한 TTL보다 오래된 콘텐츠를 표시하고 재-fetch를 트리거합니다. |
| **다중 코퍼스 라우팅** | 문서, 라이브 웹, 코드베이스, API 스펙으로 쿼리를 병렬 라우팅합니다. |
| **검색 피드백 루프** | 최종 출력에 나타난 청크를 추적합니다. 시간이 지나며 라우팅이 나아집니다. |

### 도구 실행 레이어 *(composio + MCP servers 확장)*

| 기능 | 중요한 이유 |
|---|---|
| **도구 체이닝 / DAG 실행** | 분기 로직을 가진 다단계 도구 파이프라인. |
| **샌드박스 코드 실행** | 출력 캡처와 오류 복구를 갖춘 안전 실행. |
| **도구 출력 캐싱** | 입력 해시로 결정적 결과를 캐시합니다. |
| **재시도 + 폴백 정책** | 도구별 SLA: 재시도 예산, 폴백 도구, 우아한 저하. |
| **도구 버전 관리** | 에이전트 워크플로를 특정 도구 버전에 고정합니다. |

### 계획·스펙 레이어 *(GSD + Prompt-Engineering-Guide 확장)*

| 기능 | 중요한 이유 |
|---|---|
| **동적 계획 수정** | 도구 출력에 따라 실행 중 계획이 갱신됩니다. |
| **제약 전파** | 도구 X가 실패하면 하류 단계가 자동 수정됩니다. |
| **스펙 버전 + diff** | 작업 스펙의 진화를 추적합니다. 새 스펙이 못하면 롤백. |
| **응답 전 스파링 훅** | 모든 에이전트 출력 전 필수 성찰. 발사 전 멈춤을 강제합니다. |
| **결과 평가** | 최종 출력을 원래 스펙에 대해 점수화합니다. 계획으로 신호를 되돌립니다. |

### 문서 인텔리전스 레이어 *(context-hub 완전 흡수)*

| 기능 | 중요한 이유 |
|---|---|
| **큐레이션 문서 레지스트리** | API, 프레임워크, 도구용 커뮤니티 유지·버전 관리 마크다운 문서. |
| **언어별 fetch** | 대상 언어로 문서를 가져옵니다. 관련 없는 스니펫 없음. |
| **증분 fetch** | 필요한 것만 가져옵니다. 토큰 낭비 없음. |
| **영구 주석** | 에이전트가 문서에 붙이는 로컬 노트. 세션 재시작 후에도 유지. |
| **커뮤니티 피드백 루프** | 문서별 추천/비추천이 메인테이너에게 전달됩니다. |
| **문서 오래됨 점수** | 오래된 문서를 표시하고 자동으로 다시 가져옵니다. |

---

## 아키텍처

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

**핵심 데이터 흐름 (v0.2.0):**

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

## 빠른 시작

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

### 데이터 소스 등록

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

### Cognition 패스 실행

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

### 문서 명령 *(context-hub 패리티 + 확장)*

```bash
ctx docs search openai                     # find available docs
ctx docs get openai/chat --lang py         # fetch current docs, Python variant
ctx docs get stripe/api --file webhooks    # incremental fetch
ctx docs annotate stripe/api "Note here"   # attach a persistent note
ctx docs feedback stripe/api up            # upvote a doc
```

### 메모리 명령

```bash
ctx memory store "key insight about X"
ctx memory retrieve "what do I know about stripe webhooks"
ctx memory forget "session notes from project Y"
ctx memory graph query "entity:OpenAI"
ctx memory conflicts --resolve auto
```

### 검색 명령

```bash
ctx retrieve docs "stripe payment intents python"
ctx retrieve live "openai assistants api latest"
ctx retrieve web "LLM context window best practices 2026"
ctx retrieve code "webhook verification pattern"
```

### 라우터 명령 *(v0.2.0 신규)*

```bash
ctx router register --name google_ads --churn live --index none
ctx router register --name policies --churn cold --index vector
ctx router health                          # index health across all sources
ctx router route "what queries triggered ads today"  # show routing decision
```

### Cognition 명령 *(v0.2.0 신규)*

```bash
ctx cognition think --query "should I pause branded" --domain advertising
ctx cognition budget --tokens 4000         # set context budget
ctx cognition contradictions --last        # show last detected contradictions
ctx cognition unknowns --last              # show unknown-unknown alerts
```

### 계획 명령

```bash
ctx plan create "build a stripe checkout integration"
ctx plan spar                              # pre-response sparring hook
ctx plan revise --feedback "tool X failed"
ctx plan evaluate --against-spec spec.md
```

### 오케스트레이션 명령

```bash
ctx health                                 # all 8 layers
ctx cost summary --workspace my-agent
ctx trace --id req_abc123
```

---

## 노출되는 MCP 도구

ContextOS는 MCP 프로토콜로 8개 범주에 걸쳐 **67개 도구**를 노출합니다.

### 메모리 도구 (9)
`memory_store` `memory_retrieve` `memory_forget` `memory_summarize` `memory_diff` `memory_graph_query` `memory_export` `memory_import` `memory_conflicts`

### 검색 도구 (8)
`retrieve_docs` `retrieve_live` `retrieve_web` `retrieve_code` `retrieve_merge` `retrieve_score` `retrieve_feedback` `retrieve_staleness`

### Cognition 도구 (6) *(v0.2.0 신규)*
`cognition_think` `cognition_forget` `cognition_depth` `cognition_contradictions` `cognition_unknowns` `cognition_gravity`

### 라우터 도구 (5) *(v0.2.0 신규)*
`router_register` `router_route` `router_health` `router_feedback` `router_reclassify`

### 인덱서 도구 (5) *(v0.2.0 신규)*
`indexer_status` `indexer_rebuild` `indexer_heartbeat` `indexer_circuit_reset` `indexer_model_update`

### 도구 실행 (12)
`tool_run` `tool_chain` `tool_cache_get` `tool_cache_set` `tool_register` `tool_list` `tool_schema` `tool_version_pin` `tool_retry_policy` `tool_cost` `tool_sandbox_run` `tool_composio`

### 계획 도구 (9)
`plan_create` `plan_revise` `plan_diff` `plan_evaluate` `plan_spar` `plan_decompose` `plan_constraints` `plan_rollback` `plan_template`

### 오케스트레이션 도구 (9)
`ctx_route` `ctx_trace` `ctx_schema_get` `ctx_schema_register` `ctx_cost_summary` `ctx_workspace_create` `ctx_workspace_list` `ctx_health` `ctx_version`

### 문서 인텔리전스 도구 (8)
`docs_search` `docs_get` `docs_get_file` `docs_annotate` `docs_annotate_clear` `docs_annotate_list` `docs_feedback` `docs_contribute`

---

## 에이전트 자기 개선 루프

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

## 로드맵

### Phase 1 — 흡수 *(완료)*
- [x] 통합 MCP 도구 스키마
- [x] 세션 간 지속성을 갖춘 메모리 레이어
- [x] 하이브리드 검색 엔진
- [x] DAG 실행을 갖춘 도구 레지스트리
- [x] 스파링 훅을 갖춘 계획 + 스펙 엔진
- [x] Orchestration Core
- [x] 문서 인텔리전스 레이어 (context-hub 흡수)

### Phase 1.5 — Cognition 업데이트 *(v0.2.0 — 현재)*
- [x] **Cognition 레이어**와 6가지 인지 원시
- [x] churn 인지 라우팅을 갖춘 **Retrieval Router**
- [x] 자가 치유를 갖춘 **Index Lifecycle Manager**
- [x] 소스별 프로필을 갖춘 데이터 소스 레지스트리
- [x] 컨텍스트 예산 강제
- [x] 인덱스 작업용 서킷 브레이커
- [x] 임베딩 모델 드리프트 감지
- [x] 피드백 기반 churn 재분류
- [ ] 프로덕션 통합 (sentence-transformers, rank-bm25, tantivy)
- [ ] 인지 원시에 대한 전체 테스트 스위트
- [ ] 벤치마크: cognition 레이어가 출력 품질에 미치는 영향

### Phase 2 — 복리
- [ ] 검색 피드백 루프 (라우팅 자동 개선)
- [ ] 관계 쿼리를 갖춘 엔티티 그래프
- [ ] 메모리 충돌 해결 엔진
- [ ] 도구 출력 캐싱 레이어
- [ ] 결과 평가 + 스펙 스코어링
- [ ] 규모를 위한 PostgreSQL + pgvector 백엔드
- [ ] Docker 이미지 + docker-compose

### Phase 3 — 플랫폼
- [ ] ContextOS Cloud (호스팅, 멀티 테넌트)
- [ ] 시각적 워크플로 빌더
- [ ] 도구 스키마 마켓플레이스
- [ ] 엔터프라이즈 SSO + 감사 로그
- [ ] LangChain + CrewAI + AutoGen 어댑터

---

## Cognition 레이어의 기원

v0.2.0의 여섯 가지 인지 원시는 실시간 문제 해결 대화에서 추론이 실제로 어떻게 작동하는지 추적하고, 각 연산이 실천될 때 이름을 붙이며 식별되었습니다.

출발점은 Cole Medin의 LinkedIn 글 «Is RAG Dead?」와 구조화 데이터(코딩 에이전트가 RAG를 버린 곳)와 비구조화 데이터(RAG가 번성하는 곳)를 나눈 다이어그램이었습니다. 댓글 작성자는 두 가지를 지적했습니다: RAG가 의미 검색과 혼동되고 있다(BM25로도 RAG 가능), 코딩 에이전트가 grep을 쓰는 진짜 이유는 브랜치 checkout마다 재인덱싱이 개발자 경험을 망친다는 것이었습니다.

그 통찰—데이터 변동률 vs 인덱싱 비용—이 Retrieval Router가 되었습니다. 더 깊은 질문도 생겼습니다: 검색과 출력 사이에 아무도 짓지 않는 것은 무엇인가? 답은 대화 자체에서 암묵적으로 실천되던 인지 원시들의 집합이었습니다:

- 매 턴마다 능동적 망각이 일어났습니다(글에서 관련 없는 세부를 버림)
- 깊이 보정이 자연스럽게 일어났습니다(깊이 들어갈 때와 빠른 답을 줄 때를 앎)
- 종합 감지가 있었습니다(일부 질문은 검색이 아니라 추론이 필요했음)
- 모르는 것의 모름 감지가 떠올랐습니다(댓글 작성자가 Cole이 존재를 몰랐던 사각을 찾음)
- 생산적 모순이 핵심 통찰이었습니다(Cole은 RAG가 죽었다고 **동시에** 에이전틱 검색이 미래라고 했는데, 그것은 RAG입니다)
- ContextOS 코드베이스를 분석할 때 맥락 의존적 중력이 나타났습니다(중요도 0.3의 «브랜디드 일시중지 금지» 메모리가 현재 질문이 브랜디드 캠페인 일시중지일 때 0.95로 올라감)

대화가 스펙이 되었습니다. 각 원시는 이름 붙이기 전에 먼저 실천되었습니다. 이 절은 그 기원의 기록입니다.

---

## 기여

**코드**와 **문서** 모두 PR을 환영합니다. 가이드는 [CONTRIBUTING.md](docs/CONTRIBUTING.md)를 참고하세요.

[IASAWI](https://github.com/itallstartedwithaidea) 산하에서 구축 — It All Started With A Idea.

---

## 라이선스

MIT — [LICENSE](LICENSE) 참고

---

## 인용

연구나 프로덕션에서 ContextOS를 사용한다면 다음을 인용해 주세요:

```
@software{contextos2026,
  title = {ContextOS: The Unified Context Intelligence Layer},
  author = {Williams, John and IASAWI Contributors},
  year = {2026},
  url = {https://github.com/itallstartedwithaidea/contextOS}
}
```

---

*앞선 모든 저장소에 대한 존중으로 만들었습니다.*
