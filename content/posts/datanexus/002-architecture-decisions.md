---
title: "2. 4개의 오픈소스를 이 조합으로 결정하기까지"
date: 2026-02-16
draft: false
summary: "DataNexus의 기술 스택을 DataHub + Vanna + ApeRAG + DozerDB로 결정한 과정. 후보군에서 탈락한 것들과 그 이유."
categories: ["architecture"]
tags: ["datanexus", "datahub", "vanna", "dozerdb", "aperag"]
series: ["datanexus-building-log"]
series_order: 2
ShowToc: true
---

## 비교 후보군

후보가 너무 많았다.

메타데이터 카탈로그만 해도 DataHub, Amundsen, Apache Atlas, OpenMetadata가 있었고, 상용까지 포함하면 Collibra, Alation도 후보였다. NL2SQL 엔진, 문서 지식엔진, 그래프 DB까지 네 개 축을 채워야 하는데 조합의 수가 기하급수적으로 불어났다.

구글 시트에 비교표를 만들었다. 행이 후보 도구, 열이 평가 기준. 3주쯤 지나니까 시트가 7개 탭으로 늘어나 있었다. 선택지가 많으면 안 고르는 게 문제다. 하나를 고르면 나머지와의 조합이 바뀌고, 그러면 다시 처음부터 비교해야 했다.

## 네 가지 컴포넌트, 각각의 요건

[이전 글](/posts/datanexus/001-why-datanexus/)에서 DataNexus의 네 가지 컴포넌트를 정의했다. 메타데이터 카탈로그, NL2SQL 엔진, 문서 지식엔진, 그래프 DB. 각 컴포넌트마다 양보할 수 없는 요건이 있었다.

공통 기준은 셋이다.

- **오픈소스일 것.** 엔터프라이즈 라이선스 비용은 이 프로젝트의 성격과 맞지 않는다.
- **멀티테넌시를 지원하거나 구현 가능할 것.** 그룹사별 데이터 격리는 필수였다.
- **프로덕션 레디일 것.** 커뮤니티 활성도, 릴리즈 주기, 문서화 수준을 봤다.

여기에 컴포넌트별로 추가 요건이 붙었다.

| 컴포넌트 | 핵심 요건 |
|--------|----------|
| 메타데이터 카탈로그 | Business Glossary에서 용어 간 관계 정의 가능, 변경 이벤트를 실시간으로 내보낼 수 있을 것 |
| NL2SQL 엔진 | 사용자별 컨텍스트 분리, Row-level Security 내장, 학습 루프 |
| 문서 지식엔진 | 벡터 검색 + 그래프 검색 하이브리드, 복잡한 문서(테이블/수식) 파싱 |
| 그래프 DB | Multi-DB(데이터베이스별 격리), Cypher 쿼리 지원 |

이 기준을 들고 후보를 걸렀다.

## 메타데이터 카탈로그

후보는 네 가지였다. DataHub, Amundsen, Apache Atlas, 그리고 상용 제품(Collibra/Alation).

상용은 먼저 빠졌다. 라이선스 비용도 문제지만, 이 프로젝트에서 필요한 건 카탈로그의 Glossary를 온톨로지 저장소처럼 쓰는 것이었다. 상용 제품의 Glossary는 충분히 강력하지만, 내부 데이터 모델에 접근해서 커스터마이징하는 데 한계가 있다.

Apache Atlas는 Hadoop 생태계에 묶여 있었다. HBase, Solr, Kafka를 전부 띄워야 한다. 2016년에 설계된 아키텍처가 그대로인데, 클라우드 네이티브 환경에서 운영하기에는 무겁다.

Amundsen은 깔끔한 도구다. 검색 중심의 카탈로그로는 괜찮은데, Glossary 기능이 약했다. 용어 간 관계를 정의하는 기능이 제한적이어서 온톨로지 저장소로 쓰기에는 부족했다.

DataHub를 선택한 결정적 이유는 세 가지다.

**Glossary 관계 4종.** IsA(상속), HasA(포함), Values(값 목록), RelatedTo(일반 연관). 이 네 가지 관계 유형이면 비즈니스 용어 간 계층구조를 표현할 수 있다. "순매출 IsA 매출", "매출 HasA 총매출, 반품, 에누리" 같은 식으로.

**GraphQL API.** 메타데이터를 프로그래밍 방식으로 읽고 쓸 수 있다. NL2SQL 엔진의 RAG Store에 온톨로지를 자동 동기화하려면 API가 유연해야 하는데, GraphQL이면 필요한 필드만 골라서 가져올 수 있다.

**Kafka MCL 이벤트.** Metadata Change Log라는 이벤트 스트림을 Kafka로 내보낸다. Glossary Term이 변경되면 이벤트가 발행되고, 이걸 구독해서 그래프 DB의 온톨로지를 실시간으로 동기화할 수 있다. 이전 프로젝트에서 메타데이터 변경을 수동으로 반영하다가 얼마나 고생했는지 기억나서, 이 부분은 양보할 수 없었다.

## NL2SQL 엔진

NL2SQL 엔진은 처음에 직접 만들까도 생각했다. 이미 별도로 대화형 BI 솔루션을 만든 경험이 있었다. NL2SQL에 GPT와 Gemini를 붙이고, 프롬프트 엔지니어링을 최적화하고, 멀티에이전트 아키텍처를 설계하는 데까지 갔었다.

그 경험에서 배운 건 두 가지다. DDL만으로는 LLM이 비즈니스 맥락을 이해할 수 없다는 것. 그리고 처음부터 만들면 사용자 인증, 쿼리 로깅, 데이터 필터링, 응답 스트리밍, 쿼리 학습까지 부수적인 기능이 한없이 불어난다는 것. 산정해 보니 1개월 이상이었다.

그때 Vanna가 2.0으로 업데이트 되었다.

1.x 버전은 단순했다. Python 클래스 하나를 상속받아서 `train()`, `ask()` 같은 메서드를 호출하는 구조. 프로토타이핑에는 좋은데 프로덕션에 넣기엔 부족했다. 사용자별 컨텍스트 분리가 안 되고, 보안 기능도 없었다.

2.0은 완전히 다른 물건이다.

| 변화 | 의미 |
|------|------|
| Agent 기반 아키텍처 | 독립적인 Agent 구성 요소를 조합하는 구조. 도구를 갈아 끼울 수 있다 |
| User-Aware | 모든 컴포넌트에 사용자 ID가 자동 전파된다. 테넌트별 쿼리 컨텍스트가 분리된다 |
| Row-level Security | 사용자별 데이터 필터링이 프레임워크 수준에서 지원된다 |
| Tool Memory | 성공한 쿼리를 자동으로 학습한다. 같은 패턴의 질문이 오면 이전 성공 사례를 참고한다 |
| Streaming | 테이블, 차트 같은 Rich UI Component를 실시간으로 전송한다 |

User-Aware와 Row-level Security가 결정적이었다. DataNexus는 그룹사별로 데이터를 격리해야 하는데, 이걸 NL2SQL 엔진 레벨에서 지원한다는 건 직접 구현해야 할 코드가 대폭 줄어든다는 뜻이다.

Tool Memory도 컸다. NL2SQL의 정확도를 올리는 가장 확실한 방법 중 하나가 성공한 쿼리를 축적해서 유사 질문에 재활용하는 건데, 이게 프레임워크에 내장되어 있다.

## 문서 지식엔진

벡터 검색만으로는 부족했다.

사업보고서나 내부 정책문서를 검색할 때, 벡터 유사도만으로 관련 청크를 가져오면 맥락이 끊긴다. "A사업부의 매출 인식 기준"을 찾고 싶은데, 벡터 검색은 "매출"이라는 단어가 포함된 청크를 유사도 순으로 나열할 뿐이다. A사업부와 매출 인식 기준 사이의 관계, 이 기준이 언제 바뀌었는지 같은 그래프 구조의 정보는 벡터에 담기지 않는다.

ApeRAG는 세 가지 검색을 결합한다.

- **Vector Search** — 임베딩 기반 의미 검색. 기본.
- **Full-text Search** — 키워드 기반 정확 매칭. 고유명사나 코드명처럼 의미보다 정확한 문자열이 중요할 때 쓴다.
- **GraphRAG** — 문서에서 추출한 엔티티 간 관계를 그래프로 구성하고, 그래프 탐색으로 관련 정보를 찾는다.

이 하이브리드 검색이 DataNexus와 맞는 이유가 있다. DataHub의 Glossary Term을 ApeRAG의 Entity Extraction에 Taxonomy로 주입하면, 문서에서 추출된 엔티티가 자동으로 비즈니스 용어와 연결된다. Exact Match → Synonym Match → Fuzzy Match(임계값 0.85) → Context Match 순으로 4단계 Entity Resolution을 거친다.

MinerU 통합도 중요했다. 엔터프라이즈 문서에는 복잡한 테이블, 수식, 다단 레이아웃이 흔하다. 일반적인 PDF 파서로는 테이블의 행/열 구조가 깨진다. MinerU는 이런 복잡한 문서 구조를 보존하면서 파싱한다.

## 그래프 DB

그래프 DB 선택에서 가장 큰 변수는 Neo4j의 라이선스 구조였다.

Neo4j는 Community Edition과 Enterprise Edition으로 나뉜다. 결정적 차이는 Multi-DB. Community는 단일 데이터베이스만 지원한다. 하나의 인스턴스에 하나의 그래프. Enterprise는 같은 인스턴스 안에서 여러 데이터베이스를 만들 수 있다.

DataNexus에서 Multi-DB는 필수다. 그룹사별로 온톨로지 그래프를 격리해야 한다. `groupA_ontology_db`, `groupB_ontology_db`처럼 테넌트별 데이터베이스를 분리하고, 사용자 권한에 따라 접근을 제어해야 한다. Community의 단일 DB에 모든 테넌트 데이터를 넣고 라벨로 구분하는 건 보안상 허용할 수 없었다.

그렇다고 Enterprise 라이선스를 사는 건 이 프로젝트의 원칙에 어긋난다.

DozerDB가 이 딜레마를 풀었다. Neo4j Community Edition 위에 Enterprise 기능을 얹는 오픈소스 플러그인이다. Multi-DB를 지원한다. `CREATE DATABASE`로 테넌트별 그래프를 만들 수 있다. Cypher 쿼리도 그대로 쓴다.

ArangoDB도 후보에 있었다. 멀티모델(문서 + 그래프 + 키밸류)을 지원하는 점은 매력적이었는데, Cypher를 쓸 수 없다는 게 문제였다. ArangoDB의 쿼리 언어인 AQL은 그래프 탐색에는 괜찮지만, Neo4j 생태계의 라이브러리나 도구를 활용할 수 없게 된다. 온톨로지를 Cypher로 질의하는 패턴이 이미 많이 나와 있어서 생태계 호환성을 우선했다.

DozerDB의 한계도 알고 있다. Fabric(크로스 DB 쿼리)은 아직 미지원이다. 서로 다른 데이터베이스 간에 한 번의 Cypher로 질의하는 건 불가능하다. 이건 Phase 3 이후로 미뤘다. 당장은 단일 테넌트 내 질의만으로 충분하다.

## 이 조합이 만드는 것

네 가지를 나란히 놓으면 그냥 도구 네 개다. 연결하면 파이프라인이 된다.

DataHub에서 Glossary Term이 변경되면 Kafka MCL 이벤트가 발행된다. 이 이벤트를 DozerDB의 온톨로지 그래프에 실시간 동기화한다. 동시에 Vanna의 RAG Store에도 반영되어, NL2SQL 프롬프트에 주입되는 맥락이 자동 갱신된다. ApeRAG의 Entity Extraction은 DataHub Glossary를 Taxonomy로 참조하므로 문서 검색 결과도 최신 용어 체계와 연결된다.

한 곳에서 용어를 고치면 네 군데가 동시에 바뀐다. 이전 프로젝트에서 메타데이터 변경을 Excel로 관리하다가 한 곳을 빼먹어서 반나절을 날린 적이 있는데, 그때의 교훈이 이 설계에 들어갔다.

## 다음 글

DataHub의 Business Glossary를 온톨로지로 쓸 때의 한계와 우회를 다룬다.

---

*DataNexus를 설계하고 구축하는 과정을 기록합니다. [GitHub](https://github.com/biz-agentic-ai) | [LinkedIn](https://www.linkedin.com/in/leejuno/)*
