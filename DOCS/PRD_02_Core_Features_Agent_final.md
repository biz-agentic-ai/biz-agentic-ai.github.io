## 3. 핵심 기능 상세 (Key Features)

### 3.1 SEOCHO - ApeRAG 연동 (Brain & Muscle)
- **역할 정의:** SEOCHO는 DataHub의 온톨로지를 ApeRAG의 'Context Engineering' 설정으로 변환하여 주입
- **Taxonomy Injection:** DataHub Glossary를 ApeRAG Entity Extraction Prompt에 주입
- **Ontology-Driven Routing:** 온톨로지 노드의 '데이터 소스 속성(Source Affinity)'을 기반으로 정형/비정형 에이전트 최적 라우팅

### 3.2 하이브리드 검색 및 추론 (Powered by ApeRAG)
- **자동화된 그래프 구축:** ApeRAG MinerU를 통해 문서 내 표, 이미지까지 자동 지식 그래프 생성
- **DozerDB 멀티테넌시:** 그룹사별 Graph DB 분리로 데이터 격리 및 성능 최적화
- **Multi-hop Inference 엔진:** 인과 관계(`impacts`, `caused_by`) 및 계산 관계를 기반으로 복잡한 지식 그래프 추론 수행 (구체적 사용 예시는 §3.3 참조)

### 3.3 지능형 라우팅 및 질의 이해
- **Data Retrieval:** "지난달 매출 얼마야?" → SQL/Cypher 생성
- **Data Discovery:** "배민클럽 구독 정보는 어떤 테이블에 있어?" → 테이블/컬럼 해설
- **Multi-hop Inference (질의 유형):** "A 공장 이슈가 B제품 공급망에 미친 영향은?" → 위 §3.2에서 정의한 Multi-hop Inference 엔진 기반 복잡한 지식 그래프 추론 실행
- **Semantic Disambiguation:** 사용자 프로필과 온톨로지 도메인(Namespace)을 매칭하여 부서별 용어 중의성 해결

### 3.4 Query Router Agent
- **결정론적 vs 확률론적 분기:** 엄격한 논리가 필요한 질의는 사전 정의된 Cypher 템플릿으로, 일반 질의는 LLM으로 라우팅
- **Cypher 템플릿 라이브러리:** 계층 관계, 추이적 폐쇄, 집계 연산 등 검증된 쿼리 패턴 관리
- **LLM Fallback 정책:** 템플릿 매칭 실패 시 LLM 추론으로 자동 전환, 결과 검증 후 신뢰도 표시

### 3.5 Multi-Agent Studio (SEOCHO)

SEOCHO 프로젝트에서 구현된 Multi-Agent Studio는 GraphRAG 시스템을 위한 통합 에이전트 오케스트레이션 프레임워크입니다.

#### 3.5.1 계층적 에이전트 아키텍처

```txt
User Query
    │
    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                           Router Agent                                     │
│   • 쿼리 복잡도 분류 (Single-hop / Multi-hop)                             │
│   • 온톨로지 기반 데이터 소스 선택                                          │
│   • 결정론적/확률론적 라우팅 결정                                           │
└───────────────┬───────────────────────┬───────────────────────┬───────────┘
                │                       │                       │
        ┌───────▼───────┐       ┌───────▼───────┐       ┌───────▼───────┐
        │  Graph Agent  │       │ Vector Agent  │       │   Web Agent   │
        │               │       │               │       │               │
        │ • LPG 조회    │       │ • 벡터 검색   │       │ • 웹 검색     │
        │ • RDF 조회    │       │ • 유사도 랭킹 │       │ • 실시간 정보 │
        └───────┬───────┘       └───────┬───────┘       └───────┬───────┘
                │                       │                       │
        ┌───────▼───────┐               │                       │
        │   Graph DBA   │               │                       │
        │               │               │                       │
        │ • Text2Cypher │               │                       │
        │ • 스키마 인지 │               │                       │
        │ • 쿼리 최적화 │               │                       │
        └───────┬───────┘               │                       │
                │                       │                       │
                └───────────────────────┼───────────────────────┘
                                        │
                                ┌───────▼───────┐
                                │  Supervisor   │
                                │               │
                                │ • 결과 통합   │
                                │ • 충돌 해결   │
                                │ • 최종 응답   │
                                └───────────────┘
```

#### 3.5.2 에이전트 역할 정의

| 에이전트 | 역할 | 주요 기능 | 입력 | 출력 |
|----------|------|----------|------|------|
| **Router Agent** | 질의 분류 및 라우팅 | 복잡도 분석, 소스 선택 | User Query | Routing Decision |
| **Graph Agent** | 구조화된 지식 조회 | LPG/RDF 그래프 탐색 | Query + Schema | Graph Results |
| **Vector Agent** | 비정형 문서 검색 | 임베딩 유사도 검색 | Query | Document Chunks |
| **Web Agent** | 실시간 외부 정보 | 웹 검색 및 크롤링 | Query | Web Results |
| **Graph DBA** | Text2Cypher 전문가 | 스키마 인지 쿼리 생성 | NL Query + Schema | Optimized Cypher |
| **Supervisor** | 결과 통합 및 조율 | 충돌 해결, 최종 응답 생성 | Multi-Source Results | Final Answer |

#### 3.5.3 Hierarchy of Truth (진실 계층)

다중 소스에서 충돌하는 정보가 반환될 경우, Supervisor는 다음 우선순위에 따라 최종 응답을 결정합니다:

```txt
┌─────────────────────────────────────────────────────────────────────┐
│                     Hierarchy of Truth                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Priority 1: Ontology (DataHub Glossary)                          │
│   ├── 공식 정의, 비즈니스 용어, 계산식                               │
│   └── ConflictResolutionScore: 100                                  │
│                                                                     │
│   Priority 2: Structured Data (Graph/SQL)                          │
│   ├── LPG/RDF 그래프 쿼리 결과                                      │
│   ├── SQL 쿼리 실행 결과                                            │
│   └── ConflictResolutionScore: 90                                   │
│                                                                     │
│   Priority 3: Vector RAG (Documents)                                │
│   ├── 문서 기반 검색 결과                                           │
│   └── ConflictResolutionScore: 70                                   │
│                                                                     │
│   Priority 4: Web Search (External)                                 │
│   ├── 웹 검색 결과                                                  │
│   └── ConflictResolutionScore: 50                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**충돌 해결 로직:**

```python
# Phase 1 MVP: 4-소스 우선순위 기반 충돌 해결 (아래 코드)
# Phase 2+: 5-소스(external_kg 추가), Phase 3: 6-소스(graphiti 추가)로 최종 확장 — 아래 테이블 참조
class Supervisor:
    """다중 소스 결과 통합 및 충돌 해결"""

    HIERARCHY_OF_TRUTH = {
        "ontology": 100,
        "graph": 90,
        "vector": 70,
        "web": 50
        # Phase 2+: "graphiti": 65, "external_kg": 60 추가
    }
    
    def resolve_conflicts(self, results: Dict[str, Any]) -> SupervisorResult:
        """Hierarchy of Truth에 따른 충돌 해결"""
        conflicts = self._detect_conflicts(results)
        
        if not conflicts:
            return self._merge_results(results)
        
        # 우선순위에 따라 충돌 해결
        resolved = {}
        for conflict in conflicts:
            winner = max(
                conflict.sources,
                key=lambda s: self.HIERARCHY_OF_TRUTH[s.type]
            )
            resolved[conflict.key] = winner.value
            
        return SupervisorResult(
            answer=self._generate_answer(resolved),
            conflict_resolution_score=self._calculate_score(conflicts, resolved),
            sources=results,
            conflicts_detected=len(conflicts),
            resolution_method="hierarchy_of_truth"
        )
```


> **[Phase 2+/3 확장] Graphiti 및 External KG 통합 시 Hierarchy of Truth 최종 구조:**
>
> | Priority | 소스 | ConflictResolutionScore |
> |----------|------|----------------------|
> | 1 | Ontology (DataHub Glossary) | 100 |
> | 2 | Structured Data (Graph/SQL) | 90 |
> | 3 | Internal Vector RAG (Documents) | 70 |
> | 4 | Graphiti Temporal KG (Agent Memory) | 65 |
> | 5 | External Knowledge Graph (ToolsRetriever) | 60 |
> | 6 | Web Search (External) | 50 |


#### 3.5.4 Visual Debugging (Streamlit-Flow)

Agent Studio는 Streamlit-Flow를 활용하여 에이전트 실행 과정을 실시간으로 시각화합니다:

```txt
┌─────────────────────────────────────────────────────────────────────┐
│                    Agent Studio - Debug View                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [User Query]                                                      │
│   "지난 분기 VIP 고객의 매출 추이를 분석해줘"                        │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ 🔵 Router Agent            ⏱️ 234ms                         │  │
│   │ ├─ Complexity: Multi-hop                                    │  │
│   │ ├─ Selected: [Graph, Vector]                                │  │
│   │ └─ Confidence: 0.92                                         │  │
│   └─────────────────┬─────────────────────────────────────────────┘  │
│                     │                                               │
│   ┌─────────────────▼─────────────┐  ┌───────────────────────────┐  │
│   │ 🟢 Graph Agent    ⏱️ 456ms   │  │ 🟢 Vector Agent  ⏱️ 312ms │  │
│   │ ├─ Tool: Graph DBA           │  │ ├─ Tool: Qdrant Search    │  │
│   │ ├─ Cypher Generated ✓        │  │ ├─ Results: 5 chunks      │  │
│   │ └─ Results: 847 rows         │  │ └─ Relevance: 0.87        │  │
│   └─────────────────┬─────────────┘  └─────────────┬─────────────┘  │
│                     │                              │               │
│   ┌─────────────────▼──────────────────────────────▼─────────────┐  │
│   │ 🟣 Supervisor              ⏱️ 189ms                          │  │
│   │ ├─ Conflicts Detected: 0                                     │  │
│   │ ├─ ConflictResolutionScore: 95                               │  │
│   │ └─ Final Answer Generated ✓                                  │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│   [Trace ID: abc123-def456]  [Total Time: 1,191ms]                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Debug View 주요 정보:**
- 각 에이전트의 실행 시간 (ms)
- 선택된 도구 및 결정 이유
- 신뢰도 점수 (Confidence)
- 충돌 감지 및 해결 현황
- 전체 처리 시간 및 Trace ID

#### 3.5.5 Multi-Database 지원 [Phase 2+]

> **📌 MVP 범위 조정 권고 (리뷰 보고서 §1):**
>
> 아래 "현재 Phase"는 원래 설계 기준이며, "권고 Phase"가 현행 적용됩니다.

> **📌 Phase 구분:**
> - **MVP (Phase 1):** PRD_01 §2.3에 정의된 물리적 2-DB 구조(`datahub_db`, `insight_kb_db`)를 사용합니다. 모든 도메인 데이터는 `insight_kb_db` 내에서 레이블로 구분합니다.
> - **Phase 2+:** 아래의 도메인별 논리적 DB 분리를 도입합니다. 각 도메인 DB는 `insight_kb_db` 내부의 논리적 파티션으로 구현됩니다.

Agent Studio는 온톨로지별로 서로 다른 데이터베이스를 전환하여 사용할 수 있습니다:

| 온톨로지 유형 | 논리적 데이터베이스 | 물리적 DB (PRD_01 §2.3) | 스키마 | 용도 |
|--------------|-------------------|------------------------|--------|------|
| **General** | `general_db` | `insight_kb_db` | 범용 그래프 | 일반 비즈니스 질의 |
| **Financial** | `financial_db` | `insight_kb_db` | FIBO 기반 | 금융/회계 질의 |
| **Retail** | `retail_db` | `insight_kb_db` | GS1/GoodRelations | 유통/물류 질의 |
| **HR** | `hr_db` | `insight_kb_db` | 인사 온톨로지 | 인사/조직 질의 |

> 📌 **구현 코드 → Implementation_Guide_final.md 이관.** 인터페이스 계약:
> - **클래스:** `MultiDatabaseRouter(primary_db, secondary_dbs)`
> - **핵심 메서드:** `route_query(query: ParsedQuery) → DatabaseTarget`
> - **행동:** 테이블→DB 매핑 기반 자동 라우팅, Cross-DB Join 감지 시 Federation 전략 선택

#### 3.5.6 Graphiti Memory Debugger (Agent 메모리 시각화) [Phase 3 R&D]

> **📌 Phase 3 R&D:** 이 기능은 MVP 범위가 아닙니다. Phase 3 에이전트 메모리 도입 시 구현합니다.

Agent Studio에 Graphiti 기반 **시간축 사실 추적 시각화** 기능을 추가합니다. 에이전트가 축적한 지식(사실, 관계)의 변화 이력을 타임라인으로 시각화하여 디버깅과 감사를 지원합니다.

| 기능 | 설명 | 기술 스택 |
|------|------|----------|
| **Fact Timeline** | 특정 엔터티/관계의 시간별 변화 이력 시각화 | Graphiti Bi-Temporal |
| **Episode Inspector** | 에피소드(대화/이벤트)별 지식 변화 추적 | Graphiti Episode |
| **Community Map** | 자동 탐지된 엔터티 클러스터 시각화 | Label Propagation |
| **Memory Search** | 에이전트 장기 기억 하이브리드 검색 (Semantic + BM25 + Graph BFS) | Graphiti Hybrid |

상세 구현은 [PRD_04c_Ontology_Future_final.md §4.3.10](./PRD_04c_Ontology_Future_final.md) (Graphiti 기반 시간 인식 지식그래프 및 에이전트 메모리 계층)을 참조합니다. 장시간 세션에서의 컨텍스트 보존 전략은 [PRD_04c §4.3.10.10](./PRD_04c_Ontology_Future_final.md) (OpenClaw 적응 기법)을 참조합니다.


---

### 3.6 에이전트 자율성-통제 균형 프레임워크

> **신규 섹션 — Ecosystem Analysis §3 + 리뷰 보고서 §5 보안 구체화**

Moltbook 사례에서 1.5M 에이전트가 수 분 내 보안 취약점을 노출한 교훈을 반영하여, SEOCHO Multi-Agent에도 명시적 자율성-통제 균형을 설계합니다.

#### 3.6.1 작업 유형별 자율성 수준

| 작업 유형 | 자율성 수준 | 실행 정책 | 안전장치 |
|-----------|-----------|----------|---------|
| **SELECT 쿼리** (읽기 전용) | 🟢 High | 자동 실행 | 스키마 검증 + 결과 행 수 제한 (max 10,000) |
| **문서 검색** (RAG) | 🟢 High | 자동 실행 | 권한 필터 + 출처 표시 (Source Attribution) |
| **온톨로지 초안** (Drafter) | 🟡 Medium | Human-in-the-loop | LLM 초안 → 전문가 검토 → 승인 ([PRD_04a §4.5.3](./PRD_04a_Ontology_Core_final.md)) |
| **DDL/DML** (쓰기 작업) | 🔴 Low | 승인 필수 | Preview + Double-check + Rollback Plan 필수 |
| **외부 API 호출** | 🔴 Low | 승인 필수 | Rate Limit + 결과 검증 + Audit Log |

#### 3.6.2 에이전트별 권한 경계

```python
# agent_permissions.yaml - 각 SEOCHO Agent의 접근 허용 범위
agent_permissions:
  router_agent:
    allowed_actions: [CLASSIFY, ROUTE]
    forbidden_actions: [EXECUTE_QUERY, MODIFY_DATA]
    max_context_tokens: 4000
    
  graph_agent:
    allowed_databases: [datahub_db, insight_kb_db]
    forbidden_databases: [system_db, audit_db]
    allowed_operations: [READ]
    max_results: 10000
    
  graph_dba:
    allowed_databases: [insight_kb_db]
    allowed_operations: [READ, CYPHER_EXECUTE]
    forbidden_patterns: ["DELETE", "DROP", "CREATE INDEX"]
    query_timeout_ms: 30000
    
  supervisor:
    allowed_actions: [AGGREGATE, RESOLVE_CONFLICT, GENERATE_RESPONSE]
    forbidden_actions: [DIRECT_DB_ACCESS]
    audit_required: true
```

#### 3.6.3 NL2SQL 사전 스키마 검증 레이어

NL2SQL 환각 방지를 위해 SQL 생성 후 실행 전 스키마 검증을 추가합니다:

```
[자연어 질문] → [Vanna SQL 생성] → [스키마 검증] → [실행] → [결과]
                                         │
                                    ┌────▼────┐
                                    │DataHub  │
                                    │메타데이터│
                                    │ 테이블/ │
                                    │ 컬럼 확인│
                                    └─────────┘
```

**검증 항목:**
1. 생성된 SQL의 모든 테이블이 DataHub 카탈로그에 존재하는지 확인
2. 참조된 컬럼이 해당 테이블에 실제 존재하는지 확인
3. 사용자 권한 범위 내 테이블/컬럼인지 확인
4. 검증 실패 시 SQL 실행 차단 + 사용자에게 오류 안내

**현재 방어선 대비 개선:**
- 기존: Quality Gate hallucination_rate ≤ 0.05 (사후 측정)
- 개선: 사전 스키마 검증으로 존재하지 않는 테이블/컬럼 참조 원천 차단

---

### 3.9 Dashboard Promotion & 자동화 보고 (Shaper 연동)

> **신규 섹션 — Vanna NL2SQL ↔ Shaper BI 통합**

Vanna로 생성된 SQL 질의를 Shaper 대시보드로 승격(Promotion)하여 반복 KPI 모니터링, PDF/Excel 자동 보고, 임베디드 분석 기능을 제공합니다. 이를 통해 DataNexus는 "질문-응답(Pull)" 모델에서 "대시보드-리포트 자동 전송(Push)" 모델로 확장됩니다.

#### 3.9.1 Dashboard Promotion 워크플로

```txt
┌──────────────────────────────────────────────────────────────────┐
│                    DataNexus Chat UI                               │
│                                                                    │
│  사용자: "지난 분기 VIP 고객 매출 추이 보여줘"                     │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ Vanna NL2SQL → SQL 생성 → 실행 → 차트/테이블 렌더링       │   │
│  └────────────────────────────────┬───────────────────────────┘   │
│                                   │                               │
│  [📌 대시보드로 저장] [📄 리포트 예약] [📎 임베디드 코드 복사]    │
│                                                                    │
└──────────────────────────────────┬────────────────────────────────┘
                                   │
                          ┌────────▼────────┐
                          │ Promotion Engine │
                          │                  │
                          │ ① SQL 추출       │
                          │ ② 파라미터화     │
                          │ ③ Shaper 등록    │
                          │ ④ 보안 연동      │
                          └────────┬─────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
         ┌──────▼──────┐  ┌───────▼──────┐  ┌───────▼───────┐
         │ 정적 대시보드│  │ 자동 리포트  │  │ 임베디드 분석 │
         │ (Shaper UI) │  │ (PDF/Excel)  │  │ (React SDK)   │
         │             │  │              │  │               │
         │ • KPI 모니터│  │ • 예약 발송  │  │ • iframe-free │
         │ • 실시간 갱신│  │ • 링크 공유  │  │ • 화이트라벨  │
         │ • 필터 인터랙│  │ • 비밀번호   │  │ • JWT RLS     │
         └─────────────┘  └──────────────┘  └───────────────┘
```

#### 3.9.2 기능 상세

| 기능 | 설명 | 기술 스택 | Phase |
|------|------|----------|-------|
| **Dashboard Promotion** | Vanna 생성 SQL을 Shaper 대시보드로 승격, 파라미터화된 SQL 자동 등록 | Vanna API → Shaper REST API | Phase 1.5 |
| **정적 대시보드** | 반복 조회 KPI를 실시간 갱신 대시보드로 구성, 필터 인터랙션 지원 | Shaper + DuckDB | Phase 1.5 |
| **PDF/Excel 자동 보고** | 대시보드를 PDF, PNG, CSV, Excel 형식으로 자동 생성 및 예약 발송 | Shaper Task Engine | Phase 2 |
| **임베디드 분석** | React SDK를 통해 DataNexus Frontend에 iframe 없이 대시보드 임베딩 | Shaper React SDK + JWT | Phase 2 |
| **링크 공유** | 비밀번호 보호 링크로 외부 이해관계자에게 대시보드/리포트 안전 공유 | Shaper Share Link | Phase 2 |

#### 3.9.3 보안 통합 (JWT Row-level Security)

DataNexus와 Shaper 간의 Row-level Security를 JWT 토큰으로 통합합니다:

> 📌 **구현 코드 → Implementation_Guide_final.md 이관.** 인터페이스 계약:
> - **클래스:** `ShaperSecurityBridge(datanexus_auth, shaper_admin_api)`
> - **핵심 메서드:** `sync_rls_policy(user: User) → ShaperToken`
> - **행동:** DataNexus JWT → Shaper RLS 정책 동기화, 역할 기반 행 수준 보안

#### 3.9.4 Vanna ↔ Shaper 연동 인터페이스

> 📌 **구현 코드 → Implementation_Guide_final.md 이관.** 인터페이스 계약:
> - **클래스:** `DashboardPromotionService(shaper_client, lineage_store)`
> - **핵심 메서드:** `promote(query_log_id, user, options) → PromotionResult`
> - **행동:** 검증된 SQL → Shaper 대시보드 생성, 파라미터화, Lineage 기록
> - **Phase 1.5 범위:** 기본 promote + simplified lineage (query_log_id, dashboard_id, created_at)

#### 3.9.5 역할별 활용 시나리오

| 역할 | 활용 시나리오 | 기능 |
|------|-------------|------|
| **CEO/CFO** | 주간 매출 리포트를 PDF로 자동 수신 | 자동 보고 + 예약 발송 |
| **마케터** | 캠페인 성과 대시보드를 외부 파트너에게 링크 공유 | 비밀번호 보호 링크 공유 |
| **MD/상품기획** | 카테고리별 판매 추이를 사내 포털에 임베딩 | 임베디드 분석 (React SDK) |
| **운영자** | 재고 현황을 실시간 대시보드로 상시 모니터링 | 정적 대시보드 |
| **분석가** | 복잡한 NL2SQL 결과를 대시보드로 저장 후 반복 활용 | Dashboard Promotion |

#### 3.9.6 설계 원칙 (Pull → Push 전환)

> **DataNexus의 Shaper 연동은 "Chat → Dashboard" 단방향 승격 모델이되, 정합성 감시와 컨텍스트 복귀는 양방향입니다.**
>
> - **Chat (Vanna):** 탐색적 분석, 일회성 질의, 새로운 인사이트 발굴 — Pull 모델
> - **Dashboard (Shaper):** 반복 KPI 모니터링, 정기 보고, 외부 공유 — Push 모델
> - **승격 기준:** 동일 질의가 3회 이상 반복되면 자동으로 Dashboard Promotion 제안
> - **되돌림:** 대시보드에서 "Chat에서 질문하기" 버튼으로 Vanna 탐색 모드로 복귀 가능 (§3.9.9 컨텍스트 보존)
> - **데이터 흐름 방향성:** SQL 승격은 Chat → Dashboard 단방향이지만, 메타데이터 흐름(Lineage 추적, Staleness 신호)은 역방향으로도 작동
> - **정합성 보장:** Glossary 변경 시 영향받는 대시보드를 자동 감지하여 STALE 마킹 (§3.9.8)

```txt
┌──────────────────────────────────────────────────────────────────────────┐
│                     데이터 흐름 vs 메타데이터 흐름                        │
│                                                                          │
│  [데이터 흐름 — 단방향]                                                  │
│   Chat (Vanna) ──SQL 승격──▶ Dashboard (Shaper)                         │
│                                                                          │
│  [메타데이터 흐름 — 양방향]                                              │
│   Chat (Vanna) ◀──Lineage 추적──▶ Dashboard (Shaper)                    │
│                 ◀──Staleness 신호── Glossary 변경 감지                   │
│                 ◀──컨텍스트 복원── "Chat에서 질문하기"                    │
└──────────────────────────────────────────────────────────────────────────┘
```

#### 3.9.7 Promotion Lineage 관리

> ⏳ **Phase 2.0 이관 항목** — MVP(Phase 1.0~1.5)에서는 `promote_to_dashboard()` 기본 워크플로만 구현합니다. Drift 추적, Staleness 감지, 양방향 컨텍스트 보존(§3.9.7~3.9.9)은 운영 안정화 이후 Phase 2.0에서 착수합니다.

> **신규 섹션 — 승격 후 SQL 분기(Drift) 추적**

Shaper는 SQL-First 플랫폼이라 대시보드 내에서 SQL을 직접 편집할 수 있고, Git 기반 워크플로로 버전 관리됩니다. 사용자가 대시보드에서 SQL을 수정하는 순간 원본 Vanna 쿼리와의 연결이 끊어지는 문제(SQL Drift)를 방지하기 위해 Promotion Lineage를 관리합니다.

##### 3.9.7.1 DashboardLineage 데이터 모델

> 📌 **Phase 2.0 구현 예정.** 데이터 모델 계약:
> - **모델:** `DashboardLineage(BaseModel)` — 12개 필드 (query_log_id, dashboard_id, sql_hash, glossary_deps, drift_status 등)
> - **MVP 대체:** simplified 3필드 (query_log_id, dashboard_id, created_at)

##### 3.9.7.2 Drift 상태 머신

```txt
                    ┌───────────────────────────────────┐
                    │           SYNCED                    │
                    │  (원본 SQL = Shaper SQL)           │
                    └──────┬────────────────┬────────────┘
                           │                │
          사용자가 Shaper에서│      Glossary Term│
          SQL 직접 편집      │      정의 변경    │
                           │                │
                    ┌──────▼──────┐  ┌──────▼──────┐
                    │  MODIFIED   │  │   STALE     │
                    │             │  │             │
                    │ Shaper SQL이│  │ 원본 SQL의  │
                    │ 원본과 다름 │  │ 전제 조건이 │
                    │             │  │ 변경됨      │
                    └──────┬──────┘  └──────┬──────┘
                           │                │
                    재승격(RE_PROMOTE)       │
                    또는 동기화 확인         │
                           │                │
                    ┌──────▼────────────────▼────────────┐
                    │         SYNCED (복원)               │
                    └────────────────────────────────────┘
```

| 상태 | 의미 | 트리거 | 권장 조치 |
|------|------|--------|----------|
| **SYNCED** | 원본 Vanna SQL과 Shaper SQL이 동일 | 승격 직후 / 재승격 완료 | 없음 (정상) |
| **MODIFIED** | 사용자가 Shaper에서 SQL을 직접 편집 | Shaper SQL 해시 변경 감지 (주기적 폴링) | 관리자에게 알림, 수동 확인 |
| **STALE** | 참조하는 Glossary Term 정의가 변경됨 | §3.9.8 StalenessDetector가 마킹 | 대시보드 소유자에게 RE_PROMOTE 권고 알림 |

##### 3.9.7.3 Drift 감지 스케줄러

> 📌 **Phase 2.0 구현 예정.** 인터페이스 계약:
> - **클래스:** `DriftDetectionScheduler(lineage_store, shaper_client)`
> - **핵심 메서드:** `check_drift(lineage: DashboardLineage) → DriftResult`
> - **행동:** 원본 SQL 해시 vs 현재 Shaper SQL 비교, SYNCED/MODIFIED/STALE 상태 전이

#### 3.9.8 Glossary-Dashboard 정합성

> ⏳ **Phase 2.0 이관 항목** — 상세 설계는 §3.9.7 배너 참조.

> **신규 섹션 — Glossary 변경의 대시보드 역전파**

§4.3.1의 동기화 파이프라인(DataHub MCL → Kafka → DozerDB/Vanna/ApeRAG)은 Glossary 변경을 하위 시스템에 전파하지만, 이미 승격된 Shaper 대시보드는 전파 대상에 포함되어 있지 않습니다. "순매출" 정의가 변경되면 Vanna는 재학습되지만, 기존 대시보드 10개는 이전 SQL을 계속 실행합니다.

이 문제를 기존 Kafka Consumer 체인에 핸들러를 추가하는 방식으로 해결합니다 (아키텍처 변경 없음).

##### 3.9.8.1 동기화 파이프라인 확장

```txt
기존 §4.3.1 파이프라인:
DataHub MCL → Kafka → ┬─ DozerDB 동기화
                       ├─ Vanna 재학습
                       └─ ApeRAG 재색인

확장 후:
DataHub MCL → Kafka → ┬─ DozerDB 동기화
                       ├─ Vanna 재학습
                       ├─ ApeRAG 재색인
                       └─ 🆕 Dashboard Staleness Detector (§3.9.8)
```

##### 3.9.8.2 DashboardStalenessDetector

> 📌 **Phase 2.0 구현 예정.** 인터페이스 계약:
> - **클래스:** `DashboardStalenessDetector(glossary_change_stream, lineage_store)`
> - **핵심 메서드:** `on_glossary_change(event: MCLEvent) → List[StaleDashboard]`
> - **행동:** Glossary 변경 → 의존 대시보드 식별 → STALE 마킹 + 소유자 알림

##### 3.9.8.3 장애 시나리오 연계

> **📌 PRD_03 §4.3.1.1 장애 시나리오에 F-6 추가 (상호 참조)**

| 유형 | 시나리오 | 영향 | 심각도 |
| :--- | :--- | :--- | :--- |
| **F-6** | Glossary 변경 후 대시보드 Staleness 미감지 | 구식 SQL로 생성된 KPI가 경영진에게 보고됨 | **HIGH** |

F-6의 상세 복구 전략은 [PRD_03 §4.3.1.1](./PRD_03_Data_Pipeline_final.md)을 참조합니다.

#### 3.9.9 양방향 컨텍스트 보존

> ⏳ **Phase 2.0 이관 항목** — 상세 설계는 §3.9.7 배너 참조.

> **신규 섹션 — 대시보드에서 Chat으로 복귀 시 컨텍스트 유실 방지**

§3.9.6의 "Chat에서 질문하기" 버튼은 대시보드에서 Chat으로 복귀하는 기능이지만, 현재 설계에서는 원본 자연어 질의만 Chat에 전달됩니다. 파라미터화 과정에서 추가된 필터 조건, 사용자가 Shaper에서 수정한 SQL 변경사항, 해당 대시보드의 STALE 여부 등 컨텍스트가 유실됩니다.

##### 3.9.9.1 DashboardReturnService

> 📌 **Phase 2.0 구현 예정.** 인터페이스 계약:
> - **클래스:** `DashboardReturnService(lineage_store, chat_service)`
> - **핵심 메서드:** `prepare_return_context(dashboard_id, user) → ReturnContext`
> - **행동:** Dashboard → Chat 복귀 시 Drift 상태별 컨텍스트 주입, SQL diff 비교

##### 3.9.9.2 Drift 상태별 복귀 UX

| Drift 상태 | 복귀 시 동작 | 사용자에게 보이는 메시지 |
|-----------|------------|----------------------|
| **SYNCED** | 원본 자연어 질의를 Chat에 자동 입력 | "대시보드의 원본 질의로 새 대화를 시작합니다." |
| **MODIFIED** | SQL 변경 diff를 시스템 메시지로 주입 + 원본 질의 표시 | "⚠️ 이 대시보드의 SQL이 원본과 다릅니다. 변경사항을 확인하세요." |
| **STALE** | 변경된 Glossary Term 목록 표시 + 원본 질의 자동 재실행 | "🔄 '순매출' 정의가 변경되었습니다. 최신 정의로 다시 질의합니다." |

##### 3.9.9.3 재승격(RE_PROMOTE) 워크플로

STALE/MODIFIED 상태의 대시보드는 다음 워크플로로 재승격합니다:

```txt
[STALE 대시보드] → [Chat에서 질문하기]
    │
    ▼
[Chat 세션: 최신 Glossary 반영하여 자동 재질의]
    │
    ▼
[사용자: 결과 확인 → "대시보드로 저장" (RE_PROMOTE)]
    │
    ▼
[Promotion Engine: 기존 Lineage 업데이트 (새 SQL 해시, SYNCED 복원)]
    │
    ▼
[기존 대시보드 ID 유지, SQL만 교체 → 스케줄/공유 설정 보존]
```

> **📌 핵심:** RE_PROMOTE는 기존 대시보드 ID를 유지하고 SQL만 교체합니다. 이를 통해 예약 리포트 설정, 공유 링크, 임베디드 코드가 변경 없이 보존됩니다.

---

### 3.10 NL2SQL 자가 학습 피드백 루프 (Self-Reinforcing Loop)

> **📌 배경:** Vanna 2.0의 Tool Memory는 성공한 쿼리를 자동 학습하여 정확도를 지속 개선하지만, 잘못된 쿼리가 학습되면 RAG Store가 오염되어 정확도가 하락한다. GPT-4o 단독 정확도가 51%에 불과한 상황([PRD_05 §5.6.1](./PRD_05_Evaluation_Quality_final.md))에서, Tool Memory의 품질 보호는 정확도 80%+ 달성의 핵심 전제 조건이다.

#### 3.10.1 피드백 루프 아키텍처

```txt
[사용자 질문] → [Vanna SQL 생성] → [SQL 실행]
    │                                    │
    │                          ┌─────────▼─────────┐
    │                          │ 사용자 피드백      │
    │                          │ 👍 정확 / 👎 부정확 │
    │                          └─────────┬─────────┘
    │                                    │
    │                    ┌───────────────┼───────────────┐
    │                    │               │               │
    │              ┌─────▼─────┐  ┌──────▼──────┐  ┌────▼────┐
    │              │ 👍 승인    │  │ 👎 + 수정SQL │  │ 👎 단순 │
    │              │ 자동 학습  │  │ DBA 큐 전송  │  │ 로그만  │
    │              └─────┬─────┘  └──────┬──────┘  └────┬────┘
    │                    │               │              │
    │              ┌─────▼──────────────▼──────────────▼────┐
    │              │        Vanna Tool Memory               │
    │              │  (tenant_id 파티션 격리)                │
    │              └────────────────────────────────────────┘
    │
    └─→ [Query Log 저장 (§F.4.1 query_logs)]
```

#### 3.10.2 학습 데이터 품질 보호 규칙

| 규칙 | 설명 |
| :--- | :--- |
| **자동 학습 조건** | 사용자 👍 + SQL 실행 성공 + Schema Validation(§3.6.3) 통과 |
| **수동 검토 조건** | 사용자가 수정 SQL을 제출한 경우 → DBA 검토 큐 |
| **학습 거부 조건** | SQL 실행 실패, Schema Validation 미통과, 금지 패턴(DELETE/DROP/TRUNCATE) 포함 |
| **롤백** | 학습 후 EX 정확도 하락 감지(§5.6 모니터링) 시 최근 N개 학습 데이터 자동 격리 |
| **테넌트 격리** | 모든 학습 데이터는 tenant_id 기반 벡터 컬렉션 파티션에 격리 저장 |

#### 3.10.3 학습 승인 워크플로 상세

```txt
[사용자: Q-SQL 쌍 제출 또는 👍 피드백]
    │
    ▼
┌──────────────────────────────────────────┐
│           자동 검증 게이트               │
│  ① SQL 구문 유효성 (sqlfluff parse)     │
│  ② Schema Validation (§3.6.3)           │
│  ③ 금지 패턴 스캔 (DML 차단)           │
│  ④ 중복 Q-SQL 검출 (유사도 > 0.9)      │
└──────────────┬───────────────────────────┘
               │
         ┌─────▼─────┐
         │ 통과 여부  │
         └─┬───────┬─┘
           │       │
     ┌─────▼──┐  ┌─▼──────────┐
     │ 통과   │  │ 실패       │
     │        │  │ 반려 + 안내│
     └─────┬──┘  └────────────┘
           │
     ┌─────▼──────────────────────────────┐
     │ 분기: 피드백 유형                   │
     ├─ 👍 (원본 SQL 승인) → 즉시 학습    │
     └─ 수정 SQL 제출 → DBA 검토 큐       │
                            │              │
                      ┌─────▼─────┐        │
                      │ DBA 판단  │        │
                      ├─ 승인 → 학습       │
                      └─ 반려 → 사유 안내  │
     └─────────────────────────────────────┘
```

#### 3.10.4 Vanna Tool Memory ↔ Graphiti 이중 메모리 경계 (재확인)

이 피드백 루프는 CLAUDE.md에 정의된 이중 메모리 경계를 엄격히 준수한다:

| 데이터 유형 | 저장소 | 근거 |
| :--- | :--- | :--- |
| SQL 실행 결과 (Q-SQL 쌍) | **Vanna Tool Memory만** | SQL 패턴 학습은 NL2SQL 정확도 전용 |
| 비즈니스 사실/해석 패턴/KPI 정의 변경 | **Graphiti만** | 비즈니스 맥락은 에이전트 장기 기억 영역 |
| SQL + 비즈니스 맥락 복합 항목 | **분할 저장** | SQL은 Vanna, 맥락은 Graphiti |
| 사용자 선호도 (시각화, 출력 형식) | **Graphiti만** | UX 개인화는 NL2SQL과 무관 |

> **📌 안티패턴:** Vanna training에 비즈니스 해석 컨텍스트를 혼합 주입하지 않는다. SQL 쌍만 학습하고, 해석은 Graphiti에 분리 저장한다.

#### 3.10.5 정확도 모니터링 및 롤백

Tool Memory에 새로운 Q-SQL 쌍이 학습될 때마다, 주기적으로 평가 데이터셋([PRD_03 §4.2.1](./PRD_03_Data_Pipeline_final.md) D-6)에 대한 EX(Execution Accuracy)를 측정한다.

```python
# 정확도 롤백 판단 로직 (개념 설계)
ACCURACY_THRESHOLD = 0.80  # MVP 기준 (PRD_05 §5.6.1)
ROLLBACK_WINDOW = 10       # 최근 학습 건수

async def monitor_tool_memory_quality(eval_dataset, vanna_agent):
    current_ex = await run_evaluation(eval_dataset, vanna_agent)
    
    if current_ex < ACCURACY_THRESHOLD:
        # 최근 N건 학습 데이터 격리 (삭제가 아닌 비활성화)
        recent_entries = await vanna_agent.get_recent_training(limit=ROLLBACK_WINDOW)
        for entry in recent_entries:
            await vanna_agent.quarantine_training(entry.id)
        
        # 격리 후 재측정
        post_rollback_ex = await run_evaluation(eval_dataset, vanna_agent)
        
        # Opik 알림 발행
        await notify_opik(
            event="tool_memory_rollback",
            before_ex=current_ex,
            after_ex=post_rollback_ex,
            quarantined_count=ROLLBACK_WINDOW
        )
```

> **📌 참조:**
> - Training 데이터 포맷 및 품질 게이트: [PRD_03 §4.2.4](./PRD_03_Data_Pipeline_final.md)
> - Vanna 한계점 L-2 보완 상세: [부록 B.8.6](./PRD_Appendix_AB_final.md)
> - Baseline 정확도 근거: [PRD_05 §5.6.1](./PRD_05_Evaluation_Quality_final.md)

---

### 3.7 MVP 범위 조정 권고

> **⚠️ MVP 범위 과잉 문제 (리뷰 보고서 §1-2)**

현재 PRD의 Phase 1 MVP 범위가 과도하게 넓습니다. 아래 항목의 Phase 조정을 권고합니다:

| 현재 Phase | 기능 | 권고 Phase | 사유 |
|-----------|------|-----------|------|
| Phase 1 | Graphiti 시간 인식 KG (§4.3.10) | **Phase 3 R&D** | bi-temporal 모델은 핵심 기능 안정화 후 도입 |
| Phase 1 | 20+ Predicate 세분화 (§4.4.1) | **Phase 2** | MVP는 기본 5~7개 핵심 관계만 → Phase 2에서 확장 |
| Phase 1 | 4단계 품질 게이트 전체 (§5.3) | **Unit+E2E만** | MVP는 Stage 1(Unit) + Stage 4(E2E)만 필수 |
| Phase 1 | 외부 KG 자동 구축 (§4.3.9) | **Phase 2+** | 내부 온톨로지 안정화가 선행 필요 |

---

### 3.8 설계 원칙: 에이전트 학습 vs 환경 개선의 구분

> **신규 섹션 — 핵심 철학 "시행착오 비용 최소화" 구체화**

DataNexus의 여러 메커니즘이 "에이전트가 점점 똑똑해진다"는 인상을 줄 수 있으나, 실제로 개선되는 것은 에이전트가 참조하는 환경(데이터, 규칙, 온톨로지)입니다. 이 구분을 명확히 하지 않으면 "에이전트에게 맡기면 알아서 좋아지겠지"라는 위험한 가정으로 이어집니다.

#### 3.8.1 개선 주체 식별 매트릭스

| 메커니즘 | 실제 개선 주체 | 에이전트의 역할 | 사람의 역할 (품질 책임) |
|----------|---------------|----------------|----------------------|
| Vanna Tool Memory ([PRD_Appendix_AB §B.8](./PRD_Appendix_AB_final.md)) | Training Data (Qdrant 벡터 스토어) | 패턴 매칭 실행자 | 오답 제거 + 신규 패턴 품질 검증 |
| Graphiti 에피소드 (§4.3.10) | Knowledge Graph (DozerDB) | 사실 기록자 | 기록 정확성 감사 + 주기적 정리 |
| CLAUDE.md 축적 (Template §축적 정책) | 규칙 파일 시스템 | 규칙 소비자 | 규칙 작성 + 승격 결정 + 폐기 판단 |
| 온톨로지 갱신 (§4.4) | DataHub Glossary | 컨텍스트 활용자 | 도메인 전문가의 용어 정제 + CQ 검증 |
| NL2SQL 스키마 검증 (§3.6.3) | DataHub 메타데이터 카탈로그 | 검증 규칙 실행자 | 메타데이터 최신성 유지 |

#### 3.8.2 운영 함의

**Vanna Tool Memory:** 성공한 쿼리가 자동 학습되지만, 잘못된 쿼리가 학습되면 오히려 정확도가 하락합니다. 주기적인 Training Data 감사(오답 제거)가 필수이며, 이는 자동화할 수 없는 사람의 판단 영역입니다.

**Graphiti 에피소드:** 에이전트가 축적한 시간축 사실(Fact Timeline)이 증가해도, 잘못된 사실이 누적되면 추론 품질이 저하됩니다. Episode Inspector(§3.5.6)를 통한 정기 감사가 필요합니다.

**CLAUDE.md 축적:** Distill 패턴으로 규칙이 자동 승격되지만, 승격 결정과 더 이상 유효하지 않은 규칙의 폐기는 사람이 수행합니다. 규칙의 양이 늘어난다고 품질이 올라가는 것이 아닙니다.

#### 3.8.3 핵심 원칙

> **에이전트가 "성장"하는 것처럼 보이는 모든 메커니즘의 실제 품질 책임은 환경을 설계하고 검증하는 사람에게 있습니다.**

이 원칙은 SEOCHO 프로덕션 에이전트와 Claude Code 개발 에이전트 양쪽 모두에 동일하게 적용됩니다.

### 3.11 구조화된 분석 워크플로우 (alive-analysis 통합)

> **📋 Phase 범례:** Phase 1.5 기본 도입, Phase 2.0 고도화
> **관련 문서:** Implementation Strategy §23, Implementation Guide STEP 24, CLAUDE.md analysis-workflow.md

#### 3.11.1 도입 배경

DataNexus의 NL2SQL 파이프라인(Vanna)과 GraphRAG(ApeRAG)는 **데이터 접근**을 자동화한다. 그러나 검색된 데이터를 **방어 가능한 인사이트와 의사결정으로 전환**하는 분석 추론 과정은 구조화되어 있지 않았다. alive-analysis는 이 빈 공간을 채우는 구조화된 분석 사고 프레임워크이다.

**핵심 원칙:** AI 에이전트는 분석 결론을 생성하지 않는다. 구조화된 질문을 하고, 체크리스트를 강제하며, 반례를 표면화한다. 모든 분석적 판단은 사람이 내린다.

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  DataNexus   │     │ alive-analysis  │     │  분석 지식베이스  │
│  Data Access │────▶│  ALIVE Loop     │────▶│  Git-tracked MD  │
│  (Vanna/RAG) │     │  (분석 추론)    │     │  (검색 가능)     │
└──────────────┘     └─────────────────┘     └──────────────────┘
```

#### 3.11.2 ALIVE 루프와 SEOCHO 에이전트 연계

##### ALIVE 루프 5단계

| 단계 | 영문 | 역할 | DataNexus 연계 |
|------|------|------|---------------|
| **A** | Ask | 질문 정의: 범위, 가설 트리, 성공 기준 | Router Agent가 질문 유형(Investigation/Modeling/Simulation) 분류 |
| **L** | Look | 데이터 관찰: 품질 점검, 세분화, 교란변수 | Vanna NL2SQL + DataHub 메타데이터로 데이터 품질 자동 점검 |
| **I** | Investigate | 분석: 가설 검증, 다중 렌즈 프레임워크 | ApeRAG 문서 Q&A + DozerDB 그래프 추론으로 다각도 분석 지원 |
| **V** | Voice | 커뮤니케이션: "So what → Now what", 청중별 메시징 | 5개 페르소나(CEO/CFO, 마케터, MD, 운영자, 분석가)별 응답 최적화 (PRD_07 §11.12.3 연계) |
| **E** | Evolve | 발전: 후속 질문, 임팩트 추적, 회고 | Graphiti 시간축 메모리에 분석 결과 축적 (Phase 3) |

##### 분석 유형별 에이전트 라우팅

| 분석 유형 | 트리거 질문 패턴 | 주요 에이전트 | 출력 |
|----------|----------------|-------------|------|
| **Investigation** | "왜 X가 발생했는가?" | Vanna SQL Agent + Graph DBA | 원인 분석 보고서 |
| **Modeling** | "Y를 예측할 수 있는가?" | Vanna SQL Agent + RAG Search | 예측 모델 등록 + 드리프트 모니터링 설정 |
| **Simulation** | "Z라면 어떻게 되는가?" | Graph DBA (Cypher What-if) + Vanna | 시나리오 비교 테이블 |

##### 모드 선택 기준

| 모드 | 대상 | 출력 | 승격 조건 |
|------|------|------|----------|
| **Quick** | PM, 비분석가, 탐색적 질문 | 단일 마크다운 파일 | 복잡도 증가 시 자동 Full 승격 |
| **Full** | 데이터 분석가, 경영진 보고용 | 5개 버전 관리 마크다운 (단계별 1개) | — |

#### 3.11.3 실험 모듈과 Ablation Study 연계

alive-analysis의 실험 모듈은 A/B 테스트 생명주기를 구조화한다. DataNexus의 Ablation Study(PRD_05 §5.4)와 직접 연계하여 실험 품질을 표준화한다.

**실험 생명주기:** Design → Validate → Analyze → Decide → Learn

| 실험 모듈 기능 | DataNexus Ablation Study 연계 | Phase |
|--------------|------------------------------|-------|
| 사전등록 (Pre-registration) | 실험 M1-M4, A1-A6의 가설과 기대 결과를 사전 문서화 | 1.5 |
| SRM (Sample Ratio Mismatch) 검사 | 실험 데이터셋 분할 비율 검증 | 1.5 |
| 가드레일 메트릭 모니터링 | Hallucination Rate, Cache Hit Rate 등 안전 한계선 자동 감시 | 2.0 |
| 실험 아카이브 | Opik Trace 결과와 분석 파일을 함께 Git 추적 | 2.0 |

#### 3.11.4 메트릭 모니터링과 Opik 평가 연계

alive-analysis의 4단계 메트릭 분류 체계를 DataNexus의 평가 지표(PRD_05 §5.1)에 매핑한다.

| alive-analysis 메트릭 계층 | 역할 | DataNexus 대응 지표 |
|---------------------------|------|-------------------|
| **North Star** | 최종 사용자 가치 대리 | EX (Execution Accuracy) |
| **Leading** | 품질 선행 지표 | Query Router Accuracy, CQ Pass Rate, Schema Compliance |
| **Guardrail** | 안전 한계선 (절대 위반 불가) | Hallucination Rate ≤ 0.05 (ratio), Cache Hit Rate ≥ 0.70 (ratio) |
| **Diagnostic** | 원인 분석용 세부 | CTE, KVCache Cost, VES, Deterministic Query Rate |

**모니터링 에스컬레이션 규칙:**
- Guardrail 메트릭 2회 연속 위반 → 자동 알림 + Opik 대시보드 하이라이트
- North Star 메트릭 하락 추세 3일 연속 → Leading/Diagnostic 메트릭 자동 드릴다운 분석 트리거

#### 3.11.5 분석 파일 관리

**고유 ID 체계:**
- Quick 모드: `Q-YYYY-MMDD-NNN` (예: Q-2026-0315-001)
- Full 모드: `F-YYYY-MMDD-NNN` (예: F-2026-0315-001)

**저장 구조:**
```
.analysis/
├── investigations/     ← "왜?" 유형 분석
├── models/             ← "예측" 유형 분석
├── simulations/        ← "만약?" 유형 분석
├── experiments/        ← A/B 테스트 기록
├── monitoring/         ← 메트릭 모니터링 설정 및 이력
└── status.md           ← 분석 상태 추적
```

**Git 추적 규칙:**
- 모든 분석 파일은 프로젝트 레포에 커밋 (`.analysis/` 디렉토리)
- 교차참조 탐지: 동일 주제 기존 분석이 있으면 자동 링크
- 상충 발견 알림: 기존 분석 결론과 상충하는 결과 발견 시 경고

#### 3.11.6 Phase별 적용 계획

| Phase | 적용 범위 | 산출물 |
|-------|----------|-------|
| **Phase 1.5** | alive-analysis 설치, Quick 모드 기본 워크플로우, Investigation 유형 우선 적용 | `.analysis/` 디렉토리 초기화, 기본 SKILL.md 커스터마이징 |
| **Phase 2.0** | Full 모드 활성화, 실험/모니터링 모듈 Opik 연계, Modeling/Simulation 유형 추가 | Ablation Study 사전등록 자동화, 4단계 메트릭 대시보드 |
| **Phase 3+** | Graphiti 시간축 메모리와 분석 지식베이스 통합, 도메인별 커스텀 SKILL.md | 시계열 분석 인사이트 누적, Education 모듈 활용 온보딩 |

#### 3.11.7 교차 참조

| 참조 대상 | 위치 | 관계 |
|----------|------|------|
| SEOCHO Agent 아키텍처 | PRD_01 §2, PRD_02 §3 | 분석 워크플로우의 에이전트 실행 환경 |
| 평가 지표 (SSOT) | PRD_04a §4.8, PRD_05 §5.1 | 메트릭 4단계 분류 매핑 |
| Ablation Study 설계 | PRD_05 §5.4 | 실험 모듈 연계 |
| Dashboard Promotion | PRD_02 §3.9 | 분석 결과의 대시보드 승격 워크플로우 |
| NL2SQL 자가 학습 | PRD_02 §3.10 | 분석 과정에서 생성된 쿼리의 피드백 루프 |
| 5개 페르소나 응답 | PRD_07 §11.12.3 | Voice 단계의 청중별 커뮤니케이션 |
| ALIVE 루프 구현 전략 | Implementation Strategy §23 | 통합 아키텍처 및 설계 근거 |
| ALIVE 루프 설치 가이드 | Implementation Guide STEP 24 | 실행 레시피 |
| analysis-workflow.md | CLAUDE.md | 도메인 규칙 정의 |
| alive-analysis 레포 | PRD_06 §8.12 | 원본 레포지토리 참조 |
