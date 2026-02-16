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

```python
class MultiDatabaseRouter:
    """온톨로지 기반 데이터베이스 라우팅 [Phase 2+]"""

    def select_database(self, query: str, ontology_context: dict) -> str:
        """쿼리와 온톨로지 컨텍스트 기반 DB 선택"""
        domain = ontology_context.get("domain")

        database_mapping = {
            "Finance": "financial_db",
            "Retail": "retail_db",
            "HR": "hr_db"
        }

        return database_mapping.get(domain, "general_db")
```

#### 3.5.6 Graphiti Memory Debugger (Agent 메모리 시각화) [Phase 3 R&D]

> **📌 Phase 3 R&D:** 이 기능은 MVP 범위가 아닙니다. Phase 3 에이전트 메모리 도입 시 구현합니다.

Agent Studio에 Graphiti 기반 **시간축 사실 추적 시각화** 기능을 추가합니다. 에이전트가 축적한 지식(사실, 관계)의 변화 이력을 타임라인으로 시각화하여 디버깅과 감사를 지원합니다.

| 기능 | 설명 | 기술 스택 |
|------|------|----------|
| **Fact Timeline** | 특정 엔터티/관계의 시간별 변화 이력 시각화 | Graphiti Bi-Temporal |
| **Episode Inspector** | 에피소드(대화/이벤트)별 지식 변화 추적 | Graphiti Episode |
| **Community Map** | 자동 탐지된 엔터티 클러스터 시각화 | Label Propagation |
| **Memory Search** | 에이전트 장기 기억 하이브리드 검색 (Semantic + BM25 + Graph BFS) | Graphiti Hybrid |

상세 구현은 [PRD_04c_Ontology_Future.md §4.3.10](./PRD_04c_Ontology_Future.md) (Graphiti 기반 시간 인식 지식그래프 및 에이전트 메모리 계층)을 참조합니다. 장시간 세션에서의 컨텍스트 보존 전략은 [PRD_04c §4.3.10.10](./PRD_04c_Ontology_Future.md) (OpenClaw 적응 기법)을 참조합니다.


---

### 3.6 에이전트 자율성-통제 균형 프레임워크 (보강: Moltbook 교훈 + 리뷰 반영)

> **신규 섹션 — Ecosystem Analysis §3 + 리뷰 보고서 §5 보안 구체화**

Moltbook 사례에서 1.5M 에이전트가 수 분 내 보안 취약점을 노출한 교훈을 반영하여, SEOCHO Multi-Agent에도 명시적 자율성-통제 균형을 설계합니다.

#### 3.6.1 작업 유형별 자율성 수준

| 작업 유형 | 자율성 수준 | 실행 정책 | 안전장치 |
|-----------|-----------|----------|---------|
| **SELECT 쿼리** (읽기 전용) | 🟢 High | 자동 실행 | 스키마 검증 + 결과 행 수 제한 (max 10,000) |
| **문서 검색** (RAG) | 🟢 High | 자동 실행 | 권한 필터 + 출처 표시 (Source Attribution) |
| **온톨로지 초안** (Drafter) | 🟡 Medium | Human-in-the-loop | LLM 초안 → 전문가 검토 → 승인 ([PRD_04a §4.5.3](./PRD_04a_Ontology_Core.md)) |
| **DDL/DML** (쓰기 작업) | 🔴 Low | 승인 필수 | Preview + Double-check + Rollback Plan 필수 |
| **외부 API 호출** | 🔴 Low | 승인 필수 | Rate Limit + 결과 검증 + Audit Log |

#### 3.6.2 에이전트별 권한 경계 (보강: Moltbook 교훈)

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

#### 3.6.3 NL2SQL 사전 스키마 검증 레이어 (보강: Ecosystem Analysis §3)

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

### 3.7 MVP 범위 조정 권고 (보강: 리뷰 보고서 §1)

> **⚠️ MVP 범위 과잉 문제 (리뷰 보고서 §1-2)**

현재 PRD의 Phase 1 MVP 범위가 과도하게 넓습니다. 아래 항목의 Phase 조정을 권고합니다:

| 현재 Phase | 기능 | 권고 Phase | 사유 |
|-----------|------|-----------|------|
| Phase 1 | Graphiti 시간 인식 KG (§4.3.10) | **Phase 3 R&D** | bi-temporal 모델은 핵심 기능 안정화 후 도입 |
| Phase 1 | 20+ Predicate 세분화 (§4.4.1) | **Phase 2** | MVP는 기본 5~7개 핵심 관계만 → Phase 2에서 확장 |
| Phase 1 | 4단계 품질 게이트 전체 (§5.3) | **Unit+E2E만** | MVP는 Stage 1(Unit) + Stage 4(E2E)만 필수 |
| Phase 1 | 외부 KG 자동 구축 (§4.3.9) | **Phase 2+** | 내부 온톨로지 안정화가 선행 필요 |

---

### 3.8 설계 원칙: 에이전트 학습 vs 환경 개선의 구분 (보강: 시행착오 비용 관점)

> **신규 섹션 — 핵심 철학 "시행착오 비용 최소화" 구체화**

DataNexus의 여러 메커니즘이 "에이전트가 점점 똑똑해진다"는 인상을 줄 수 있으나, 실제로 개선되는 것은 에이전트가 참조하는 환경(데이터, 규칙, 온톨로지)입니다. 이 구분을 명확히 하지 않으면 "에이전트에게 맡기면 알아서 좋아지겠지"라는 위험한 가정으로 이어집니다.

#### 3.8.1 개선 주체 식별 매트릭스

| 메커니즘 | 실제 개선 주체 | 에이전트의 역할 | 사람의 역할 (품질 책임) |
|----------|---------------|----------------|----------------------|
| Vanna Tool Memory ([PRD_Appendix_AB §B.8](./PRD_Appendix_AB.md)) | Training Data (Qdrant 벡터 스토어) | 패턴 매칭 실행자 | 오답 제거 + 신규 패턴 품질 검증 |
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
