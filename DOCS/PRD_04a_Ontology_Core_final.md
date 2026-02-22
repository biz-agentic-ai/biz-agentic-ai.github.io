# DataNexus PRD – §4.4~4.5, §4.6~4.8 온톨로지 엔지니어링 (Core)


> **📋 오버엔지니어링 주의사항 (리뷰 보고서 §3 반영)**
> 
> 본 섹션에는 리뷰에서 지적된 오버엔지니어링 항목이 포함되어 있습니다:
> - §4.4.1 Predicate 20+ 세분화 → **MVP는 5~7개 핵심 관계만 적용, 나머지는 Phase 2로 이관**
> - §4.4.2 3단계 스키마 강제성 → **MVP는 Stage 1(Pre-Extraction) + Stage 3(Resolution)만, Stage 2는 Phase 2**
> - §4.3.10 Graphiti 시간 인식 KG → **Phase 3 R&D로 전면 이관**
> 
> 각 섹션 내에서 `[MVP 범위]` / `[Phase 2+]` 태그로 구분합니다.

> **구현 코드 포함 안내 (리뷰 보고서 P3):** 본 파일에는 SchemaEnforcer, CQValidator, ImpactAnalyzer, OntologyVersionManager, HybridReasoningPipeline 등 ~500행의 Python 클래스 구현 코드가 포함되어 있습니다. PRD 수준의 인터페이스 정의를 넘어서는 구현 코드는 향후 리팩토링 시 Implementation Guide로 분리를 권장합니다.

## 4.4 온톨로지 엔지니어링 방어 로직

### 4.4.1 관계(Relationship) 표현력 세분화

#### 4.4.1.1 문제 정의
기존 PRD까지는 DataHub의 기본 관계(`IsA`, `HasA`, `RelatedTo`)만 활용하고 있어, 복잡한 Multi-hop 추론 시 의미론적 모호성이 발생할 수 있습니다.

**예시 문제:**
- "A 공장에서 **생산된** B 제품" vs "A 공장에 **재고가 있는** B 제품"
- 단순 `RelatedTo`로는 '생산(Manufactures)'과 '재고(Stocks)'를 구분할 수 없음
- 이로 인해 LLM이 잘못된 추론 경로를 선택하여 환각(Hallucination) 발생 가능

#### 4.4.1.2 세분화된 서술어(Predicate) 체계

**비즈니스 도메인별 관계 유형 확장:**

| 관계 카테고리 | 서술어(Predicate) | 설명 | 예시 |
| :--- | :--- | :--- | :--- |
| **생산/제조** | `Manufactures` | 생산 관계 | Factory → Manufactures → Product |
| | `ProducedBy` | 역방향 생산 관계 | Product → ProducedBy → Factory |
| | `AssembledFrom` | 조립 구성 관계 | Product → AssembledFrom → Component |
| **공급망** | `SuppliesTo` | 공급 관계 | Supplier → SuppliesTo → Factory |
| | `StoredAt` | 재고 위치 관계 | Product → StoredAt → Warehouse |
| | `DistributedBy` | 유통 관계 | Product → DistributedBy → Distributor |
| **재무/거래** | `SoldBy` | 판매 관계 | Product → SoldBy → Store |
| | `PurchasedBy` | 구매 관계 | Product → PurchasedBy → Customer |
| | `CalculatedFrom` | 계산 파생 관계 | NetSales → CalculatedFrom → GrossSales |
| **인과관계** | `Causes` | 원인 관계 | Event → Causes → Impact |
| | `CausedBy` | 결과 관계 | Impact → CausedBy → Event |
| | `Impacts` | 영향 관계 | Factor → Impacts → Metric |
| **시간적** | `PrecedesTo` | 선행 관계 | Phase1 → PrecedesTo → Phase2 |
| | `OccursDuring` | 기간 내 발생 | Event → OccursDuring → Period |

**DozerDB 구현 방안:**

```cypher
// 세분화된 관계 유형을 엣지 라벨로 구현
CREATE (factory:Entity {name: 'A공장', type: 'Factory'})
CREATE (product:Entity {name: 'B제품', type: 'Product'})
CREATE (factory)-[:MANUFACTURES {
 since: '2024-01-01',
 volume: 10000,
 confidence: 0.95
}]->(product)

// 재고 관계는 별도 엣지로 구분
CREATE (factory)-[:STOCKS {
 quantity: 500,
 last_updated: '2026-02-01'
}]->(product)
```

**DataHub 메타데이터 확장:**

```json
{
 "relatedTerms": [
    {
      "urn": "urn:li:glossaryTerm:B제품",
      "relationship_type": "RelatedTo",
      "predicate": "Manufactures",
      "predicate_metadata": {
        "direction": "outgoing",
        "cardinality": "one-to-many",
        "temporal": true,
        "confidence_required": true
      }
    }
 ]
}
```

#### 4.4.1.3 관계 표현력 검증 지표

| 지표명 | 정의 | 목표 기준 |
| :--- | :--- | :--- |
| **Predicate Specificity Score** | (세분화된 관계 수 / 전체 관계 수) × 100 | 80% 이상 |
| **Ambiguity Detection Rate** | Multi-hop 쿼리에서 모호한 경로 탐지 비율 | 5% 미만 |
| **Reasoning Accuracy** | 관계 기반 추론의 정확도 | 85% 이상 (Phase 2: 90% 이상; 정식 기준은 §4.8 SSOT 참조) |

#### 4.4.1.4 현재 설계의 한계 및 실무적 보완 전략

**현재 PRD 설계의 한계:**

DataNexus PRD에서는 DataHub를 메타데이터 저장소로 활용하고 있지만, DataHub UI와 메타데이터 모델의 제약으로 관계 표현에 한계가 있습니다. DataHub의 메타데이터 모델은 기본적으로 외래키와 내장 관계(소유자, 계보, 글로서리 링크 등) 중심이며, 임의의 관계 타입을 추가하려면 PDL(Persona Data Language)로 새로운 Aspect와 @Relationship 어노테이션을 정의하고 DataHub를 재배포해야 합니다. 이는 개발 비용이 높고 실시간 확장이 어렵습니다.

그 결과, 온톨로지 상의 다양한 관계(예: "유사한 제품", "업무 도메인 관련성", "파생 지표 계산식" 등)를 DataHub 내에서 직접 표현하지 못하고, 텍스트 설명이나 별도 문서로 우회하고 있을 수 있습니다. 시각화 측면에서도 DataHub 기본 UI는 라인리지(데이터 계보)나 간단한 엔티티 연결만 트리 형태로 보여주며, 복잡한 그래프 탐색 화면을 제공하지 않습니다.

**실무적 보완 전략:**

1. **메타데이터 모델 확장**
   - DataHub의 커스텀 메타데이터 모델 확장 기능을 활용하여 필요한 관계를 **First-class entity**로 등록합니다.
   - PDL을 통해 `@Relationship` 어노테이션을 부여하면 ingestion 시 해당 관계가 그래프에 추가됩니다.
   - 자주 쓰이는 관계 유형(예: "참조한다(References)", "구성요소이다(ConsistsOf)" 등)을 몇 가지 선정하여 모델에 추가합니다.
   - Glossary 용어 기능을 적극 활용하여, 엔티티-용어 매핑 이상의 의미론적 연결(예: 용어 계층 구조)을 표현합니다.

2. **Neo4j 연계 및 그래프 뷰어 활용**
   - DataHub 메타데이터를 **Neo4j와 동기화**하여 보다 풍부한 관계를 별도 그래프DB에서 관리하고 시각화합니다.
   - DataHub의 GraphQL API나 Metadata Change Event 스트림을 이용해 Neo4j로 온톨로지 그래프 복제본을 유지합니다.
   - **Neo4j Bloom** 같은 시각화 도구를 사용하면 온톨로지 관계를 인터랙티브하게 탐색할 수 있습니다.
   - Bloom 외에 Linkurious, Graphistry, Gephi 등의 도구도 검토 가능합니다.

3. **관계 메타데이터 및 주석 강화**
   - 관계 자체에 속성을 부여하는 전략: 예를 들어 "데이터셋 A *연관됨(related_to)* 데이터셋 B"라는 관계에 "유사한 고객 특성"이라는 주석이나 관계 강도(weight) 값을 부여합니다.
   - 관계를 **엔터티로 승격**: 관계 자체를 하나의 노드(예: Relation 노드)로 만들고 원래 두 엔터티와 각각 연결하여, Relation 노드에 속성을 다는 모델링입니다.
   - 온톨로지 전용 저장소(예: RDF 트리플스토어)를 병행 운영하고 DataHub의 엔티티 URN을 연결 고리로 사용하는 것도 고려해야 합니다.

4. **LLM 활용 자연어 인터페이스**
   - 대화형 질의 인터페이스를 도입: 사용자가 자연어로 "X와 연관된 데이터 자산을 보여줘"라고 물으면, LLM이 백엔드 그래프에 질의를 생성하고 결과를 요약해주는 방식입니다.
   - 복잡한 관계도 자연어 설명으로 이해할 수 있게 합니다.
   - 구현 시 LLM에게 DataHub에서 추출한 관계 메타데이터(JSON)나 Neo4j Cypher 질의 결과를 포함시켜야 합니다.

**참고 사례 및 기술:**

- 링크드인: 내부적으로 유니버설 메타데이터 그래프를 구축할 때 DataHub와 별도로 RDF 기반 온톨로지 저장소를 사용하여 복잡한 관계를 표현
- Intuit: 자사 카탈로그의 메타데이터를 Neo4j로 옮겨 Neo4j Bloom으로 데이터 계보와 개념 체계를 시각화
- neosemantics(n10s): Neo4j에 RDF/OWL 온톨로지를 적재하여 기본적인 RDFS 계층을 표현하는 라이브러리
- Atlan, Collibra: 상용 데이터 카탈로그의 액티브 메타데이터 기능으로 사용자 정의 관계를 UI에서 추가하고 그래프로 확인 가능

---

### 4.4.2 스키마 강제성(Schema Enforcement) 파이프라인

#### 4.4.2.1 문제 정의
ApeRAG는 텍스트에서 스키마를 발견하는 **상향식(Bottom-up)** 도구인 반면, DataNexus는 정의된 온톨로지를 주입하는 **하향식(Top-down)**을 지향합니다. 이 두 방식의 충돌 시 처리 로직이 부재합니다.

**예시 문제:**
- LLM이 문서 파싱 중 DataHub에 없는 임의의 엔티티 생성
- 예: 'Sales' 대신 'Revenue', '매출' 대신 '세일즈' 등 비표준 용어 추출
- 결과적으로 지식 그래프에 표준화되지 않은 노드가 혼재

#### 4.4.2.2 Strict Mode 필터링 파이프라인

**3단계 스키마 강제 아키텍처:**

```txt
┌─────────────────────────────────────────────────────────────────────┐
│ Schema Enforcement Pipeline │
├─────────────────────────────────────────────────────────────────────┤
│ │
│ [Stage 1: Pre-Extraction] │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ • Glossary Term List를 LLM Prompt에 주입 │ │
│ │ • "다음 용어집에 있는 개체만 추출하세요: [용어1, 용어2, ...]" │ │
│ │ • 허용된 관계 유형 목록 제공 │ │
│ └──────────────────────────────────────────────────────────────┘ │
│ ▼ │
│ [Stage 2: Post-Extraction Validation] │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ • 추출된 Triple (S, P, O) 검증 │ │
│ │ • Subject: Glossary URI 매칭 확인 │ │
│ │ • Predicate: 허용된 관계 유형 확인 │ │
│ │ • Object: Glossary URI 또는 리터럴 값 확인 │ │
│ └──────────────────────────────────────────────────────────────┘ │
│ ▼ │
│ [Stage 3: Resolution & Action] │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │ │
│ │ │ ACCEPT │ │ REMAP │ │ REJECT │ │ │
│ │ │ 100% 일치 │ │ 동의어 매핑 │ │ 불일치 → 검토 큐 │ │ │
│ │ └─────────────┘ └─────────────┘ └─────────────────────┘ │ │
│ └──────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────┘
```

**검증 알고리즘:**

> 📌 **구현 코드 → Implementation_Guide_final.md 이관.** 인터페이스 계약:
> - **클래스:** `SchemaEnforcer(glossary_terms: List[GlossaryTerm])`
> - **핵심 메서드:** `validate_triple(triple: Triple) → ValidationResult`
> - **검증 4단계:** Exact Match(ACCEPT) → Synonym Match(REMAP) → Fuzzy Match 0.85(REVIEW) → REJECT
> - **액션 매핑:** ACCEPT/REMAP → STORE, REVIEW → QUEUE(관리자 검토), REJECT → DISCARD

**관리자 검토 UI 요소:**

| UI 컴포넌트 | 기능 |
| :--- | :--- |
| **Pending Review Queue** | REVIEW 상태 트리플 목록 |
| **Suggestion Panel** | LLM 제안 매핑 표시 (예: "Revenue → 매출" 제안) |
| **Action Buttons** | [Approve as-is] / [Map to Term] / [Add New Term] / [Reject] |
| **Bulk Actions** | 유사 패턴 일괄 처리 |

#### 4.4.2.3 스키마 강제성 지표

| 지표명 | 정의 | 목표 기준 |
| :--- | :--- | :--- |
| **Schema Compliance Rate** | ACCEPT 또는 REMAP 처리된 트리플 비율 | 90% 이상 |
| **Rejection Rate** | REJECT 처리된 트리플 비율 | 5% 미만 |
| **Review Queue Latency** | 검토 큐 평균 처리 시간 | 24시간 이내 |
| **False Rejection Rate** | 잘못 거부된 유효 트리플 비율 | 2% 미만 |

#### 4.4.2.4 운영 비용과 Review Queue 병목 문제 해결 전략

**문제 요약:**

엄격한 스키마 강제(Strict Mode)는 데이터 품질과 일관성을 높여주지만, 모든 변경 사항을 사전에 검증하려다 보면 운영 비용이 급증합니다. 특히 새로운 필드나 스키마 변경이 발생할 때마다 인적 리뷰 절차를 거치게 되면 처리 지연이 발생해 개발 속도를 저해합니다. 검증 대기열(Review Queue)이 길어지면 데이터 플랫폼의 민첩성이 떨어지고, 사용자들은 규정을 피하는 방향으로 움직일 위험이 있습니다.

**현재 PRD 설계의 한계:**

현재 온톨로지 설계에서는 스키마를 엄격히 준수하도록 요구하고 있어, 예상치 못한 스키마 변경이나 신규 데이터 필드가 나타나면 모두 수동 검토를 받아야 합니다. 이로 인해 Review Queue에 항목이 쌓이고 처리 지연이 발생하는 병목 현상이 있습니다. 현재 설계는 변경 허용 여부를 이분법적(승인/거부)으로 다루고 있어, 경미한 변경에 대해서도 전면 차단되는 문제가 있습니다.

**실무적 보완 전략:**

1. **완화된 스키마 모드(Relaxed Mode) 도입**
   - 프로덕션에서는 Strict Mode를 기본으로 하되, 사전 정의된 규칙에 따라 부분적 유연성을 부여합니다.
   - 새로운 컬럼이 추가되었을 때 자동 승인 조건을 정합니다: 네이밍 컨벤션 준수하고 기존 온톨로지 용어와 유사한 경우 임시로 받아들이고, 추후 검토하도록 이중 단계 적용을 합니다.
   - 변경사항의 **위험도 분류** 자동화: 중대(P0) 변경(필수 필드 제거, 데이터 타입 변경 등)만 즉시 차단하고, 그 외에는 일단 수용한 후 경고를 기록하거나 일정 기간 내 검토합니다.

   ```python
   class RelaxedSchemaEnforcer(SchemaEnforcer):
       """완화된 스키마 모드 - 운영 병목 최소화"""
       
       def validate_triple_relaxed(self, triple: Triple) -> ValidationResult:
           # 기존 검증 수행
           result = super().validate_triple(triple)
           
           # 위험도 분류
           risk_level = self._classify_risk(triple, result)
           
           if risk_level == "CRITICAL":
               return result  # 기존 로직 그대로 (차단)
           elif risk_level == "WARNING":
               # 경고 기록 후 통과
               self._log_warning(triple, result)
               result.action = "STORE_WITH_WARNING"
               return result
           else:
               # 자동 승인 조건 충족
               if result.subject_status == "REVIEW" and self._auto_approve_eligible(triple):
                   result.subject_status = "AUTO_APPROVED"
                   result.action = "STORE"
               return result
       
       def _classify_risk(self, triple: Triple, result: ValidationResult) -> str:
           """위험도 분류: CRITICAL / WARNING / LOW"""
           # P0 위험: 필수 필드 제거, 데이터 타입 변경, 보안 관련
           if self._is_critical_change(triple):
               return "CRITICAL"
           # 경미한 변경: 신규 컬럼 추가, 동의어 확장
           elif self._is_minor_change(triple):
               return "LOW"
           return "WARNING"
       
       def _auto_approve_eligible(self, triple: Triple) -> bool:
           """자동 승인 조건: 네이밍 컨벤션 준수 + 유사도 95% 이상"""
           return (
               self._follows_naming_convention(triple.subject) and
               self._fuzzy_match(triple.subject) >= 0.95
           )
   ```

2. **자동 검증 파이프라인 (CI/CD 통합)**
   - CI/CD 파이프라인에 데이터 스키마 테스트를 추가하여, 배포 전에 스키마 변경을 자동 검출하고 검증합니다.
   - 데이터 계약(Data Contract)을 YAML/JSON으로 정의해 두고, 이를 기반으로 **Great Expectations**나 **JSON Schema** 검증을 통해 사전 테스트를 수행합니다.
   - 데이터 변경 시 자동으로 거버넌스 팀에 알람과 diff 리포트를 보내주는 툴을 사용해 수동 검토 작업량을 줄입니다.

   ```yaml
   # data_contract_schema.yaml
   contract:
     name: "GRS_SALES_CONTRACT"
     version: "1.2"
     owner: "grs-data-team@lotte.net"
     
   schema:
     columns:
       - name: "NET_SALES_AMT"
         type: "DECIMAL(15,2)"
         nullable: false
         description: "순매출금액"
         ontology_term: "urn:li:glossaryTerm:순매출"
         
   rules:
     - type: "not_null"
       columns: ["NET_SALES_AMT", "TRANSACTION_DATE"]
     - type: "range_check"
       column: "NET_SALES_AMT"
       min: 0
       
   change_policy:
     auto_approve:
       - "add_nullable_column"
       - "extend_string_length"
     requires_review:
       - "remove_column"
       - "change_data_type"
       - "add_not_null_constraint"
   ```

3. **LLM 기반 메타데이터 어시스턴트**
   - 대형언어모델(LLM)을 활용하여 새로운 필드나 테이블의 메타데이터를 자동 생성하고, 온톨로지 매핑 제안을 할 수 있습니다.
   - 새로운 컬럼 이름이 들어오면 LLM이 해당 이름을 분석해 기존 용어와의 유사도를 판단하거나, 민감정보(PII) 여부를 식별하여 자동 태깅합니다.
   - 리뷰어는 LLM의 제안을 빠르게 검토 및 승인만 하면 되므로, 처리량을 증대하고 대기열 병목을 완화할 수 있습니다.

   ```python
   class LLMMetadataAssistant:
       """LLM 기반 메타데이터 자동 분류 및 매핑 제안"""
       
       def suggest_ontology_mapping(self, new_column: str, context: dict) -> MappingSuggestion:
           prompt = f"""
           새로운 데이터 컬럼이 추가되었습니다.
           컬럼명: {new_column}
           테이블: {context.get('table_name')}
           기존 컬럼들: {context.get('existing_columns')}
           
           기존 온톨로지 용어집:
           {self._get_glossary_summary()}
           
           다음을 분석해주세요:
           1. 가장 유사한 기존 온톨로지 용어 (유사도 점수 포함)
           2. PII(개인정보) 포함 여부
           3. 권장 매핑 또는 신규 용어 등록 제안
           """
           
           response = self.llm.generate(prompt)
           return self._parse_suggestion(response)
   ```

4. **자가 서비스 및 카탈로그 협업**
   - 데이터 생산자들이 스키마 변경을 자가 서비스로 제안하고 추적할 수 있는 워크플로를 구축합니다.
   - DataHub 상에서 스키마 제안 기능이나, Pull Request를 통해 온톨로지 레지스트리(entity-registry)에 변경사항을 기여하도록 합니다.
   - 승인 프로세스도 투명하게 공개하여 이해관계자가 함께 리뷰하도록 하면 중앙팀 부담이 줄어듭니다.
   - 핵심: **"컴플라이언스 경로도 빠르게"** - 승인 절차를 자동화하고, 템플릿화된 표준 변경은 바로바로 적용되도록 합니다.

**참고 사례 및 기술:**

| 기술/사례 | 설명 | 적용 방안 |
| :--- | :--- | :--- |
| **데이터 계약(Data Contracts)** | 스키마와 품질 규칙을 코드로 관리하고 파이프라인에서 자동 검증 | 넷플릭스, 링크드인 사례 참조 |
| **Delta Lake schemaEvolution** | 엄격 스키마 모드에서 명시적으로 스키마 변경 허용 | 새로운 컬럼 자동 병합 설정 |
| **Great Expectations / Deequ** | 데이터 품질 프레임워크로 스키마 규칙 모니터링 | CI/CD 파이프라인 통합 |
| **DLT Expectations** | 기대 조건 설정 후 위반 시 경고 누적 및 대시보드 기록 | 위반 사례 주기적 검토 |
| **Monte Carlo / Bigeye** | 데이터 관측성 도구, 스키마 드리프트 자동 감지 및 알림 | 사후 대응 체계 구축 |

**개선된 검토 큐 관리 UI:**

| UI 컴포넌트 | 기능 | 개선 사항 |
| :--- | :--- | :--- |
| **Smart Review Queue** | 위험도별 분류된 검토 목록 | Critical/Warning/Low 탭 분리 |
| **LLM Suggestion Panel** | AI 제안 매핑 표시 | 신뢰도 점수 + 근거 설명 포함 |
| **Bulk Actions** | 유사 패턴 일괄 처리 | 동일 테이블 변경 그룹화 |
| **Auto-Approval Log** | 자동 승인된 항목 감사 이력 | 사후 검토 및 롤백 지원 |
| **SLA Dashboard** | 큐 대기 시간 모니터링 | 24시간 초과 항목 알림 |

---

### 4.4.3 적합성 질문(Competency Questions) 검증 프레임워크

#### 4.4.3.1 문제 정의
기존 PRD은 구축 후의 구조적 지표(고립 노드 비율 등)에 집중하고 있으나, **"이 온톨로지로 현업의 핵심 질문에 답할 수 있는가?"**를 사전에 검증하지 않으면 구축 후 전면 수정이 필요할 수 있습니다.

**Competency Questions(CQs)란:**
온톨로지가 반드시 답할 수 있어야 하는 질문들로, 온톨로지의 범위와 요구사항을 정의합니다. CQs는 온톨로지가 원하는 지식을 적절히 표현하고 있는지 검증하는 메커니즘을 제공합니다.

※ 출처: Springer "Use of Competency Questions in Ontology Engineering: A Survey" (2023)

#### 4.4.3.2 CQ 유형 분류 (Model for Competency Questions)

최근 연구에 따르면 CQs는 5가지 주요 유형으로 분류됩니다:

| CQ 유형 | 목적 | DataNexus 적용 예시 |
| :--- | :--- | :--- |
| **Scoping CQ (SCQ)** | 온톨로지 범위 정의 | "이 온톨로지는 어떤 도메인의 매출 데이터를 다루는가?" |
| **Validating CQ (VCQ)** | 온톨로지 정확성 검증 | "순매출은 총매출에서 무엇을 차감한 값인가?" |
| **Foundational CQ (FCQ)** | 핵심 개념 존재 확인 | "고객 유형을 구분하는 개념이 정의되어 있는가?" |
| **Relationship CQ (RCQ)** | 관계 표현력 확인 | "제품과 공장 간의 생산 관계를 표현할 수 있는가?" |
| **Metaproperty CQ (MpCQ)** | 메타 속성 검증 | "VIP 고객의 정의 조건은 무엇인가?" |

※ 출처: arXiv "Discerning and Characterising Types of Competency Questions for Ontologies" (2024)

#### 4.4.3.3 CQ 기반 검증 파이프라인

**Phase 0: CQ 수집 및 정의**

```txt
┌─────────────────────────────────────────────────────────────────────┐
│ Competency Questions Collection Workflow │
├─────────────────────────────────────────────────────────────────────┤
│ │
│ [Step 1: 현업 인터뷰] │
│ • 도메인 전문가와 워크숍 진행 │
│ • "데이터로 답하고 싶은 질문" 수집 │
│ • 5WH 프레임워크 활용 (Who, What, When, Where, Why, How) │
│ │
│ [Step 2: CQ 정형화] │
│ • 자연어 질문 → 구조화된 CQ 템플릿 변환 │
│ • CQ 유형 분류 (SCQ/VCQ/FCQ/RCQ/MpCQ) │
│ • 우선순위 부여 (Critical/High/Medium/Low) │
│ │
│ [Step 3: CQ 검증] │
│ • 모호성 검사 │
│ • 측정 가능성 확인 │
│ • 중복 제거 │
│ │
└─────────────────────────────────────────────────────────────────────┘
```

**CQ 정의 템플릿:**

```yaml
# competency_question_template.yaml
cq_id: "CQ-GRS-001"
domain: "GRS 영업"
question_natural: "지난 달 VIP 고객의 순매출 합계는 얼마인가?"
cq_type: "RCQ" # Relationship CQ
priority: "Critical"

required_concepts:
 - name: "VIP고객"
    type: "Entity"
    definition_required: true
 - name: "순매출"
    type: "Metric"
    formula_required: true
 - name: "기간"
    type: "Temporal"

required_relationships:
 - subject: "VIP고객"
    predicate: "PurchasedBy"
    object: "거래"
 - subject: "거래"
    predicate: "HasMetric"
    object: "순매출"

expected_query_pattern: |
 SELECT SUM(net_sales)
 FROM transactions t
 JOIN customers c ON t.customer_id = c.id
 WHERE c.customer_type = 'VIP'
    AND t.transaction_date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)

validation_criteria:
 - "VIP 고객 정의 조건이 온톨로지에 명시되어야 함"
 - "순매출 계산식이 정의되어야 함"
 - "기간 필터링이 가능해야 함"
```

**CQ 검증 시뮬레이션:**

> 📌 **구현 코드 → Implementation_Guide_final.md 이관.** 인터페이스 계약:
> - **클래스:** `CQValidator(ontology: Ontology, llm: LLM)`
> - **핵심 메서드:** `validate_cq(cq: CompetencyQuestion) → CQValidationResult`
> - **검증 5단계:** 개념 존재 → 관계 표현력 → 쿼리 생성 시뮬레이션 → 실행 가능성 → LLM-as-a-Judge 평가
> - **출력:** concept_coverage, relationship_coverage, query_generated, llm_score, missing_elements, recommendation

#### 4.4.3.4 CQ 검증 대시보드

| UI 섹션 | 표시 정보 |
| :--- | :--- |
| **CQ Coverage Matrix** | CQ별 통과/실패 현황 히트맵 |
| **Gap Analysis** | 누락된 개념/관계 목록 및 권장 조치 |
| **Priority Queue** | Critical CQ 중 미해결 항목 우선순위 정렬 |
| **Trend Chart** | 시간별 CQ 통과율 추이 |
| **Simulation Log** | 쿼리 생성 시뮬레이션 결과 상세 로그 |

#### 4.4.3.5 CQ 검증 지표

| 지표명 | 정의 | 목표 기준 |
| :--- | :--- | :--- |
| **CQ Pass Rate** | 검증 통과한 CQ 비율 | Phase 1: 80%, Phase 2: 95% |
| **Critical CQ Coverage** | Critical 우선순위 CQ 통과율 | 100% |
| **Concept Coverage** | CQ에서 요구하는 개념 중 정의된 비율 | 95% 이상 |
| **Query Generation Success** | CQ 질문으로부터 유효한 쿼리 생성 성공률 | 85% 이상 |

---

### 4.4.4 변경 관리(Versioning) 및 증분 업데이트 전략

#### 4.4.4.1 문제 정의
온톨로지가 변경될 때마다 전체 인덱싱을 다시 하는 것은 비용 효율적이지 않습니다. 특히 대규모 지식 그래프에서는 다음 문제가 발생합니다:

- **재색인 비용:** 전체 벡터 임베딩 재생성 시 GPU/API 비용 급증
- **서비스 중단:** 재구축 중 쿼리 가용성 저하
- **이력 손실:** 변경 전 상태로 롤백 불가
- **연쇄 영향:** 상위 개념 변경 시 하위 인스턴스와의 연결 파악 어려움

#### 4.4.4.2 증분 업데이트(Incremental Update) 아키텍처

**변경 유형별 업데이트 전략:**

| 변경 유형 | 영향 범위 | 업데이트 전략 | 예상 비용 절감 |
| :--- | :--- | :--- | :--- |
| **Term 추가** | 신규 노드만 | 신규 노드 + 직접 연결 엣지만 인덱싱 | 95% |
| **Term 정의 수정** | 해당 노드 + 직접 참조 | 해당 노드 임베딩 + 연관 문서 청크 재색인 | 80% |
| **관계 추가/삭제** | 연결된 노드 쌍 | 그래프 인덱스 부분 업데이트 | 90% |
| **Term 삭제** | 하위 노드 + 참조 문서 | Soft Delete → 참조 검사 → Hard Delete | 70% |
| **계층 구조 변경** | 서브트리 전체 | 영향받는 서브그래프만 재계산 | 60% |

**증분 업데이트 파이프라인:**

```txt
┌─────────────────────────────────────────────────────────────────────┐
│ Incremental Update Pipeline Architecture │
├─────────────────────────────────────────────────────────────────────┤
│ │
│ [1. Change Detection] │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ DataHub Webhook → Change Event Capture │ │
│ │ • Entity URN │ │
│ │ • Change Type (CREATE/UPDATE/DELETE) │ │
│ │ • Changed Aspects (definition, relationships, etc.) │ │
│ │ • Timestamp │ │
│ └──────────────────────────────────────────────────────────────┘ │
│ ▼ │
│ [2. Impact Analysis] │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ • 변경된 Term과 연결된 노드 탐색 (1-hop, 2-hop) │ │
│ │ • 영향받는 문서 청크 식별 │ │
│ │ • 영향받는 Vanna Training Data 식별 │ │
│ │ • 영향 범위 점수화 (Impact Score) │ │
│ └──────────────────────────────────────────────────────────────┘ │
│ ▼ │
│ [3. Selective Re-indexing] │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │ │
│ │ │ DozerDB │ │ Qdrant │ │ Vanna AI │ │ │
│ │ │ 그래프 부분 │ │ 벡터 부분 │ │ Documentation │ │ │
│ │ │ 업데이트 │ │ 업데이트 │ │ 부분 재학습 │ │ │
│ │ └─────────────┘ └─────────────┘ └─────────────────────┘ │ │
│ └──────────────────────────────────────────────────────────────┘ │
│ ▼ │
│ [4. Consistency Verification] │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ • 참조 무결성 검사 │ │
│ │ • 버전 일관성 확인 │ │
│ │ • CQ 회귀 테스트 (Critical CQs만) │ │
│ └──────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────┘
```

**영향 분석 알고리즘:**

> 📌 **구현 코드 → Implementation_Guide_final.md 이관.** 인터페이스 계약:
> - **클래스:** `ImpactAnalyzer(graph_db: DozerDB, vector_db: Qdrant)`
> - **핵심 메서드:** `analyze_change_impact(change_event: ChangeEvent) → ImpactReport`
> - **분석 4단계:** 직접 영향 1-hop → 간접 영향 2-hop(계층 변경 시) → 문서 청크 식별 → 영향 점수 계산
> - **전략 추천:** impact_score < 0.1 → INCREMENTAL, < 0.5 → PARTIAL_REBUILD, else → FULL_REBUILD
> - **출력:** affected_nodes, affected_documents, impact_score, recommended_strategy, estimated_time

**버전 관리 스키마:**

```yaml
# ontology_version_schema.yaml
version:
 major: 2 # 스키마 비호환 변경
 minor: 8 # 기능 추가 (하위 호환)
 patch: 1 # 버그 수정

changelog:
 - version: "2.8.1"
    date: "2026-02-02"
    changes:
      - type: "TERM_ADDED"
        entity: "urn:li:glossaryTerm:신규매출지표"
        impact_score: 0.05
      - type: "DEFINITION_UPDATED"
        entity: "urn:li:glossaryTerm:순매출"
        old_value: "총매출 - 반품"
        new_value: "총매출 - 반품 - 할인 - 에누리"
        impact_score: 0.15

rollback_points:
 - version: "2.8.0"
    snapshot_uri: "gs://ontology-snapshots/v2.8.0.tar.gz"
    created_at: "2026-02-01T00:00:00Z"
```

#### 4.4.4.3 DataHub 버전 이력 활용

DataHub는 모든 메타데이터 변경을 Append-Only 이력으로 저장합니다:

```graphql
# DataHub GraphQL API로 버전 이력 조회
query getTermHistory($urn: String!) {
 glossaryTerm(urn: $urn) {
    urn
    aspects(input: { aspectNames: ["glossaryTermProperties"] }) {
      aspect
      version
      createdOn
      createdBy
      entityKeyAspect
    }
 }
}
```

**롤백 프로세스:**

> 📌 **구현 코드 → Implementation_Guide_final.md 이관.** 인터페이스 계약:
> - **클래스:** `OntologyVersionManager`
> - **핵심 메서드:** `rollback_to_version(target_version: str)`
> - **롤백 5단계:** 스냅샷 로드 → diff 계산 → DataHub 적용(TERM_DELETED/MODIFIED) → RAG Store 동기화 → 버전 메타데이터 갱신
> - **버전 규칙:** 롤백 시 patch 버전 증가, rollback_from/rollback_to 메타데이터 기록

#### 4.4.4.4 변경 관리 지표

| 지표명 | 정의 | 목표 기준 |
| :--- | :--- | :--- |
| **Incremental Update Ratio** | 증분 업데이트로 처리된 변경 비율 | 90% 이상 |
| **Average Reindex Time** | 변경 당 평균 재색인 소요 시간 | 5분 이내 |
| **Cost Reduction Rate** | 전체 재구축 대비 비용 절감률 | 70% 이상 |
| **Rollback Success Rate** | 롤백 시도 성공률 | 99% 이상 |
| **Version Consistency Score** | 모든 컴포넌트 간 버전 일관성 | 100% |

---

## 4.5 온톨로지 엔지니어링 실무 대응

### 4.5.1 SKOS 호환성 레이어 (표준 호환성 확보)

#### 4.5.1.1 문제 정의
현재 설계는 시맨틱 웹 표준인 RDF/OWL과의 호환성을 '향후 검토 사항'으로 미뤄두었습니다. 이로 인해:
- **외부 온톨로지 활용 제한:** FIBO(금융), Schema.org(범용) 등 성숙한 산업별 표준 온톨로지를 Import하여 초기 구축 비용을 줄이는 데 제약
- **시스템 간 지식 공유 제한:** 기업 내 타 시스템과 지식을 공유하거나 Export할 때 데이터 손실 발생 가능

#### 4.5.1.2 SKOS(Simple Knowledge Organization System) 개념 차용

당장 RDF/OWL로 전면 전환하는 것은 비효율적이나, W3C 표준인 SKOS의 핵심 구조를 내부적으로 매핑하여 향후 확장성을 확보합니다.

**DataHub → SKOS 매핑 테이블 (개념 소개용 요약):**

> **📌 SSOT:** 정밀 필드 매핑(양방향, 변환 규칙 포함)은 **§4.7.1 SKOS-DataHub 필드 매핑**을 참조하세요. 아래는 개념 이해를 위한 간략 매핑입니다.

| DataHub 개념 | SKOS 대응 개념 | 설명 | 매핑 방식 |
| :--- | :--- | :--- | :--- |
| GlossaryTerm.name | skos:prefLabel | 기본 레이블 (표준 명칭) | 1:1 직접 매핑 |
| GlossaryTerm.synonyms | skos:altLabel | 대체 레이블 (동의어, 약어) | 배열 → 다중 altLabel |
| GlossaryTerm.definition | skos:definition | 용어 정의 | 1:1 직접 매핑 |
| IsA (relatedTerms) | skos:broader | 상위 개념 관계 | 방향 반전 필요 |
| HasA (relatedTerms) | skos:narrower | 하위 개념 관계 | 방향 반전 필요 |
| RelatedTo | skos:related | 연관 관계 | 1:1 직접 매핑 |
| GlossaryNode | skos:ConceptScheme | 용어 그룹/스키마 | 1:1 직접 매핑 |

#### 4.5.1.3 외부 온톨로지 Import 전략

**지원 대상 표준 온톨로지:**

| 온톨로지 | 도메인 | 활용 시나리오 | Import 우선순위 |
| :--- | :--- | :--- | :--- |
| **FIBO** | 금융 | 금융 용어 (자산, 부채, 수익) 초기 구축 | 높음 (금융 계열사) |
| **Schema.org** | 범용 | 조직, 제품, 장소 등 공통 개념 | 중간 |
| **GoodRelations** | 전자상거래 | 상품, 가격, 결제 관련 용어 | 높음 (유통 계열사) |

<!-- TODO(비즈니스): 그룹사 목록 확정 후 업데이트 필요 - 현재 "금융 계열사", "유통 계열사"는 예시입니다 -->

#### 4.5.1.4 SKOS 호환성 지표

| 지표명 | 정의 | 목표 기준 |
| :--- | :--- | :--- |
| **SKOS Mapping Coverage** | SKOS 매핑이 완료된 GlossaryTerm 비율 | 95% 이상 |
| **Export Validation Rate** | 유효한 RDF로 Export된 비율 (SHACL 검증) | 100% |
| **Import Success Rate** | 외부 온톨로지 Import 성공률 | 90% 이상 |

---

### 4.5.2 Query Router Agent (추론 엔진 보완)

#### 4.5.2.1 문제 정의
DataNexus는 지식 그래프의 구조적 추론을 LLM의 경로 탐색에 의존합니다. 그러나:
- **확률적 추론의 한계:** LLM 기반 추론은 확률적이므로, 논리적 정합성(Consistency)을 100% 보장하기 어려움
- **비용 효율성:** 모든 질의에 LLM을 사용하면 비용과 지연 시간 증가
- **엄격한 비즈니스 룰:** 금융/제조 분야에서는 "대략 맞는" 답이 아닌 확정적인 답이 필요

#### 4.5.2.2 질의 분류 및 라우팅 전략

| 분류 | 특징 | 라우팅 대상 | 예시 |
| :--- | :--- | :--- | :--- |
| **DETERMINISTIC** | 정해진 패턴, 논리적 연산, 집계 | Cypher 템플릿 | "A의 모든 하위 조직은?", "B 제품의 총 매출은?" |
| **HYBRID** | 부분적 규칙 + 해석 필요 | 규칙 + LLM 검증 | "VIP 고객 중 최근 이탈 위험이 있는 사람은?" |
| **PROBABILISTIC** | 자유 형식, 창의적 해석 필요 | Full LLM | "경쟁사 대비 우리 강점 분석해줘" |

#### 4.5.2.3 Cypher 템플릿 라이브러리

**핵심 패턴 템플릿 (20+ 개 초기 구축):**
- 계층 관계 쿼리 (하위 노드 조회, 상위 노드 조회)
- 추이적 폐쇄 (Transitive Closure) - 공급망 추적
- 집계 연산 (카테고리별 합계/평균)
- 인과관계 체인 추론

<!-- TODO(개발): Cypher 템플릿 20+ 상세 목록 추가 필요 - 현재 4개 핵심 패턴만 나열됨. PRD_Appendix_CDE_final.md §D.2, §E.1 참조 (초기 20개 템플릿 구현 및 테스트 필요) -->

#### 4.5.2.4 LLM Fallback ì •ì±…
- 템플릿 매칭 실패 시 LLM으로 자동 전환
- 결과 검증기(ResultValidator)로 온톨로지 정합성 확인
- 신뢰도 점수 계산 및 사용자 표시 (0.7 미만 시 경고)

#### 4.5.2.5 Router Agent 지표

| 지표명 | 정의 | 목표 기준 |
| :--- | :--- | :--- |
| **Query Router Accuracy** | 올바른 경로로 라우팅된 질의 비율 | ≥ 0.95 (ratio; Phase 2: ≥ 0.97; 정식 기준은 §4.8 SSOT 참조) |
| **Deterministic Query Rate** | 템플릿으로 처리된 질의 비율 | 60% 이상 |
| **LLM Fallback Rate** | LLM으로 Fallback된 질의 비율 | 30% 미만 |
| **Average Response Time (Deterministic)** | 템플릿 기반 질의 평균 응답 시간 | 500ms 이내 |

#### 4.5.2.6 전문 추론 엔진 부재에 따른 추론 능력 한계와 보완 전략

**문제 요약:**

온톨로지의 강점 중 하나는 추론(Inference)을 통해 암묵적 지식을 이끌어내는 것입니다. 예를 들어 온톨로지에 "A는 B의 부분집합"이고 "B는 C의 부분집합"이라는 사실이 명시되면, 전문 추론 엔진은 자동으로 "A는 C의 부분집합"이라는 숨겨진 관계를 유추해냅니다. 그러나 전용 추론 엔진이 없으면 이러한 논리적 추론을 일일이 쿼리나 코드를 통해 구현해야 하고, 그마저도 일부 패턴만 다룰 수 있어 한계가 있습니다.

**현재 PRD 설계의 한계:**

현재 DataNexus PRD는 Neo4j(DozerDB) 기반의 온톨로지 저장을 사용하면서도, OWL 같은 서술논리 추론기(Reasoner)를 통합하지 않은 상태입니다. 그 결과, Cypher 템플릿 전략으로 일부 추론을 대체하고 있습니다. 문제는 이러한 접근이 규칙 추가나 변경에 비효율적이고, 추론 범위가 제한적이라는 것입니다. 새로운 논리 규칙이 생길 때마다 쿼리를 작성해야 하며, 추론 결과의 일관성도 보장하기 어렵습니다. OWL의 복잡한 규칙(동일성, 상호 배타 등)은 Cypher로 모두 표현하기 힘듭니다.

**실무적 보완 전략:**

1. **전문 Reasoner 도입 검토**
   
   가장 근본적인 해결책은 온톨로지를 지원하는 추론 엔진을 도입하는 것입니다.

   | 솔루션 | 유형 | 추론 수준 | 적용 방안 |
   | :--- | :--- | :--- | :--- |
   | **neosemantics (n10s)** | Neo4j 플러그인 | RDFS/OWL-Horst | 클래스 계층 추론, 관계 상속 |
   | **Apache Jena** | RDF 프레임워크 | OWL RL | 배치 추론 파이프라인 구축 |
   | **GraphDB (Ontotext)** | RDF 스토어 | OWL 2 RL | 완전한 RDF 추론 환경 |
   | **Stardog** | 상용 그래프DB | OWL DL + SWRL | 고급 비즈니스 룰 처리 |

   ```python
   class HybridReasoningPipeline:
       """Neo4j + 외부 Reasoner 연계 파이프라인"""
       
       def __init__(self, neo4j_client, jena_reasoner):
           self.neo4j = neo4j_client
           self.jena = jena_reasoner
           
       def run_batch_inference(self):
           """배치 추론 파이프라인 실행"""
           
           # 1. Neo4j에서 온톨로지 데이터 Export
           rdf_export = self.neo4j.export_to_rdf()
           
           # 2. Jena Reasoner로 추론 수행
           inferred_triples = self.jena.reason(
               data=rdf_export,
               rules="RDFS_PLUS_OWL_RL"
           )
           
           # 3. 추론 결과를 Neo4j에 Import
           for triple in inferred_triples:
               if triple.is_new:
                   self.neo4j.execute(f"""
                       MATCH (s {{uri: '{triple.subject}'}})
                       MATCH (o {{uri: '{triple.object}'}})
                       MERGE (s)-[:INFERRED_{triple.predicate} {{
                           inferred_at: datetime(),
                           rule: '{triple.applied_rule}'
                       }}]->(o)
                   """)
           
           return InferenceReport(
               new_triples=len(inferred_triples),
               execution_time=elapsed
           )
   ```

   - neosemantics(n10s)를 사용하면 Neo4j에 OWL 형태로 온톨로지를 로드하고, RDFS/OWL-Horst 수준의 추론 질의를 할 수 있습니다.
   - 완전한 OWL DL 추론은 어렵더라도, 클래스 계층 추론이나 관계 상속 등 핵심 기능은 지원됩니다.
   - DataHub/Neo4j에서 온톨로지 데이터를 정기적으로 export하여 Jena의 Ontology Model로 넣고 내장 Reasoner를 태워 추론 결과를 다시 가져오는 배치를 만들 수 있습니다.

2. **룰 기반 엔진 + Cypher 연계**
   
   OWL 같은 포멀한 추론기 대신, 룰 엔진을 활용하는 방법도 있습니다.

   ```python
   class RuleBasedReasoner:
       """Drools/Prolog 스타일 룰 엔진 연계"""
       
       def __init__(self, rule_config: str):
           self.rules = self._load_rules(rule_config)
           
       def apply_rules(self, facts: List[Triple]) -> List[Triple]:
           """
           규칙 적용 예시:
           IF (A, subClassOf, B) AND (B, subClassOf, C)
           THEN (A, subClassOf, C)
           """
           inferred = []
           
           for rule in self.rules:
               matches = self._pattern_match(rule.conditions, facts)
               for match in matches:
                   conclusion = rule.apply(match)
                   if conclusion not in facts:
                       inferred.append(conclusion)
           
           return inferred
   ```

   - Drools와 같은 룰 엔진이나, Prolog와 같은 논리 프로그래밍을 통해 도메인 규칙을 관리합니다.
   - 온톨로지 데이터를 Prolog 팩트로 내보내고 Prolog 엔진을 통해 질의/추론합니다.
   - 추론 결과(결론 부분)는 다시 Cypher를 통해 Neo4j에 반영하거나 DataHub의 메타데이터 변경 API를 호출하여 저장합니다.
   - Neo4j의 APOC 트리거를 사용하면 특정 노드/관계 생성 시 자동 Cypher 실행이 가능하므로, 국지적 추론을 실시간으로 처리할 수 있습니다.

3. **Cypher 템플릿 고도화**
   
   완전한 reasoner 도입이 어렵다면, 기존 Cypher 템플릿 방식을 모듈화/자동화하여 쓰는 전략입니다.

   ```yaml
   # reasoning_rules.yaml
   rules:
     - id: "TRANSITIVE_SUBCLASS"
       name: "Transitive SubClass Closure"
       description: "A→B, B→C이면 A→C"
       pattern: |
         MATCH (a)-[:SUBCLASS_OF]->(b)-[:SUBCLASS_OF]->(c)
         WHERE NOT (a)-[:INFERRED_SUBCLASS_OF]->(c)
       action: |
         MERGE (a)-[:INFERRED_SUBCLASS_OF {
           rule: 'TRANSITIVE_SUBCLASS',
           created: datetime()
         }]->(c)
       schedule: "DAILY"
       
     - id: "INVERSE_RELATION"
       name: "Inverse Relation Generation"
       description: "A→manufactures→B이면 B→producedBy→A"
       pattern: |
         MATCH (a)-[:MANUFACTURES]->(b)
         WHERE NOT (b)-[:PRODUCED_BY]->(a)
       action: |
         MERGE (b)-[:PRODUCED_BY {
           rule: 'INVERSE_RELATION',
           created: datetime()
         }]->(a)
       schedule: "ON_CREATE"
   ```

   ```python
   class CypherRuleEngine:
       """Cypher 템플릿 기반 추론 규칙 관리"""
       
       def __init__(self, rule_config_path: str):
           self.rules = yaml.safe_load(open(rule_config_path))
           
       def execute_scheduled_rules(self, schedule_type: str = "DAILY"):
           """스케줄된 추론 규칙 실행"""
           for rule in self.rules['rules']:
               if rule['schedule'] == schedule_type:
                   self._execute_rule(rule)
                   
       def execute_on_event(self, event_type: str, affected_nodes: List):
           """이벤트 기반 추론 규칙 실행"""
           for rule in self.rules['rules']:
               if rule['schedule'] == f"ON_{event_type}":
                   for node in affected_nodes:
                       self._execute_rule(rule, context={'node': node})
   ```

   - 현재 수동으로 관리하는 Cypher 규칙들을 정리해 룰 메타데이터로 관리합니다.
   - JSON이나 YAML로 규칙들을 나열해 두고, 이를 파싱하여 Cypher 쿼리를 자동 생성/실행하는 스크립트를 작성합니다.
   - 미리계산(materialized)하는 것과 질의 시 추론(on-the-fly) 하는 것을 구분합니다.
   - 생성된 추론 결과는 원본과 혼동되지 않게 별도 관계 타입이나 플래그를 붙여 관리합니다.

4. **LLM 기반 보조 추론**
   
   추론 엔진 없이도, ChatGPT와 같은 LLM을 제한적으로 추론에 활용하는 방법입니다.

   ```python
   class LLMReasoningAssistant:
       """LLM 기반 보조 추론 및 설명 생성"""
       
       def explain_relationship(self, entity_a: str, entity_b: str) -> str:
           """두 엔티티 간 관계 추론 및 설명"""
           
           # 그래프에서 관련 정보 수집
           paths = self.graph_db.find_all_paths(entity_a, entity_b, max_depth=3)
           properties_a = self.graph_db.get_properties(entity_a)
           properties_b = self.graph_db.get_properties(entity_b)
           
           prompt = f"""
           두 엔티티 간의 관계를 분석해주세요.
           
           엔티티 A: {entity_a}
           - 속성: {properties_a}
           
           엔티티 B: {entity_b}
           - 속성: {properties_b}
           
           발견된 연결 경로:
           {self._format_paths(paths)}
           
           위 정보를 바탕으로:
           1. 두 엔티티의 관계를 설명해주세요.
           2. 암묵적으로 유추할 수 있는 추가 관계가 있다면 제안해주세요.
           3. 비즈니스적 함의를 설명해주세요.
           
           주의: 그래프에 명시된 정보만 사용하고, 외부 지식은 사용하지 마세요.
           """
           
           return self.llm.generate(prompt)
   ```

   - 온톨로지 그래프에서 찾기 어려운 연역적 질문(왜/어떻게 관련되었는지)을 사용자가 묻는 경우, 관련된 그래프 요소들을 검색한 후 LLM에게 맥락을 설명해달라고 합니다.
   - LLM은 주어진 정보를 바탕으로 인과 관계 추론이나 설명 생성을 수행합니다.
   - Retrieval-Augmented Generation(RAG) 기법으로 그래프에서 필요한 정보만 추출해 프롬프트에 넣고, 답변의 근거로 해당 정보들을 인용하게 합니다.

**참고 사례 및 기술:**

| 기술 | 설명 | 적용 방안 |
| :--- | :--- | :--- |
| **neosemantics (n10s)** | Neo4j에서 RDF 삼중 스토어처럼 동작, RDFS/OWL 추론 질의 지원 | 클래스 계층, 관계 상속 추론 |
| **GraphAware JSON Rules** | JSON으로 작성한 규칙을 트리거처럼 동작 | 조건 충족 시 자동 액션 |
| **OWL 2 RL 규칙 집합** | 시맨틱 웹 표준 추론 패턴 | 추론 템플릿 설계 참조 |
| **Drools** | Java 기반 비즈니스 룰 엔진 | 복잡한 비즈니스 규칙 처리 |
| **APOC 트리거** | Neo4j 노드/관계 생성 시 자동 실행 | 실시간 국지적 추론 |

**추론 능력 관련 지표:**

| 지표명 | 정의 | 목표 기준 |
| :--- | :--- | :--- |
| **Inference Coverage** | 자동 추론으로 생성된 관계 비율 | 30% 이상 |
| **Inference Accuracy** | 추론된 관계의 정확도 | 95% 이상 |
| **Rule Execution Time** | 배치 추론 규칙 평균 실행 시간 | 5분 이내 |
| **Explanation Quality Score** | LLM 설명의 사용자 만족도 | 4.0/5.0 이상 |

---

### 4.5.3 LLM 기반 온톨로지 Drafting (자동화 효율성 제고)

#### 4.5.3.1 문제 정의
DataNexus는 현업 도메인 전문가가 용어를 정의하는 Data Mesh 사상을 따릅니다. 그러나:
- **초기 구축 공수:** 맨땅에서 시작하면 현업 담당자의 부담이 큼
- **참여 저조 리스크:** 현업 참여가 저조하면 전체 RAG 성능이 병목

#### 4.5.3.2 LLM 기반 초안 생성 전략

**핵심 원칙: 인간은 '창조'가 아닌 '검토'에 집중**

**Drafting 파이프라인:**
1. **스키마 → Triple 자동 추출:** DDL 분석을 통한 초기 온톨로지 구축
2. **문서 → 용어/관계 추천:** NER + LLM으로 비정형 문서에서 용어 후보 추출
3. **Human Review UI:** 승인/수정/거부 워크플로우

#### 4.5.3.3 외부 표준 온톨로지 활용
- FIBO(금융), GoodRelations(유통) 등 산업 표준을 Import하여 기본 뼈대 구축
- LLM 기반 한국어 레이블 번역 제안

#### 4.5.3.4 Drafting 자동화 지표

| 지표명 | 정의 | 목표 기준 |
| :--- | :--- | :--- |
| **Draft Acceptance Rate** | 수정 없이 승인된 초안 비율 | 50% 이상 |
| **Modified Acceptance Rate** | 수정 후 승인된 초안 비율 | 80% 이상 |
| **Time Savings** | 수동 대비 시간 절감률 | 60% 이상 |

---

### 4.5.4 DataHub 업그레이드 호환성 전략

#### 4.5.4.1 문제 정의
DataNexus는 DataHub의 커스텀 Aspect(synonyms, formula 등)에 의존합니다. DataHub 업그레이드 시:
- **커스텀 스키마 비호환:** 메타데이터 모델 변경으로 커스텀 필드가 손실될 수 있음
- **공식 기능 충돌:** 커스텀으로 구현한 기능이 공식 지원되면 마이그레이션 필요

#### 4.5.4.2 버전별 호환성 매트릭스

| DataHub 버전 | synonyms 지원 | 커스텀 Aspect | DataNexus 호환 |
| :--- | :--- | :--- | :--- |
| 1.3.0.1 (현재, 2026.02 확인 기준) | ⚠️ 로드맵 반영 중 | ✅ 커스텀 구현 | ✅ 완전 호환 |
| 1.4.x~1.5.x (예상, 미확정) | ✅ Glossary Synonyms 공식 지원 예상 | ✅ 유지 | ✅ 호환 (마이그레이션 권장) |
| 2.x (향후, 미확정) | ✅ 완전 지원 | ⚠️ 재검토 필요 | ⚠️ 마이그레이션 필수 |

> **⚠️ 주의:** 1.4.x 이상 버전 정보는 DataHub 공식 로드맵 기반 **추정치**이며, 실제 릴리스 시 변경될 수 있습니다. 프로젝트 진행 시 최신 릴리스 노트를 확인하세요.

> **DataHub 릴리스 이력:**
> - v1.3.0.1: 2025-11-13 (현재 최신 안정 버전, kafka-setup 버그 수정)
> - v1.3.0: 2025-07-19
> - v1.2.0: 2025-05-28
> - v1.1.0: 2025-03-14
> - v1.0.0: 2025-01-21
>
> **참고:** DataHub 2025 로드맵에 "Glossary Synonyms" 기능이 포함되어 있으며, 향후 버전에서 공식 지원될 예정입니다. 현재는 customProperties를 활용한 커스텀 구현 방식을 사용합니다.

#### 4.5.4.3 API 추상화 레이어
- DataHubClientInterface 추상 클래스 정의
- 버전별 Client 구현 (DataHubClientV1, DataHubClientV2 — §4.5.4.2 호환성 매트릭스 참조)
- 팩토리 패턴으로 버전 자동 감지 및 선택

#### 4.5.4.4 업그레이드 호환성 지표

| 지표명 | 정의 | 목표 기준 |
| :--- | :--- | :--- |
| **Migration Success Rate** | 마이그레이션 성공률 | 99.9% 이상 |
| **Downtime** | 업그레이드 중 서비스 중단 시간 | 4시간 이내 |
| **Data Integrity** | 마이그레이션 후 데이터 무결성 | 100% |

---

## 4.6 유통/물류 표준 온톨로지 도입 방안 (Seed Ontology Strategy)

### 4.6.1 목적 (Why)
- 표준 온톨로지를 Seed로 주입하여 온톨로지 구축의 Cold Start Problem(맨땅에서 시작하는 공수)을 줄입니다.
- LLM 기반 Drafting 단계에서 "상품/점포/가격/거래/물류거점" 같은 핵심 개념의 정의·관계를 표준으로 선점하여 Draft 품질과 일관성을 높입니다.
- 표준 식별자(GTIN, GLN 등)를 활용해 향후 ERP/SCM/외부 파트너 시스템과의 상호운용성(Interoperability) 및 매핑 비용을 개선합니다.

### 4.6.2 우선 적용 표준 (What)
- GoodRelations (전자상거래/거래 관계 중심): Offering, PriceSpecification, BusinessEntity 등 거래/가격/제안 모델링에 활용합니다.
- GS1 Web Vocabulary (상품/물류 식별 및 거점 중심): Product, Organization, Place 및 gtin/gln 등 식별 속성을 핵심 메타데이터로 활용합니다.

> 추정: 실제 도메인 범위(유통/물류/SCM)와 CQ(Competency Questions)에 따라 적용 범위와 매핑 우선순위는 조정될 수 있습니다.

### 4.6.3 적용 절차 (How)
1) Import (SKOS 호환성 레이어)
- 외부 RDF/OWL을 SKOS 호환 포맷으로 변환해 DataHub Glossary에 일괄 등록합니다.
- 원본 URI/Prefix(예: gs1:Product, gr:Offering)를 customProperties로 보존해 Export 및 추적성을 확보합니다.

2) Mapping (관계/서술어 정규화)
- 표준 관계를 DataNexus의 관계(Predicate) 분류 체계(IsA/HasA/Values/RelatedTo + 내부 Predicate 카탈로그)에 매핑합니다.
- 예: gs1:manufacturedBy → ProducedBy, gr:availableAtOrFrom → SoldBy (내부 표준명은 조직 표준에 맞춰 확정)

3) Context Engineering (LLM 주입)
- DataHub Glossary(표준 용어집)를 ApeRAG 프롬프트/룰에 Taxonomy로 주입합니다.
- 비정형 문서(운송장/거래명세서 등)에서 "A 물품이 B 창고로 이동" 같은 서술을 표준 관계(예: ShippedTo/SuppliesTo)로 안정적으로 추출하도록 유도합니다.

4) CQ 기반 사전 검증
- 표준 Seed가 "우리 비즈니스 질문에 답할 수 있는가?"를 CQ 매트릭스로 검증합니다.
- CQ Pass Rate를 품질 게이트로 설정하고, 실패 시 용어/관계/동의어 누락을 보완한 뒤 동기화(RAG Store 반영)를 진행합니다.

### 4.6.4 산출물 (Deliverables)
- 표준 용어집 YAML(DataHub Glossary ingest용)
- Ingestion Recipe(DataHub CLI)
- CQ 매트릭스 및 자동화 테스트(Pytest) (부록 G 참조)


---

### 4.7 SKOS-DataHub 매핑 갭 해소

> **⚠️ SKOS 호환성 레이어와 DataHub 실제 구현 간 매핑 테이블 부재 (리뷰 보고서 §2-4)**

§4.5.1에서 SKOS 호환성을 설계했으나, DataHub 필드와의 실제 매핑 테이블이 누락되었습니다.

#### 4.7.1 DataHub ↔ SKOS 필드 매핑

| DataHub 필드 | SKOS 속성 | 변환 방향 | 비고 |
|-------------|----------|----------|------|
| `glossaryTerm.name` | `skos:prefLabel` | 양방향 | 1:1 매핑 |
| `glossaryTerm.definition` | `skos:definition` | 양방향 | 1:1 매핑 |
| `glossaryTerm.isRelatedTerms` (IsA) | `skos:broader` / `skos:narrower` | 양방향 | 계층 관계 보존 |
| `glossaryTerm.relatedTerms` | `skos:related` | 양방향 | 일반 연관 |
| `glossaryTerm.synonyms` (커스텀) | `skos:altLabel` | 양방향 | DataHub는 커스텀 필드 필요 |
| `glossaryNode` (그룹) | `skos:ConceptScheme` | Export만 | Import 시 GlossaryNode로 생성 |
| `glossaryTerm.domain` | `skos:inScheme` | Export만 | Scheme 멤버십 매핑 |
| `glossaryTerm.uri` | `@id` (RDF URI) | 양방향 | URN → URI 변환 규칙 필요 |

#### 4.7.2 URN ↔ URI 변환 규칙

```python
from urllib.parse import quote, unquote

# DataHub URN → SKOS URI 변환
def urn_to_uri(datahub_urn: str) -> str:
    # urn:li:glossaryTerm:순매출 → https://datanexus.example.com/ontology/glossaryTerm/%EC%88%9C%EB%A7%A4%EC%B6%9C
    prefix = "https://datanexus.example.com/ontology/"
    path = datahub_urn.replace("urn:li:", "").replace(":", "/")
    # 한글 등 비-ASCII 문자를 퍼센트 인코딩 (RFC 3986)
    return prefix + quote(path, safe="/")

# SKOS URI → DataHub URN 변환 (Import 시)
def uri_to_urn(skos_uri: str) -> str:
    prefix = "https://datanexus.example.com/ontology/"
    path = unquote(skos_uri.replace(prefix, ""))
    return "urn:li:" + path.replace("/", ":")
```

#### 4.7.3 미매핑 SKOS 속성 처리 전략

| SKOS 속성 | DataHub 대응 | 처리 전략 |
|----------|-------------|----------|
| `skos:scopeNote` | 없음 | `definition`에 `[Scope]` 접두사로 병합 |
| `skos:historyNote` | 없음 | 커스텀 프로퍼티로 저장 |
| `skos:notation` | 없음 | `customProperties.notation`으로 저장 |
| `skos:exactMatch` (외부 온톨로지) | 없음 | 커스텀 프로퍼티 + Neo4j 관계로 이중 저장 |
| `skos:closeMatch` | 없음 | `relatedTerms`로 매핑 + 메타데이터에 match_type 기록 |

---

### 4.8 품질 지표 통합 정의

> **⚠️ 품질 지표 단일 진실 공급원 (SSOT)**
>
> 아래 테이블이 모든 품질 지표의 **유일한 정의처**입니다. 다른 문서에서는 이 테이블을 참조만 하고, 수치를 직접 복사하지 않습니다.
> - **단위 표기 규칙:** 모든 비율 지표는 ratio(0~1) 형식으로 표기합니다. 예: 0.05 (= 5%)

| 지표 | 통합 정의 | MVP 기준 | Phase 2 기준 | 단위 | 참조 섹션 |
|------|----------|---------|-------------|------|----------|
| **Query Router Accuracy** | Query Router의 올바른 에이전트/경로 선택 비율 | ≥ 0.95 | ≥ 0.97 | ratio | §3.4, §5.1 |
| **Hallucination Rate** | 근거 없는 정보가 응답에 포함된 비율 | ≤ 0.05 | ≤ 0.03 | ratio | §5.1, §5.3 |
| **Schema Compliance** | 스키마 강제성 통과 비율 (ACCEPT+REMAP) | ≥ 0.90 | ≥ 0.95 | ratio | §4.4.2.3, §5.1 |
| **CQ Pass Rate** | 적합성 질문 검증 통과율 | ≥ 0.80 | ≥ 0.95 | ratio | §4.4.3, §5.1 |
| **EX (Execution Accuracy)** | NL2SQL 실행 결과값 일치율 | ≥ 0.80 | ≥ 0.90 | ratio | §5.1, §5.3.4 |
| **ConflictResolutionScore** | 다중 소스 충돌 해결 품질 | ≥ 0.95 | ≥ 0.97 | ratio | §3.5.3, §5.1 |
| **Reasoning Accuracy** | 관계 기반 추론의 정확도 (Multi-hop 포함) | ≥ 0.85 | ≥ 0.90 | ratio | §4.4.1.3 |
| **CTE (Context Token Efficiency)** | 답변 품질 점수 / 주입된 컨텍스트 토큰 수. LPG/RDF별 토큰 효율성 비교 | — | LPG CTE ≥ RDF CTE | ratio | §5.1.3, §5.4.4.1 |
| **KVCache Cost per Query** | Ablation 실험별 평균 프롬프트 토큰 수 × API 단가 (캐시 미스분 과금) | — | 전월 대비 증가 ≤ 10% | KRW/query | §5.1.3, §5.4.4.1 |
| **Quality-Cost Pareto Score** | 비용-품질 파레토 프론티어 대비 현재 구성의 정규화 효율성 (0~1) | — | ≥ 0.80 | §5.1.3, §5.4.4.1 |

> **📌 CTE/KVCache 지표 안내:** 위 3개 비용 효율성 지표는 Phase 2 고도화 지표이며 MVP에서는 측정하지 않습니다. KGC2026 정이태 발표("Mastering Graph Agents: Unifying LPG & RDF Workflows with Opik for Financial GraphRAG")에서 제시된 인사이트—단순 정확도뿐 아니라 Generation Stage의 KVCache 프롬프트 비용 관점까지 평가해야 한다—를 반영한 것입니다. 상세 메트릭 정의 및 측정 코드는 §5.4.4.1을 참조하세요.

**규칙:** 위 표의 수치가 PRD 내 다른 섹션과 상이한 경우, 본 표의 수치가 우선합니다.
