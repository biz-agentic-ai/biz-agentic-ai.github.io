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

## 왜 Glossary를 온톨로지로 쓰려 했나

DataNexus의 핵심 아이디어는 단순하다. 비즈니스 용어 사이의 관계를 그래프로 정의해두면, NL2SQL 엔진이 그 그래프를 참조해서 자연어를 SQL로 바꿀 수 있다. 이 그래프가 온톨로지다.

온톨로지라고 하면 학술 논문에나 나올 것 같은데, 실체는 별거 없다. "순매출은 매출의 한 종류다(IsA)", "매출은 총매출, 반품, 에누리를 포함한다(HasA)". 사람 머릿속에 있는 업무 지식을 기계가 읽게 옮긴 것이다.

문제는 이걸 어디에 저장하느냐였다. 온톨로지 전용 시스템을 하나 더 띄우면 관리 포인트가 늘어난다. 이미 DataHub를 메타데이터 플랫폼으로 쓰고 있었고, 거기에 **Business Glossary**가 있었다. 용어 등록, 관계 설정 다 된다. [이전 글](/posts/datanexus/002-architecture-decisions/)에서 Glossary의 관계 4종(IsA, HasA, RelatedTo, Values)이면 비즈니스 용어 계층구조를 표현할 수 있다고 판단했었다.

Glossary를 온톨로지 저장소로 겸용하면 시스템 하나를 줄인다. GraphQL API로 프로그래밍 접근이 되고, 용어가 변경되면 Kafka MCL(Metadata Change Log) 이벤트가 자동 발행된다. 나쁘지 않은 출발점이었다.

## Glossary에 용어를 넣기 시작했다

DataHub 세팅하고 제일 먼저 한 게 Glossary Term 등록이었다. "순매출 IsA 매출", "매출 HasA 총매출, 반품, 에누리". 이런 식으로 용어를 넣고 관계를 걸었다.

기본적인 계층구조는 잘 들어갔다. 매출 → 총매출, 순매출 → 실매출. 깔끔했다.

문제는 그 다음이었다.

## 관계 4종의 한계: "공장과 제품"

실제 업무 데이터를 모델링하면서 벽에 부딪혔다.

"A 공장에서 **생산된** B 제품"과 "A 공장에 **재고가 있는** B 제품". 둘 다 공장과 제품 사이의 관계다. 하나는 생산(Manufactures), 하나는 재고(Stocks). 의미가 완전히 다르다.

DataHub Glossary에서 이 두 관계를 표현하면? 둘 다 `RelatedTo`. "공장 RelatedTo 제품"이 두 개 생기는데, 어느 게 생산이고 어느 게 재고인지 구분이 안 된다.

이게 왜 치명적이냐면, DataNexus의 NL2SQL 엔진이 온톨로지를 보고 SQL을 만들기 때문이다. "A 공장에서 생산된 제품 목록 보여줘"라는 질문이 들어오면, 엔진은 공장-제품 관계를 찾고 거기에 해당하는 테이블과 JOIN 경로를 결정한다.

```
사용자 질문: "A 공장에서 생산된 제품은?"

온톨로지 조회: 공장 → RelatedTo → 제품  (생산? 재고? 알 수 없음)

→ LLM이 production 테이블 대신 inventory 테이블을 JOIN할 수 있음
→ 잘못된 결과 반환
```

관계 유형이 `RelatedTo` 하나뿐이니, 엔진한테는 판단 근거가 없다. 잘못된 JOIN 경로를 타면 사용자에게 엉뚱한 데이터가 나간다.

### 확장하려면 재배포가 필요하다

그러면 DataHub에서 관계를 세분화하면 되지 않느냐. 이게 쉽지 않다.

1. PDL(Persona Data Language)로 새 Aspect를 정의하고
2. `@Relationship` 어노테이션으로 관계 유형을 선언하고
3. DataHub를 빌드해서 재배포해야 한다

관계 유형 하나 추가할 때마다 이 사이클을 돌아야 한다. 비즈니스 현장에서 모델링하다 보면 관계는 계속 늘어난다. "공급(Supplies)", "검수(Inspects)", "반품(Returns)"... 업무 맥락에 따라 수십 가지가 필요해지는데, 하나마다 코드 수정하고 재배포하는 건 말이 안 된다.

## 파고 들어가니 더 나왔다

관계 유형만 문제가 아니었다.

### 동의어 충돌

"순매출"과 "실매출"을 동의어로 등록했다. 같은 개념의 다른 이름이다. 그런데 두 용어 모두 "Net Sales"라는 영문 동의어를 갖고 있었다. 하나의 영문명에 한글 용어 두 개가 매핑된 상황인데, DataHub는 이걸 그냥 넘긴다. 경고도 없다.

NL2SQL에서 동의어 매핑이 꼬이면 엔진이 엉뚱한 용어를 참조한다. 용어가 수백 개를 넘어가면 이런 충돌을 눈으로 잡는 건 불가능하다. 결국 커스텀 검증 로직을 따로 짜야 한다는 뜻이다.

### 시각화

DataHub UI는 데이터 계보(Lineage) 보는 데 맞춰져 있다. 테이블 A → 테이블 B로 데이터가 흐르는 방향성 있는 트리.

온톨로지는 구조 자체가 다르다. 노드 수십~수백 개가 다대다로 엮인 그물망이다. "제품"이 "공장", "창고", "거래처", "카테고리"와 전부 다른 관계로 연결되어 있고, 그 노드들이 또 서로 물려 있다. DataHub에는 이런 그래프를 탐색하는 화면 자체가 없다. 온톨로지를 만들어 놓고 전체 그림을 못 보면 관리할 수가 없다.

### 관계에 속성을 붙일 수 없다

이게 제일 컸다.

DataHub Glossary에서 "A RelatedTo B"를 설정하면, 그 관계에 아무것도 더 붙일 수 없다. 실무에서는 관계 자체에 정보가 필요한 경우가 많다.

**신뢰도(confidence)**가 대표적이다. 자동 추출된 관계는 0.7, 전문가가 직접 정의한 관계는 0.95. 이 차이를 NL2SQL 엔진이 알아야 한다. **유효 기간(temporal)**도 빠질 수 없다. 조직 개편으로 부서-제품 매핑이 바뀌면, "이 관계가 언제부터 언제까지 유효한지"를 추적해야 한다. **카디널리티(cardinality)**는 JOIN 전략에 직접 영향을 준다.

L사 차세대 정보계 프로젝트(54억, 13개월짜리) 할 때 비슷한 문제를 겪었다. 조직 개편이 프로젝트 중간에 터졌는데, 과거 시점의 조직 구조로 현재 데이터를 조회하는 바람에 리포트 수치가 안 맞았다. 관계의 시간축을 관리하지 않으면 생기는 전형적인 사고다. 같은 걸 반복하고 싶지 않았다.

### 정리: 되는 것과 안 되는 것

| 되는 것 | 안 되는 것 |
|---------|-----------|
| 용어 정의 (name, definition) | 세분화된 관계 유형 (MANUFACTURES, STOCKS 등) |
| 동의어 등록 (커스텀 필드) | 동의어 중복/충돌 자동 감지 |
| 4종 관계 (IsA, HasA, RelatedTo, Values) | 관계에 속성 부여 (신뢰도, 유효 기간) |
| GraphQL API로 프로그래밍 접근 | 복잡한 그래프 탐색 UI |
| Kafka MCL 이벤트 스트림 | 재배포 없는 실시간 관계 유형 확장 |

DataHub Glossary는 용어 사전으로서는 훌륭하지만, 온톨로지 저장소로는 표현력이 모자랐다.

## 역할을 나눴다: DataHub + DozerDB

Glossary를 완전히 버리는 건 답이 아니었다. 용어 정의의 원천(Source of Truth)으로 DataHub를 대체할 게 없다. GraphQL API, Kafka MCL 이벤트—이 인프라를 다른 도구에서 바닥부터 만드는 건 시간 낭비다.

그래서 각자 잘하는 걸 맡겼다.

- **DataHub Glossary** → 용어 정의와 기본 관계의 원천 (Source of Truth)
- **DozerDB** → 세분화된 관계, 속성 달린 엣지, 그래프 추론 담당

DozerDB를 고른 이유는 Cypher 쿼리를 쓸 수 있는 그래프 DB이기 때문이다. 관계(엣지)에 속성을 자유롭게 붙이고, 관계 유형을 추가할 때 스키마 변경도 재배포도 필요 없다.

![DataHub + DozerDB 역할 분리](/images/datanexus/datahub-dozerdb-sync.png)

동기화 흐름은 간단하다. DataHub에서 Glossary Term이 바뀌면 Kafka MCL 이벤트가 나간다. 이벤트를 구독하는 Consumer가 DozerDB 온톨로지 그래프에 반영한다. 이름, 정의 같은 기본 정보는 DataHub가 쥐고 있고, DozerDB는 그 위에 세분화된 관계와 속성을 얹는 구조다.

### DozerDB에서의 관계 정의

아까 문제됐던 "공장-제품" 관계. DozerDB에서는 이렇게 풀린다.

```cypher
// 엔티티 생성 (DataHub에서 동기화된 용어)
CREATE (factory:Entity {name: 'A공장', type: 'Factory'})
CREATE (product:Entity {name: 'B제품', type: 'Product'})

// 생산 관계 — 시작 시점과 신뢰도를 속성으로 기록
CREATE (factory)-[:MANUFACTURES {
  since: '2024-01-01',
  confidence: 0.95
}]->(product)

// 재고 관계 — 별도 엣지, 수량과 갱신 시점
CREATE (factory)-[:STOCKS {
  quantity: 500,
  last_updated: '2026-02-01'
}]->(product)
```

`MANUFACTURES`와 `STOCKS`가 별개의 관계 유형이다. "A 공장에서 생산된 제품"이라는 질문이 오면, 엔진이 `MANUFACTURES`를 찾아서 production 테이블로 정확히 JOIN한다. `RelatedTo` 하나로 퉁치던 것과는 근본적으로 다르다.

### 파생 지표도 그래프에 넣었다

이전 회사에서, 파생 지표 정의를 Excel로 관리하다가 반나절을 날린 적이 있다. "순매출 = 총매출 - 반품 - 에누리"가 시트 어딘가에 적혀 있었는데, 총매출 정의가 바뀌면서 순매출 시트는 업데이트가 안 됐다. 리포트 수치가 안 맞아서 고객사 미팅에서 곤란했다.

이번에는 `CALCULATED_FROM` 관계로 계산식 자체를 그래프에 넣었다.

```cypher
// 순매출의 계산 구조를 관계로 표현
MATCH (net:Entity {name: '순매출'})
MATCH (gross:Entity {name: '총매출'})
MATCH (returns:Entity {name: '반품'})
MATCH (discounts:Entity {name: '에누리'})

CREATE (net)-[:CALCULATED_FROM {operator: 'subtract'}]->(gross)
CREATE (net)-[:CALCULATED_FROM {operator: 'subtract'}]->(returns)
CREATE (net)-[:CALCULATED_FROM {operator: 'subtract'}]->(discounts)
```

계산식이 바뀌면 관계를 수정한다. 변경 이력은 그래프 DB가 알아서 추적한다. Excel 시트 어딘가에 묻혀서 누가 언제 고쳤는지도 모르는 것보다 낫다.

## 남은 문제: 표준 호환

DataHub Glossary 모델은 DataHub만의 구조다. 업계에는 FIBO(금융), Schema.org(범용) 같은 표준 온톨로지가 있다. 산업 표준을 가져오거나 DataNexus 온톨로지를 밖으로 내보내려면 표준 포맷 지원이 필요한데, 지금 구조로는 DataNexus 안에서만 통하는 독자 체계가 된다.

외부 상호운용성이 없는 온톨로지는 가치가 제한된다.

다음 글에서 SKOS 호환 레이어를 왜 넣었는지 다룬다.

---

*DataNexus를 설계하고 구축하는 과정을 기록합니다. [GitHub](https://github.com/biz-agentic-ai) | [LinkedIn](https://www.linkedin.com/in/leejuno/)*