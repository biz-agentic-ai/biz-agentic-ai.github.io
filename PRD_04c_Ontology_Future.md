# DataNexus PRD – §4.3.9~4.3.10 온톨로지 확장 로드맵 (Future)

> **📌 이 파일의 내용은 대부분 Phase 2+ 또는 Phase 3 R&D 범위입니다.**
> **예외:** §4.3.10.10.1(컨텍스트 윈도우 가드)과 §4.3.10.10.2(도구 결과 가드)는 **Phase 1 MVP에 선행 적용**합니다.
> 그 외 섹션은 MVP(Phase 0.5~1.0)에서 참조하지 않습니다.
> 핵심 온톨로지 설계는 PRD_04a(Core)와 PRD_04b(Extended)를 참조하세요.

> **구현 코드 포함 안내 (리뷰 보고서 P3):** 본 파일에는 ToolsRetriever, Graphiti 통합, LangGraph 워크플로우, ContextWindowGuard, DualMemoryRouter 등 ~280행의 Python 구현 코드가 포함되어 있습니다. 향후 리팩토링 시 Implementation Guide로 분리를 권장합니다.

---

### 4.3.9 외부 데이터 소스 기반 온톨로지 지식그래프 자동 구축 파이프라인

#### 4.3.9.1 문제 정의

현재 DataNexus의 온톨로지 구축은 주로 두 가지 내부 경로에 의존합니다.

1. **정형 데이터:** DataHub Ingestion으로 DM DB의 DDL/메타데이터를 수집하고, 관리자가 Glossary Term을 수동 정의
2. **비정형 데이터:** ApeRAG(MinerU)가 사내 문서에서 엔터티/관계를 추출하여 Knowledge Graph 생성

그러나 온톨로지의 **풍부성(Richness)**과**최신성(Freshness)**을 높이기 위해서는 외부 데이터 소스(뉴스, 산업 리포트, 규제 문서, 경쟁사 공시 등)로부터의 지식 수집과 그래프 적재가 필요합니다. 특히 유통/물류 도메인에서는 산업 동향, 공급망 이슈, 규제 변경 등 외부 맥락이 사내 데이터 해석에 직접적인 영향을 미칩니다.

**현재 설계의 한계:**

- 외부 비정형 텍스트(뉴스 기사 등)에서 엔터티/관계를 추출하여 DozerDB에 적재하는 체계적 파이프라인이 부재
- 수집된 외부 데이터를 기존 온톨로지(DataHub Glossary)와 자동으로 연결(Entity Resolution)하는 메커니즘 미정의
- 다양한 검색 전략(벡터 유사도, 그래프 구조, 자연어→Cypher)을 질의 유형에 따라 자동 선택하는 Agentic Retrieval 전략 미반영

#### 4.3.9.2 외부 데이터 수집 및 그래프 적재 아키텍처

**전체 파이프라인 플로우:**

```txt
┌─────────────────────────────────────────────────────────────────────┐
│            외부 데이터 → 지식그래프 자동 구축 파이프라인              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [Stage 1: 데이터 수집 (Scraping)]                                  │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • Selenium/Playwright 기반 동적 웹 크롤링                     │   │
│  │ • 대상: 뉴스(카테고리별), 산업 리포트, 공시, 규제 문서         │   │
│  │ • 수집 필드: 제목, 본문, 게시일, 카테고리, 출처(미디어)       │   │
│  │ • 산출물: 정형화된 기사 데이터 (JSON/Excel)                   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                            ▼                                        │
│  [Stage 2: 텍스트 청킹 및 Triple 추출]                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • RecursiveCharacterTextSplitter로 본문 → 청크 분할           │   │
│  │ • LLM 기반 엔터티/관계 추출 (Subject-Predicate-Object)        │   │
│  │ • OpenAI Embeddings로 청크별 벡터 임베딩 생성                 │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                            ▼                                        │
│  [Stage 3: Neo4j(DozerDB) 그래프 적재]                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • 노드 생성: Article, Content(청크), Media(출처), Category    │   │
│  │ • 관계 생성: HAS_CHUNK, PUBLISHED, BELONGS_TO                │   │
│  │ • 벡터 인덱스 구축: Content 노드의 임베딩 → Vector Index      │   │
│  │ • Entity Resolution: 추출 엔터티 ↔ DataHub Glossary 매핑     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                            ▼                                        │
│  [Stage 4: Agentic GraphRAG 검색 (ToolsRetriever)]                 │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • LLM이 질의 유형에 따라 최적 Retriever 자동 선택             │   │
│  │ • Vector / VectorCypher / Text2Cypher 통합                   │   │
│  │ • GraphRAG 파이프라인으로 최종 답변 생성                      │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 4.3.9.3 그래프 스키마 설계 (외부 데이터용)

기존 DataNexus의 insight_kb_db 내에 외부 데이터 전용 레이블을 추가하여 사내 온톨로지와 연결합니다.

**노드 타입:**

| 노드 레이블 | 속성 | 설명 |
| :--- | :--- | :--- |
| **ExternalArticle** | article_id, title, url, published_date, source_type | 외부 기사/문서 원본 |
| **ExternalContent** | chunk, chunk_index, embedding, content_id | 기사 본문 청크 + 벡터 임베딩 |
| **ExternalMedia** | name, domain, reliability_score | 출처 미디어/기관 (신뢰도 점수 포함) |
| **ExternalCategory** | name, mapped_domain | 외부 카테고리 → DataHub Domain 매핑 |
| **ExtractedEntity** | name, type, confidence, glossary_uri | LLM이 추출한 엔터티 (Glossary 연결) |

**관계 타입:**

| 관계 | 방향 | 설명 |
| :--- | :--- | :--- |
| HAS_CHUNK | ExternalArticle → ExternalContent | 기사 → 청크 분할 관계 |
| PUBLISHED_BY | ExternalArticle → ExternalMedia | 기사 → 출처 미디어 |
| BELONGS_TO | ExternalArticle → ExternalCategory | 기사 → 카테고리 분류 |
| MENTIONS | ExternalContent → ExtractedEntity | 청크 내 엔터티 언급 |
| MAPS_TO | ExtractedEntity → GlossaryTerm | 추출 엔터티 → DataHub 온톨로지 연결 |
| RELATED_CONTEXT | ExtractedEntity → ExtractedEntity | 엔터티 간 동시 출현(Co-occurrence) 관계 |

**Cypher 스키마 생성 예시:**

```cypher
// 벡터 인덱스 생성
CREATE VECTOR INDEX external_content_embedding IF NOT EXISTS
FOR (c:ExternalContent)
ON (c.embedding)
OPTIONS {indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
}};

// 전문검색 인덱스 (Hybrid 검색용)
CREATE FULLTEXT INDEX external_content_fulltext IF NOT EXISTS
FOR (c:ExternalContent)
ON EACH [c.chunk];
```

#### 4.3.9.4 Neo4j GraphRAG ToolsRetriever 기반 Agentic 검색 전략

**핵심 개념:** Neo4j GraphRAG Python 패키지의 `ToolsRetriever`는 여러 Retriever를 Tool로 등록하고, LLM이 질의 특성에 따라 최적의 Retriever를 자동 선택하는 Agentic RAG 패턴입니다. DataNexus의 기존 Query Router Agent(섹션 4.5.2)의 검색 계층을 강화합니다.

**3가지 검색 방식 + ToolsRetriever 통합:**

| Retriever | 검색 원리 | 최적 사용 시나리오 | DataNexus 적용 |
| :--- | :--- | :--- | :--- |
| **VectorRetriever** | 임베딩 유사도 기반 의미론적 검색 | "공급망 이슈 관련 뉴스 찾아줘" 같은 개방형 의미 검색 | Content 노드의 chunk 임베딩 검색 |
| **VectorCypherRetriever** | 벡터 검색 후 Cypher 그래프 순회 | "IT 분야 관련 기사 중 최근 AI 트렌드는?" 같은 구조+의미 복합 검색 | 벡터 검색 → 카테고리/미디어 관계 탐색 |
| **Text2CypherRetriever** | 자연어 → Cypher 변환 → 그래프 직접 질의 | "조선일보가 발행한 경제 기사 몇 건이야?" 같은 구조적 질의 | LLM이 스키마 인지 Cypher 생성 |
| **ToolsRetriever** | LLM이 위 3개를 Tool로 인식, 질의별 자동 선택/조합 | 모든 유형의 자연어 질의 | SEOCHO Router Agent에 통합 |

**ToolsRetriever 구현 설계:**

```python
from neo4j import GraphDatabase
from neo4j_graphrag.retrievers import (
    VectorRetriever, VectorCypherRetriever, 
    Text2CypherRetriever, ToolsRetriever
)
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.generation import GraphRAG

# DozerDB 연결 (외부 데이터 전용 DB 또는 insight_kb_db)
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", os.environ["NEO4J_PASSWORD"]),  # 환경변수 사용 필수
    database="insight_kb_db"  # DozerDB Multi-DB (PRD_01 §2.3 참조)
)

llm = OpenAILLM(model_name="gpt-4o", model_params={"temperature": 0})
embedder = OpenAIEmbeddings(model="text-embedding-3-large")

# ── Retriever 1: 의미론적 벡터 검색 ──
vector_retriever = VectorRetriever(
    driver=driver,
    index_name="external_content_embedding",
    embedder=embedder,
    return_properties=["chunk", "content_id", "title"],
)

# ── Retriever 2: 벡터 + 그래프 순회 복합 검색 ──
retrieval_query = """
    WITH node AS content, score
    MATCH (content)<-[:HAS_CHUNK]-(article:ExternalArticle)
    OPTIONAL MATCH (article)-[:BELONGS_TO]->(category:ExternalCategory)
    OPTIONAL MATCH (article)-[:PUBLISHED_BY]->(media:ExternalMedia)
    OPTIONAL MATCH (content)-[:MENTIONS]->(entity:ExtractedEntity)
    RETURN
        content.chunk AS chunk,
        article.title AS article_title,
        article.url AS article_url,
        article.published_date AS published_date,
        category.name AS category_name,
        media.name AS media_name,
        score AS similarity_score,
        collect(DISTINCT entity.name)[0..5] AS mentioned_entities
"""

vector_cypher_retriever = VectorCypherRetriever(
    driver=driver,
    index_name="external_content_embedding",
    retrieval_query=retrieval_query,
    embedder=embedder,
)

# ── Retriever 3: 자연어 → Cypher 직접 검색 ──
text2cypher_retriever = Text2CypherRetriever(
    driver=driver,
    llm=llm,
    neo4j_schema=None,  # 자동 스키마 추출
    examples=[
        "사용자: 경제 카테고리 기사 수는? "
        "Cypher: MATCH (a:ExternalArticle)-[:BELONGS_TO]->(c:ExternalCategory {name: '경제'}) "
        "RETURN count(a) AS article_count",
        "사용자: 최근 일주일 IT 분야 기사 목록 "
        "Cypher: MATCH (a:ExternalArticle)-[:BELONGS_TO]->(c:ExternalCategory {name: 'IT/과학'}) "
        "WHERE a.published_date >= date() - duration('P7D') "
        "RETURN a.title, a.url, a.published_date ORDER BY a.published_date DESC",
    ],
)

# ── ToolsRetriever: 3가지를 Tool로 통합, LLM이 자동 선택 ──
vector_tool = vector_retriever.convert_to_tool(
    name="semantic_search",
    description="의미론적 유사도 기반 검색. 기사 본문 내용을 기반으로 "
                "관련 뉴스를 찾을 때 사용합니다.",
)
vector_cypher_tool = vector_cypher_retriever.convert_to_tool(
    name="context_search",
    description="벡터 검색 후 관련 카테고리, 미디어, 엔터티까지 "
                "그래프를 탐색하여 풍부한 맥락 정보를 반환합니다.",
)
text2cypher_tool = text2cypher_retriever.convert_to_tool(
    name="structured_query",
    description="미디어별, 카테고리별, 날짜별 기사 수 집계 등 "
                "구조적 데이터 질의에 사용합니다.",
)

tools_retriever = ToolsRetriever(
    driver=driver,
    llm=llm,
    tools=[vector_tool, vector_cypher_tool, text2cypher_tool],
)

# ── GraphRAG 파이프라인으로 최종 답변 생성 ──
rag = GraphRAG(retriever=tools_retriever, llm=llm)
response = rag.search(
    query_text="최근 AI 반도체 관련 뉴스 중 공급망에 영향을 미치는 건?"
)
```

#### 4.3.9.5 SEOCHO Agent 아키텍처와의 통합

ToolsRetriever는 기존 SEOCHO Multi-Agent 아키텍처의 **Vector Agent** 및 **Graph DBA**를 강화하는 위치에 놓입니다.

```txt
┌────────────────────────────────────────────────────────────────┐
│                    SEOCHO Router Agent                          │
│  (질의 복잡도 분류 + 데이터 소스 선택)                          │
└──────────┬───────────────────┬──────────────────┬──────────────┘
           │                   │                  │
    ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐
    │ Graph Agent │    │ Vector Agent│    │  Web Agent  │
    │  (내부 KG)  │    │  (내부 문서) │    │  (외부 검색) │
    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
           │                  │                  │
           │           ┌──────▼──────┐           │
           │           │ToolsRetriever│          │  ← 신규 추가
           │           │(외부 데이터  │           │
           │           │ 지식그래프)  │           │
           │           ├─────────────┤           │
           │           │• Vector     │           │
           │           │• VectorCypher│          │
           │           │• Text2Cypher│           │
           │           └──────┬──────┘           │
           │                  │                  │
    ┌──────▼──────────────────▼──────────────────▼──────┐
    │                    Supervisor                       │
    │  (Hierarchy of Truth + ConflictResolutionScore)    │
    └────────────────────────────────────────────────────┘
```

**Hierarchy of Truth 확장:**

| Priority | 소스 | ConflictResolutionScore | 비고 |
| :--- | :--- | :--- | :--- |
| 1 | Ontology (DataHub Glossary) | 100 | 기존 유지 |
| 2 | Structured Data (Graph/SQL) | 90 | 기존 유지 |
| 3 | Internal Vector RAG (Documents) | 70 | 기존 유지 |
| 4 | **External Knowledge Graph** | **60** | **신규: ToolsRetriever 결과** |
| 5 | Web Search (External) | 50 | 기존 유지 |

> **📌 참고:** 이 테이블은 External KG 단독 도입(Phase 2) 시점의 5-소스 구조입니다. Graphiti Temporal KG(Priority 4, Score 65)는 Phase 3에서 추가되며, 최종 6-소스 구조는 PRD_02 §3.5.3을 참조하세요.

#### 4.3.9.6 데이터 수집 스케줄 및 품질 관리

**수집 대상 및 주기:**

| 수집 소스 | 수집 주기 | 수집 범위 | 권한/합법성 |
| :--- | :--- | :--- | :--- |
| 산업 뉴스 (카테고리별) | 매일 06:00 (Batch) | 정치, 경제, 사회, IT/과학, 세계 | robots.txt 준수, API 우선 |
| 금융감독원 공시 | 매일 09:00 | 관련 계열사 공시 | 공개 데이터 |
| 산업 리포트 | 주간 (월요일 02:00) | 유통/물류/SCM 분야 | 구독 라이선스 |
| 규제/법률 변경 | 이벤트 기반 | 관련 법령 개정 고시 | 공개 데이터 |

**품질 게이트:**

| 검증 항목 | 기준 | 실패 시 조치 |
| :--- | :--- | :--- |
| 출처 신뢰도(reliability_score) | 0.7 이상만 적재 | 저신뢰 출처 별도 큐로 격리, 관리자 승인 후 적재 |
| 엔터티 추출 신뢰도(confidence) | 0.8 이상 자동 적재 | 0.6~0.8은 Review Queue, 0.6 미만 폐기 |
| Glossary 매핑률(MAPS_TO) | 추출 엔터티의 50% 이상 매핑 | 미매핑 엔터티는 Ontology Drafter(섹션 4.5.3)에 신규 용어 후보로 전달 |
| 중복 검사 | 동일 URL 또는 제목 유사도 95% 이상 | 중복 기사 스킵, 기존 노드에 최신 정보만 업데이트 |

#### 4.3.9.7 기존 온톨로지와의 연결 전략 (Entity Resolution)

외부 데이터에서 추출된 엔터티를 DataHub Glossary의 기존 온톨로지에 연결하여 통합된 지식그래프를 구성합니다.

**매핑 파이프라인:**

```txt
[LLM 추출 엔터티] 
    → [Stage 1: Exact/Synonym Match (Glossary prefLabel/altLabel)]
    → [Stage 2: 벡터 임베딩 유사도 (Qdrant에 저장된 Glossary 벡터)]  
    → [Stage 3: LLM Context Ranking (섹션 4.3.6.2 파이프라인 재활용)]
    → [자동 매핑 (≥0.90) | Review Queue (0.70~0.90) | 신규 후보 (<0.70)]
    # ※ 임계값 척도는 PRD_04b §4.3.6 HybridEntityResolver 기준 (0.0-1.0 스케일) 준수
```

매핑이 성공하면 `MAPS_TO` 관계를 통해 외부 엔터티가 DataHub Glossary URI에 연결되고, 이는 사용자가 "공급망 이슈"를 질의할 때 내부 온톨로지의 관련 테이블/컬럼과 외부 뉴스 맥락을 함께 제공하는 Cross-Source Retrieval을 가능하게 합니다.

#### 4.3.9.8 지표 (Metrics)

| 지표명 | 정의 | 목표 기준 |
| :--- | :--- | :--- |
| **External KG Node Count** | 외부 데이터에서 생성된 노드 수 | Stage 2: 10,000+ |
| **Entity-Glossary Mapping Rate** | 추출 엔터티의 DataHub Glossary 매핑 비율 | 50% 이상 |
| **ToolsRetriever Routing Accuracy** | LLM이 적절한 Retriever를 선택한 비율 | 90% 이상 (SSOT 외부; 외부 KG 전용 지표 — 프로젝트 전체 Routing Accuracy SSOT는 §4.8 참조) |
| **Cross-Source Query Success Rate** | 내부+외부 데이터를 함께 활용한 질의 성공률 | 80% 이상 |
| **Data Freshness** | 외부 데이터 수집 후 그래프 반영까지 지연 시간 | 24시간 이내 |
| **Source Reliability Score Avg** | 적재된 외부 소스의 평균 신뢰도 점수 | 0.8 이상 |

#### 4.3.9.9 로컬 Stage별 구현 로드맵

> **📌 로컬 Stage ↔ 프로젝트 Phase 매핑:** 본 섹션의 Stage는 외부 데이터 파이프라인 내부 단계이며, 전체 프로젝트 Phase(PRD_06 §9.1)와 다음과 같이 매핑됩니다: Stage 0.5~1 = 프로젝트 Phase 2, Stage 2~3 = 프로젝트 Phase 3.

| Stage | 범위 | 주요 산출물 | 기간 |
| :--- | :--- | :--- | :--- |
| **Stage 0.5** (PoC) | 뉴스 크롤링 → DozerDB 적재 → VectorRetriever 단일 검색 | 수집 스크립트, 그래프 스키마, 기본 검색 API | 2주 |
| **Stage 1** | VectorCypher + Text2Cypher 추가, ToolsRetriever 통합 | Agentic 검색 파이프라인, SEOCHO 통합 | 3주 |
| **Stage 2** | Entity Resolution(Glossary 연결), 품질 게이트, 스케줄러 | Cross-Source Retrieval, 품질 대시보드 | 4주 |
| **Stage 3** | 다양한 외부 소스 확장 (공시, 리포트, 규제), 자동 온톨로지 확장 | 멀티소스 수집기, Ontology Drafter 연동 | 4주 |

---

### 4.3.10 Graphiti 기반 시간 인식 지식그래프 및 에이전트 메모리 계층

> 본 섹션은 정적 지식그래프의 한계를 분석하고, Graphiti를 에이전트 메모리 계층으로 도입하는 설계를 다룹니다.
> **Phase 3 R&D 이관 항목** (리뷰 보고서 §3 반영)

#### 현재 DataNexus 지식그래프의 한계

DataNexus의 현행 그래프DB(DozerDB) 활용은 **정적 지식그래프(Static KG)** 모델에 기반합니다.

**현재 파이프라인의 구조적 한계:**

| 한계 영역 | 현재 상태 | 실무 영향 |
| :--- | :--- | :--- |
| **시간 인식 부재** | 엔터티/관계에 시간 메타데이터 없음 | "지난달 매출 지표 정의가 변경됐나?"와 같은 시간 기반 질의 불가 |
| **배치 기반 갱신** | ApeRAG/DataHub 배치 Ingestion 의존 | 실시간 데이터 변경 반영 지연 (최소 수 시간~1일) |
| **사실 충돌 처리 미흡** | 새 정보 입력 시 기존 정보 단순 덮어쓰기 | "이전 정의"가 유실되어 감사/추적 불가 |
| **에이전트 메모리 부재** | 대화 세션 간 컨텍스트 유실 | 사용자가 이전 질의에서 논의한 맥락을 매번 재설명 필요 |
| **에피소드 기반 학습 없음** | 사용자 상호작용 이력이 그래프에 반영되지 않음 | 개인화된 분석 추천이나 반복 질의 최적화 불가 |
| **온톨로지 진화 추적 불가** | Glossary Term 변경 시 이전 버전 소실 | 규제 감사 시 "당시 기준" 확인이 어려움 |

#### Graphiti가 해결하는 핵심 문제

Graphiti는 Zep이 개발한 오픈소스 프레임워크로, **시간 인식 지식그래프(Temporal Knowledge Graph)**를 실시간으로 구축·관리하며, 특히 AI 에이전트의 동적 메모리 계층으로 설계되었습니다.

**Graphiti vs. 기존 GraphRAG (ApeRAG) 비교:**

| 특성 | ApeRAG (현행) | Graphiti (도입 제안) |
| :--- | :--- | :--- |
| **그래프 갱신** | 배치 재구축 (전체 그래프 재계산) | 실시간 점진적 업데이트 (에피소드 단위) |
| **시간 모델링** | 없음 | Bi-Temporal (이벤트 시간 + 입수 시간) |
| **충돌 해결** | 마지막 쓰기 우선 (Last-Write-Wins) | 시간 메타데이터 기반 지능형 무효화(Invalidation) |
| **사실 추적** | 스냅샷 | 유효 기간(t_valid, t_invalid) + 이력 보존 |
| **검색 방식** | 벡터 유사도 위주 | Hybrid (Semantic + BM25 + Graph BFS) |
| **에이전트 연동** | 독립 RAG 파이프라인 | LangGraph/MCP 네이티브 통합 |
| **커스텀 엔터티** | 스키마리스 추출 | Pydantic 기반 도메인 특화 엔터티 정의 |
| **커뮤니티 탐지** | LLM 기반 커뮤니티 요약 | 동적 레이블 전파(Label Propagation) |

#### 4.3.10.1 아키텍처 개요

Graphiti를 DataNexus의 **에이전트 메모리 계층(Agent Memory Layer)**으로 도입하여, 기존 정적 지식그래프를 보완합니다. 기존 ApeRAG의 GraphRAG 기능을 대체하는 것이 아니라,**사용자 상호작용 기반 동적 지식 축적** 및 **시간 추론** 기능을 추가합니다.

```txt
┌──────────────────────────────────────────────────────────────────────────┐
│                     DataNexus Knowledge Layer (확장)                      │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐ │
│  │  정적 지식그래프     │  │  시간 인식 지식그래프  │  │  외부 데이터 KG     │ │
│  │  (ApeRAG/DozerDB)  │  │  (Graphiti/DozerDB) │  │  (ToolsRetriever)  │ │
│  │                    │  │                    │  │                    │ │
│  │  • 사내 문서 KG     │  │  • 에이전트 메모리   │  │  • 뉴스/공시 KG     │ │
│  │  • DataHub 메타KG   │  │  • 대화 이력 그래프  │  │  • 외부 엔터티      │ │
│  │  • 엔터티/관계 추출  │  │  • 시간 추론        │  │  • Entity Resolution│ │
│  │  • 커뮤니티 요약     │  │  • 사실 진화 추적   │  │  • Agentic 검색     │ │
│  └────────┬───────────┘  └────────┬───────────┘  └────────┬───────────┘ │
│           │                       │                       │              │
│  ┌────────▼───────────────────────▼───────────────────────▼───────────┐ │
│  │              DozerDB (Neo4j 5.26.3 호환) Multi-DB                  │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │ │
│  │  │ datahub_db   │  │graphiti_memory_db│  │insight_kb_db │           │ │
│  │  │ (정적 KG)    │  │ (시간 KG)    │  │ (외부 KG)    │             │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘             │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

#### 4.3.10.2 Bi-Temporal 데이터 모델

Graphiti의 핵심 차별화 요소는 **Bi-Temporal(이중 시간) 모델링**입니다. 모든 관계(Edge)에 두 종류의 타임스탬프를 부여합니다.

**시간 메타데이터 구조:**

| 타임스탬프 | 유형 | 설명 | DataNexus 적용 예시 |
| :--- | :--- | :--- | :--- |
| `t_valid` | Event Time | 사실이 현실 세계에서 유효해진 시점 | "매출총이익률 정의가 2025-04-01부터 변경됨" |
| `t_invalid` | Event Time | 사실이 현실 세계에서 무효화된 시점 | "이전 정의는 2025-03-31까지 유효했음" |
| `t_created` | Transaction Time | 시스템이 해당 사실을 인지한 시점 | "2025-04-05에 DataHub에서 변경 감지됨" |
| `t_expired` | Transaction Time | 시스템이 해당 사실을 무효화 처리한 시점 | "2025-04-05에 이전 Edge를 무효화함" |

**시간 질의 활용 시나리오:**

```txt
사용자: "3월 기준으로 매출총이익률은 어떻게 계산했지?"
  → Graphiti: t_valid <= 2025-03-31인 Edge에서 해당 정의 검색
  → 결과: "매출총이익률 = (매출액 - 매출원가) / 매출액 × 100"

사용자: "지금은 어떻게 바뀌었어?"
  → Graphiti: t_valid가 현재 유효한 최신 Edge 검색
  → 결과: "매출총이익률 = (순매출액 - 직접원가) / 순매출액 × 100 (2025-04-01~)"

사용자: "언제 바뀐 거야?"
  → Graphiti: 동일 Predicate의 Edge 이력 조회
  → 결과: "2025-04-01부터 변경. 이전 정의는 2024-01-01~2025-03-31 유효."
```

#### 4.3.10.3 에피소드(Episode) 기반 지식 축적

Graphiti는 데이터를 **에피소드(Episode)** 단위로 점진적 수집(Incremental Ingestion)합니다. DataNexus에서 에피소드는 다음과 같이 매핑됩니다.

**에피소드 유형 및 매핑:**

| 에피소드 유형 | 소스 | 수집 방식 | Graphiti Source Type |
| :--- | :--- | :--- | :--- |
| **사용자 대화** | Chat UI 질의/응답 | 실시간 (대화 종료 시) | `message` |
| **Glossary 변경** | DataHub Glossary Term 생성/수정/삭제 | 이벤트 기반 (Kafka ChangeEvent) | `json` |
| **SQL 실행 이력** | Vanna AI 생성 SQL + 실행 결과 요약 | 실시간 (질의 완료 시) | `text` |
| **외부 데이터 수집** | 뉴스/공시 (섹션 4.3.9) | 배치 (스케줄 기반) | `text` |
| **관리자 피드백** | SQL 품질 평가, 용어 수정 | 이벤트 기반 | `json` |
| **시스템 이벤트** | 스키마 변경, 데이터 소스 추가 | 이벤트 기반 | `json` |

**에피소드 수집 구현 설계:**

```python
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from datetime import datetime
import asyncio

# DozerDB(Neo4j 호환) 연결 - Graphiti 전용 DB
graphiti = Graphiti(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password",
    database="graphiti_memory_db"  # DozerDB Multi-DB 활용
)

# 초기화 (최초 1회)
await graphiti.build_indices_and_constraints()

# ── 에피소드 1: 사용자 대화 수집 ──
await graphiti.add_episode(
    name="user_query_session_20250408_001",
    episode_body=(
        "이준호(분석가): 올해 1분기 매출총이익률은 어떻게 되나요?\n"
        "DataNexus: 2025년 1분기 매출총이익률은 34.2%입니다. "
        "이는 전년 동기(32.8%) 대비 1.4%p 개선되었습니다."
    ),
    source=EpisodeType.message,
    source_description="DataNexus Chat UI 질의 응답",
    reference_time=datetime(2025, 4, 8, 14, 30),
    group_id="tenant_retail_01"  # 멀티테넌시 격리
)

# ── 에피소드 2: Glossary Term 변경 감지 ──
await graphiti.add_episode(
    name="glossary_change_gross_margin_v2",
    episode_body=json.dumps({
        "event": "glossary_term_updated",
        "term_urn": "urn:li:glossaryTerm:gross_margin",
        "field_changed": "definition",
        "old_value": "매출총이익률 = (매출액 - 매출원가) / 매출액 × 100",
        "new_value": "매출총이익률 = (순매출액 - 직접원가) / 순매출액 × 100",
        "changed_by": "admin@company.com",
        "effective_date": "2025-04-01"
    }),
    source=EpisodeType.json,
    source_description="DataHub Glossary ChangeEvent",
    reference_time=datetime(2025, 4, 5, 9, 0),
    group_id="tenant_retail_01"
)

# ── 에피소드 3: SQL 실행 이력 축적 ──
await graphiti.add_episode(
    name="sql_execution_log_q1_margin",
    episode_body=(
        "질문: 1분기 매출총이익률\n"
        "생성SQL: SELECT ROUND((SUM(net_sales) - SUM(direct_cost)) / "
        "SUM(net_sales) * 100, 1) AS gross_margin_pct "
        "FROM mart_sales WHERE quarter = '2025Q1'\n"
        "결과: 34.2%\n"
        "실행시간: 1.2초\n"
        "사용자평가: 정확"
    ),
    source=EpisodeType.text,
    source_description="Vanna AI SQL 실행 이력",
    reference_time=datetime(2025, 4, 8, 14, 31),
    group_id="tenant_retail_01"
)
```

#### 4.3.10.4 커스텀 엔터티 및 관계 정의 (DataNexus 도메인 특화)

Graphiti의 **Custom Entity Types** 기능을 활용하여 DataNexus 도메인에 특화된 엔터티를 Pydantic 모델로 정의합니다. 이는 LLM의 엔터티 추출 정확도를 크게 향상시킵니다.

```python
from pydantic import BaseModel, Field
from typing import Optional, List

# ── DataNexus 커스텀 엔터티 정의 ──

class BusinessMetric(BaseModel):
    """비즈니스 지표 (KPI) 엔터티"""
    metric_name: str = Field(description="지표명 (예: 매출총이익률)")
    calculation_formula: Optional[str] = Field(description="계산식")
    data_source_table: Optional[str] = Field(description="원천 테이블명")
    glossary_urn: Optional[str] = Field(description="DataHub Glossary URN")
    unit: Optional[str] = Field(description="단위 (%, 원, 건 등)")

class DataAsset(BaseModel):
    """데이터 자산 (테이블/뷰) 엔터티"""
    asset_name: str = Field(description="테이블/뷰 이름")
    schema_name: Optional[str] = Field(description="스키마명")
    asset_type: str = Field(description="table | view | materialized_view")
    owner_team: Optional[str] = Field(description="소유 팀")
    datahub_urn: Optional[str] = Field(description="DataHub 데이터셋 URN")

class AnalysisPattern(BaseModel):
    """분석 패턴 (반복되는 질의 패턴) 엔터티"""
    pattern_name: str = Field(description="패턴명 (예: 월별 추이 분석)")
    typical_sql_template: Optional[str] = Field(description="대표 SQL 템플릿")
    related_metrics: List[str] = Field(default_factory=list, description="관련 지표 목록")
    frequency: Optional[str] = Field(description="사용 빈도 (daily/weekly/monthly)")

class UserPreference(BaseModel):
    """사용자 선호도 엔터티 (에이전트 개인화)"""
    user_id: str = Field(description="사용자 ID")
    preferred_chart_type: Optional[str] = Field(description="선호 차트 유형")
    preferred_metrics: List[str] = Field(default_factory=list, description="자주 조회하는 지표")
    department: Optional[str] = Field(description="소속 부서")
    analysis_depth: Optional[str] = Field(description="분석 깊이 선호 (summary/detail)")

# Graphiti에 커스텀 엔터티 등록
graphiti = Graphiti(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password",
    database="graphiti_memory_db"
)
graphiti.register_entity_types([
    BusinessMetric, DataAsset, AnalysisPattern, UserPreference
])
```

#### 4.3.10.5 Hybrid 검색 전략

Graphiti는 3가지 검색 방식을 결합한 **Hybrid Retrieval**을 제공합니다. 이는 기존 SEOCHO Agent의 검색 계층을 보완합니다.

**검색 방식 비교:**

| 검색 방식 | 원리 | 강점 | DataNexus 적용 |
| :--- | :--- | :--- | :--- |
| **Semantic Search** (Cosine) | 임베딩 벡터 유사도 | 의미론적 유사 질의 매칭 | "수익성 관련 질의"와 유사한 과거 대화 검색 |
| **Full-Text Search** (BM25) | 키워드 기반 전문 검색 | 정확한 용어 매칭 | "매출총이익률" 정확한 용어 검색 |
| **Graph BFS** (Breadth-First) | 그래프 구조 순회 | 맥락적 연결 탐색 | 특정 지표와 연결된 테이블/계산식/변경이력 탐색 |

**Center Node 기반 검색 (에이전트 개인화):**

```python
# 사용자 노드를 중심으로 검색 → 개인화된 결과 우선순위
edge_results = await graphiti.search(
    query="매출 분석 관련 정보",
    center_node_uuid=user_node_uuid,  # 사용자 노드 기준
    num_results=10
)

# 검색 결과: 해당 사용자와 가까운(관련 깊은) 사실이 상위 랭크
# - 사용자가 자주 조회한 지표
# - 사용자의 과거 질의에서 추출된 관계
# - 사용자 부서와 관련된 데이터 자산
```

#### 4.3.10.6 에이전트 메모리로서의 Graphiti (LangGraph 통합)

기존 SEOCHO Multi-Agent 아키텍처에 Graphiti를 **에이전트 장기 메모리(Long-term Memory)**로 통합합니다.

```txt
┌────────────────────────────────────────────────────────────────────────────┐
│                     SEOCHO Agent + Graphiti Memory                         │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [사용자 질의 입력]                                                         │
│         │                                                                  │
│         ▼                                                                  │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │ ① Context Retrieval (Graphiti Search)                     │              │
│  │   • 최근 대화에서 관련 사실(Edge) 검색                      │              │
│  │   • 사용자 노드 중심 개인화 랭킹                            │              │
│  │   • 시간 기반 사실 필터링 (현재 유효한 정보만)               │              │
│  └──────────────────┬───────────────────────────────────────┘              │
│                     ▼                                                      │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │ ② SEOCHO Router Agent                                     │              │
│  │   • Graphiti 컨텍스트 + 질의 → 에이전트 라우팅               │              │
│  │   • 시스템 프롬프트에 Graphiti 사실(Facts) 주입              │              │
│  └──────────────────┬───────────────────────────────────────┘              │
│                     ▼                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │Graph Agent│  │Vector Agt│  │ SQL Agent │  │ Web Agent│                  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘                  │
│       └──────────────┼──────────────┼──────────────┘                      │
│                      ▼                                                     │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │ ③ Supervisor + Response Generation                        │              │
│  │   • Hierarchy of Truth 기반 결과 병합                      │              │
│  │   • 최종 답변 생성                                         │              │
│  └──────────────────┬───────────────────────────────────────┘              │
│                     ▼                                                      │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │ ④ Knowledge Persistence (Graphiti Episode 저장)            │              │
│  │   • 질의/응답 쌍을 새 에피소드로 비동기 저장                 │              │
│  │   • 엔터티/관계 자동 추출 및 기존 그래프 갱신                │              │
│  │   • 사실 충돌 시 Bi-Temporal 무효화 처리                    │              │
│  └──────────────────────────────────────────────────────────┘              │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

**LangGraph + Graphiti 에이전트 구현 설계:**

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage
from graphiti_core import Graphiti

# ── Graphiti 에이전트 상태 정의 ──
class AgentState(TypedDict):
    messages: list
    user_name: str
    user_node_uuid: str
    graphiti_context: list  # Graphiti에서 검색한 사실 목록

# ── Step 1: Graphiti 컨텍스트 검색 ──
async def retrieve_memory(state: AgentState) -> AgentState:
    """사용자 질의와 관련된 과거 사실을 Graphiti에서 검색"""
    last_message = state["messages"][-1]
    query = f'{state["user_name"]}: {last_message.content}'
    
    # 사용자 노드 중심 검색 (개인화)
    edge_results = await graphiti.search(
        query,
        center_node_uuid=state["user_node_uuid"],
        num_results=10
    )
    
    # 사실 목록을 컨텍스트로 변환
    facts = [f"- {edge.fact}" for edge in edge_results]
    state["graphiti_context"] = facts
    return state

# ── Step 2: SEOCHO Router에 컨텍스트 주입 ──
async def route_with_context(state: AgentState) -> AgentState:
    """Graphiti 컨텍스트를 포함하여 에이전트 라우팅"""
    context_str = "\n".join(state["graphiti_context"])
    
    system_prompt = f"""당신은 DataNexus 데이터 분석 어시스턴트입니다.
    
사용자에 대해 알고 있는 정보:
{context_str}

이 정보를 바탕으로 맞춤형 분석을 제공하세요.
간결하고 정확하게 답변하세요."""
    
    # ... SEOCHO Router Agent 호출 (기존 로직)
    response = await seocho_router.invoke(state, system_prompt)
    return state

# ── Step 3: 대화를 Graphiti에 에피소드로 저장 ──
async def persist_knowledge(state: AgentState) -> AgentState:
    """대화 내용을 Graphiti 지식그래프에 비동기 저장"""
    last_user_msg = state["messages"][-2]  # 사용자 질의
    last_ai_msg = state["messages"][-1]    # AI 응답
    
    await graphiti.add_episode(
        name=f"chat_{datetime.now().isoformat()}",
        episode_body=(
            f'{state["user_name"]}: {last_user_msg.content}\n'
            f'DataNexus: {last_ai_msg.content}'
        ),
        source=EpisodeType.message,
        source_description="DataNexus Chat Session",
        reference_time=datetime.now(),
        group_id=state.get("tenant_id", "default")
    )
    return state

# ── LangGraph 워크플로우 구성 ──
workflow = StateGraph(AgentState)
workflow.add_node("retrieve_memory", retrieve_memory)
workflow.add_node("route_with_context", route_with_context)
workflow.add_node("persist_knowledge", persist_knowledge)

workflow.set_entry_point("retrieve_memory")
workflow.add_edge("retrieve_memory", "route_with_context")
workflow.add_edge("route_with_context", "persist_knowledge")
workflow.add_edge("persist_knowledge", END)

# MemorySaver: 세션 내 단기 기억 (LangGraph)
# Graphiti: 세션 간 장기 기억 (Knowledge Graph)
app = workflow.compile(checkpointer=MemorySaver())
```

#### 4.3.10.7 Graph Namespacing을 통한 멀티테넌시

Graphiti의 `group_id`를 활용하여 DataNexus의 기존 멀티테넌시(DozerDB Multi-DB)와 연계합니다.

| 격리 수준 | 메커니즘 | 설명 |
| :--- | :--- | :--- |
| **DB 수준** | DozerDB Multi-DB | 테넌트별 완전 격리 (general_db, financial_db 등) |
| **그래프 수준** | Graphiti `group_id` | 동일 DB 내 논리적 네임스페이스 격리 |
| **사용자 수준** | Center Node UUID | 검색 시 사용자별 개인화 랭킹 |

#### 4.3.10.8 커뮤니티 탐지 및 자동 요약

Graphiti는 **동적 레이블 전파(Label Propagation)** 알고리즘으로 엔터티 클러스터(커뮤니티)를 자동 탐지합니다. DataNexus에서는 이를 **도메인 자동 분류** 및 **관련 자산 그룹핑**에 활용합니다.

```txt
커뮤니티 예시:
┌─────────────────────────────────────────────────┐
│ Community: "유통 매출 분석"                       │
│                                                 │
│  [매출총이익률] ←──CALCULATED_FROM──→ [mart_sales] │
│       │                                │        │
│  RELATED_TO                        HAS_COLUMN   │
│       │                                │        │
│  [순매출액] ←───USED_BY───→ [월별 추이 분석 패턴]  │
│       │                                         │
│  QUERIED_BY                                     │
│       │                                         │
│  [이준호(분석가)]                                │
└─────────────────────────────────────────────────┘

→ 자동 요약: "유통 매출 분석 커뮤니티는 매출총이익률, 순매출액 등의
   지표를 중심으로 mart_sales 테이블에서 월별 추이를 분석하는 패턴으로 구성됨.
   주 사용자: 이준호(분석가)"
```

#### 4.3.10.9 MCP(Model Context Protocol) 서버 통합

Graphiti의 MCP 서버를 활용하여 외부 AI 도구(Claude Desktop, Cursor 등)에서도 DataNexus의 지식그래프에 접근할 수 있게 합니다.

**MCP 서버 배포 구성:**

```yaml
# docker-compose.graphiti-mcp.yml
version: '3.8'
services:
  graphiti-mcp:
    image: ghcr.io/getzep/graphiti-mcp:latest
    environment:
      NEO4J_URI: bolt://dozerdb:7687
      NEO4J_USER: neo4j
      NEO4J_PASSWORD: ${NEO4J_PASSWORD}
      NEO4J_DATABASE: graphiti_memory_db
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      GROUP_ID: ${TENANT_ID}  # 멀티테넌시 격리
    ports:
      - "8100:8000"
    depends_on:
      - dozerdb
```

**MCP 연동 시 제공되는 Tool:**

| MCP Tool | 기능 | DataNexus 활용 |
| :--- | :--- | :--- |
| `add_episode` | 에피소드(지식) 추가 | 외부 도구에서 분석 결과 저장 |
| `search_graph` | 하이브리드 검색 | 외부 AI에서 DataNexus KG 조회 |
| `get_entity` | 엔터티 상세 조회 | 특정 지표/테이블 정보 조회 |
| `delete_episode` | 에피소드 삭제 | 잘못된 정보 정정 |


### 4.3.10.10 세션 내 컨텍스트 보존 전략 (OpenClaw 적응)

> **Phase 3 R&D — Graphiti 에이전트 메모리와 동시 도입**
> 본 섹션은 OpenClaw의 컨텍스트 보존 8가지 기법을 SEOCHO Agent에 적응시킨 설계입니다.
> 단, 기법 1(컨텍스트 윈도우 가드)과 기법 3(도구 결과 가드)은 Phase 1 MVP에 선행 적용합니다.
> Reference: https://codepointerko.substack.com/p/openclaw-ai-8

**배경:** §4.3.10.1~4.3.10.9는 세션 **간**(inter-session) 장기 메모리를 설계합니다. 본 섹션은 세션 **내**(intra-session) 컨텍스트 윈도우 관리를 다루며, 두 계층은 컴팩션 전 메모리 플러시(기법 6)를 통해 연결됩니다.

**5계층 방어선 구조:**

| Layer | 역할 | 기법 | Phase |
|-------|------|------|-------|
| 예방 | 세션 시작 전 검증 | 컨텍스트 윈도우 가드, 도구 결과 가드 | **Phase 1 (MVP)** |
| 보존 | 컴팩션 전 핵심 정보 영구화 | Graphiti 메모리 플러시 | Phase 3 |
| 적응 | 대화 구조 인식 제한 | 턴 기반 히스토리 제한, 적응형 청크 비율 | Phase 2~3 |
| 최적화 | 비용·의미 균형 | 캐시 인식 프루닝, 앞/뒤 콘텐츠 보존 | Phase 2 |
| 견고성 | 엣지 케이스 방어 | 단계적 요약 | Phase 3 |

#### 4.3.10.10.1 컨텍스트 윈도우 가드 (Phase 1 MVP)

세션 시작 전 모델의 컨텍스트 윈도우 용량을 프리플라이트 검증합니다. DataNexus는 온톨로지 컨텍스트(~8K) + DDL 스키마(~6K) + 시스템 프롬프트(~4K)가 기본 점유하므로, OpenClaw(16K/32K)보다 높은 임계값을 적용합니다.

| 임계값 | 값 | 동작 |
|--------|---|------|
| 하드 최소값 | 32K tokens | `FailoverError` — 세션 시작 차단 |
| 경고 임계값 | 64K tokens | 경고 로그 — 실행은 허용 |
| 권장 최소값 | 128K tokens | 다중 에이전트 도구 결과 여유 공간 확보 |

```python
class ContextWindowGuard:
    HARD_MINIMUM = 32_000      # DataNexus 기본 컨텍스트 점유 감안
    WARNING_THRESHOLD = 64_000  # Graphiti + HoT 규칙 포함 시
    RECOMMENDED_MIN = 128_000   # Multi-agent 도구 결과 여유 공간

    def validate(self, model_context_tokens: int) -> GuardResult:
        if model_context_tokens < self.HARD_MINIMUM:
            raise FailoverError(
                f"모델 컨텍스트 윈도우 {model_context_tokens}은 "
                f"DataNexus 최소 요구사항 {self.HARD_MINIMUM}에 미달"
            )
        if model_context_tokens < self.WARNING_THRESHOLD:
            logger.warning(
                f"컨텍스트 윈도우 {model_context_tokens}: "
                f"장시간 세션에서 공간 부족 가능성"
            )
        return GuardResult(ok=True, available=model_context_tokens)
```

**기존 PRD_02 §3.6.2 `agent_permissions.yaml`의 `max_context_tokens`와 연계하여 에이전트별 제한을 적용합니다.**

#### 4.3.10.10.2 도구 결과 가드 (Phase 1 MVP)

모든 `tool_call`에 대응하는 `tool_result` 존재를 보장합니다. SEOCHO의 다중 에이전트 구조에서 Graph DBA 타임아웃(30초), 외부 API 장애 시 트랜스크립트 손상을 방지합니다.

| 도구 | 실패 시나리오 | 합성 플레이스홀더 |
|------|-------------|-----------------|
| Graph DBA (Cypher) | 30초 타임아웃 | "Cypher 쿼리 타임아웃. 복잡도 감소 또는 인덱스 확인 필요." |
| Vector Agent (FAISS) | OOM | "벡터 검색 메모리 초과. Top-K 축소 후 재시도." |
| Web Agent | 외부 API 장애 | "외부 소스 접근 실패. 내부 데이터로 응답 생성." |
| Vanna SQL | SQL 실행 에러 | "SQL 실행 실패. 스키마 검증 결과 확인." |

#### 4.3.10.10.3 캐시 인식 프루닝 (Phase 2)

LLM 프로바이더(Anthropic)의 프롬프트 프리픽스 캐시 타이밍을 로컬 추적하여, 캐시 유효 시 앞부분을 유지하고 만료 시에만 프루닝합니다. DataNexus의 대형 온톨로지 컨텍스트(~8K)와 DDL 스키마(~6K)의 매 턴 재처리 비용을 절감합니다.

| 프루닝 단계 | 트리거 (컨텍스트 사용률) | 동작 |
|------------|----------------------|------|
| 소프트 트림 | > 30% | 도구 결과의 앞 1,500자 + 뒤 1,500자만 보존 |
| 하드 클리어 | > 50% | 도구 결과 전체를 플레이스홀더로 교체 |

**보호 규칙:** 최근 3턴의 어시스턴트 메시지는 프루닝 대상에서 항상 제외합니다.

**비용 절감 추정:** 온톨로지(~8K) + DDL(~6K) + HoT 규칙(~5K) = ~19K tokens/턴 → 캐시 히트 시 0 → **~80% 입력 비용 절감**

#### 4.3.10.10.4 앞/뒤 콘텐츠 보존 (Phase 2)

트리밍 시 시작(스키마, 헤더)과 끝(에러 메시지, 요약)을 보존합니다.

| 콘텐츠 유형 | 앞 비율 | 뒤 비율 | 마커 | 적용 대상 |
|------------|--------|--------|------|----------|
| 도구 결과 (4,000자 초과) | 1,500자 | 1,500자 | — | Graph DBA, SQL, RAG 결과 |
| 시스템 프롬프트 (부트스트랩) | 70% | 20% | 10% | 역할별 페르소나 프로필 |
| 온톨로지 컨텍스트 | 60% | 30% | 10% | 핵심 용어 정의(앞) + 최근 변경(뒤) |
| DDL 스키마 | 50% | 40% | 10% | 주요 테이블(앞) + 관계/인덱스(뒤) |

#### 4.3.10.10.5 턴 기반 히스토리 제한 (Phase 2)

메시지 개수가 아닌 **사용자 턴 단위**로 대화 히스토리를 제한합니다. SEOCHO에서 하나의 사용자 질의가 Router → Graph Agent → Graph DBA → Supervisor까지 여러 내부 메시지를 생성하므로, 턴 단위 절단이 대화 구조를 보존합니다.

**역할별 턴 제한:**

| 페르소나 | 최대 턴 | 사유 |
|---------|--------|------|
| Analyst | 15 | 분석 이력이 장기 추론에 중요 |
| CFO | 12 | 감사 추적 맥락 보존 |
| CMO / PM | 10 | 최근 전략 맥락 중심 |
| Ops | 8 | 최근 운영 상태 중심 |

#### 4.3.10.10.6 컴팩션 전 Graphiti 메모리 플러시 (Phase 3)

> **핵심: OpenClaw의 `MEMORY.md` 파일 기록 → Graphiti 에피소드 커밋으로 대체**

컨텍스트 사용률이 70%에 도달하면, 컴팩션 이전에 에이전트가 대화에서 발견한 중요 사실을 Graphiti에 에피소드로 커밋하는 별도 턴을 실행합니다. 사이클당 1회 제한.

**역할별 플러시 우선순위:**

| 페르소나 | 플러시 우선 항목 | 플러시 하위 항목 |
|---------|---------------|---------------|
| CMO | 마케팅 KPI 해석 패턴, 선호 시각화 | SQL 실행 세부사항 |
| CFO | 재무 지표 정의 변경, 감사 관련 사실 | 차트 선호도 |
| Analyst | SQL 실행 이력, 분석 패턴, 데이터 품질 이슈 | 시각화 선호도 |
| PM | 프로젝트 진행 상태, 데이터 소스 매핑 | 과거 질의 이력 |
| Ops | 시스템 상태, 알림 이력, 장애 패턴 | 개인화 선호도 |

**§4.3.10.3 에피소드 기반 지식 축적과의 연계:** 메모리 플러시에서 생성된 에피소드는 §4.3.10.3의 "사용자 대화" 에피소드 유형으로 분류되며, `source_description`에 `"memory_flush_pre_compaction"`을 표시하여 일반 대화 에피소드와 구분합니다.

#### 4.3.10.10.7 적응형 청크 비율 및 단계적 요약 (Phase 3)

**적응형 청크:** 메시지 평균 크기가 컨텍스트 윈도우의 15% 초과 시 청크 비율을 0.4→0.25로 낮춥니다 (200K 윈도우 기준 80K→50K 청크). Graph DBA의 대규모 Cypher 결과 처리에 특히 유효합니다.

**단계적 요약:** 3단계 재귀적 요약으로 컨텍스트 윈도우 초과를 방지합니다:
1. 드롭된 메시지 → 1줄 요약
2. 메인 히스토리 → 적응형 청크 크기로 분할 요약
3. 분할된 턴 접두사 → 맥락 보존 요약

각 단계에서 입력이 청크 제한 초과 시 재귀적 추가 분할이 이루어집니다.
#### 4.3.10.10.8 Vanna Tool Memory ↔ Graphiti 이중 메모리 경계 관리 (Phase 3)

> **v1.3 신규 — 2026-02-13 추가**
> **핵심: Vanna 자체 학습(세션 간) ↔ Graphiti 에피소드 축적(세션 내→영구)의 역할 분리 및 중복 방지**

Vanna 2.0의 Tool Memory는 성공한 질문-SQL 쌍을 벡터스토어(Qdrant)에 자동 학습하여 이후 유사 질의의 정확도를 높이는 **세션 간(inter-session)** 학습 메커니즘입니다. 반면 §4.3.10.10.6의 Graphiti 메모리 플러시는 대화 중 발견된 사실·패턴을 시간축 지식그래프에 커밋하는 **세션 내(intra-session) → 영구 보존** 메커니즘입니다. Phase 3에서 양쪽이 동시에 활성화되면 동일 정보가 두 저장소에 중복 축적되는 문제가 발생합니다.

##### 4.3.10.10.8.1 메모리 유형별 책임 분리

| 구분 | Vanna Tool Memory | Graphiti 에피소드 |
|------|------------------|-------------------|
| **저장 대상** | 질문-SQL 쌍 (정답 쿼리) | 사실(Fact), 관계(Relation), 해석 패턴 |
| **저장 시점** | SQL 실행 성공 + 사용자 긍정 피드백 시 | 컴팩션 전 메모리 플러시 시 (컨텍스트 70%) |
| **저장소** | Qdrant 벡터 컬렉션 (`vanna_training`) | Neo4j (DozerDB) 시간축 그래프 |
| **검색 방식** | 임베딩 유사도 기반 Few-shot 검색 | Hybrid Search (Semantic + BM25 + Graph BFS) |
| **활용 목적** | NL2SQL 생성 정확도 향상 (Few-shot) | 대화 맥락 보존, 개인화, 시간 기반 추론 |
| **TTL** | 영구 (수동 삭제 시까지) | Bi-temporal (valid_at + invalid_at) |
| **테넌트 격리** | 벡터 컬렉션 파티션 (tenant_id) | DozerDB Multi-DB 격리 |

##### 4.3.10.10.8.2 중복 방지 규칙

메모리 플러시(§4.3.10.10.6) 실행 시 아래 분류 기준을 적용하여 저장소를 결정합니다:

```python
class DualMemoryRouter:
    """Vanna Tool Memory와 Graphiti 간 저장 대상 분류"""
    
    def route_memory(self, memory_item: MemoryItem) -> MemoryDestination:
        # 규칙 1: SQL 실행 결과 → Vanna만 (Graphiti 제외)
        if memory_item.type == "sql_execution":
            return MemoryDestination.VANNA_ONLY
        
        # 규칙 2: 비즈니스 사실/해석 패턴 → Graphiti만 (Vanna 제외)
        if memory_item.type in ("business_fact", "interpretation_pattern", 
                                 "kpi_definition_change"):
            return MemoryDestination.GRAPHITI_ONLY
        
        # 규칙 3: SQL + 비즈니스 맥락이 결합된 복합 항목 → 분할 저장
        if memory_item.type == "sql_with_context":
            # SQL 쌍은 Vanna, 비즈니스 맥락은 Graphiti
            return MemoryDestination.SPLIT
        
        # 규칙 4: 사용자 선호도 (시각화, 출력 형식) → Graphiti만
        if memory_item.type == "user_preference":
            return MemoryDestination.GRAPHITI_ONLY
        
        # 기본: Graphiti (안전한 기본값)
        return MemoryDestination.GRAPHITI_ONLY
```

##### 4.3.10.10.8.3 역할별 이중 메모리 활용 차이

| 페르소나 | Vanna 활용 비중 | Graphiti 활용 비중 | 사유 |
|---------|----------------|-------------------|------|
| **Analyst** | 🔴 높음 (70%) | 🟡 중간 (30%) | SQL 패턴 재사용이 핵심 가치 |
| **CFO** | 🟡 중간 (40%) | 🔴 높음 (60%) | 재무 지표 정의 변경 추적이 핵심 |
| **CMO** | 🟢 낮음 (20%) | 🔴 높음 (80%) | KPI 해석 패턴, 시각화 선호도 중심 |
| **PM** | 🟡 중간 (50%) | 🟡 중간 (50%) | 프로젝트별 데이터 소스 매핑 + 진행 추적 |
| **Ops** | 🔴 높음 (60%) | 🟡 중간 (40%) | 반복적 운영 쿼리 패턴이 핵심 |

##### 4.3.10.10.8.4 일관성 검증 메커니즘

Vanna와 Graphiti 간 정보 일관성을 주기적으로 검증합니다:

| 검증 항목 | 주기 | 검증 방법 | 불일치 시 처리 |
|----------|------|----------|--------------|
| SQL 쌍의 테이블/컬럼 유효성 | 일 1회 | Vanna 학습 데이터의 DDL 참조 vs DataHub 최신 스키마 | 무효화된 쌍에 `deprecated` 태그 |
| Glossary Term 정의 변경 | DataHub Change Event 시 | Graphiti 사실 노드의 valid_at vs DataHub 수정 시각 | Graphiti 노드 invalid_at 설정 + 신규 노드 생성 |
| Vanna-Graphiti 교차 참조 | 주 1회 | Vanna SQL 내 테이블명 ↔ Graphiti 엔터티 매칭율 | 매칭율 < 80% → 관리자 알림 |

##### 4.3.10.10.8.5 구현 체크리스트

| 구현 항목 | 담당 Teammate | 예상 공수 | 의존성 |
|----------|-------------|----------|--------|
| DualMemoryRouter 클래스 | Backend Core | 3 M/D | §4.3.10.10.6 메모리 플러시 |
| Vanna Training 격리 (tenant 파티션) | Backend Core | 2 M/D | Vanna 2.0 Agent 기반 구현 |
| 일관성 검증 배치 작업 | Graph Engine | 3 M/D | DataHub Change Event 파이프라인 |
| 역할별 메모리 라우팅 설정 | Agent Logic | 2 M/D | DualMemoryRouter |
| 이중 메모리 모니터링 대시보드 | Frontend | 2 M/D | Admin UI Phase 2 |

**총 예상 공수:** 12 M/D (Phase 3 Graphiti 메모리 플러시 5 M/D에 추가)

**§4.3.10.10.6과의 관계:** 메모리 플러시 실행 시 DualMemoryRouter가 각 항목의 저장 대상을 분류한 후, Graphiti 대상 항목만 에피소드로 커밋합니다. Vanna 대상 항목은 별도의 `VannaTrainingPipeline`을 통해 벡터스토어에 학습됩니다.
