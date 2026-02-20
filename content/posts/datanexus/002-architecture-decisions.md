---
title: "2. 4개의 오픈소스를 이 조합으로 결정하기까지"
date: 2026-02-17
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

메타데이터 카탈로그만 해도 DataHub, Amundsen, Apache Atlas, OpenMetadata. 상용까지 포함하면 Collibra, Alation도 있다. NL2SQL 엔진, 문서 지식엔진, 그래프 DB까지 네 축을 채워야 하는데 조합이 기하급수적으로 불어났다.

엑셀 시트에 비교표를 만들었다. 행이 후보 도구, 열이 평가 기준. 3주쯤 지나니까 탭이 7개로 늘어나 있었다. 선택지가 많으면 안 고르는 게 문제다. 하나를 고르면 나머지와의 조합이 바뀌고, 다시 처음부터 비교해야 한다.

## 네 가지 컴포넌트, 각각의 요건

[이전 글](/posts/datanexus/001-why-datanexus/)에서 DataNexus의 네 가지 컴포넌트를 정의했다. 메타데이터 카탈로그, NL2SQL 엔진, 문서 지식엔진, 그래프 DB.

양보할 수 없는 공통 기준이 세 가지 있었다. 오픈소스일 것. 멀티테넌시를 지원하거나 구현 가능할 것 — 그룹사별 데이터 격리는 필수다. 프로덕션 레디일 것 — 커뮤니티 활성도, 릴리즈 주기, 문서화 수준까지 봤다.

컴포넌트마다 추가 요건도 달랐다. 메타데이터 카탈로그는 Business Glossary에서 용어 간 관계를 정의할 수 있어야 하고, 변경 이벤트를 실시간으로 내보낼 수 있어야 했다. NL2SQL 엔진 쪽은 사용자별 컨텍스트 분리와 Row-level Security. 문서 지식엔진은 벡터 검색만으로 안 되고 그래프 검색까지 하이브리드로 돌려야 했다. 그래프 DB는 Multi-DB와 Cypher 쿼리 지원이 전제였다.

이 기준을 들고 후보를 걸렀다.

## 메타데이터 카탈로그

DataHub, OpenMetadata, Amundsen, Apache Atlas, 상용(Collibra/Alation). 다섯을 놓고 봤다.

상용은 먼저 빠졌다. 라이선스 비용도 문제지만 이 프로젝트에서 필요한 건 카탈로그의 Glossary를 온톨로지 저장소처럼 쓰는 거다. 상용 Glossary가 강력하긴 한데 내부 데이터 모델에 접근해서 커스터마이징하는 데 한계가 있다.

Apache Atlas는 Hadoop 생태계에 묶여 있다. HBase, Solr, Kafka를 전부 띄워야 한다. 2016년 설계 그대로인데 클라우드 네이티브 환경에서 돌리기엔 무겁다. Amundsen은 검색 중심 카탈로그로는 괜찮은데 Glossary에서 용어 간 관계를 정의하는 기능이 빈약하다. 온톨로지 저장소로 쓸 수 없었다.

끝까지 고민한 건 OpenMetadata다. 아키텍처가 깔끔하고 데이터 품질 측정이 내장돼 있어서 단독 카탈로그로는 훌륭했다. 문제는 Glossary 관계가 Parent-Child와 RelatedTerms 위주라는 점. 상속(IsA)과 포함(HasA)을 명확히 구분해야 하는 온톨로지 표현에는 모자랐다. 실시간 이벤트 동기화도 웹훅 방식이라 대규모 스트리밍에서 Kafka 네이티브 대비 신뢰성이 떨어졌다.

DataHub를 고른 이유는 명확하다.

Glossary 관계가 4종이다. IsA(상속), HasA(포함), Values(값 목록), RelatedTo(일반 연관). 이 네 가지면 비즈니스 용어 간 계층을 표현할 수 있다. "순매출 IsA 매출", "매출 HasA 총매출, 반품, 에누리" 같은 식이다.

GraphQL API도 한몫했다. 메타데이터를 프로그래밍 방식으로 읽고 쓸 수 있어야 NL2SQL 엔진의 RAG Store에 온톨로지를 자동 동기화하는데, GraphQL이면 필요한 필드만 골라서 가져온다.

결정적이었던 건 Kafka MCL 이벤트다. Metadata Change Log를 Kafka로 내보내는 구조인데, Glossary Term이 바뀌면 이벤트가 발행된다. 이걸 구독해서 그래프 DB 온톨로지를 실시간 동기화할 수 있다. 메타데이터 변경을 수동으로 반영하는 건 규모가 커질수록 반드시 누락이 생긴다. 양보할 수 없는 요건이었다.

## NL2SQL 엔진

처음에는 직접 만들까 생각했다. 대화형 BI 솔루션을 구축하면서 NL2SQL에 GPT와 Gemini를 붙이고, 프롬프트 엔지니어링을 최적화하고, 멀티에이전트 아키텍처까지 설계하는 데까지 갔었다.

거기서 배운 게 두 가지다. DDL만으로는 LLM이 비즈니스 맥락을 이해할 수 없다는 것. 그리고 처음부터 만들면 사용자 인증, 쿼리 로깅, 데이터 필터링, 응답 스트리밍, 쿼리 학습까지 부수 기능이 한없이 불어난다는 것. 견적을 내보니 1개월 넘게 잡아먹힐 판이었다.

그때 Vanna가 2.0으로 올라왔다.

1.x는 단순했다. Python 클래스 하나 상속받아서 `train()`, `ask()` 호출하는 구조. 프로토타이핑엔 괜찮은데 프로덕션에 넣기엔 부족했다. 사용자별 컨텍스트 분리도 안 되고 보안 기능도 없었다.

2.0은 다른 물건이다. Agent 기반 아키텍처로 바뀌면서 독립적인 구성 요소를 조합하는 방식이 됐고, 모든 컴포넌트에 사용자 ID가 자동 전파되는 User-Aware 구조가 들어갔다. Row-level Security가 프레임워크 수준에서 지원된다. 성공한 쿼리를 자동 학습하는 Tool Memory도 내장. 테이블이나 차트 같은 Rich UI Component를 실시간 전송하는 Streaming까지 갖췄다.

User-Aware와 Row-level Security가 결정적이었다. DataNexus는 그룹사별로 데이터를 격리해야 하는데 NL2SQL 엔진 레벨에서 이걸 지원한다는 건 직접 구현할 코드가 대폭 줄어든다는 뜻이다.

Tool Memory도 컸다. NL2SQL 정확도를 올리는 가장 확실한 방법 중 하나가 성공 쿼리를 축적해서 유사 질문에 재활용하는 건데 이게 프레임워크에 내장돼 있다. 직접 구현하면 쿼리 저장, 유사도 매칭, 버전 관리까지 만져야 하는데 그 공수가 통째로 빠진다.

## 문서 지식엔진

벡터 검색만으로는 부족하다.

사업보고서나 내부 정책문서를 검색할 때 벡터 유사도만으로 청크를 가져오면 맥락이 끊긴다. "A사업부의 매출 인식 기준"을 찾고 싶은데 벡터 검색은 "매출"이 포함된 청크를 유사도 순으로 나열할 뿐이다. A사업부와 매출 인식 기준의 관계라든가, 기준이 언제 바뀌었는지 같은 그래프 구조 정보는 벡터에 안 담긴다.

ApeRAG는 세 가지 검색을 조합해서 이 문제를 푼다. 임베딩 기반 의미 검색인 Vector Search, 고유명사나 코드명처럼 문자열 자체가 중요한 Full-text Search, 문서에서 추출한 엔티티 간 관계를 그래프로 탐색하는 GraphRAG. 이 셋을 동시에 돌린다.

이 하이브리드가 DataNexus와 특히 잘 맞는 이유가 있다. DataHub의 Glossary Term을 ApeRAG Entity Extraction의 Taxonomy로 주입하면 문서에서 추출된 엔티티가 자동으로 비즈니스 용어와 연결된다. Exact Match → Synonym Match → Fuzzy Match(임계값 0.85) → Context Match, 4단계 Entity Resolution을 거치는 구조다.

MinerU 통합도 빠뜨릴 수 없다. 엔터프라이즈 문서에는 복잡한 테이블, 수식, 다단 레이아웃이 흔한데 일반 PDF 파서로는 테이블 행/열이 깨진다. 특히 사업보고서처럼 테이블 안에 병합 셀이 난무하는 문서는 파싱 결과가 처참하다. MinerU는 문서 구조를 보존하면서 파싱하기 때문에 이 문제를 정면으로 해결한다.

## 그래프 DB

가장 큰 변수는 Neo4j 라이선스였다.

Community Edition과 Enterprise Edition의 결정적 차이는 Multi-DB다. Community는 인스턴스 하나에 그래프 하나. Enterprise는 같은 인스턴스 안에서 여러 데이터베이스를 만들 수 있다.

DataNexus에서 Multi-DB는 필수다. 그룹사별로 온톨로지 그래프를 격리해야 한다. `groupA_ontology_db`, `groupB_ontology_db`처럼 테넌트별 데이터베이스를 분리하고 사용자 권한으로 접근을 제어하는 구조. Community 단일 DB에 전부 넣고 라벨로 구분하는 건 보안상 말이 안 된다.

그렇다고 Neo4j Enterprise 라이선스를 살 수는 없다. 오픈소스 프로젝트의 원칙에 어긋난다.

DozerDB가 이 딜레마를 풀었다. Neo4j Community Edition 위에 Enterprise 기능을 얹는 오픈소스 플러그인인데 Multi-DB를 지원한다. `CREATE DATABASE`로 테넌트별 그래프를 만들 수 있고, Cypher 쿼리도 그대로 쓴다.

ArangoDB도 봤다. 멀티모델(문서 + 그래프 + 키밸류)이 매력적인데 Cypher를 쓸 수 없다. 자체 쿼리 언어 AQL이 그래프 탐색에는 괜찮지만 Neo4j 생태계의 라이브러리나 도구를 못 쓰게 된다. 온톨로지를 Cypher로 질의하는 패턴과 레퍼런스가 압도적으로 많기 때문에 생태계 호환성을 택했다.

DozerDB의 한계도 안다. Fabric — 크로스 DB 쿼리 — 은 아직 미지원이라 서로 다른 데이터베이스를 한 번의 Cypher로 질의하는 건 불가능하다. Phase 3 이후로 미뤘다. 당장은 단일 테넌트 내 질의만으로 충분하다.

## 네 개를 연결하면

네 가지를 나란히 놓으면 도구 네 개다. 연결해야 파이프라인이 된다.

![메타데이터 동기화 아키텍처](/images/datanexus/metadata-sync.png)

DataHub에서 Glossary Term이 바뀌면 Kafka MCL 이벤트가 발행된다. 이 이벤트가 DozerDB 온톨로지 그래프에 실시간 반영되고, 동시에 Vanna의 RAG Store에도 들어간다. NL2SQL 프롬프트에 주입되는 맥락이 자동 갱신되는 셈이다. ApeRAG의 Entity Extraction은 DataHub Glossary를 Taxonomy로 참조하니까 문서 검색 결과도 최신 용어 체계에 연결된다.

한 곳에서 용어를 고치면 네 군데가 동시에 바뀐다. 메타데이터 변경을 수동으로 전파하는 구조는 규모가 커질수록 반드시 어딘가 누락된다. 이 파이프라인이 그 문제를 막는다.

## 다음 글

[DataHub의 Business Glossary를 온톨로지로 쓸 때의 한계와 우회를 다룬다.](/posts/datanexus/003-datahub-glossary-as-ontology/)

---

*DataNexus를 설계하고 구축하는 과정을 기록합니다. [GitHub](https://github.com/biz-agentic-ai) | [LinkedIn](https://www.linkedin.com/in/leejuno/)*