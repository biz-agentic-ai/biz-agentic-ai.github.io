---
title: "4. SKOS 호환 레이어를 왜 넣었는가"
date: 2026-02-20
draft: false
summary: "DataNexus 온톨로지를 외부와 연결하기 위해 SKOS를 선택한 이유. LPG와 RDF, 두 그래프 모델을 잇는 호환 레이어 설계."
categories: ["ontology"]
tags: ["datanexus", "skos", "dozerdb", "rdf", "lpg"]
series: ["datanexus-building-log"]
series_order: 4
ShowToc: true
---

## 외부와 말이 안 통했다

[이전 글](/posts/datanexus/003-datahub-glossary-as-ontology/)에서 DataHub + DozerDB 이중 구조로 내부 온톨로지 문제를 풀었다. 내부 시스템에서만 쓰기에는 충분했다.

문제는 외부 시스템과의 연동이었다. 금융 도메인을 탐색하다가 FIBO(Financial Industry Business Ontology)를 발견했는데, 금융업계 표준 용어 체계로 "Financial Product", "Loan", "Interest Rate" 같은 개념이 계층으로 정리돼 있다. 유통 쪽도 마찬가지다. GS1의 GPC(Global Product Classification)에는 "의류 → 여성복 → 원피스"처럼 상품 분류 체계가 표준으로 잡혀 있다. 의료엔 SNOMED CT, 제조엔 ISA-95. 도메인마다 수천 개 용어가 이미 정리돼 있는데, 이걸 가져다 쓸 수 있으면 온톨로지를 밑바닥부터 만들 필요가 없다.

FIBO 파일을 열어봤다. OWL 포맷이었다. DozerDB 그래프에 넣으려니 구조 자체가 안 맞았다. 반대 방향도 마찬가지 — DataNexus 온톨로지를 고객사 기존 시스템(Collibra, TopBraid 같은)에 내보내고 싶어도 표준 포맷이 없으니 방법이 없었다. 내부에서는 잘 돌아가는데 밖으로 꺼내는 순간 무용지물이 되는 상황.

외부 호환이 안 되면 생기는 문제가 한두 개가 아니다. 대기업은 이미 Collibra나 Alation 같은 메타데이터 관리 툴을 쓰고 있는 경우가 많다. DataNexus를 도입한다고 기존 용어 체계를 버리진 않는다. 표준 포맷으로 내보낼 수 있으면 공존이 가능한데, 못하면 용어 수백 개를 수작업으로 옮겨야 한다. 그것만으로 몇 달이 날아간다.

유통 그룹처럼 백화점·마트·온라인몰이 각각 "매출"을 다르게 정의하는 경우, 그룹 차원에서 용어를 통합하거나 최소한 매핑하려면 공통 포맷이 있어야 한다. 없으면 관계사마다 따로 논다. 금융권은 감독 기관에 데이터 계보(lineage)나 용어 정의를 보고해야 하는 규제 요건도 있다. 거기에 벤더 종속(vendor lock-in) 문제까지. DataNexus를 쓰다가 다른 플랫폼으로 바꿔야 할 수도 있는데, 표준 포맷으로 Export가 되면 옮길 수 있지만 안 되면 갇힌다. 도입을 결정하는 자리에서 이게 꽤 크게 작용한다.

내부에서만 통하는 언어로는 외부와 대화할 수 없다.

## 같은 그래프인데 언어가 다르다

DozerDB는 **LPG(Labeled Property Graph)** 방식을 쓴다.

- 노드(동그라미)에 이름과 속성을 붙인다: `순매출 {definition: "총매출-반품-에누리"}`
- 노드 사이에 화살표를 긋고, 그 화살표에도 속성을 단다: `-[MANUFACTURES {since: "2024-01-01"}]->`

핵심은 화살표 자체에 "언제부터", "신뢰도 얼마" 같은 정보를 달 수 있다는 점이다. [이전 글](/posts/datanexus/003-datahub-glossary-as-ontology/)에서 `MANUFACTURES`, `STOCKS` 관계를 만들 때 이걸 활용했다.

SKOS를 포함한 웹 표준들은 완전히 다른 체계를 쓴다. **RDF(Resource Description Framework)** — 모든 정보를 세 단어짜리 문장으로 쪼갠다.

- `순매출` → `broader` → `매출` (순매출의 상위 개념은 매출이다)
- `순매출` → `prefLabel` → `"순매출"@ko` (한국어 이름은 "순매출"이다)

주술목(주어-서술어-목적어), 이 세 단어가 하나의 단위다. **트리플(triple)** 이라고 부른다.

여기서 갈린다. LPG는 관계에 속성을 자유롭게 붙일 수 있지만, RDF는 트리플이 원자 단위라서 관계 자체에 속성을 직접 달 수 없다. 대신 URI 기반이라 전 세계 어디서든 같은 개념을 같은 주소로 가리킬 수 있다. 시스템 간 데이터 교환에는 RDF가 압도적이다.

내부 표현력의 LPG, 외부 호환성의 RDF. DataNexus에는 둘 다 필요했다.

## OWL은 과하고, RDFS는 부족하고

RDF 세계에도 표준이 여러 개다.

**OWL(Web Ontology Language)** 은 가장 강력하다. 클래스 상속, 제약 조건, 자동 추론까지 지원한다. 법률 문서에 비유할 수 있다 — 모든 조항과 예외를 정밀하게 기술할 수 있는 대신 추론 엔진(Reasoner)을 별도로 띄워야 하고 학습 곡선이 가파르다. FIBO가 OWL인 이유도 금융 규제의 복잡성 때문이다.

DataNexus가 하려는 건 추론이 아니다. "객단가가 뭔지, 어떤 테이블의 어떤 컬럼에 있는지"를 NL2SQL 엔진에 알려주는 맥락 제공이다. OWL은 과했다.

**RDFS(RDF Schema)** 는 반대로 너무 가볍다. `subClassOf` 정도는 되는데 동의어나 용어 정의를 달 표준 속성이 없다.

**SKOS(Simple Knowledge Organization System)** 가 딱 맞았다. 이름부터 "단순한 지식 조직 체계"다. 도서관 분류 체계나 시소러스(Thesaurus: 동의어·유의어·상하위어를 매핑해둔 용어 관계 사전)를 표현하려고 만든 W3C 표준인데 — DataNexus가 하는 일이 정확히 비즈니스 용어 사전 관리다. 핏이 맞을 수밖에 없다.

SKOS 개념이 DataNexus 구조에 어떻게 대응되는지 정리하면:

| SKOS | DataNexus (DataHub + DozerDB) | 쉽게 말하면 |
|------|-------------------------------|-------------|
| skos:Concept | Glossary Term / Entity 노드 | 용어 하나 |
| skos:broader | IsA 관계 (상위 개념) | "객단가는 매출지표의 일종" |
| skos:narrower | IsA 역방향 (하위 개념) | "매출지표의 하위에 객단가" |
| skos:related | RelatedTo 계열 | "관련 있는 용어" * |
| skos:prefLabel | Term name (한국어 대표명) | 공식 이름 |
| skos:altLabel | 동의어 (영문, 약어) | "객단가" = "ATV", "Average Transaction Value" |
| skos:definition | Term definition | 용어 뜻풀이 |
| skos:ConceptScheme | 도메인별 용어 묶음 | "유통 용어집", "재무 용어집" |

\* 주의할 점이 있다. `skos:related`는 양방향이다. "A related B"이면 자동으로 "B related A"도 성립한다. DozerDB의 `SELLS`나 `SUPPLIED_BY` 같은 관계는 방향이 있다. A매장이 B상품을 판매한다고 B상품이 A매장을 판매하진 않는다. 이 방향 정보는 SKOS로 내보낼 때 손실된다. 뒤에서 다시 다룬다.

## DozerDB 위에 SKOS를 얹다

원칙은 간단했다. 기존 그래프를 건드리지 않는다.

DozerDB에 이미 들어간 `MANUFACTURES`, `STOCKS`, `CALCULATED_FROM` 같은 관계를 바꾸면 기존 쿼리가 전부 깨진다. 잘 돌아가는 구조를 표준 맞추겠다고 뒤집는 건 현장에서 가장 흔한 삽질이다.

기존 노드 위에 SKOS 메타데이터를 **오버레이** 했다. 투명 필름 한 장 덮는 느낌이다.

```cypher
// 기존 Entity 노드에 SKOSConcept 라벨과 SKOS 속성을 추가
MATCH (net:Entity {name: '순매출'})
SET net:SKOSConcept
SET net.skos_prefLabel = '순매출'
SET net.skos_altLabel = ['Net Sales', '순매출액']
SET net.skos_definition = '총매출에서 반품과 에누리를 차감한 금액'
SET net.skos_inScheme = 'finance-terms'
```

유통 도메인도 똑같다.

```cypher
// 유통 도메인 용어 예시
MATCH (atv:Entity {name: '객단가'})
SET atv:SKOSConcept
SET atv.skos_prefLabel = '객단가'
SET atv.skos_altLabel = ['ATV', 'Average Transaction Value', '객단']
SET atv.skos_definition = '총매출액을 구매 고객수로 나눈 값'
SET atv.skos_inScheme = 'retail-terms'
```

기존 `Entity` 노드는 그대로다. `SKOSConcept`이라는 라벨과 `skos_` 접두사 속성이 위에 붙을 뿐. 기존 Cypher 쿼리에는 영향이 없다.

`broader`/`narrower` 관계는 두 가지 방법이 있었다. `BROADER`, `NARROWER` 엣지를 `IsA`와 나란히 미리 만들어두거나, 기존 `IsA` 관계를 Export 시점에 `skos:broader`로 바꿔 출력하거나.

후자를 택했다. 엣지를 이중으로 만들면 `IsA`가 바뀔 때마다 `BROADER`도 동기화해야 한다. 동기화가 어긋나면 데이터가 꼬인다. 원천(Source of Truth)은 하나여야 한다. Export 시점에 한 번 변환하는 게 단순하고 안전하다.

## 가져오기와 내보내기

표준이 들어가면서 두 가지가 가능해졌다.

**가져오기** — FIBO에서 금융 용어를, GS1 GPC에서 상품 분류 체계를 DataNexus로 끌어오는 경우다. FIBO는 원래 OWL로 배포되지만 SKOS로 변환된 파생 버전도 있다. GPC도 마찬가지로 SKOS 매핑이 가능하다. "의류 → 여성복 → 원피스" 같은 상품 계층을 그대로 가져와서 유통 고객사 온톨로지의 뼈대로 쓸 수 있다. OWL의 복잡한 제약 조건은 빠지지만, DataNexus에 필요한 건 용어 이름·정의·상하위 관계뿐이다. SKOS 서브셋으로 충분하다.

**내보내기** — DataNexus 용어를 고객사 시스템으로 보내는 경우. DozerDB 그래프에서 특정 도메인(예: retail-terms)의 노드와 관계를 꺼내서 SKOS Turtle 포맷으로 변환한다.

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dnx:  <http://datanexus.ai/ontology/> .

dnx:atv a skos:Concept ;
  skos:prefLabel "객단가"@ko ;
  skos:altLabel  "ATV"@en, "Average Transaction Value"@en ;
  skos:definition "총매출액을 구매 고객수로 나눈 값"@ko ;
  skos:broader dnx:sales-metrics ;
  skos:inScheme dnx:retail-terms .

dnx:sales-metrics a skos:Concept ;
  skos:prefLabel "매출지표"@ko ;
  skos:narrower dnx:atv, dnx:net-sales, dnx:upt ;
  skos:inScheme dnx:retail-terms .
```

유통 현장에서 "객단가"라고 부르는 걸 어떤 시스템에서는 "ATV"로, 어떤 곳에서는 "평균구매단가"로 부른다. `altLabel`에 이 별칭들을 다 넣어두면 NL2SQL 엔진이 어떤 이름으로 질문이 들어와도 같은 테이블을 찾을 수 있다. 이 파일을 Collibra든 TopBraid이든 SKOS를 지원하는 어떤 시스템에든 넣을 수 있다.

가져오기/내보내기가 되면 앞서 얘기한 문제들이 풀린다. 유통 그룹에서 백화점은 "매출"을 점포별 POS 합산으로, 온라인몰은 결제 완료 기준으로, 마트는 반품 차감 후 기준으로 각각 정의하고 있다고 하자. 각 관계사가 DataNexus에 자기 용어를 SKOS로 내보내면, 그룹 본사에서 이걸 받아 매핑 테이블을 만들 수 있다. "백화점의 매출 = 온라인몰의 확정매출 = 마트의 순매출"이라는 관계가 표준 포맷으로 잡히는 거다. 금융 고객사라면 감독 기관에 용어 정의와 데이터 계보를 보고해야 할 때 SKOS Turtle 파일을 그대로 제출하거나, 기관이 요구하는 포맷으로 변환할 수 있다. 표준이 없으면 이런 건 전부 수작업이다.

Schema.org 같은 RDFS/OWL 기반 표준은 이 SKOS 레이어 범위 밖이다. 필요해지면 별도 변환기를 만들면 되지만 당장 우선순위는 아니다.

## 남은 한계

SKOS로 전부 해결되진 않는다.

SKOS에는 레이블 자체에 메타데이터를 붙이는 확장(SKOS-XL)이 있다. "순매출"이라는 이름이 언제 등록됐는지, 누가 승인했는지를 기록할 수 있다. 다국어 레이블 관리가 복잡해지면 꺼내 써야 할 수도 있는데, 아직은 안 넣었다.

OWL 수준의 추론도 SKOS 범위 밖이다. "A가 B의 하위이고, B가 C의 하위이면, A는 C의 하위다" 같은 자동 추론. 온톨로지 규모가 작을 땐 없어도 되는데, 수천 개 용어가 쌓이면 얘기가 달라질 수 있다.

가장 아쉬운 건 커스텀 관계 Export다. DozerDB의 `SELLS`, `STOCKS`, `SUPPLIED_BY` 같은 유통 도메인 특화 관계는 SKOS 표준에 대응하는 게 없다. "A매장이 B상품을 판매한다"는 방향이 있는 관계인데, `skos:related`로 뭉뚱그리면 방향과 의미가 사라진다. `dnx:sells` 같은 커스텀 네임스페이스로 확장하면 정보는 보존되는데, 받는 쪽이 이 커스텀 관계를 이해할 수 있어야 한다. 정보 손실 vs 호환성 — 트레이드오프다.

80%는 SKOS 표준으로 커버하고, 20%는 DozerDB 커스텀 관계로 보완한다. 표준이 못 담는 부분은 내부 확장으로 채우되, 무리해서 표준 안에 구겨넣지 않는다.

## 다음 글

온톨로지를 만들었는데, 이게 제대로 된 건지 어떻게 알까. [다음 글에서는 CQ(Competency Questions)로 온톨로지를 사전 검증하는 방법을 다룬다.](/posts/datanexus/005-competency-questions/)

---

*DataNexus를 설계하고 구축하는 과정을 기록합니다. [GitHub](https://github.com/biz-agentic-ai) | [LinkedIn](https://www.linkedin.com/in/leejuno/)*