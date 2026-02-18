---
title: "3. DataHub Glossary를 온톨로지로 쓸 수 있을까"
date: 2026-02-18
draft: false
summary: "DataHub의 Business Glossary를 온톨로지 저장소로 쓰려고 했다. 되는 것과 안 되는 것, 그리고 우회한 방법."
categories: ["ontology"]
tags: ["datanexus", "datahub", "dozerdb", "til"]
series: ["datanexus-building-log"]
series_order: 3
ShowToc: true
---

## Glossary에 용어를 넣기 시작했다

DataHub를 세팅하고 첫 번째로 한 작업이 Glossary Term 등록이었다.

"순매출 IsA 매출", "매출 HasA 총매출, 반품, 에누리". [이전 글](/posts/datanexus/002-architecture-decisions/)에서 DataHub의 Glossary 관계 4종(IsA, HasA, RelatedTo, Values)이면 비즈니스 용어 계층구조를 표현할 수 있다고 썼다. 틀린 말은 아니었다. 용어 간 상하위 관계를 잡는 데는 충분하다.

문제는 그 다음이었다.

## 관계 4종의 한계

"A 공장에서 생산된 B 제품"과 "A 공장에 재고가 있는 B 제품"을 구분해야 하는 상황이 왔다. 둘 다 공장과 제품의 관계다. 하나는 생산(Manufactures), 하나는 재고(Stocks).

DataHub Glossary에서는 둘 다 `RelatedTo`. 구분이 안 된다.

NL2SQL 엔진이 온톨로지를 참조해서 쿼리를 생성할 때, "A 공장에서 생산된 제품"이라는 질문에 생산 테이블을 찾아야 한다. RelatedTo 하나로는 생산인지 재고인지 판단할 근거가 없다. LLM이 잘못된 JOIN 경로를 탈 수 있다.

관계를 세분화하려면 DataHub의 메타데이터 모델을 확장해야 한다. PDL(Persona Data Language)로 새로운 Aspect를 정의하고, `@Relationship` 어노테이션을 붙이고, DataHub를 재배포한다. 관계 유형이 하나 늘 때마다 이 사이클을 돈다.

비용이 높다. 실시간 확장은 불가능하다.

## 파고 들어가니 더 나왔다

동의어 처리부터 걸렸다. "순매출"과 "실매출"을 동의어로 등록하면서, 둘 다 "Net Sales"라는 영문 동의어를 갖고 있었다. DataHub는 이 충돌을 잡아주지 않는다. 커스텀 검증 로직을 직접 짜야 하는데, 용어가 수백 개 넘어가면 수작업 검증은 현실적이지 않다.

시각화도 문제였다. DataHub UI는 데이터 계보(Lineage)를 트리 형태로 보여주는 데 맞춰져 있다. 온톨로지처럼 노드 수십 개가 그물망으로 엮인 구조를 탐색하는 화면은 애초에 없다.

결정적으로 걸린 건 관계에 속성을 못 단다는 거다. 신뢰도(confidence), 유효 기간, 카디널리티. 이전에 대기업 DW 프로젝트에서 "이 관계가 언제부터 유효한지"를 추적하지 못해서 데이터 정합성이 무너진 적이 있었다. 같은 실수를 반복하고 싶지 않았다.

| 되는 것 | 안 되는 것 |
|---------|-----------|
| 용어 정의 (name, definition) | 세분화된 관계 유형 |
| 동의어 등록 (커스텀 필드) | 동의어 중복 자동 감지 |
| 4종 관계 (IsA, HasA, RelatedTo, Values) | 관계에 속성 부여 |
| GraphQL API | 복잡한 그래프 탐색 UI |
| Kafka MCL 이벤트 스트림 | 실시간 관계 유형 확장 |

## 역할을 나눴다

Glossary를 버리는 건 답이 아니다. 용어 정의의 원천(Source of Truth)으로서 DataHub를 대체할 게 마땅히 없다. GraphQL API로 프로그래밍 방식의 접근이 되고, 변경이 생기면 Kafka MCL 이벤트가 알아서 나온다. 이 두 가지를 다른 도구에서 바닥부터 구현하는 건 비용 낭비다.

DataHub Glossary는 용어 정의와 기본 관계의 원천으로 유지하되, 세분화된 관계나 속성이 달린 엣지, 그래프 추론은 DozerDB에 넘겼다. 동기화는 이미 있는 파이프라인을 쓴다. DataHub에서 Glossary Term이 변경되면 Kafka MCL 이벤트가 발행되고, 이걸 구독해서 DozerDB의 온톨로지 그래프를 실시간으로 반영한다.

```
DataHub Glossary (원천)
  │
  ├─ 용어 정의 (name, definition, synonyms)
  ├─ 기본 관계 (IsA, HasA, RelatedTo)
  │
  │  ── Kafka MCL Event ──▶
  │
DozerDB (확장)
  │
  ├─ 세분화된 관계 (MANUFACTURES, STOCKS, CALCULATED_FROM ...)
  ├─ 관계 속성 (confidence, temporal, cardinality)
  └─ 그래프 추론 (Transitive Closure, Inverse Relations)
```

DozerDB에서는 Cypher로 바로 정의한다.

```cypher
CREATE (factory:Entity {name: 'A공장', type: 'Factory'})
CREATE (product:Entity {name: 'B제품', type: 'Product'})

// 생산 관계
CREATE (factory)-[:MANUFACTURES {
  since: '2024-01-01',
  confidence: 0.95
}]->(product)

// 재고 관계는 별도 엣지
CREATE (factory)-[:STOCKS {
  quantity: 500,
  last_updated: '2026-02-01'
}]->(product)
```

이전 프로젝트에서 파생 지표 정의를 Excel로 관리하다가 한 곳을 안 고쳐서 반나절을 날린 적이 있다. 그래서 이번에는 `CALCULATED_FROM` 관계로 순매출의 계산식을 그래프에 넣었다. 계산식이 바뀌면 관계를 수정하고, 변경 이력은 그래프 DB가 추적한다. Excel 시트 어딘가에 묻혀 있는 것보다 낫다.

## 남은 문제

DataHub의 Glossary 모델은 DataHub 고유의 구조다. FIBO(금융)나 Schema.org(범용) 같은 산업 표준 온톨로지를 가져오거나, DataNexus의 온톨로지를 다른 시스템에 내보내려면 표준 포맷이 필요하다. 지금 구조로는 DataNexus 안에서만 통하는 용어 체계가 된다.

다음 글에서 SKOS 호환 레이어를 왜 넣었는지 다룬다.

---

*DataNexus를 설계하고 구축하는 과정을 기록합니다. [GitHub](https://github.com/biz-agentic-ai) | [LinkedIn](https://www.linkedin.com/in/leejuno/)*