## 부록 A: 기술 조사 결과 요약

### A.1 DataHub Glossary 관계 정의 지원
DataHub의 비즈니스 글로서리(Glossary) 기능에서는 용어 간 관계(Relationship)를 정의할 수 있습니다. 공식적으로 지원되는 관계 유형은 4가지입니다: IsA (상속 관계), HasA (포함 관계), Values (값 목록 관계), RelatedTo (일반 연관 관계).

이러한 관계들은 DataHub 메타데이터 모델의 `glossaryRelatedTerms` aspect를 통해 구현되며, 각 관계 유형별로 `isRelatedTerms`, `hasRelatedTerms`, `values`, `relatedTerms` 필드에 관련 용어의 URN을 배열로 저장합니다.

DataHub GraphQL API를 통해 GlossaryTerm 엔티티의 `relationships` 필드로 관계 정보를 조회하고 조작할 수 있습니다.

※ 출처: DataHub 공식 문서 (GlossaryTerm 메타데이터 스키마), DataHub GraphQL API

### A.2 ApeRAG Entity Extraction Glossary 주입 방식
ApeRAG의 엔티티 추출 모듈은 DataHub Glossary를 Taxonomy 형태로 주입하여, 문서에서 추출된 개체명을 비즈니스 용어와 연결합니다. 구체적으로 Glossary Term들을 Entity Extraction Prompt에 포함시켜 LLM이 표준화된 용어를 인식하고 해당 URN으로 내보내도록 유도합니다.

Entity Resolution 과정은 4단계로 구성됩니다: Exact Match → Synonym Match → Fuzzy Match (임계값 0.85) → Context Match.

※ 출처: ApeRAG Ontology-RAG PRD 문서, SEOCHO Taxonomy Injection 설계

### A.3 DataHub 동의어(Synonyms) 중복 감지 기능
현재 DataHub는 Glossary Term에 대해 동의어(synonym)를 별도로 관리하는 공식 필드나 기능을 제공하지 않습니다. GlossaryTerm에는 name, description, definition 등의 필드만 있고, 동의어 목록을 저장하는 필드는 존재하지 않습니다.

커뮤니티에서는 동의어 관리 요구가 존재하여 Glossary Term에 "AKA" 형태로 별칭을 추가하는 기능 요청이 제기된 상태입니다.

따라서 DataNexus에서는 커스텀 synonyms 필드를 구현하고, 자체 Validation 로직으로 중복을 감지해야 합니다.

※ 출처: DataHub 공식 문서, DataHub Feature Requests (Ability to add synonyms)

---

## 부록 B: 향후 검토 항목별 상세 분석
본 부록은 10.2 절에 명시된 향후 검토 필요 항목들에 대한 심층 기술 조사 결과를 정리한 것입니다. 각 항목별로 기술 구현 가능성, 커뮤니티 로드맵, 유사 사례, DataNexus 통합 고려사항, 일정/우선순위를 분석하였습니다.

### B.1 DozerDB Fabric 지원 (크로스 DB 쿼리)

#### B.1.1 기술 구현 가능성 및 제약
Neo4j Enterprise의 Fabric 기능을 오픈소스로 제공하는 DozerDB를 활용하여 다수 그래프(DB) 간 크로스 쿼리가 가능합니다. 현재 DozerDB는 멀티-데이터베이스 생성 및 관리까지만 지원하며, Fabric 기반 교차 쿼리 기능은 로드맵 상 추후 도입 예정입니다.

DozerDB는 Neo4j Community Edition에 엔터프라이즈 기능을 추가하는 오픈소스 플러그인으로, 멀티-데이터베이스 기능을 이미 제공하고 있습니다. 즉, 하나의 DozerDB 인스턴스에서 복수의 그래프 DB를 생성(CREATE DATABASE)하고 사용할 수 있어 테넌트별 데이터 격리가 가능합니다.

그러나 서로 다른 데이터베이스 간에 한 번의 Cypher로 질의하는 Fabric 기능은 아직 구현되어 있지 않습니다. 현재(2025년 초 기준) DozerDB v1.x에서는 Fabric 미지원으로 교차 DB 조인 질의는 불가능하며, 이 제약을 우회하려면 응용단에서 개별 쿼리를 수행 후 결과를 합치는 논리가 필요합니다.

#### B.1.2 커뮤니티/로드맵 및 공식 지원 계획
DozerDB 공식 사이트와 개발사 자료에 따르면 Fabric 지원은 이후 계획되어 있습니다. 2025년 2월 발표된 DozerDB 5.26.3.0 버전에서는 Multi-DB까지만 지원하고, Fabric (다중 그래프 질의) 기능은 아직 베타/알파 단계로 보입니다.

Greystones 그룹의 DozerDB 소개 자료에서도 Neo4j Enterprise에만 있던 크로스 DB 질의, 분산 그래프 기능을 DozerDB에서도 제공할 것임을 명시하고 있습니다.

#### B.1.3 유사 사례 및 오픈소스 구현
현재 Neo4j Enterprise 이외에 크로스 그래프 질의를 지원하는 대표적 사례는 찾기 어렵습니다. 과거 Neo4j Community 사용자는 Fabric 미지원 문제를 해결하기 위해 하나의 거대 그래프에 모든 노드를 넣거나, 응용계층에서 여러 DB를 순차 질의하는 방식을 사용했습니다.

DozerDB는 이러한 맥락에서 거의 유일한 오픈소스 구현 사례이며, 커뮤니티에서도 많은 관심을 받고 있습니다. DozerDB Fabric은 커뮤니티 주도 최초의 크로스 Neo4j DB 쿼리 구현 시도로 볼 수 있습니다.

#### B.1.4 DataNexus 통합 고려사항
DataNexus에서는 그룹사별로 분리된 Neo4j 그래프(DB)를 사용하여 데이터 격리를 구현 중입니다. 향후 교차 도메인 질의 요구 발생 시 DozerDB Fabric 기능이 필요합니다.

통합 시, 각 그래프를 원격 노드로 등록하고 Fabric 질의를 수행해야 하므로 DozerDB 설정 및 쿼리 구조에 변경이 생깁니다. 또한 권한 관리 측면에서, Fabric으로 통합 쿼리 시에도 임의의 그래프 간 접근 통제가 필요하므로 추가 보안 레이어 검토가 필요합니다.

Fabric 쿼리는 일반 쿼리보다 응답 지연이 있을 수 있으므로, DataNexus의 실시간 응답 성능에 미칠 영향도 고려해야 합니다.

#### B.1.5 일정 및 우선순위
현재까지는 단일 도메인 질문 위주로 요구사항이 정의되어 Fabric의 부재가 치명적이지는 않습니다. 따라서 Fabric 지원은 단기적으로 최우선 과제는 아니며, DozerDB 측의 기능 출시 시점에 맞춰 중장기적으로 검토하면 됩니다.

2025년 중으로 DozerDB 2.0이 나오고 안정화된다면, 해당 버전을 평가환경에 적용하여 파일럿 테스트를 진행할 수 있을 것입니다. 우선순위는 중간 정도로 두되, DozerDB 업데이트에 따른 기술 검증을 사전 수행하는 것을 권장합니다.

### B.2 Query Log 자동 수집 (사용 쿼리 로그 축적 및 Sample SQL 학습)

#### B.2.1 기술 구현 가능성 및 제약
데이터베이스 쿼리 로그의 자동 수집은 비교적 성숙된 기술입니다. 많은 데이터 웨어하우스가 내부적으로 쿼리 이력을 제공하며, DataHub 같은 메타데이터 플랫폼은 이를 받아 메타데이터 엔티티로 저장하는 기능을 지원합니다.

DataHub에서는 Query라는 엔티티 타입을 통해 쿼리문, 해당 쿼리가 참조한 데이터셋, 실행 빈도 등의 속성을 관리합니다. Snowflake의 경우 `ACCOUNT_USAGE.QUERY_HISTORY` 뷰, BigQuery의 `INFORMATION_SCHEMA.JOBS` 등에서 최근 쿼리와 사용자, 스캔된 바이트 등을 조회 가능합니다.

주요 제약은 보안/프라이버시입니다. 쿼리 안에 이메일, 주민번호 등 민감정보 리터럴이 포함될 수 있어 로그를 수집/저장할 때 마스킹이 필요할 수 있습니다. 또한 쿼리 로그 양이 방대하면, 모든 쿼리를 저장하기보다 상위 N개 인기 쿼리 위주로 수집하거나 요약 통계만 저장하는 전략도 검토해야 합니다.

#### B.2.2 커뮤니티 및 공식 지원 계획
DataHub 오픈소스는 Dataset Usage & Query History라는 기능으로 쿼리 히스토리를 다루고 있으며, 이를 통해 특정 데이터셋을 어떤 쿼리가 얼마나 사용했는지 확인하는 UI를 제공합니다.

공식 문서에 언급된 바와 같이, Snowflake, Redshift 등 주요 DB에 대한 사용량 수집 커넥터가 기본 제공됩니다. DataNexus 자체 로드맵에서는 쿼리 로그 수집이 Phase 2 예정 기능으로 명시되어 있습니다.

#### B.2.3 유사 사례 및 오픈소스 구현 사례
Usage Analytics는 메타데이터 관리에서 흔히 볼 수 있는 기능입니다. DataHub에서는 UI 상의 Queries 탭에 상위 5개 쿼리를 노출하여 해당 데이터셋의 대표적 사용 형태를 알 수 있게 합니다.

NL2SQL 맥락에서는, OpenAI의 SQL GPT 시연이나, 일부 스타트업(예: DataHerald 등 오픈소스 프로젝트)에서 벡터 DB에 과거 쿼리를 저장해 유사 질문 시 참고하거나, LLM을 튜닝할 때 실제 사용자 로그를 활용하기도 합니다.

#### B.2.4 DataNexus 통합 고려사항
DataNexus에서는 DataHub를 통해 수집된 쿼리 로그를 RAG 학습 데이터로 활용하는 시나리오가 고려됩니다. PRD 명세에 따르면 초기 구축 시 기존 쿼리 로그를 수집해 초기 지식 그래프를 구축한다고 언급되어 있습니다.

운영 단계에서는 Chat UI를 통해 사용자가 NL 질의 → SQL 생성하게 되는데, 이때 발생한 질문-답변 쿼리 페어 또한 로그로 남길 수 있습니다. 이러한 로그들을 모아 DataHub의 Query 엔티티로 넣으면, DataHub 측에서 데이터셋과 GlossaryTerm의 사용 현황을 학습할 수 있습니다.

통합 구현 시 고려할 점은, 다양한 출처의 로그 통합입니다. DataWarehouse의 운영 쿼리 로그 + DataNexus 자체 생성 쿼리 로그를 한데 모아야 하는데, 각각 수집 방식이 다를 수 있습니다.

#### B.2.5 일정 및 우선순위
Query Log 자동 수집/학습 기능은 DataNexus Phase 2의 핵심 목표 중 하나입니다. 이는 현재 시스템이 기본 QA 기능을 충실히 구현한 다음, 지속적 학습과 성능 향상 단계로 넘어갈 때 투입될 기능으로 보입니다.

일정상 1차 릴리스 이후 빠른 시일 내 개발이 이상적이며, 우선순위 또한 높다고 할 수 있습니다. 2단계 초기에 주요 DW 1~2종(예: Oracle, Snowflake)의 쿼리 로그만 수집/활용해 효과를 검증한 후, 점차 지원 범위를 늘리는 것을 권장합니다.

### B.3 온톨로지 버전 관리 (Glossary Term 변경 이력 및 롤백)

#### B.3.1 기술 구현 가능성 및 제약
DataHub는 모든 메타데이터 변경을 Append-Only 이력으로 저장하기 때문에, Glossary Term의 변경 내역도 이론적으로 조회 및 복원 가능합니다. 예를 들어 용어 정의를 수정할 때마다 해당 GlossaryTerm 엔티티의 새로운 버전 번호가 매겨지고, GraphQL API로 과거 버전들을 질의할 수 있습니다.

실제로 DataHub GraphQL의 `aspects` 쿼리를 사용하면 특정 엔티티의 특정 Aspect(예: `glossaryTermProperties`)에 대한 과거 값 목록을 얻을 수 있습니다. 이러한 기반 기술로 버전 관리는 가능하나, UI 상 제공되지 않는 점이 제약입니다.

롤백 기능도 자동화되어 있지 않습니다. 롤백을 하려면 이전 버전 데이터를 새로운 업데이트로 재적용하는 식으로 처리해야 합니다. 이를 위해서는 이전 버전 내용을 가져와 동일한 GlossaryTerm URN에 다시 덮어써야 하며, GraphQL mutation이나 Metadata Change Proposal(MCP) API를 활용해야 합니다.

#### B.3.2 커뮤니티 및 로드맵
DataHub 커뮤니티에서는 메타데이터 변경 이력에 대한 요구가 지속되어 왔습니다. 2023년 후반~2024년에 걸쳐 DataHub에 Schema History라는 기능이 도입되어 데이터셋의 스키마 변경을 UI에서 비교할 수 있게 되었습니다.

GlossaryTerm에 대해서는 아직 UI 차원 History는 제공되지 않으나, Timeline API 수준에서는 지원됩니다. 2025 로드맵을 보면 메타데이터 Audit Logging 강화가 언급되어, 추후 UI에 전반적인 변경 이력 기능이 추가될 가능성이 있습니다.

한편, DataHub 문서에서는 Glossary를 Git으로 관리하는 방법을 안내하고 있습니다. 즉, 사내 용어집을 Git 저장소의 YAML/JSON으로 소스 관리하고, CI 파이프라인을 통해 DataHub에 반영하는 방식입니다.

#### B.3.3 유사 사례 및 구현 사례
Collibra나 Alation 같은 상용 데이터 카탈로그는 비즈니스 용어에 대해 히스토리 열람 및 승인 워크플로우를 제공합니다. 예를 들어 용어 정의를 변경하면 관리자 승인을 받도록 하고, 이전 정의와 새 정의를 비교하여 승인자가 볼 수 있게 하거나, 변경 이력을 타임라인 형태로 보여줍니다.

오픈소스 생태계에서는 DataHub가 유일하게 Glossary 기능을 어느 정도 제공하는데, 아직 상용만큼 UI가 세련되게 갖춰지진 않았습니다. DataHub + Git 연동이 가장 일반적인 해결책으로 받아들여지고 있습니다.

#### B.3.4 DataNexus 통합 고려사항
DataNexus는 용어 편집을 자체 Admin UI에서 제공할 계획이므로, 여러 사용자가 Glossary를 수정할 때 충돌이나 실수로 인한 잘못된 편집에 대비한 이력 관리가 중요합니다.

DataHub 자체가 변경 이력을 쌓고 있으므로, DataNexus 측에서 이를 활용하면 됩니다. 예를 들어 "최근 변경내역" 버튼을 눌렀을 때 DataHub GraphQL로 해당 용어의 이전 버전들을 가져와 타임라인 표를 보여줄 수 있습니다.

롤백 구현은 기술적으로 해당 버전의 aspect 내용을 다시 upsert하면 되므로, DataNexus 서버단에서 GraphQL로 이전 버전을 받고, 그 데이터를 `updateGlossaryTerm` Mutation으로 보내는 식으로 가능합니다.

**업데이트:** 섹션 4.4.4에서 증분 업데이트 전략과 버전 관리 스키마가 상세히 정의되었습니다. 이를 기반으로 구현을 진행할 수 있습니다.

#### B.3.5 일정 및 우선순위
Glossary 버전 관리 기능은 서비스 초기 단계보다는 용어 체계가 점차 복잡해지고 사용자 편집이 활발해질 단계에 필요합니다. 현재 DataNexus를 도입하는 조직에서 온톨로지 관리를 소수의 데이터 관리자가 전담한다면, 변경 이력을 수동으로 기록하거나, 문제가 생기면 직접 수정하는 것으로 충분할 수 있습니다.

하지만 용어의 수가 수백 개 이상으로 늘고, 여러 도메인 전문가가 동시다발적으로 편집하는 상황이 오면 버전 관리의 중요성이 급격히 높아집니다. Phase 2 이후 온톨로지 개방형 편집이 계획된다면, 그 이전에 이력을 추적하고 복원할 수 있는 기능을 마련해야 합니다.

### B.4 OWL/RDF 표준 호환 (DataHub Glossary ↔ OWL Ontology 변환)

#### B.4.1 기술 구현 가능성 및 제약
DataHub의 Glossary는 메타데이터 DB에 저장되는 용어/정의/관계 정보이고, OWL/RDF는 시맨틱 웹 표준 포맷입니다. 두 포맷 간의 상호 변환은 충분히 구현 가능하지만 직접 지원은 없음이 전제입니다.

기술적으로 Glossary Term을 OWL 클래스(Class)로 보고, Glossary 관계인 IsA(상위/하위)는 OWL의 `rdfs:subClassOf`로, HasA(포함관계)는 OWL 객체속성이나 SKOS의 `skos:broader` 관계 등으로 매핑할 수 있습니다.

제약으로는 표현력 한계가 있습니다. DataHub Glossary는 주로 용어의 정의와 관계만 관리하며, OWL처럼 논리적인 제약(예: 속성 도메인/범위, 상호 배타적 관계 등)을 표현하지 않습니다. 따라서 복잡한 OWL 온톨로지를 가져오면 일부 정보는 DataHub에 담을 곳이 없습니다.

#### B.4.2 커뮤니티/로드맵
현재까지 DataHub 프로젝트에서는 RDF나 OWL 호환성에 대한 계획을 공개한 적이 없습니다. DataHub는 자체 LiMeta 모델(JSON 기반)을 사용하고, 이를 GraphQL/REST API로 노출하는 데 초점을 맞춥니다.

시맨틱 웹 표준 연계는 주요 목표가 아니었기에, 공식 로드맵에서 해당 항목을 찾기 어렵습니다. 커뮤니티 문의에서도 OWL 내보내기보다는, "DataHub 데이터를 다른 툴에서 쓰고 싶으면 API로 가져가라"는 식의 답변이 일반적입니다.

#### B.4.3 유사 사례 및 구현
OWL/RDF 호환은 온톨로지 관리 전문 툴에서 주로 다룹니다. 대표적으로 TopQuadrant의 TopBraid EDG는 모든 용어와 관계를 RDF Triple Store에 저장하며, Export to OWL/RDF 기능을 UI로 제공합니다.

W3C의 SKOS(Simple Knowledge Organization System)가 용어 사전/분류체계를 RDF로 표현하는 표준으로 널리 쓰입니다. SKOS는 Concept이라는 클래스로 용어를 표현하고, `skos:broader`, `skos:narrower`로 상하위 관계, `skos:related`로 연관관계를 나타내며, `skos:altLabel`로 동의어를 다루는 등 DataHub Glossary와 개념적으로 유사합니다.

#### B.4.4 DataNexus 통합 고려사항
만약 DataNexus에 OWL/RDF 호환 기능을 도입한다면, 두 가지 시나리오가 있을 수 있습니다: (1) 기존 OWL 온톨로지 가져오기 – 외부 전문가가 관리하던 OWL 파일을 DataHub로 불러와 초기 Glossary로 사용하는 경우, (2) Glossary를 표준 형식으로 배포 – DataNexus에서 관리된 용어집을 타 부서 또는 공개 형식으로 제공하기 위해 RDF로 export.

통합 시 주의할 점은 동기화 문제입니다. OWL로 가져온 후 Glossary가 수정되면 OWL 원본과 불일치가 생길 수 있고, 반대로 Glossary를 RDF로 export했는데 이후 Glossary 편집이 되면 내보낸 버전은 구버전이 됩니다. 1회성 마이그레이션 도구로 제한하거나, read-only 용도로 export만 지원하는 식으로 범위를 한정하는 게 현실적입니다.

#### B.4.5 일정 및 우선순위
OWL/RDF 호환 기능은 DataNexus의 핵심 가치에는 직접 영향이 크지 않으므로, 우선순위는 낮은 편입니다. 현업 사용자는 자연어 질의와 답변 정확도에 관심이 높지, 용어집을 OWL로 주고받는 것은 주된 요구사항이 아닐 것입니다.

다만, 데이터 거버넌스/아키텍트 관점에서는 장기적으로 자사의 온톨로지를 국제 표준 형태로 관리하고 싶어 할 수 있습니다. 만약 이런 전략적 방향이 있다면, 우선순위가 상승할 수 있습니다. 이 항목은 Phase 3 또는 그 이후의 검토 과제로 보는 것이 적절합니다.

### B.5 자동 관계 추천 (LLM 기반 Glossary Term 관계 제안)

#### B.5.1 기술 구현 가능성 및 제약
LLM(예: GPT-4, Llama2 등)의 뛰어난 자연어 처리 능력을 활용하면, 용어들의 정의를 입력으로 주고 이들 사이의 관계를 추론 또는 분류하도록 시킬 수 있습니다. 예를 들어 Glossary에 "매출"과 "순매출"이라는 용어가 있고 각자의 정의가 있다면, LLM에게 "용어 A는 용어 B의 부분집합인가? 상위 개념인가?" 등을 질문해 관계를 유추하게 할 수 있습니다.

제약과 한계도 분명합니다. 첫째, LLM의 응답은 확률적인 언어 생성이므로, 환각(hallucination)이나 과잉 일반화 등 오류가 발생할 수 있습니다. 둘째, 규모 문제가 있습니다. 용어가 N개 있으면 잠재적 관계 쌍은 N^2에 달하는데, LLM에게 모든 조합을 일일이 평가시키는 것은 현실적이지 않습니다.

셋째, LLM이 잘 이해하지 못하는 전문 용어나 약어 등이 있다면 결과의 신뢰도가 떨어집니다. 넷째, LLM API를 쓴다면 비용(tokens 사용량)과 지연시간 이슈도 고려해야 하며, 사내에서 운영한다면 GPU 리소스 부하도 생각해야 합니다.

#### B.5.2 커뮤니티/로드맵
현재 DataHub나 유사한 오픈소스 메타데이터 툴에서 LLM을 이용한 관계 추천 기능은 공식적으로 언급되지 않고 있습니다. DataHub의 경우 2023년에 AI Glossary Term Suggestion이라는 기능을 클라우드 버전에서 선보였는데, 이는 테이블/컬럼에 붙일 적절한 Glossary 용어를 LLM이 추천하는 것입니다.

업계 전반으로 보면, LLM+Knowledge Graph 통합이 화두가 되면서, Graph DB 벤더들이 "LLM으로 손쉽게 온톨로지 작성" 같은 비전을 제시하기 시작했습니다. 학계에서도 LLM을 활용해 온톨로지 확장, 관계 추론을 하는 연구들이 2023~2024년에 다수 발표되었습니다.

#### B.5.3 유사 사례 및 오픈소스
자동 관계 추천과 가장 유사한 기술 영역은 Knowledge Graph Completion 및 Ontology Learning입니다. 전통적으로는 임베딩 모델(TransE 등)을 사용해 그래프의 missing link를 예측하는 방식이 연구되었는데, LLM 등장 이후에는 텍스트로부터 온톨로지 추출이 주목받고 있습니다.

마이크로소프트가 발표한 GraphRAG 등도 LLM으로 데이터 관계를 파악하는 아이디어의 연장선입니다. 전반적으로, LLM 기반 관계 추천은 이제 막 등장한 컨셉으로, 참고할 만한 완성형 오픈소스는 드문 상황입니다.

#### B.5.4 DataNexus 통합 고려사항
자동 관계 추천을 DataNexus에 통합하려면, UX와 백엔드 설계 모두 신중히 해야 합니다. Glossary 편집 화면에 "관계 제안" 혹은 "연관 용어 추천" 버튼을 둘 수 있습니다. 관리자가 어떤 용어나 온톨로지 섹션을 선택하고 이 기능을 실행하면, 백엔드에서 LLM API를 호출하여 해당 용어와 관련 있을 만한 다른 용어를 찾아줍니다.

비용 최적화를 위해 1회 프롬프트에 여러 관계를 묶어 질문하거나, 임베딩으로 예비 후보를 선정한 뒤 LLM 확인을 거치는 식이 필요할 것입니다. 추천 정확도를 높이기 위해, LLM output에 self-confidence score를 포함시키거나, 동일 질문을 여러 패턴으로 물어봐 일관된 답만 채택하는 등 전략을 쓸 수 있습니다.

또한, 추천 결과를 그대로 적용하면 잘못된 관계가 들어갈 우려가 있으므로, 반드시 사람의 승인 절차(Human-in-the-loop)를 거치게 해야 합니다.

#### B.5.5 일정 및 우선순위
자동 관계 추천은 굉장히 흥미로운 기능이지만, 기본 제품 기능의 완성도에 비하면 부차적인 요소입니다. 이 기능 없이도 Glossary 관계는 도메인 전문가가 수동으로 정의할 수 있고, 당장 DataNexus의 핵심 가치 실현에는 문제가 없습니다.

따라서 우선순위는 상대적으로 낮으며, Phase 1~2에서는 배제하고 Phase 3 이후 R&D 테마로 다루는 게 현실적입니다. 다만, 최근 AI 트렌드를 활용한 차별화 포인트가 될 수 있기에 프로토타입 수준에서 미리 실험해볼 가치는 있습니다.

### B.6 DataHub synonyms 필드 공식 지원 여부 (동의어 관리 기능)

#### B.6.1 기술 구현 가능성 및 제약
DataHub의 GlossaryTerm 객체는 기본적으로 name, definition, termLinks, relatedTerms 등의 필드를 갖지만 synonyms 전용 필드가 없습니다. 따라서 하나의 개념에 대한 여러 이름(AKA)을 관리하려면, 현재는 커스텀 어트리뷰트를 정의하거나, 설명에 "별칭: ..." 형태로 기입하는 방식으로 우회해야 했습니다.

DataNexus에서는 이 한계를 인지하고 이미 커스텀 synonyms 필드(JSON 배열)를 GlossaryTerm에 붙여 쓰고 있습니다. PRD에서 언급된 바와 같이, Exact/Synonym/Fuzzy 매칭으로 사용자의 다양한 용어 표현을 공식 용어로 식별하는 로직에 이 synonyms 데이터가 활용됩니다.

제약으로는, 커스텀 구현은 DataHub 표준 API나 UI에서 바로 보이지 않으므로 유지보수가 번거롭다는 점입니다.

#### B.6.2 커뮤니티 및 공식 지원 계획
DataHub 커뮤니티에서는 Glossary Synonyms 필요성이 일찍부터 제기되어, 공식 Feature Request 플랫폼에 해당 요청이 올라간 상태입니다 (제목: "Ability to add synonyms").

2025년 DataHub 로드맵을 다룬 Medium 글에서도 "Glossary Synonyms: Link glossary terms to other synonym terms"라는 항목이 잠재적 기능으로 언급되어 있습니다. 이는 용어들 간에 동의어 관계를 연결하고, 검색 시 해당 용어 또는 그 동의어로도 검색되도록 하는 내용을 담고 있습니다.

이로 보아 DataHub 핵심 팀도 동의어 지원의 중요성을 인지하고 있으며, 2025년 내에 구현을 검토하고 있음을 알 수 있습니다. 공식 지원은 시간 문제로 보입니다.

#### B.6.3 유사 사례
Collibra의 Business Glossary 모듈에는 용어 속성 중 Abbreviation/Acronym이나 Also Known As 같은 필드가 있어 동의어나 약칭을 관리할 수 있습니다. 또한 Google Data Catalog(현재 Dataplex)도 Tag로 유사어를 붙이는 사례가 있습니다.

SKOS 온톨로지 표준에서도 `skos:altLabel`을 통해 한 개념의 대체 레이블(동의어, 약어)을 지정하게 되어 있어, 업계 전반적으로 동의어 관리는 표준적인 요구라고 볼 수 있습니다.

#### B.6.4 DataNexus 통합 고려사항
DataNexus는 현재 동의어 커스텀 필드를 이미 운영 중이므로, 공식 필드가 생기면 두 가지를 통합하는 작업이 필요합니다. 우선 DataHub를 업그레이드할 때, 기존 커스텀 필드에 저장된 동의어 리스트를 새로운 공식 구조로 옮겨야 합니다.

또한, DataNexus의 검색 및 Q&A 파이프라인 중 동의어를 처리하는 부분을 공식 기능에 맞게 수정해야 합니다. 현재는 엔티티 추출 단계에서 커스텀 synonyms 목록을 참조하여 사용자의 질문 토큰이 어느 GlossaryTerm의 동의어인지 매핑하고 있는데, 공식 지원 후에는 DataHub의 검색 API나 추천 API가 그 기능을 제공할 수도 있습니다.

권고되는 접근은, 공식 지원 전까지는 현행 커스텀 방식을 유지하되, 공식 지원 후 최대한 빨리 전환하는 것입니다.

#### B.6.5 일정 및 우선순위
동의어 관리 기능은 온톨로지 사용자 경험에 매우 중요한 요소입니다. 하나의 개념을 사람마다 다른 용어로 부르는 경우가 흔하여, 이를 관리하지 않으면 자연어 질문 인식률이 떨어지기 때문입니다.

DataNexus에서 이를 Phase 1에 커스텀 구현한 것도 그 중요성 때문입니다.

향후 공식 지원이 나오면, 이는 DataNexus에 긍정적인 변화를 줄 전망입니다. 공식 기능으로 전환함으로써 DataHub 커뮤니티의 업데이트 혜택(예: synonyms까지 고려한 검색 향상)을 얻고, 커스텀 코드 양을 줄여 유지보수성을 높일 수 있습니다.

2025년 내 지원이 유력하므로, 그 시기에 업그레이드 플랜을 세워두는 것이 좋습니다. 공식 지원 시 즉각 마이그레이션하는 것이 바람직합니다.

### B.7 종합 우선순위 매트릭스
각 향후 검토 항목에 대한 종합 평가 결과를 아래 표로 정리합니다.

| 검토 항목 | 기술 준비도 | 비즈니스 가치 | 권장 Phase | 핵심 고려사항 |
| :--- | :--- | :--- | :--- | :--- |
| DozerDB Fabric 지원 | 중간 | 중간 | Phase 3+ | DozerDB 출시 시점 모니터링, 크로스 DB 질의 수요 발생 시 검토 |
| Query Log 자동 수집 | 높음 | 높음 | Phase 2 | NL2SQL 품질 향상의 핵심, DataHub 커넥터 활용으로 개발 효율화 |
| 온톨로지 버전 관리 | 중간 | 중간-높음 | Phase 2 | 다수 편집자 참여 시 필수, DataHub UI 지원 동향 모니터링, **기본 전략 정의됨** |
| OWL/RDF 표준 호환 | 중간 | 낮음 | Phase 3+ | 전략적 표준화 방향에 따라 결정, 당장은 우선순위 낮음 |
| 자동 관계 추천 (LLM) | 낮음-중간 | 중간 | R&D | 혁신 포인트 가능, 정확도/비용 검증 후 제품화 결정 |
| DataHub synonyms 공식 지원 | 높음 (예정) | 높음 | Phase 1.5 | 현재 커스텀 구현 중, 공식 지원 시 즉시 마이그레이션 |
| **관계 표현력 세분화** | **높음** | **높음** | **Phase 1** | **Multi-hop 추론 정확도 핵심, 즉시 적용 권장** |
| **스키마 강제성** | **높음** | **높음** | **Phase 1** | **지식 그래프 품질 보장, 즉시 적용 권장** |
| **CQ 기반 검증** | **높음** | **높음** | **Phase 0.5** | **구축 전 적합성 검증으로 실패 비용 최소화** |
| **증분 업데이트** | **중간-높음** | **높음** | **Phase 1** | **운영 비용 절감의 핵심, 즉시 적용 권장** |
| **SKOS 호환 레이어** | **높음** | **중간** | **Phase 1.5** | **표준 호환성 확보, 외부 온톨로지 활용** |
| **Query Router Agent** | **높음** | **높음** | **Phase 1** | **논리적 정확성 보장, 비용 효율화** |
| **LLM Drafting** | **중간** | **높음** | **Phase 1** | **구축 공수 60% 절감** |
| **DataHub 호환성** | **높음** | **중간** | **Phase 2** | **플랫폼 안정성, 무중단 업그레이드** |
| **Shaper 대시보드 연동** | **높음** | **높음** | **Phase 1.5** | **Vanna NL2SQL→대시보드 승격, PDF/Excel 보고 자동화, 임베디드 분석** |

#### B.7.1 권장 실행 로드맵
- **Phase 0.5 (2026 Q1):** CQ 기반 검증 프레임워크 구축
- **Phase 1 (2026 Q1-Q2):** 관계 표현력 세분화, 스키마 강제성 파이프라인, 증분 업데이트 전략, **Query Router Agent, LLM Drafting, Vanna 2.0 기반 NL2SQL 구축**
- **Phase 1.5 (2026 Q2):** DataHub synonyms 공식 지원 시 마이그레이션, **SKOS 호환 레이어**, **Shaper 도입 및 Dashboard Promotion 기본 워크플로, JWT RLS 통합**
- **Phase 2 (2026 Q2-Q3):** Query Log 자동 수집, 온톨로지 버전 관리 UI, **DataHub 업그레이드 호환성 관리**, **Shaper PDF/Excel 자동 보고, 임베디드 분석(React SDK), 예약 리포트 발송**
- **Phase 3+ (2026 Q4 이후):** DozerDB Fabric, **전면 OWL/RDF 표준 호환, 전문 추론 엔진**
- **R&D (지속):** LLM 기반 자동 관계 추천 프로토타입 개발 및 검증, **Federated Ontology 연구**

### B.8 Vanna 2.0 적용 가이드 (신규 구축)

#### B.8.1 Vanna 2.0 핵심 특징
Vanna 2.0은 프로덕션 환경을 위해 완전히 재설계된 버전으로, DataNexus의 엔터프라이즈 요구사항에 최적화되어 있습니다:

| 특징 | 설명 | DataNexus 활용 |
| :--- | :--- | :--- |
| **Agent-based API** | 독립적인 Agent 구성 요소 조합 | 모듈화된 NL2SQL 파이프라인 구축 |
| **User-aware** | 모든 컴포넌트에 사용자 ID 자동 전파 | 테넌트별 쿼리 컨텍스트 분리 |
| **Streaming** | Rich UI Components (테이블, 차트) 실시간 전송 | Chat UI 사용자 경험 향상 |
| **Row-level Security** | 사용자별 데이터 필터링 내장 | 그룹사별 데이터 격리 강화 |
| **Tool Memory** | 성공한 쿼리 자동 학습 | NL2SQL 정확도 지속 개선 |
| **Audit Logs** | 사용자별 쿼리 추적 내장 | 컴플라이언스 요구사항 충족 |

#### B.8.2 DataNexus 구현 설계

**1. Agent 구성**
```python
from vanna.core import Agent, ToolRegistry
from vanna.tools import RunSqlTool
from vanna.llm import AnthropicLlmService

# DataNexus용 사용자 인증 연동
class DataNexusUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        # DataNexus 인증 시스템과 연동
        token = request_context.get_header('Authorization')
        user_data = self.verify_insight_token(token)
        return User(
            id=user_data['user_id'],
            email=user_data['email'],
            group_memberships=[user_data['tenant_id']]  # 테넌트 기반 권한
        )

# Agent 초기화
llm = AnthropicLlmService(model="claude-sonnet-4-5-20250929")  # 실제 배포 시 최신 모델 ID로 교체
tools = ToolRegistry()
tools.register(RunSqlTool(sql_runner=BigQueryRunner(project="insight-agent")))

agent = Agent(
    llm_service=llm,
    tool_registry=tools,
    user_resolver=DataNexusUserResolver()
)
```

**2. 온톨로지 컨텍스트 주입**
```python
from vanna.tools import Tool, ToolContext

class OntologyAwareSqlTool(Tool):
    """DataHub 온톨로지를 활용한 NL2SQL"""
    
    async def execute(self, context: ToolContext, args: SqlArgs) -> ToolResult:
        user = context.user
        tenant_id = user.group_memberships[0]
        
        # 테넌트별 온톨로지 로드
        ontology = await self.load_ontology(tenant_id)
        
        # 온톨로지 컨텍스트로 SQL 생성 정확도 향상
        enhanced_prompt = self.inject_ontology_context(
            question=args.question,
            ontology=ontology
        )
        
        return await self.generate_sql(enhanced_prompt)
```

**3. Web UI 통합**
```html
<!-- DataNexus Chat UI에 Vanna 컴포넌트 통합 -->
<script src="https://img.vanna.ai/vanna-components.js"></script>
<vanna-chat 
    sse-endpoint="/api/v1/nl2sql/chat"
    theme="light"
    tenant-id="{{current_tenant}}"
>
</vanna-chat>
```

#### B.8.3 구현 체크리스트

| 구현 항목 | 담당 | 예상 공수 | 우선순위 |
| :--- | :--- | :--- | :--- |
| DataNexusUserResolver 구현 | 백엔드 | 3일 | 높음 |
| OntologyAwareSqlTool 구현 | 백엔드 | 5일 | 높음 |
| Agent 초기화 및 라우팅 설정 | 백엔드 | 2일 | 높음 |
| SSE 엔드포인트 구현 (Streaming) | 백엔드 | 3일 | 높음 |
| Row-level Security 테넌트 연동 | 백엔드 | 3일 | 높음 |
| Chat UI Streaming 컴포넌트 통합 | 프론트엔드 | 5일 | 중간 |
| Tool Memory 학습 파이프라인 | 백엔드 | 3일 | 중간 (Phase 2) |
| Audit Log 대시보드 | 프론트엔드 | 3일 | 낮음 |

**총 예상 공수:** 27 M/D

#### B.8.4 Vanna 2.0 활용 장점

| 기존 직접 구현 필요 항목 | Vanna 2.0 내장 기능 | 절감 효과 |
| :--- | :--- | :--- |
| 사용자별 쿼리 로깅 | Audit Logs | 5 M/D |
| 테넌트별 데이터 필터링 | Row-level Security | 8 M/D |
| 실시간 응답 스트리밍 | Streaming Components | 5 M/D |
| 쿼리 패턴 학습 | Tool Memory | 10 M/D |
| **합계** | | **~28 M/D 절감** |

※ 본 분석은 2026년 2월 기준 정보를 바탕으로 작성되었으며, 각 오픈소스 프로젝트의 로드맵 변경에 따라 우선순위가 조정될 수 있습니다.

#### B.8.5 Text-to-SQL 경쟁 솔루션 비교

DataNexus가 Vanna AI를 선정한 근거를 경쟁 솔루션과의 비교를 통해 명확히 한다. Snowflake 내부 벤치마크에서 GPT-4o 단독 Text-to-SQL 정확도가 51%에 불과했다는 결과(Cortex Analyst Behind the Scenes)는, RAG 없는 LLM 네이티브 접근의 한계를 보여준다.

| 특성 | Vanna AI 2.0 | Snowflake Cortex Analyst | LangChain SQL Agent | Wren AI |
| :--- | :--- | :--- | :--- | :--- |
| **아키텍처** | RAG 기반 Python 프레임워크 | Semantic View + Multi-Agent | LLM 네이티브 추론 | Full BI + Semantic Layer |
| **핵심 강점** | 유연성, 셀프호스팅, 오픈소스 | 높은 정확도, Snowflake 생태계 통합 | LangChain 에코시스템 활용 | 거버넌스, E2E BI |
| **정확도 수준** | RAG로 ~70-75% (온톨로지 추가 시 향상) | ~85-90% (Multi-Agent 보정) | ~51% (LLM 단독 수준) | Semantic Layer로 향상 |
| **멀티테넌시** | User-aware + Row-level Security 내장 | Snowflake 네이티브 | 직접 구현 필요 | Enterprise 플랜 |
| **DB 지원** | 다중 DB (Snowflake, BigQuery, PostgreSQL 등) | Snowflake 전용 | 다중 DB (SQLAlchemy) | 다중 DB |
| **학습 방식** | Q-SQL 쌍 + DDL + 문서 RAG | Semantic View 정의 | Few-shot 프롬프트 | Semantic Modeling |
| **오픈소스** | Yes (MIT) | No (Snowflake 서비스) | Yes (MIT) | Yes (AGPL) |
| **프론트엔드** | `<vanna-chat>` 웹 컴포넌트 + Flask/Chainlit | Snowflake UI 내장 | 직접 구현 | 내장 UI |
| **인증** | Google Cloud Ready — BigQuery (2025) | Snowflake 네이티브 | 없음 | 없음 |

**DataNexus 선정 근거:**

- **오픈소스 + 셀프호스팅:** 엔터프라이즈 보안 요구사항(JWT, 테넌트 격리) 충족 가능
- **온톨로지 확장성:** Vanna의 RAG Store에 DataHub Glossary 컨텍스트를 주입하는 구조가 DataNexus 아키텍처(§4.3)와 자연스럽게 맞물림
- **Agent-based API (2.0):** Tool Memory, Row-level Security 등 프로덕션 필수 기능 내장으로 ~28 M/D 절감 (§B.8.4)
- **Cortex Analyst 대비 트레이드오프:** 정확도는 Cortex가 높지만, 벤더 종속(Snowflake Only) + 비공개 소스라는 제약이 있음. DataNexus는 다중 DB 환경을 전제하므로 Vanna가 적합
- **LangChain SQL Agent 대비:** LLM 네이티브 추론만으로는 51% 수준이므로, RAG 기반 Vanna가 구조적으로 우위

> **📌 정확도 비교 상세:** [PRD_05 §5.6.1 NL2SQL Baseline 정확도 컨텍스트](./PRD_05_Evaluation_Quality_final.md) 참조
> **📌 경쟁 솔루션 URL:** [PRD_06 §8.6](./PRD_06_Requirements_Roadmap_final.md) 참조 (반영 예정)

#### B.8.6 Vanna 알려진 한계 및 DataNexus 보완 전략

Vanna AI는 RAG 기반 NL2SQL 프레임워크로서 코드 효율성과 확장성이 뛰어나나, 프로덕션 적용 시 다음 한계를 인지해야 한다. 각 한계에 대한 DataNexus의 구체적 보완 전략을 함께 정리한다.

| # | 한계점 | 영향 | DataNexus 보완 |
| :--- | :--- | :--- | :--- |
| L-1 | **질문에 직접 답변하지 않음** — SQL + 차트/테이블만 반환, 자연어 인사이트 미제공 | 사용자가 결과 해석을 직접 해야 함 | DataNexus는 Vanna SQL 실행 결과를 LLM에 재투입하여 자연어 요약 + 인사이트를 생성 ([PRD_01 §2.1.3](./PRD_01_Overview_Architecture_final.md) 플로우 ④단계) |
| L-2 | **잘못된 학습 데이터 주입 위험** — 사용자가 Q-SQL 쌍을 직접 추가 가능 | 부정확한 SQL이 RAG Store에 누적 → 정확도 하락 | Admin 승인 프로세스 도입: 사용자 제출 → 자동 Schema Validation → DBA 검증 → 승인 후 학습 반영 ([PRD_02 §3.8](./PRD_02_Core_Features_Agent_final.md)) |
| L-3 | **UX 커스터마이징 제한** — VannaFlaskApp 1,200줄 이상, 프론트엔드 커스텀 진입장벽 높음 | 디자인 시스템 일관성 확보 어려움 | DataNexus 자체 Chat UI ([PRD_07 §11 Design System](./PRD_07_UI_Design_final.md)) + Vanna SSE 엔드포인트만 활용. `<vanna-chat>` 웹 컴포넌트는 PoC 전용 |
| L-4 | **벡터 검색 정밀도 한계** — 유사 질문이 많으면 관련 없는 Q-SQL 쌍 검색 | 프롬프트 오염 → 잘못된 SQL 생성 | 온톨로지 기반 메타데이터 필터링: 질문에서 추출한 Glossary Term으로 RAG 검색 범위를 사전 축소 ([PRD_03 §4.3](./PRD_03_Data_Pipeline_final.md) ⑦단계) |
| L-5 | **보안 취약점** — Prompt Injection으로 임의 SQL 실행 가능 (CVE-2024-5565) | 데이터 유출, DB 손상 위험 | SQL Allowlist 검증 ([PRD_02 §3.8](./PRD_02_Core_Features_Agent_final.md)), Row-level Security 강제, 금지 패턴 차단 (DELETE, DROP, TRUNCATE) |

##### L-2 보완: 학습 데이터 승인 워크플로

```txt
[사용자: Q-SQL 쌍 제출] → [자동 검증]
    ├─ SQL 구문 유효? → No → 반려 + 오류 안내
    ├─ Schema Validation 통과? → No → 반려 + 존재하지 않는 테이블/컬럼 안내
    └─ 통과 → [DBA 검토 큐]
                ├─ 승인 → Vanna Tool Memory에 학습
                └─ 반려 → 사용자에게 수정 요청 + 사유 안내
```

이 워크플로는 §3.9의 Dashboard Promotion 승인 프로세스와 동일한 패턴을 따른다.

##### L-1 보완: LLM 인사이트 생성 체인

Vanna가 SQL + DataFrame만 반환하는 한계를 극복하기 위해, DataNexus는 아래 체인을 추가로 실행한다:

```python
# Vanna SQL 실행 후 인사이트 생성 체인 (개념 설계)
# 참고: Chainlit + LlamaIndex 통합 패턴 (MITB For All, 2025.06)

async def generate_insight(question: str, sql: str, df: DataFrame) -> str:
    """Vanna 결과를 LLM에 재투입하여 자연어 인사이트 생성"""
    prompt = f"""
    사용자 질문: {question}
    실행된 SQL: {sql}
    결과 데이터:
    {df.to_markdown(index=False)}
    
    위 데이터를 바탕으로 사용자 질문에 대한 인사이트를 자연어로 작성하세요.
    핵심 수치와 트렌드를 강조하고, 추가 분석이 필요한 부분을 제안하세요.
    """
    return await llm.agenerate(prompt)
```

이 패턴은 §2.1.3 플로우의 ④단계(LLM 응답 생성)에 해당하며, Vanna의 SQL 생성과 DataNexus의 인사이트 생성이 역할 분리된 구조를 유지한다.

##### 참고: Chainlit 기반 PoC 프론트엔드

DataNexus 본 UI는 React 기반 커스텀 Chat UI(§11)를 사용하지만, Phase 0.5 PoC 또는 내부 DBA/DA 전용 데모 용도로 Chainlit 기반 경량 프론트엔드를 병행할 수 있다. Chainlit은 Python만으로 ~150줄 내에 Vanna의 SQL 생성 → 실행 → 시각화 → 후속 질문 파이프라인을 구현 가능하다.

- **GitHub 참조:** https://github.com/vanna-ai/vanna-chainlit
- **활용 시나리오:** Phase 0.5 PoC 데모, DBA 전용 분석 도구 (본 UI 개발 전 임시), Vanna training 데이터 검증용 테스트 인터페이스

> ⚠️ Chainlit은 PoC 전용이며, 프로덕션 Chat UI는 반드시 Design System(§11) 기반 React 컴포넌트를 사용한다.

### B.9 Shaper 도입 가이드 (SQL 기반 대시보드 & 자동화 보고)

#### B.9.1 기술 개요 및 선정 근거

Shaper는 DuckDB 기반의 오픈소스 SQL-First 데이터 대시보드 플랫폼으로, 기존 Metabase/Superset 대비 코드 기반 워크플로와 경량 배포에 강점이 있습니다.

**DataNexus에 Shaper를 선정한 근거:**

| 비교 기준 | Metabase | Superset | **Shaper** | DataNexus 적합성 |
| :--- | :--- | :--- | :--- | :--- |
| 아키텍처 | Java (Clojure) | Python (Flask) | **Go + TypeScript** | Go의 경량 바이너리, 컨테이너 친화적 |
| SQL 접근 방식 | GUI 중심 + SQL 보조 | GUI 중심 + SQL 에디터 | **SQL-First (모든 구성이 SQL)** | Vanna 생성 SQL의 직접 재사용에 최적 |
| 임베딩 방식 | iframe | iframe | **React SDK (iframe-free)** | DataNexus Frontend에 네이티브 통합 |
| Row-level Security | 별도 설정 필요 | RBAC + Row-level | **JWT 기반 RLS 내장** | DataNexus JWT 토큰 직접 연동 |
| 리포트 자동화 | Pro 유료 기능 | 제한적 | **PDF/CSV/Excel 기본 제공** | MVP부터 자동 보고 기능 활용 |
| 배포 복잡도 | 중간 (Java 런타임) | 높음 (다수 의존성) | **낮음 (단일 Docker)** | DataNexus 인프라에 경량 추가 |
| 라이선스 | AGPL-3.0 | Apache-2.0 | **MPL-2.0** | 상업적 활용 유연성 |
| 버전 관리 | UI 기반 | UI 기반 | **Git 기반 워크플로** | 대시보드 코드 리뷰 + CI/CD 통합 |

**핵심 선정 이유:** Vanna가 생성한 SQL을 변환 없이 Shaper에 직접 등록할 수 있어, NL2SQL → 대시보드 승격 워크플로의 기술적 마찰이 최소화됩니다. 또한 React SDK 기반 iframe-free 임베딩은 DataNexus의 React/Next.js Frontend와 네이티브 수준으로 통합됩니다.

#### B.9.2 DataNexus 통합 아키텍처

```txt
┌─────────────────────────────────────────────────────────────────┐
│                      DataNexus Platform                          │
│                                                                   │
│  ┌───────────────┐    ┌───────────────┐    ┌──────────────────┐  │
│  │ Chat UI       │    │ Admin UI      │    │ Embedded         │  │
│  │ (Vanna NL2SQL)│    │ (대시보드 관리)│    │ Dashboard        │  │
│  └───────┬───────┘    └───────┬───────┘    │ (React SDK)      │  │
│          │                    │            └──────────┬───────┘  │
│          │                    │                       │          │
│  ┌───────▼────────────────────▼───────────────────────▼───────┐  │
│  │            DataNexus Backend (FastAPI)                       │  │
│  │   ┌──────────────────────────────────────────────────────┐  │  │
│  │   │  Dashboard Promotion Service                          │  │  │
│  │   │  • SQL 추출 + 파라미터화                              │  │  │
│  │   │  • Shaper API 연동                                    │  │  │
│  │   │  • JWT RLS Token 생성                                 │  │  │
│  │   └──────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────┬────────────────────────────────┘  │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               │
                      ┌────────▼────────┐
                      │     Shaper      │
                      │  (DuckDB 기반)  │
                      │                 │
                      │ • SQL Dashboard │
                      │ • Report Engine │
                      │ • Embed API     │
                      └────────┬────────┘
                               │
                    ┌──────────┼──────────┐
                    │          │          │
              ┌─────▼────┐ ┌──▼───┐ ┌───▼────┐
              │PostgreSQL │ │ CSV/ │ │ DW     │
              │(DataNexus)│ │Parquet│ │(Oracle/│
              │           │ │      │ │Snowflk)│
              └──────────┘ └──────┘ └────────┘
```

#### B.9.3 구현 체크리스트

| 구현 항목 | 담당 | 예상 공수 | Phase | 우선순위 |
| :--- | :--- | :--- | :--- | :--- |
| Shaper Docker 인프라 구성 | DevOps | 1일 | Phase 1.5 | 높음 |
| Dashboard Promotion API 설계/구현 | 백엔드 | 5일 | Phase 1.5 | 높음 |
| Vanna ↔ Shaper SQL 파라미터화 엔진 | 백엔드 | 3일 | Phase 1.5 | 높음 |
| JWT RLS 토큰 브릿지 구현 | 백엔드 | 3일 | Phase 1.5 | 높음 |
| Chat UI "대시보드로 저장" 버튼 | 프론트엔드 | 2일 | Phase 1.5 | 높음 |
| 대시보드 목록/관리 Admin UI | 프론트엔드 | 3일 | Phase 1.5 | 중간 |
| **Promotion Lineage 테이블 + API (§3.9.7)** | **백엔드** | **2일** | **Phase 1.5** | **높음** |
| **Drift Detection 스케줄러 (§3.9.7.3)** | **백엔드** | **1일** | **Phase 1.5** | **높음** |
| React SDK 임베디드 통합 | 프론트엔드 | 5일 | Phase 2 | 중간 |
| PDF/Excel 자동 보고 파이프라인 | 백엔드 | 3일 | Phase 2 | 중간 |
| 예약 리포트 발송 (Celery Task) | 백엔드 | 3일 | Phase 2 | 중간 |
| 자동 승격 제안 로직 (반복 질의 감지) | 백엔드 | 2일 | Phase 2 | 낮음 |
| **DashboardStalenessDetector + Kafka 핸들러 (§3.9.8)** | **백엔드** | **3일** | **Phase 2** | **높음** |
| **DashboardReturnService + 컨텍스트 주입 (§3.9.9)** | **백엔드** | **2일** | **Phase 2** | **중간** |
| **Lineage/Staleness Admin UI (Drift 모니터링)** | **프론트엔드** | **2일** | **Phase 2** | **중간** |
| **RE_PROMOTE 워크플로 (기존 대시보드 SQL 교체)** | **백엔드** | **1일** | **Phase 2** | **중간** |

**총 예상 공수:** 41 M/D (Phase 1.5: 20일 + Phase 2: 21일)

> **📌 기존 30 M/D 대비 +11 M/D 증가.** Lineage 테이블(2일), Drift 감지(1일)는 Phase 1.5에 포함하여 승격과 동시에 추적을 시작합니다. Staleness 감지(3일), Return Service(2일), Admin UI(2일), RE_PROMOTE(1일)는 Phase 2에서 구현합니다.

#### B.9.4 Shaper 기술 스택 상세

| 기술 | 버전 | 역할 |
| :--- | :--- | :--- |
| Go | 1.22+ | Shaper 백엔드 서버 (49.7%) |
| TypeScript | 5.x | Shaper 프론트엔드/React SDK (47.2%) |
| DuckDB | 내장 | SQL 실행 엔진 (서버 불필요) |
| Docker | 24.0+ | 배포 (`docker run -p5454:5454 taleshape/shaper`) |

**DataNexus 인프라 포트 배정:**

| 서비스 | 포트 | 비고 |
| :--- | :--- | :--- |
| Shaper Web UI | 5454 | 기존 DataNexus 인프라 포트와 충돌 없음 |

> **리포지토리:** https://github.com/taleshape-com/shaper
> **공식 문서:** https://taleshape.com/shaper/docs
> **라이선스:** MPL-2.0

---
