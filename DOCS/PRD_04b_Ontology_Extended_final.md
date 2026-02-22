# DataNexus PRD – §4.3.5~4.3.8 온톨로지 확장 파이프라인 (Extended)

> 본 섹션은 온톨로지 품질 검증, Entity Resolution, DataHub→Vanna 동기화 파이프라인,
> 품질 향상 효과 측정 등 확장 기능을 다룹니다.
> (외부 데이터 소스 통합, Graphiti 시간 인식 KG는 PRD_04c로 이관되었습니다.)
> 핵심 온톨로지 설계(§4.4~4.5)는 PRD_04a를 참조하세요.

> [!NOTE]
> **구현 코드 포함 안내 (리뷰 보고서 P3):** §4.3.6 Entity Resolution에 Python 클래스 구현 코드가
> 포함되어 있습니다. 향후 리팩토링 시 Implementation Guide로 분리를 권장합니다.

#### 4.3.5 온톨로지 품질 검증 파이프라인
RAG 동기화 전에 온톨로지의 논리적 일관성을 검증하여 환각(Hallucination) 위험을 최소화합니다.

⚠️ DataHub는 동의어 중복 감지 기능을 공식 지원하지 않습니다. 커스텀 Validation 로직으로 구현해야 합니다.

| 검증 유형 | 검증 규칙 | 오류 예시 | 처리 방식 |
| :--- | :--- | :--- | :--- |
| 동의어 중복 | 동일 synonym이 여러 Term에 등록 불가 (커스텀 검증) | "순매출"과 "실매출"이 모두 "Net Sales" 등록 | 경고 + 관리자 확인 요청 |
| 정의 충돌 | 동일 Term에 상이한 definition 존재 시 감지 | A 부서: 순매출=총매출-반품, B 부서: 순매출=총매출-반품-할인 | 동기화 차단 + 조정 요청 |
| 순환 참조 | relatedTerms에서 순환 그래프 감지 | A→B→C→A 관계 형성 | 동기화 차단 + 수정 요구 |
| 고아 참조 | linked_columns가 존재하지 않는 테이블/컬럼 참조 | GRS_DM.DELETED_TABLE.COL 참조 | 경고 + 링크 해제 권고 |
| 필수 필드 누락 | name, definition 미입력 | definition 없이 Term 생성 시도 | 저장 차단 |

#### 4.3.5.1 DataNexus 온톨로지 품질 평가 지표 설계 (제안)
제안드린 **'온톨로지 자체 품질 평가 지표'**는 DataNexus가 단순 용어집을 넘어**'추론 가능한 지식 베이스'**로 기능하기 위해 필수적인 관리 기준입니다.

제공해주신 자료(PRD, 논문, 기술 영상 등)를 종합하여,**구조적(Structural)**, **의미적(Semantic)**, **기능적(Functional)** 세 가지 차원에서 실무에 바로 적용 가능한 구체적인 지표를 설계해 보았습니다.

**1. 구조적 건전성 지표 (Structural Health Metrics)**
그래프 데이터베이스(DozerDB)의 성능과 검색 효율성에 직결되는 물리적 구조를 평가합니다.

| 지표명 | 정의 및 계산식 | 평가 목적 및 관리 기준 |
| :--- | :--- | :--- |
| **고립 노드 비율**<br>(Orphan Node Ratio) | N_orphan / N_total<br>(관계가 0인 노드 수 / 전체 노드 수) | **목적:** 검색 시 연결된 맥락 정보를 전혀 제공하지 못하는 '죽은 지식'을 식별합니다.<br>**기준:** 5% 미만 유지 (PRD 4.3.5의 '고아 참조' 경고와 연계) |
| **슈퍼 노드 지수**<br>(Supernode Index) | 특정 임계값(예: 엣지 1,000개) 이상 연결된 노드의 존재 여부 | **목적:** '매출', '고객' 처럼 너무 많은 노드와 연결된 용어는 검색 시 노이즈(Out-of-Memory)를 유발합니다.<br>**조치:** 슈퍼 노드 탐지 시 하위 개념(예: '순매출', '총매출')으로 분화를 유도해야 합니다. |
| **스키마 깊이**<br>(Ontology Depth) | Root 노드에서 Leaf 노드까지의 평균/최대 깊이 | **목적:** 계층 구조가 너무 얕으면 추론이 단순해지고, 너무 깊으면 탐색 비용이 증가합니다. <br>**기준:** 도메인 복잡도에 따라 다르나, 통상 3~5단계 권장 |

**2. 의미적 충실도 지표 (Semantic Completeness Metrics)**
LLM이 온톨로지를 얼마나 명확하게 이해할 수 있는지를 평가합니다. **'LLM-as-a-Judge'** 방식을 활용할 수 있습니다.

| 지표명 | 정의 및 계산식 | 평가 목적 및 관리 기준 |
| :--- | :--- | :--- |
| **정의 명확성 점수**<br>(Definition Clarity Score) | LLM에게 용어 정의(Definition)만 주고, 해당 용어를 역으로 맞추게 했을 때의 정확도 | **목적:** 사람이 이해하기 모호한 정의는 LLM도 헷갈립니다.<br>**기준:** GPT-4 기준 90점 이상 (PRD의 '정의 충돌' 검증 고도화) |
| **동의어 풍부성**<br>(Synonym Coverage) | 노드당 평균 동의어(Synonyms) 개수 | **목적:** 현업의 다양한 발화(Slang, 약어)를 커버하기 위함입니다.<br>**기준:** 주요 엔티티(Key Entity)는 최소 3개 이상의 동의어 보유 권장 |
| **논리적 일관성**<br>(Logical Consistency) | A → B (IsA), B → C (IsA) 일 때, A → C 가 논리적으로 성립하는지 검증 | **목적:** 추론 과정에서 모순이 발생하지 않도록 보장합니다. (PRD의 '순환 참조' 검증 확장) |

**3. 기능적 효용성 지표 (Functional Utility Metrics)**
RAG 파이프라인에서 온톨로지가 실제로 얼마나 기여하고 있는지를 측정합니다.

| 지표명 | 정의 및 계산식 | 평가 목적 및 관리 기준 |
| :--- | :--- | :--- |
| **온톨로지 커버리지**<br>(OCA, Ontology Coverage) | (사용자 질의 내 식별된 온톨로지 용어 수 / 질의 핵심 키워드 수) | **목적:** 사용자가 자주 묻는 질문을 온톨로지가 얼마나 커버하고 있는지 측정합니다. <br>**기준:** Phase 2 목표 90% 이상 (PRD 5.1 참조) |
| **엔티티 해결 성공률**<br>(Entity Resolution Rate) | 텍스트 내 추출된 엔티티가 온톨로지 URI로 매핑된 비율 | **목적:** ApeRAG가 비정형 텍스트를 지식 그래프로 변환하는 효율을 측정합니다. |
| **쿼리 라우팅 정확도**<br>(Query Router Accuracy) | 온톨로지 정보(정형/비정형 속성)를 기반으로 Router가 적절한 에이전트(Vanna vs ApeRAG)를 선택한 비율 | **목적:** 온톨로지가 질의 분해 및 라우팅의 '신호등' 역할을 제대로 수행하는지 검증합니다. |

---

### 실행을 위한 제언 (Next Steps)

1. **자동화 도구 도입 (Phase 0.5):** 위 지표 중 **'구조적 지표'**는 Neo4j(DozerDB)의 Graph Data Science 라이브러리나 간단한 Cypher 쿼리로 자동 계산할 수 있습니다. **'의미적 지표'**는 구축된 온톨로지(JSON/YAML)를 LLM에게 프롬프트로 입력하여 주기적으로 리포팅하도록 파이프라인을 구성하십시오.
2. **데이터 메쉬와 연동:** DataHub의 'Data Quality' 탭이나 별도 대시보드에 이 지표들을 시각화하여, 현업 데이터 오너가 자신의 온톨로지 품질을 스스로 모니터링하고 개선하도록 유도하십시오. (DataNexus PRD 4.3.5 품질 검증 파이프라인 확장)

이 지표들을 **Admin UI의 '품질 검증 대시보드' (Phase 1)**에 포함시킨다면, 시스템의 신뢰도를 관리자에게 수치로 증명할 수 있는 강력한 기능이 될 것입니다.

---

#### 4.3.5.2 온톨로지 구축 및 유지보수 실무적 관점 (Engineering Reality)
기존 PRD은 Data Mesh 철학을 기반으로 DataHub와 ApeRAG를 연동하는 매우 구체적이고 수준 높은 설계를 담고 있습니다. 하지만 '온톨로지 구축 및 유지보수(Engineering Reality)' 관점에서 몇 가지 보완하면 좋을 핵심적인 사항들을 분석해 드립니다.

**1. 관계(Relationship) 표현력의 한계와 보완** → **PRD_04a 섹션 4.4.1에서 상세 보완**
PRD는 DataHub의 기본 관계인 IsA, HasA, RelatedTo를 주로 활용하고 있습니다. 하지만 복잡한 비즈니스 추론(Multi-hop Inference)을 위해서는 이것만으로는 부족할 수 있습니다.

**2. 스키마 강제성(Schema Enforcement) 전략 부재** → **PRD_04a 섹션 4.4.2에서 상세 보완**
ApeRAG는 텍스트에서 스키마를 발견하는 상향식(Bottom-up) 성격이 강한 반면, DataNexus는 정의된 온톨로지를 주입하는 하향식(Top-down)을 지향합니다. 이 두 방식의 충돌 처리가 명확하지 않습니다.

**3. 변경 관리(Versioning)와 재색인 비용** → **PRD_04a 섹션 4.4.4에서 상세 보완**
PRD의 '향후 검토 사항'에 온톨로지 버전 관리가 포함되어 있으나, 이는 초기부터 고려해야 할 리스크입니다.

**4. 적합성 질문(Competency Questions, CQs) 기반 검증** → **PRD_04a 섹션 4.4.3에서 상세 보완**
PRD는 사후 품질 지표(구조/의미/기능)에 집중하고 있습니다. 하지만 구축 단계에서 **'이 온톨로지가 비즈니스 질문을 해결할 수 있는가?'**를 검증하는 절차가 선행되어야 합니다.

#### 4.3.6 비정형/정형 데이터 온톨로지 통합
문서(ApeRAG)와 DB(Vanna AI)가 동일한 온톨로지를 공유하여 복합 질의를 지원합니다.

#### 4.3.6.1 ApeRAG Entity Resolution 로직
ApeRAG는 문서에서 추출한 엔티티를 DataHub Glossary 용어와 매칭하는 Entity Resolution 과정을 거칩니다.

| 매칭 방식 | 로직 설명 | 예시 |
| :--- | :--- | :--- |
| 1. Exact Match | LLM 출력 엔티티가 Glossary Term name과 정확히 일치 | 문서: "순매출" → URI: urn:li:glossaryTerm:순매출 |
| 2. Synonym Match | 커스텀 synonyms 배열과 대조하여 별칭 일치 확인 | 문서: "Net Sales" → URI: urn:li:glossaryTerm:순매출 |
| 3. Fuzzy Match | 문자열 유사도 기반 검색, 임계값 (0.85) 이상 시 후보 제시 ※ 0-1 스케일 | 문서: "순 매출액" → 후보 제시, 관리자 확인 요청 |
| 4. Context Match | 주변 문맥(domain, related_terms)을 활용한 disambiguation | 문서: "매출" + 문맥:GRS → urn:li:glossaryTerm:GRS 매출 |

※ 출처: ApeRAG Ontology-RAG PRD 문서, SEOCHO Taxonomy Injection 설계

#### 4.3.6.2 문맥 기반 엔티티 정규화(Entity Disambiguation) 고도화 전략

**문제 요약:**

엔티티 정규화는 동일한 객체를 가리키는 다양한 표현을 하나의 식별자로 통합하는 작업입니다. 이것은 데이터 통합과 정확한 분석을 위해 매우 중요하지만, 현실에서는 엔티티 명이 모호하거나 동일 이름이 여러 대상을 가리키는 경우가 많아 복잡한 과제입니다. 특히 문맥(Context) 정보를 활용한 엔티티 식별은 난도가 높습니다 -- 예컨대 "Apple"이라는 단어가 과일인지 기업인지를 문맥으로 파악해야 하는 문제입니다. 잘못 정규화하면 오류 전파나 잘못된 지식 연결이 발생합니다.

**현재 PRD 설계의 한계:**

현재 엔티티 매칭을 비교적 단순한 규칙이나 키워드 기반(Exact Match, Synonym Match, Fuzzy Match)으로 처리하고 있습니다. 이러한 접근은 유지보수 부담도 크고, 새로운 변이나 오타, 문맥의 뉘앙스를 반영하기 어렵습니다. 또한 문맥 기반으로 판단하려는 시도는 기존에 룰 엔진이나 통계적 NLP로 일부 했겠지만, 도메인 지식이 필요하고 예외 케이스가 많아 사용자 수동 태깅에 의존하거나 미해결 상태로 남는 엔티티도 많을 수 있습니다.

**실무적 보완 전략:**

1. **하이브리드 매칭 파이프라인 구축**
   
   정규화 정확도를 높이려면 규칙 기반 + 머신러닝 기반 접근을 결합한 하이브리드 파이프라인이 효과적입니다.

   ```
   ┌─────────────────────────────────────────────────────────────────────┐
   │ 3단계 하이브리드 Entity Resolution Pipeline │
   ├─────────────────────────────────────────────────────────────────────┤
   │ │
   │ [Stage 1: 규칙 기반 전처리] │
   │ ┌──────────────────────────────────────────────────────────────┐ │
   │ │ • 대소문자 정규화 │ │
   │ │ • 특수문자 제거 │ │
   │ │ • 약어 확장 (예: "ML팀" → "머신러닝팀") │ │
   │ │ • 동의어 사전 매칭 │ │
   │ └──────────────────────────────────────────────────────────────┘ │
   │ ▼ │
   │ [Stage 2: 임베딩 기반 후보군 생성] │
   │ ┌──────────────────────────────────────────────────────────────┐ │
   │ │ • 문자열 유사도 (Levenshtein, Jaro-Winkler) │ │
   │ │ • 벡터 임베딩 유사도 (Sentence-BERT) │ │
   │ │ • Top-K 후보 추출 (K=5) │ │
   │ └──────────────────────────────────────────────────────────────┘ │
   │ ▼ │
   │ [Stage 3: 문맥 기반 LLM 랭킹] │
   │ ┌──────────────────────────────────────────────────────────────┐ │
   │ │ • 주변 속성/연결 관계 분석 │ │
   │ │ • LLM 기반 최종 판단 (신뢰도 점수 산출) │ │
   │ │ • 임계값 기반 자동화 (0.90↑: 자동, 0.70-0.90: 검토, 0.70↓: 신규) │ │
   │ └──────────────────────────────────────────────────────────────┘ │
   │ │
   └─────────────────────────────────────────────────────────────────────┘
   ```

   ```python
   class HybridEntityResolver:
       """3단계 하이브리드 엔티티 정규화 파이프라인"""
       
       def __init__(self, glossary_terms: List[GlossaryTerm], llm: LLM):
           self.preprocessor = RuleBasedPreprocessor()
           self.candidate_generator = EmbeddingCandidateGenerator(glossary_terms)
           self.llm_ranker = LLMContextRanker(llm)
           
       def resolve(self, entity: str, context: dict) -> ResolutionResult:
           # Stage 1: 규칙 기반 전처리
           normalized = self.preprocessor.normalize(entity)
           
           # Stage 2: 후보군 생성
           candidates = self.candidate_generator.get_candidates(
               normalized, 
               top_k=5
           )
           
           if not candidates:
               return ResolutionResult(status="NEW_ENTITY", entity=entity)
           
           # 정확 일치 발견 시 즉시 반환
           if candidates[0].similarity >= 0.99:
               return ResolutionResult(
                   status="EXACT_MATCH",
                   matched_uri=candidates[0].uri,
                   confidence=1.0
               )
           
           # Stage 3: 문맥 기반 LLM 랭킹
           ranked = self.llm_ranker.rank_with_context(
               entity=entity,
               candidates=candidates,
               context=context  # 주변 텍스트, 도메인, 관련 엔티티 등
           )
           
           # 임계값 기반 결정 (0.0-1.0 스케일 — §4.3.6.1 ApeRAG 및 PRD_04a SchemaEnforcer와 통일)
           if ranked[0].score >= 0.90:
               return ResolutionResult(
                   status="AUTO_MATCHED",
                   matched_uri=ranked[0].uri,
                   confidence=ranked[0].score
               )
           elif ranked[0].score >= 0.70:
               return ResolutionResult(
                   status="REVIEW_REQUIRED",
                   candidates=ranked[:3],
                   confidence=ranked[0].score
               )
           else:
               return ResolutionResult(status="NEW_ENTITY", entity=entity)
   ```

2. **LLM 도입 및 지식 통합**
   - 최신 대형언어모델을 엔티티 정규화에 활용하면 뛰어난 문맥 이해 능력을 활용할 수 있습니다.
   - 규칙/ML로 애매한 경우 LLM에게 최종 판단을 맡기는 구조를 만듭니다.
   - 사내 지식이 반영된 프롬프트나 사전 정의 룰을 LLM에게 함께 제공하면 일관성 있는 결과를 얻습니다.
   - LLM을 통해 엔티티 설명을 생성하고, 이를 기존 온톨로지 엔티티들의 설명과 비교하여 가장 유사한 것을 찾는 방법도 있습니다.

   ```python
   class LLMContextRanker:
       """문맥 기반 LLM 엔티티 랭킹"""
       
       def rank_with_context(self, entity: str, candidates: List, context: dict) -> List:
           prompt = f"""
           텍스트에서 추출된 엔티티를 온톨로지와 매칭해야 합니다.
           
           추출된 엔티티: "{entity}"
           출현 문맥: "{context.get('surrounding_text', '')}"
           도메인: {context.get('domain', 'Unknown')}
           
           후보 온톨로지 용어:
           {self._format_candidates(candidates)}
           
           각 후보에 대해 0.0-1.0 사이의 매칭 점수와 근거를 제공해주세요.
           문맥을 고려하여 가장 적절한 후보를 선택하세요.
           동일한 단어라도 문맥에 따라 다른 의미일 수 있습니다.
           """
           
           response = self.llm.generate(prompt)
           return self._parse_rankings(response)
   ```

3. **지식 그래프 및 외부 KB 활용**
   - 온톨로지 정규화 성능을 높이기 위해 내부 데이터뿐 아니라 외부 지식베이스(KB)를 활용합니다.
   - 공개된 위키데이터(Wikidata)나 도메인 온톨로지를 참조하여 엔티티를 식별합니다.
   - 명명된 엔터티 링크(NE Linking) 기법 활용: 텍스트에서 인식된 엔터티를 위키피디아 등의 식별자로 연결합니다.
   - 각 객체에 대한 설명 메타데이터를 온톨로지에 저장해두고, 정규화 시 임베딩 비교를 통해 가장 가까운 엔티티를 선택합니다.

4. **임계값 및 인간 검증 설정**
   
   완벽한 자동 정규화는 어려우므로, 신뢰도 임계값을 두고 반자동화하는 것이 현실적입니다.

   | 신뢰도 점수 | 처리 방식 | 설명 |
   | :--- | :--- | :--- |
   | 0.90 이상 | 자동 매핑 | 높은 신뢰도, 즉시 온톨로지에 연결 |
   | 0.70~0.90 | 리뷰 대상 | 후보 1~3순위 제시, 관리자 선택 |
   | 0.70 미만 | 신규 엔티티 취급 | 새로운 용어 등록 또는 수동 매핑 |

   - 검증 작업을 돕기 위해 매칭 후보 리뷰 UI를 만들어, 추천 1~3순위 후보와 신뢰도 점수를 함께 보여주고 클릭 한 번으로 올바른 엔티티를 선택할 수 있게 합니다.
   - 사람이 검증하여 확정한 매핑 결과는 곧바로 온톨로지에 반영하고 해당 사례를 룰/모델에 피드백하여 학습 재훈련 또는 룰 업데이트에 활용합니다.

**참고 사례 및 기술:**

| 기술/도구 | 설명 | 적용 방안 |
| :--- | :--- | :--- |
| **spaCy Entity Linking** | 기본 NER + KB 연결 컴포넌트 | 사용자 정의 KB 구축 후 연동 |
| **Facebook BLINK** | 위키피디아 엔티티 링크 특화 모델 | 문맥 기반 후보 랭킹 참조 |
| **Zero-shot NED** | LLM과 지식그래프 결합, 사전 학습 없이 엔티티 구별 | 신규 도메인 확장 시 활용 |
| **Neo4j GDS** | Node2Vec 임베딩 + KNN으로 유사 노드 탐색 | 그래프 구조 기반 힌트 제공 |
| **Tamr / Informatica MDM** | 유사 레코드 통합 기능 제공 | 상용 MDM 솔루션 참조 |

**Entity Resolution 고도화 지표:**

| 지표명 | 정의 | 목표 기준 |
| :--- | :--- | :--- |
| **Resolution Accuracy** | 올바르게 매핑된 엔티티 비율 | 92% 이상 |
| **Auto-Resolution Rate** | 자동으로 처리된 엔티티 비율 | 75% 이상 |
| **Disambiguation Success** | 동음이의어 문맥 구분 성공률 | 85% 이상 |
| **False Merge Rate** | 다른 엔티티를 잘못 병합한 비율 | 2% 미만 |

#### 4.3.7 DataHub → Vanna AI 동기화 파이프라인
DataHub의 메타데이터와 온톨로지를 Vanna AI RAG Store에 학습시키는 핵심 로직입니다.

**동기화 대상 데이터 유형:**

| 유형 | DataHub 소스 | Vanna Training 방식 | 품질 영향 |
| :--- | :--- | :--- | :--- |
| DDL | schemaMetadata aspect | vn.train(ddl="CREATE TABLE...") | Schema Linking ↑ |
| Documentation | Glossary Terms | vn.train(documentation="비즈니스 정의...") | 비즈니스 용어 이해 ↑ |
| Sample SQL | Query Log / 수동 등록 | vn.train(question="...", sql="...") | 유사 질문 정확도 ↑ |
| 컬럼 설명 | fieldDescription aspect | vn.train(documentation="컬럼명: 설명") | 컬럼 선택 정확도 ↑ |

**Glossary Term → Documentation 변환 예시:**

```txt
비즈니스 용어: 순매출 (Net Sales)
정의: 총매출에서 반품, 할인, 에누리를 차감한 실제 매출액
계산식: 순매출 = 총매출(GROSS_SALES_AMT) - 반품(RETURN_AMT) - 할인(DISCOUNT_AMT) - 에누리(ALLOWANCE_AMT)
동의어: 실매출, 넷세일즈, Net Sales
관련 테이블: GRS_DM.MART_SALES
관련 컬럼: NET_SALES_AMT (순매출금액)
```

**동기화 트리거 방식:**

| 트리거 유형 | 발생 시점 | 동기화 범위 |
| :--- | :--- | :--- |
| 수동 (Manual) | 관리자가 '동기화' 버튼 클릭 | 선택된 테이블 또는 전체 |
| 스케줄 (Scheduled) | 설정된 Cron 주기 (예: 매일 02:00) | 변경된 항목만 (Incremental) |
| 이벤트 (Event-driven) | DataHub Glossary Term 생성/수정 시 | 해당 Term 및 연결된 테이블만 |

#### 4.3.8 온톨로지 적용 시 품질 향상 효과

**시나리오별 개선 효과**

| 시나리오 | 온톨로지 미적용 | 온톨로지 적용 | 개선 |
| :--- | :--- | :--- | :--- |
| "순매출 알려줘" | TOTAL_SALES 선택 (오류) | NET_SALES_AMT 정확 선택 | Schema Linking ↑ |
| "VIP 고객 매출" | VIP 정의 불명확 → 오류 | "VIP = 연매출 1억 이상" 적용 | 비즈니스 로직 ↑ |
| "재구매율 추이" | 계산식 추측 실패 | 정의된 공식 적용 | 복합 지표 ↑ |
| "매출액" vs "세일즈" | 별개 개념으로 인식 | 동의어로 동일 처리 | 자연어 이해 ↑ |
| "GRS 월별 실적" | 어느 테이블인지 불명확 | MART_SALES 자동 매핑 | 테이블 선택 ↑ |

**정량적 기대 효과 (추정)**

| 평가 지표 | 온톨로지 미적용 | 온톨로지 적용 | 개선율 |
| :--- | :--- | :--- | :--- |
| EX (Execution Accuracy) | 60-70% | 80-85% | +15-20%p |
| 비즈니스 용어 매핑 정확도 | 40-50% | 85-90% | +40-45%p |
| 복합 지표 계산 정확도 | 30-40% | 70-80% | +35-45%p |
| 동의어/유사 표현 인식률 | 50-60% | 90-95% | +35-40%p |

---


---

> **📌 Phase 2+/3 내용 분리 안내**
>
> 아래 섹션들은 PRD_04c_Ontology_Future_final.md로 이관되었습니다:
> - §4.3.9 외부 데이터 소스 기반 온톨로지 지식그래프 자동 구축 파이프라인 (Phase 2+)
> - §4.3.10 Graphiti 기반 시간 인식 지식그래프 및 에이전트 메모리 계층 (Phase 3 R&D)
> - §4.3.10.10 세션 내 컨텍스트 보존 전략 (Phase 2~3)
>
> 자세한 내용은 [PRD_04c_Ontology_Future_final.md](./PRD_04c_Ontology_Future_final.md)를 참조하세요.
