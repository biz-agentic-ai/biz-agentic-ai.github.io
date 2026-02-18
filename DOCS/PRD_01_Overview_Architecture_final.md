# DataNexus PRD
**Ontology-Driven Autonomous Data Agent**

---

## 1. 제품 개요 (Product Overview)

**제품명:** DataNexus  
**태그라인:** "Connect. Unify. Discover."  
**비전:** "Everyone is an Analyst." 구성원 누구나 자연어로 사내 데이터 자산(문서 + DB)을 탐색하고 분석하는 AI 동료.

### 제품명 의미
**Nexus**(연결점)라는 단어를 활용하여, 분산된 정형·비정형 데이터를 하나로 연결해주는 **허브(Hub)**를 의미합니다. 사일로화(Siloed)된 데이터를 결합하여 **통합된 메타데이터 카탈로그**와 **지식 베이스**를 제공하는 플랫폼 이미지를 전달합니다.

```txt
     ┌─────────┐      ┌─────────┐      ┌─────────┐
     │   DW    │      │  문서   │      │   BI    │
     │ (정형)  │      │(비정형) │      │ 리포트  │
     └────┬────┘      └────┬────┘      └────┬────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
                    ┌──────▼──────┐
                    │             │
                    │  DataNexus  │  ← 연결점 (Nexus)
                    │             │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
         │ 통합    │  │ 지식    │  │ AI      │
         │ 카탈로그│  │ 베이스  │  │ 인사이트│
         └─────────┘  └─────────┘  └─────────┘
```

### 핵심 철학
- **체계화 (Systematization):** 데이터 메쉬(Data Mesh) 사상 도입, 도메인 전문가가 정의한 용어(Ontology)가 모델의 지식이 됨
- **정확성 (Accuracy):** 지식 그래프의 구조적 추론으로 벡터 검색 한계 보완, 정량적 평가(NL2SQL360)로 품질 보증
- **접근성 (Accessibility):** React/Next.js 기반 통합 Chat UI로 데이터 디스커버리까지 지원
- **격리성 (Isolation):** DozerDB 멀티 데이터베이스로 그룹사별 데이터 완전 격리
- **자동화 (Automation):** DataHub 온톨로지가 변경되면 Vanna AI RAG Store에 자동 동기화
- **품질 보증 (Quality Assurance):** RAG 동기화 전 온톨로지 품질 검증 및 자체 품질 지표(Structural/Semantic/Functional)로 환각 위험 최소화
- **표준 호환성 (Interoperability):** SKOS 표준 구조 차용으로 외부 온톨로지 Import/Export 및 장기 확장성 확보
- **시행착오 비용 최소화 (Agent Trial-Error Cost Minimization):** 에이전트(SEOCHO 런타임 / Claude Code 개발)의 모든 아키텍처 결정은 "단독 성공률을 높이는가?"와 "실패 시 복구 비용을 줄이는가?" 두 축으로 평가. 23%짜리 복합 문제를 79%짜리 단위 작업으로 분해하고, 환경 설계(온톨로지, 테스트, 모듈 분리)로 성공률 자체를 높이는 것이 핵심 전략

### 전략적 포지셔닝 (Strategic Positioning)

> **핵심 명제:** 초지능 전환기(향후 24개월)에는 Frontier를 직접 하지 못하더라도, 타이밍과 도메인 선택으로 '대체 불가능한 3rd Party 포지션'을 선점해야 한다.

**배경:** Frontier Lab이 Compute + RL Environment에 집중하고, 모델 간 Agentic self-improvement가 본격화되면 외부 플레이어의 범용 업무 가치는 급격히 낮아질 수 있다. 단순 기획·문서 생성 중심 역할은 빠르게 commoditization될 가능성이 높다.

**DataNexus의 방어선:** DataNexus는 Non-verifiable Domain + Proprietary Data 영역에 위치한다. 기업 내부의 암묵적 지식, 역할별 해석 차이(동일한 매출 데이터를 CMO와 PM이 다르게 해석), 비공개 운영 데이터, 시간축을 가진 조직 고유의 분석 패턴 — 이러한 데이터는 공인된 외부 검증 절차로 즉시 판별하기 어렵기 때문에, 해당 도메인에서의 온톨로지 설계 역량, 신뢰 기반 관계, 내부 데이터 축적이 경쟁 우위로 작용한다.

**방어선 지속 조건:** 이 우위도 영구적이지 않다. 방어선의 수명을 늘리려면 **도메인 데이터 축적 속도 > 범용 모델의 일반화 속도**를 유지해야 한다. DataNexus의 온톨로지 기반 지식 그래프, Graphiti 시간축 메모리, 역할별 컨텍스트 누적은 이 속도 우위를 구조적으로 확보하기 위한 설계이다.

| 방어선 요소 | DataNexus 구현 | 축적 메커니즘 |
|------------|---------------|-------------|
| 온톨로지 기반 맥락 이해 | DataHub Glossary + SKOS 호환 레이어 | 도메인 전문가의 지속적 용어 정제 |
| 역할별 해석 차이 | Role-optimized Response (5개 페르소나: CEO/CFO, 마케터, MD/상품기획, 운영자, 분석가 — PRD_07 §11.12.3 참조, Phase 2+ 개인화) | 사용 패턴 기반 개인화 누적 |
| 시간축 지식 그래프 | Graphiti Temporal KG (Phase 3) | Episode 기반 실시간 지식 축적 |
| 비공개 운영 데이터 | DozerDB 격리 + Row-level Security | 그룹사별 독립 데이터 자산화 |
| 검증 난이도 높은 현장 맥락 | CQ 기반 온톨로지 검증 체계 | 현업-AI 협업 피드백 루프 |

**생존 전략 요약:**
1. **Timing:** 2026 Q1-Q2 MVP 선점 → 데이터 축적 루프 조기 가동
2. **Domain:** 검증 난이도·현장 맥락·운영 데이터가 강한 엔터프라이즈 데이터 분석 영역 집중

### 주요 구성 요소 (Key Components)

DataNexus는 네 가지 핵심 오픈소스 솔루션을 조합하여 구성됩니다:

| 컴포넌트 | 버전 | 역할 | 주요 특징 |
|----------|------|------|-----------|
| **DataHub** | v1.3.0.1 | 메타데이터 카탈로그 & 계보 관리 | 맞춤형 홈 화면, 요약 탭 커스터마이징, MCL 지원 |
| **ApeRAG** | v0.5.0-alpha.14 | 문서 기반 AI 지식엔진 (GraphRAG) | MinerU 통합, 하이브리드 검색, MCP 지원 |
| **DozerDB** | v5.26.3.0 | Neo4j Enterprise 기능 플러그인 | Multi-DB, DOD 보안 하드닝, APOC 호환 |
| **Vanna** | v2.0.2 | 사용자-인지 AI 에이전트 | User-Aware 설계, SSE 스트리밍, Row-level Security |

#### DataHub v1.3.0.1 – 메타데이터 카탈로그 & 계보 관리
LinkedIn 주도의 오픈소스 데이터 카탈로그 플랫폼으로, 다양한 데이터 자산의 메타데이터를 수집하고 검색/관리합니다.

**최신 버전 주요 기능:**
- **맞춤형 홈 화면:** 관리자가 조직별로 카탈로그 메인 대시보드 구성 가능
- **요약 탭 커스터마이징:** 데이터셋, 도메인, 글로서리 용어 등의 요약 화면 속성 직접 구성
- **다양한 소스 메타데이터 수집:** Tableau BigQuery 지원, Excel 파일, SnapLogic 파이프라인 지원 추가
- **SDK 및 플랫폼 개선:** 계보 처리 성능 개선, MCL(Metadata Change Log) 지원, OIDC OAuth 인증
- **메타데이터 변경 추적:** Kafka 이벤트 버스를 통한 Change Events 기록/전파

#### ApeRAG v0.5.0-alpha.14 – 문서 기반 AI 지식엔진 (GraphRAG 플랫폼)
ApeCloud에서 개발한 프로덕션 준비형 RAG 플랫폼으로, 문서 및 비정형 데이터를 다각도로 인덱싱합니다.

**최신 버전 주요 기능:**
- **하이브리드 검색 인덱스:** 벡터 임베딩 + 전문(full-text) 검색 + GraphRAG 통합
- **GraphRAG 및 지식 그래프:** LightRAG 기법 확장, 문서에서 추출한 개념을 노드로 구성
- **멀티모달 및 요약 인덱싱:** PDF, Word, Excel, 이미지/도표 처리
- **고급 문서 파싱 – MinerU 통합:** GPU 가속 지원, 표/공식/학술문서 정교한 파싱
- **MCP 지원:** Anthropic MCP(Model Context Protocol) 호환, 외부 AI 에이전트 통합

#### DozerDB v5.26.3.0 – Neo4j Enterprise 기능 플러그인
Neo4j Community Edition에 엔터프라이즈 기능을 무료로 추가해주는 오픈소스 플러그인입니다.

**최신 버전 주요 기능:**
- **멀티-데이터베이스:** 하나의 Neo4j 인스턴스에 복수의 DB 운영 (datahub_db + insight_kb_db, graphiti_memory_db [Phase 3])
- **보안 강화:** DOD(미국 국방성) Hardened Configuration 적용
- **엔터프라이즈 기능:** RBAC, 트리거/일정 실행, APOC 확장 호환
- **OpenGDS 지원:** Graph Data Science 라이브러리 연동

#### Vanna v2.0.2 – 사용자-인지 AI 에이전트
자연어를 데이터베이스 질의로 변환하고 결과를 해석해주는 오픈소스 AI 에이전트 프레임워크입니다.

**최신 버전 주요 기능:**
- **에이전트 기반 아키텍처:** 모듈식 툴 연결 (SQLTool, VisualizationTool, RAGTool)
- **사용자 인지(User-Aware) 설계:** 사용자 컨텍스트와 권한을 모든 층에서 인지, Row-level Security
- **현대적인 웹 인터페이스:** `<vanna-chat>` 컴포넌트, SSE 스트리밍, Light/Dark 테마
- **프로덕션 준비된 백엔드:** FastAPI 기반, JWT/OAuth 연동, Tracing/Metrics 내장
- **다양한 DB/LLM 지원:** PostgreSQL, Oracle, Snowflake, BigQuery + OpenAI, Claude, Gemini, Ollama

---

## 2. 시스템 아키텍처 (System Architecture)

| 계층 (Layer) | 구성 요소 | 기술 스택 | 역할 |
| :--- | :--- | :--- | :--- |
| **Interface** | Chat UI | React / Next.js | 사용자 접근성 강화 |
| **Interface** | Admin UI | React / Next.js | DB 연결, 온톨로지 편집, RAG 관리, 품질 대시보드 |
| **Orchestrator** | Governance SEOCHO [Brain] | Router, 스키마/프롬프트 Controller (LangGraph) | 동기화 관리 및 온톨로지 기반 질의 분해 |
| **Orchestrator** | **Query Router Agent** | **Classification + Cypher Templates** | **결정론적/확률론적 질의 라우팅** |
| **Orchestrator** | Sync Hub | SEOCHO Extension | URI 기반 Vanna/ApeRAG/DozerDB 통합 동기화 |
| **Core Engine** | Unified RAG Engine | ApeRAG [Muscle] | GraphRAG + Vector Hybrid 검색 |
| **Data Storage** | Graph DB | DozerDB | Neo4j 호환 + Multi-DB (멀티테넌시) |
| **Data Storage** | Vector DB | Qdrant | ApeRAG 및 Vanna AI 벡터 스토어 |
| **Governance** | Data Mesh | DataHub | 비즈니스 용어(Glossary), 테이블 메타데이터 원천 |
| **Governance** | **SKOS Compatibility Layer** | **매핑 테이블, RDF Export** | **표준 온톨로지 호환성** |
| **NL2SQL** | SQL Generator | Vanna AI | 정형 데이터(DW) 조회, 온톨로지 컨텍스트 활용 |
| **Automation** | **Ontology Drafter** | **LLM + Human Review** | **초안 자동 생성 및 외부 온톨로지 Import** |

### 2.1 처리 흐름 (Processing Flows)

#### 2.1.1 메타데이터 수집 (Metadata Ingestion) 플로우
```txt
[데이터 소스] → [DataHub Ingestion 커넥터] → [Kafka ChangeEvent]
    → [DataHub GMS] → [Neo4j 메타DB + OpenSearch 인덱스 갱신]
```
- 새로운 데이터 소스 생성 또는 메타데이터 초기 로드 시 DataHub Metadata Ingestion 프레임워크 사용
- DataHub v1.3에서 Excel, SnapLogic 등 신규 커넥터 지원
- Lineage 정보도 함께 수집/저장 (ETL 파이프라인 관계 그래프 추가)

#### 2.1.2 문서 지식베이스 구축 (Document KB Build) 플로우
```txt
[문서 업로드/크롤링] → [ApeRAG Document Processor (MinerU)]
    → [텍스트 추출 + Chunking] → [임베딩 벡터 생성]
    → [벡터 인덱스 + 전문검색 인덱스 + Knowledge Graph (Neo4j)]
```
- MinerU: 표, 이미지 포함 복잡한 문서 구조화 처리
- LightRAG 알고리즘: 엔터티 추출 및 관계 식별 → Knowledge Graph 노드/엣지 생성
- 주기적 문서 크롤링 및 변경 문서 재색인으로 KB 최신화

#### 2.1.3 AI 질의 응답 (Insight Query) 플로우
```txt
[사용자 질문] → [Vanna 에이전트 서버]
    ├─→ [권한 정보 조회 (SSO JWT)] → [Row-level 필터 내재화]
    ├─→ [LLM: SQL 생성] → [권한 검사] → [DB 실행]
    │       └─→ [결과 후처리] → [VisualizationTool: 차트 생성]
    └─→ [LLM: 응답 생성] → [SSE 스트리밍] → [프론트엔드 표시]
```

**상세 단계:**
1. **SQL 생성:** LLM이 질문 의도 파악 → SQLTool로 쿼리 생성 → 권한 검사 (금지 테이블/컬럼 접근 차단)
2. **데이터베이스 조회:** SQL 실행 결과 → 데이터프레임 변환 → 상위 N개 제한/집계 재처리
3. **시각화:** VisualizationTool이 차트 생성 (시계열 라인차트 등)
4. **LLM 응답 생성:** 결과 데이터 요약 + 인사이트 추출 → 자연어 답변 작성
5. **응답 표시:** SSE 스트림으로 점진적 응답 (표 → 차트 → 요약 문장)
6. **후속 질문:** 대화 메모리 유지 → 맥락 지속 질문 지원

#### 2.1.4 문서 기반 Q&A (Hybrid Query) 플로우
```txt
[사용자 질문] → [Vanna: 질문 의도 분류]
    ├─→ [SQLTool: DB 통계 조회]
    └─→ [RAGTool: ApeRAG 지식 검색]
        └─→ [결과 취합] → [LLM: 통합 답변 생성]
            └─→ [데이터 사실 + 문서 맥락 융합 인사이트]
```
- 정형 데이터(DB)와 비정형 문서(RAG) 양쪽 모두 활용
- ApeRAG는 관련 문서 스니펫 + Knowledge Graph 결과 반환
- 권한 검사: ApeRAG도 사용자 권한에 따라 민감 문서 접근 제한

#### 2.1.5 컴포넌트 연계 구조

| 연계 | 통신 방식 | 설명 |
|------|----------|------|
| Frontend ↔ Vanna | SSE (Server-Sent Events) | 실시간 스트리밍 응답 |
| Vanna ↔ Data Sources | SQLAlchemy/JDBC | DB 커넥터 (Snowflake, Oracle 등) |
| Vanna ↔ ApeRAG | REST API / MCP | 지식 검색 API 호출 |
| DataHub ↔ Vanna/ApeRAG | GraphQL/REST | URN 기반 메타데이터 참조 |
| Neo4j(DozerDB) ↔ All | Bolt Protocol | 멀티DB 분리 (datahub_db, insight_kb_db, graphiti_memory_db [Phase 3]) |

#### 2.1.6 Agent Studio 컴포넌트 아키텍처

SEOCHO Agent Studio는 Multi-Agent 시스템을 시각화하고 디버깅할 수 있는 통합 환경입니다. 계층적 에이전트 구조(Router → Graph/Vector/Web → DBA → Supervisor)를 통해 질의를 처리하며, Hierarchy of Truth 기반 충돌 해결과 Visual Debugging을 제공합니다.

> **📌 상세 설계는 [PRD_02 §3.5 Multi-Agent Studio (SEOCHO)](./PRD_02_Core_Features_Agent_final.md)를 참조하세요.**
> 에이전트 역할 정의, 계층 아키텍처 다이어그램, Hierarchy of Truth, Visual Debugging, 자율·통제 균형 프레임워크 등 모든 상세 사항은 §3.5에서 단일 관리합니다.

**Agent Studio 접근 URL:**

| 서비스 | URL | 설명 |
|--------|-----|------|
| Agent Studio UI | `http://localhost:8501` | 채팅 및 에이전트 트레이스 시각화 |
| API Server | `http://localhost:8001/docs` | FastAPI 백엔드 (Swagger UI) |
| Neo4j Browser | `http://localhost:7474` | 그래프 데이터베이스 직접 조회 |
| DataHub UI | `http://localhost:9002` | 메타데이터 카탈로그 |
| Opik Dashboard | `http://localhost:5173` | LLM Observability 대시보드 |

---

### 2.2 에이전트 프레임워크 용어 정의 (보강: 리뷰 반영)

> **⚠️ 용어 혼용 방지 (리뷰 보고서 §2 - 가장 중요한 논리 불일치)**

DataNexus에서 사용하는 두 가지 에이전트 체계를 명확히 구분합니다:

| 구분 | SEOCHO Agent (제품 런타임) | Claude Code Agent Teams (개발 도구) |
|------|---------------------------|-------------------------------------|
| **목적** | 사용자 질의를 처리하는 프로덕션 에이전트 | PRD를 구현하는 개발용 멀티에이전트 |
| **에이전트** | Router, Graph, Vector, Web, DBA, Supervisor | Team Lead, Backend Core, Graph Engine, RAG Pipeline, Agent Logic |
| **프레임워크** | LangGraph + openai-agents SDK | Claude Code Agent Teams (Anthropic 네이티브) |
| **실행 환경** | Docker 컨테이너 (프로덕션/스테이징) | 개발자 로컬 환경 (Claude Code CLI) |
| **통신 방식** | LangGraph State Graph + Tool Calls | Shared Task List + Direct Messaging |
| **문서 위치** | 본 PRD (Section 3.5) | Implementation Strategy / Guide |

**혼용 주의사항:**
- "Agent Teams"는 **항상** Claude Code 개발 도구를 의미합니다
- "SEOCHO Agent" 또는 "Multi-Agent Studio"는 **항상** 프로덕션 런타임을 의미합니다
- 두 체계의 "Router"는 완전히 다른 컴포넌트입니다 (SEOCHO Query Router ≠ Agent Teams Task Router)

---

### 2.3 DozerDB Multi-Database 격리 구조 명확화 (보강: 리뷰 반영)

> **⚠️ DozerDB Multi-DB vs Graphiti group_id 관계 (리뷰 보고서 §2)**

DozerDB의 멀티테넌시와 Graphiti의 데이터 격리는 서로 다른 계층에서 작동합니다:

```txt
┌─────────────────────────────────────────────────────────────┐
│ DozerDB Instance                                             │
├──────────────────┬──────────────────┬────────────────────────┤
│ datahub_db       │ insight_kb_db    │ graphiti_memory_db     │
│ (메타데이터)     │ (지식그래프)     │ (에이전트 메모리)      │
│ [Phase 1 MVP]    │ [Phase 1 MVP]    │ [Phase 3 R&D]          │
│                  │                  │                        │
│ DataHub 메타     │ ApeRAG KG        │ Graphiti group_id로    │
│ URN 기반 격리    │ 도메인별 격리    │ 논리적 Namespace 격리  │
└──────────────────┴──────────────────┴────────────────────────┘
```

| 격리 메커니즘 | 적용 대상 | 격리 수준 | Phase |
|--------------|----------|----------|-------|
| **DozerDB Multi-DB** | 그룹사별 전체 데이터 | 물리적 DB 분리 | Phase 1 (MVP) |
| **Graphiti group_id** | 에이전트 메모리 네임스페이스 | 논리적 Namespace | Phase 3 (R&D) |
| **Row-level Security** | 사용자별 쿼리 결과 | 행 수준 필터링 | Phase 1 (MVP) |

**핵심:** DozerDB Multi-DB는 Phase 1 MVP 필수 요소이며, Graphiti group_id는 Phase 3 에이전트 메모리 도입 시 적용합니다. 두 메커니즘은 보완적이지만 독립적으로 작동합니다.

