> **📋 오버엔지니어링 주의 (리뷰 보고서 §3-4):**
> 4단계 품질 게이트(Unit → Integration → CQ → E2E) 중 MVP에서는 **Stage 1(Unit) + Stage 4(E2E)만 필수** 적용합니다. 상세는 §5.3 참조.

## 5. 평가 및 품질 관리 (Evaluation Strategy)

### 5.1 주요 지표 (Metrics)

> **Phase 범례:** **1** = MVP 필수, 1→2 = MVP에서 도입 후 Phase 2에서 목표 상향, 1.5 = Phase 1 안정화, 2 = Phase 2 고도화, 3 = Phase 3 R&D.
>
> **📊 SSOT 미러링 (정식 출처: PRD_04a §4.8)**
> - **단위 표기:** 모든 비율 지표는 ratio(0~1) 형식. 예: 0.05 = 5%
> - 수치가 상이한 경우 **§4.8 기준이 우선**합니다.

#### 5.1.1 Phase 1 MVP 필수 지표 (10개)

| 지표 | 설명 | MVP 기준 | Phase 2 목표 | Phase |
| :--- | :--- | :--- | :--- | :---: |
| **EX (Execution Accuracy)** | 실행 결과값의 일치 여부 | ≥ 0.80 (ratio) | ≥ 0.90 | **1 → 2** |
| **VES (Valid Efficiency Score)** | 생성된 쿼리의 실행 효율성 | P95 < 3초 | — | **1** |
| **VPA (Validation Pass Rate)** | 품질 검증 통과율 | ≥ 0.95 (ratio) | — | **1** |
| **CQ Pass Rate** | 적합성 질문 검증 통과율 | ≥ 0.80 (ratio) | ≥ 0.95 | **1 → 2** |
| **Schema Compliance** | 스키마 강제성 준수율 (ACCEPT+REMAP) | ≥ 0.90 (ratio) | ≥ 0.95 | **1 → 2** |
| **Deterministic Query Rate** | 템플릿 기반 결정론적 질의 비율 | ≥ 0.60 (ratio) | — | **1** |
| **Query Router Accuracy** | Query Router 정확도 | ≥ 0.95 (ratio) | ≥ 0.97 | **1 → 2** |
| **Tool Guard Activation Rate** | 도구 결과 가드 발동 빈도 (낮을수록 양호) | < 0.05 (ratio) | — | **1** |
| **Hallucination Rate** | 근거 없는 정보가 응답에 포함된 비율 (낮을수록 양호) | ≤ 0.05 (ratio) | ≤ 0.03 | **1 → 2** |
| **ConflictResolutionScore** | 다중 소스 충돌 해결 품질 | ≥ 0.95 (ratio) | ≥ 0.97 | **1 → 2** |
| **Reasoning Accuracy** | 관계 기반 추론의 정확도 | ≥ 0.85 (ratio) | ≥ 0.90 | **1 → 2** |

#### 5.1.2 Phase 1.5 안정화 지표 (4개)

| 지표 | 설명 | 목표 | Phase |
| :--- | :--- | :--- | :---: |
| QVT (Query Variance Testing) | 질문 표현 변화에 대한 일관성 검증 | 일관성 90% 이상 | 1.5 |
| Incremental Update Ratio | 증분 업데이트 처리 비율 | 90% 이상 | 1.5 |
| SKOS Mapping Coverage | SKOS 표준 매핑 완료율 | 95% 이상 | 1.5 |
| Draft Acceptance Rate | LLM 초안 승인율 (수정 없이) | 50% 이상 | 1.5 |

#### 5.1.3 Phase 2 고도화 지표 (8개)

| 지표 | 설명 | 목표 | Phase |
| :--- | :--- | :--- | :---: |
| OCA (Ontology Coverage) | 온톨로지 정의 용어에 대한 정확도 | 90% 이상 | 2 |
| External KG Mapping Rate | 외부 데이터 엔터티의 Glossary 매핑률 | 50% 이상 | 2 |
| ToolsRetriever Routing Accuracy | Agentic Retriever 자동 선택 정확도 | 90% 이상 | 2 |
| Context Preservation Rate | 컴팩션 후 핵심 사실 보존율 (§4.3.10.10) | 90% 이상 | 2 |
| Cache Hit Rate | LLM 프리픽스 캐시 활용률 (Implementation Strategy §22) | 70% 이상 | 2 |
| **CTE (Context Token Efficiency)** | 답변 품질 점수 / 주입된 컨텍스트 토큰 수 (§5.4.4.1) | LPG ≥ RDF (동일 품질 대비) | 2 |
| **KVCache Cost per Query** | Ablation 실험별 평균 프롬프트 토큰 수 × API 단가 (§5.4.4.1) | 전월 대비 감소 추세 | 2 |
| **Quality-Cost Pareto Score** | 비용-품질 파레토 최적점 대비 현재 구성의 효율성 (§5.4.4.1) | 0.8 이상 (1.0 = 파레토 최적) | 2 |

> **📌 CTE/KVCache Cost 운영 가이드 (KGC2026 정이태 발표 인사이트 반영):**
> LPG와 RDF는 Generation Stage에서 Agent에게 제공하는 컨텍스트의 토큰 효율성이 다릅니다. LPG는 구조화된 Cypher 결과로 compact한 반면, RDF 트리플은 verbose할 수 있어 동일 정보량 대비 토큰 소비가 상이합니다. 단순 '정확도'만이 아닌 KVCache 실무 관점의 비용 효율성까지 평가해야 최적 아키텍처 결정이 가능합니다.
> - **측정 방법:** Opik Trace에서 각 Agent 호출 시 `prompt_tokens`, `completion_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`를 수집하여 실험별 집계
> - **비교 기준:** A1(LPG Only) vs A2(RDF Only) vs A4(LPG+RDF) 간 CTE 비교로 각 그래프 모델의 토큰 효율성 정량화
> - **상세:** §5.4.4.1 Context Token Efficiency 메트릭 정의 참조

> **📌 Cache Hit Rate 운영 가이드 (Claude Code 팀 교훈 적용):**
> Claude Code 팀은 캐시 히트율을 가동률(uptime)처럼 모니터링하며, 저하 시 SEV를 선언합니다. DataNexus도 동일 수준을 적용합니다.
> - **≥ 80%**: 정상 운영 | **70~80%**: 경고 + Opik 알림 | **60~70%**: SEV-3 즉시 원인 조사 | **< 60%**: SEV-2 긴급 패치
> - **주요 캐시 미스 원인:** 도구 정의 순서 변경, 세션 중 모델 전환, 시스템 프롬프트 내 동적 값(타임스탬프 등), 컴팩션 시 별도 프리픽스 사용
> - **측정 방법:** Anthropic API 응답의 `cache_creation_input_tokens` vs `cache_read_input_tokens` 비율로 계산
> - **상세:** Implementation Strategy §22.6, PRD_04c §4.3.10.10.3.1 참조

#### 5.1.4 Phase 3 R&D 지표 (12개)

| 지표 | 설명 | 목표 | Phase |
| :--- | :--- | :--- | :---: |
| Cross-Source Query Rate | 내부+외부 통합 검색 활용 질의 비율 | 30% 이상 | 3 |
| Agent Memory Recall@10 | Graphiti 검색으로 관련 과거 사실 회수율 | 85% 이상 | 3 |
| Temporal Query Accuracy | 시간 기반 질의 (과거 시점) 정확도 | 90% 이상 | 3 |
| Episode Ingestion Latency | 에피소드 수집→그래프 반영 지연 시간 | 5초 이내 (실시간) | 3 |
| Personalization Hit Rate | 개인화 컨텍스트가 응답에 반영된 비율 | 70% 이상 | 3 |
| Fact Conflict Detection Rate | 사실 충돌 자동 탐지율 | 95% 이상 | 3 |
| Community Coherence Score | 자동 탐지된 커뮤니티의 의미적 일관성 | 0.8 이상 | 3 |
| Memory Flush Success Rate | Graphiti 에피소드 커밋 성공률 | 99% 이상 | 3 |
| Compaction Overhead | 컴팩션으로 인한 추가 지연 시간 | 3초 이내 | 3 |
| Dual Memory Dedup Rate | Vanna↔Graphiti 간 중복 저장 방지율 (§4.3.10.10.8) | 95% 이상 | 3 |
| Vanna-Graphiti Cross Match | Vanna SQL 테이블명 ↔ Graphiti 엔터티 교차 매칭율 | 80% 이상 | 3 |
| Memory Router Accuracy | DualMemoryRouter 저장 대상 분류 정확도 | 90% 이상 | 3 |

> **📌 Phase 3 지표 운영 안내:** 위 12개 지표는 Phase 3 R&D 범위이며, Graphiti/에이전트 메모리 도입 시 측정을 시작합니다. MVP 시점에서는 §5.1.1(Phase 1 필수 10개)에 집중하세요.

#### 5.1.5 alive-analysis 메트릭 4단계 분류 매핑 (Phase 1.5+)

> **📌 alive-analysis 연계:** alive-analysis의 4단계 메트릭 분류 체계(North Star → Leading → Guardrail → Diagnostic)를 DataNexus 평가 지표에 매핑합니다. 이 분류는 사용자가 분석 워크플로우 내에서 메트릭을 계층적으로 이해하고 모니터링하기 위한 운영 레이어이며, §4.8 SSOT 지표의 정의 자체를 변경하지 않습니다.
> - **상세:** PRD_02 §3.11.4, Implementation Strategy §23.4 참조

| alive-analysis 계층 | 역할 | DataNexus 대응 지표 | 모니터링 주기 | 에스컬레이션 |
|---------------------|------|-------------------|-------------|------------|
| **North Star** | 최종 사용자 가치 대리 | EX (Execution Accuracy) | Daily | 하락 추세 3일 연속 → Leading 자동 드릴다운 |
| **Leading** | 품질 선행 지표 | Query Router Accuracy, CQ Pass Rate, Schema Compliance | Per deployment | 기준 미달 → Diagnostic 세부 분석 트리거 |
| **Guardrail** | 안전 한계선 (절대 위반 불가) | Hallucination Rate ≤ 0.05 (ratio), Cache Hit Rate ≥ 0.70 (ratio) | Continuous | 2회 연속 위반 → 자동 알림 + Opik 하이라이트 |
| **Diagnostic** | 원인 분석용 세부 | CTE, KVCache Cost, VES, Deterministic Query Rate | Weekly | 이상 감지 → 근본 원인 분석 (ALIVE 루프 Investigation) |

### 5.2 오류 분석 (Error Taxonomy)
- Schema Linking 실패
- JOIN 오류
- Nested Query 오류
- 집계 함수(Aggregation) 오류
- 온톨로지 미매핑 오류
- Entity Resolution 오류: 문서 엔티티와 Glossary Term 매칭 실패
- **관계 모호성 오류:** 세분화되지 않은 관계로 인한 Multi-hop 추론 실패
- **스키마 불일치 오류:** 비표준 엔티티 추출로 인한 그래프 오염
- **라우팅 오류:** 질의 유형 오분류로 인한 부적절한 처리
- **표준 매핑 오류:** SKOS 변환 시 정보 손실
- **초안 품질 오류:** LLM 생성 초안의 부정확한 정의/관계
- **이중 메모리 불일치 오류:** Vanna Tool Memory의 SQL 쌍이 참조하는 테이블/컬럼이 Graphiti 엔터티와 불일치하여 발생하는 맥락 단절 (§4.3.10.10.8.4)

---

### 5.3 테스트 전략 및 검증 체계

DataNexus의 품질 보증을 위해 **4단계 검증 프레임워크**를 적용합니다. 정식 운영에서는 각 단계가 이전 단계의 통과를 전제로 하며, 품질 게이트(Quality Gate)를 통과해야 다음 단계로 진행합니다.

> **📌 MVP 예외:** Phase 1 MVP에서는 **Stage 1(Unit) + Stage 4(E2E)만 필수** 적용합니다. Stage 2(Integration)와 Stage 3(CQ Validation)는 Stage 1→4 직행이 가능하며, Phase 1.5 이후 순차 도입합니다.

테스트 순서: **'단위 기능(Logic) → 데이터 무결성(Data) → 논리적 적합성(CQ) → 전체 성능(E2E)'**

```txt
┌─────────────────────────────────────────────────────────────────────────────┐
│ DataNexus 4단계 테스트 프레임워크 │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ [Stage 1: Unit Testing] 핵심 로직 검증 │
│ ──────────────────────────────────────────────────────────────────────── │
│ • Query Router Agent 분기 로직 │
│ • Schema Enforcer 검증 로직 │
│ • Impact Analyzer 영향 분석 │
│ • 목표: 개별 모듈 정확도 95% 이상 │
│ ▼ │
│ [Stage 2: Integration Testing] 데이터 무결성 검증 │
│ ──────────────────────────────────────────────────────────────────────── │
│ • SKOS Import/Export 호환성 │
│ • DataHub ↔ Vanna 동기화 │
│ • DozerDB 멀티테넌시 격리 │
│ • 목표: 파이프라인 무결성 100% │
│ ▼ │
│ [Stage 3: CQ Validation] 논리적 적합성 검증 │
│ ──────────────────────────────────────────────────────────────────────── │
│ • 적합성 질문(Competency Questions) 시뮬레이션 │
│ • 온톨로지 경로 탐색 가능성 │
│ • 비즈니스 질의 답변 가능성 │
│ • 목표: Critical CQ 100%, 전체 CQ 80%+ │
│ ▼ │
│ [Stage 4: E2E Evaluation] 전체 성능 평가 │
│ ──────────────────────────────────────────────────────────────────────── │
│ • NL2SQL 정확도 (EX) │
│ • 응답 시간 (VES) │
│ • 온톨로지 커버리지 (OCA) [Phase 2] │
│ • 목표: EX 80%+ (MVP) / 90%+ (Phase 2), P95 < 3초 │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 5.3.1 Stage 1: 단위 테스트 (Unit Testing)

개별 모듈이 의도대로 작동하는지 `pytest` 기반으로 검증합니다.

##### 5.3.1.1 Query Router Agent 테스트

**목적:** 질의 유형에 따른 라우팅 분기가 정확한지 검증 (PRD 목표: 정확도 95% 이상)

| 테스트 케이스 | 입력 예시 | 예상 라우팅 | 검증 기준 |
| :--- | :--- | :--- | :--- |
| 결정론적 질의 (Deterministic) | "A의 하위 조직은?" | Cypher 템플릿 | 템플릿 ID 정확 매칭 |
| 확률론적 질의 (Probabilistic) | "경쟁사 대비 강점은?" | LLM Fallback | LLM 호출 확인 |
| 계층 탐색 질의 | "매출의 상위 개념들" | HIERARCHY_ANCESTORS | 신뢰도 1.0 |
| 집계 질의 | "부서별 매출 합계" | AGGREGATION_BY_GROUP | 쿼리 실행 성공 |

```python
# tests/unit/test_query_router.py
class TestQueryRouter:
    """Query Router Agent 단위 테스트"""

    def test_deterministic_routing_hierarchy(self):
        """계층 질의 → Cypher 템플릿 라우팅"""
        query = "A의 하위 조직은?"
        result = router.classify(query)

        assert result.route == "CYPHER_TEMPLATE"
        assert result.template_id == "HIERARCHY_DESCENDANTS"
        assert result.confidence == 1.0  # 결정론적 = 100%

    def test_probabilistic_routing_analysis(self):
        """분석 질의 → LLM Fallback"""
        query = "경쟁사 대비 우리 회사의 강점을 분석해줘"
        result = router.classify(query)

        assert result.route == "LLM_FALLBACK"
        assert result.confidence >= 0.7

    def test_template_execution_accuracy(self):
        """Cypher 템플릿 실행 정확도"""
        template_result = router.execute_template(
            template_id="TRANSITIVE_CLOSURE",
            params={"start_node": "urn:li:glossaryTerm:매출"}
        )

        assert template_result.execution_success
        assert len(template_result.results) > 0
```

**품질 게이트:** Router 분류 정확도 ≥ 95%

##### 5.3.1.2 Schema Enforcer 테스트

**목적:** 비표준 용어 감지 및 처리 로직이 정확한지 검증

| 테스트 케이스 | 입력 트리플 | 예상 상태 | 예상 액션 |
| :--- | :--- | :--- | :--- |
| 정확 일치 | (순매출, CalculatedFrom, 총매출) | ACCEPT | STORE |
| 동의어 매핑 | (Net Sales, IsA, 매출) | REMAP | STORE (정규화) |
| 유사 매칭 | (순매출액, IsA, 매출) | REVIEW | QUEUE (검토) |
| 미등록 용어 | (Revenue, IsA, 매출) | REJECT | DISCARD |

```python
# tests/unit/test_schema_enforcer.py
class TestSchemaEnforcer:
    """Schema Enforcer 단위 테스트"""

    def test_exact_match_accept(self):
        """정확히 일치하는 표준 용어 → ACCEPT"""
        triple = Triple(subject="순매출", predicate="CalculatedFrom", object="총매출")
        result = enforcer.validate_triple(triple)

        assert result.subject_status == "ACCEPT"
        assert result.action == "STORE"

    def test_synonym_remap(self):
        """동의어 → REMAP 후 정규화 저장"""
        triple = Triple(subject="Net Sales", predicate="IsA", object="매출")
        result = enforcer.validate_triple(triple)

        assert result.subject_status == "REMAP"
        assert result.subject_uri == "urn:li:glossaryTerm:순매출"

    def test_fuzzy_match_review(self):
        """유사도 0.85 이상 → REVIEW 큐로 전송"""
        triple = Triple(subject="순매출액", predicate="IsA", object="매출")
        result = enforcer.validate_triple(triple)

        assert result.subject_status == "REVIEW"
        assert result.similarity_score >= 0.85

    def test_unknown_term_reject(self):
        """미등록 용어 → REJECT"""
        triple = Triple(subject="Revenue", predicate="IsA", object="매출")
        result = enforcer.validate_triple(triple)

        assert result.subject_status == "REJECT"
        assert result.action == "DISCARD"
```

**품질 게이트:** Schema Compliance Rate ≥ 90%, False Rejection Rate < 2%

##### 5.3.1.3 Impact Analyzer 테스트

**목적:** 온톨로지 변경 시 영향 범위 분석이 정확한지 검증

```python
# tests/unit/test_impact_analyzer.py
class TestImpactAnalyzer:
    """Impact Analyzer 단위 테스트"""

    def test_term_add_minimal_impact(self):
        """Term 추가 → 최소 영향 (증분 업데이트)"""
        event = ChangeEvent(entity_urn="urn:li:glossaryTerm:신규용어", change_type="CREATE")
        report = analyzer.analyze_change_impact(event)

        assert report.impact_score < 0.1
        assert report.recommended_strategy == "INCREMENTAL"

    def test_hierarchy_change_subtree_impact(self):
        """계층 구조 변경 → 서브트리 전체 영향"""
        event = ChangeEvent(entity_urn="urn:li:glossaryTerm:매출", change_type="HIERARCHY_CHANGE")
        report = analyzer.analyze_change_impact(event)

        assert len(report.affected_nodes) > 10
        assert report.recommended_strategy in ["PARTIAL_REBUILD", "FULL_REBUILD"]

    def test_cost_saving_verification(self):
        """증분 업데이트 비용 절감 검증 (목표: 70% 이상)"""
        full_cost = analyzer.estimate_full_reindex_cost()
        incremental_cost = analyzer.estimate_incremental_cost(event)

        assert incremental_cost < full_cost * 0.3
```

#### 5.3.2 Stage 2: 통합 테스트 (Integration Testing)

데이터가 흐르는 파이프라인의 연결 상태와 무결성을 검증합니다.

##### 5.3.2.1 SKOS 호환성 테스트

**목적:** SKOS 표준 Import/Export 시 정보 손실이 없는지 검증

| 테스트 시나리오 | 검증 항목 | 성공 기준 |
| :--- | :--- | :--- |
| DataHub → SKOS Export | 계층 구조 보존 | broader/narrower 관계 100% 유지 |
| SKOS → DataHub Import | 외부 온톨로지 통합 | SHACL 검증 통과 |
| Round-trip 테스트 | Export → Import → 비교 | 노드/엣지 수 동일 |

```python
# tests/integration/test_skos_compatibility.py
class TestSKOSCompatibility:
    """SKOS 표준 호환성 통합 테스트"""

    def test_datahub_to_skos_export(self):
        """DataHub Glossary → RDF/SKOS Export"""
        exporter = SKOSExporter(datahub_client)
        rdf_graph = exporter.export(glossary_urn="urn:li:glossaryNode:GRS영업")

        # SHACL 스키마 검증
        validation_result = shacl_validator.validate(rdf_graph)
        assert validation_result.conforms

    def test_external_ontology_import(self):
        """외부 SKOS 온톨로지 Import (예: Protégé에서 작성한 파일)"""
        importer = ExternalOntologyImporter()
        result = importer.import_skos(source="fibo_corporate.ttl", target_glossary="urn:li:glossaryNode:재무")

        assert result.imported_terms > 0
        assert len(result.conflicts) == 0

    def test_roundtrip_integrity(self):
        """Round-trip (Export → Import) 무결성"""
        original = datahub_client.get_glossary("urn:li:glossaryNode:테스트")
        rdf_export = exporter.export(original)
        imported = importer.import_from_rdf(rdf_export)

        assert original.term_count == imported.term_count
```

**품질 게이트:** SKOS Mapping Coverage ≥ 95%

##### 5.3.2.2 동기화(Sync) 파이프라인 테스트

**목적:** DataHub 변경 시 Vanna AI RAG Store 자동 동기화 검증

```python
# tests/integration/test_sync_pipeline.py
class TestSyncPipeline:
    """DataHub ↔ Vanna 동기화 통합 테스트"""

    def test_glossary_change_triggers_sync(self):
        """Glossary 변경 → Vanna 재학습 트리거"""
        datahub_client.update_term(
            urn="urn:li:glossaryTerm:순매출",
            definition="총매출에서 반품, 할인, 에누리를 차감한 금액 (변경됨)"
        )

        event = webhook_listener.wait_for_event(timeout=30)
        assert event.change_type == "UPDATE"

        sync_job = sync_pipeline.get_latest_job()
        assert sync_job.status == "COMPLETED"
```

##### 5.3.2.3 DozerDB 멀티테넌시 테스트

**목적:** 그룹사별 데이터 격리가 완벽한지 검증

```python
# tests/integration/test_multitenancy.py
class TestMultitenancy:
    """DozerDB 멀티테넌시 격리 테스트"""

    def test_cross_database_isolation(self):
        """크로스 DB 쿼리 불가 확인"""
        with pytest.raises(PermissionError):
            dozerdb.execute(database="group_a_db", query="MATCH (n) WHERE n.tenant = 'group_b' RETURN n")

    def test_tenant_data_isolation(self):
        """테넌트별 데이터 완전 분리 확인"""
        dozerdb.execute("group_a_db", "CREATE (:Product {name: 'A제품'})")
        dozerdb.execute("group_b_db", "CREATE (:Product {name: 'A제품'})")

        result_a = dozerdb.execute("group_a_db", "MATCH (p:Product) RETURN count(p)")
        result_b = dozerdb.execute("group_b_db", "MATCH (p:Product) RETURN count(p)")

        assert result_a == 1
        assert result_b == 1
```

**품질 게이트:** 파이프라인 무결성 100%, 테넌트 격리 100%

#### 5.3.3 Stage 3: 적합성 질문 검증 (CQ Validation)

기존 PRD의 핵심인 **Competency Questions**를 사용하여 온톨로지가 비즈니스 질의를 처리할 수 있는지 평가합니다.

##### 5.3.3.1 CQ 시뮬레이션 테스트

**목적:** 정의된 CQ에 대해 온톨로지가 답변 가능한지 검증

| CQ 유형 | 예시 질문 | 검증 항목 |
| :--- | :--- | :--- |
| Foundational (FCQ) | "고객 유형을 구분하는 개념이 정의되어 있는가?" | 개념 존재 확인 |
| Relationship (RCQ) | "A 공장 이슈가 B 제품 공급망에 미친 영향은?" | 경로 탐색 가능성 |
| Validating (VCQ) | "순매출은 총매출에서 무엇을 차감한 값인가?" | 정의 정확성 |
| Metaproperty (MpCQ) | "VIP 고객의 정의 조건은 무엇인가?" | 메타 속성 완전성 |

```python
# tests/cq/test_competency_questions.py
class TestCompetencyQuestions:
    """적합성 질문(CQ) 검증 테스트"""

    def test_foundational_cq_concept_existence(self):
        """FCQ: 핵심 개념 존재 확인"""
        cq = CompetencyQuestion(
            cq_id="CQ-FCQ-001",
            question="고객 유형을 구분하는 개념이 정의되어 있는가?",
            required_concepts=["고객", "VIP고객", "일반고객", "신규고객"]
        )

        result = cq_validator.validate(cq)
        assert result.concept_coverage == 1.0
        assert result.status == "PASS"

    def test_relationship_cq_path_traversal(self):
        """RCQ: 관계 경로 탐색 가능성"""
        cq = CompetencyQuestion(
            cq_id="CQ-RCQ-001",
            question="A 공장 이슈가 B 제품 공급망에 미친 영향은?",
            required_relationships=[
                {"subject": "Factory", "predicate": "Impacts", "object": "SupplyChain"},
                {"subject": "SupplyChain", "predicate": "Affects", "object": "Product"}
            ]
        )

        result = cq_validator.validate(cq)
        assert result.relationship_coverage == 1.0

        path = graph_db.find_path(start="urn:li:glossaryTerm:A공장", end="urn:li:glossaryTerm:B제품")
        assert path is not None

    def test_critical_cq_must_pass(self):
        """Critical CQ는 100% 통과 필수"""
        critical_cqs = cq_repository.get_by_priority("Critical")

        for cq in critical_cqs:
            result = cq_validator.validate(cq)
            assert result.status == "PASS", f"Critical CQ 실패: {cq.cq_id}"
```

##### 5.3.3.2 쿼리 생성 시뮬레이션

**목적:** CQ로부터 실제 SQL/Cypher 쿼리가 생성 가능한지 검증

```python
# tests/cq/test_query_generation.py
class TestCQQueryGeneration:
    """CQ 기반 쿼리 생성 시뮬레이션"""

    def test_cq_to_sql_generation(self):
        """자연어 CQ → SQL 변환 성공 여부"""
        cq = CompetencyQuestion(question="지난 달 VIP 고객의 순매출 합계는 얼마인가?")
        generated_sql = vanna_client.generate_sql(cq.question)

        assert sql_validator.is_valid(generated_sql)
        assert "SUM" in generated_sql.upper()

    def test_cq_pass_rate_threshold(self):
        """전체 CQ Pass Rate 검증"""
        all_cqs = cq_repository.get_all()
        results = [cq_validator.validate(cq) for cq in all_cqs]

        pass_rate = sum(1 for r in results if r.status == "PASS") / len(results)
        assert pass_rate >= 0.80, f"CQ Pass Rate {pass_rate:.1%} < 80%"
```

**품질 게이트:** Critical CQ 100% 통과, 전체 CQ Pass Rate ≥ 80%

#### 5.3.4 Stage 4: End-to-End 성능 평가 (E2E Evaluation)

실제 사용자 경험 관점에서 RAG의 품질을 정량화합니다.

##### 5.3.4.1 NL2SQL 정확도 측정

**목적:** NL2SQL360 벤치마크 기준 정확도 평가

| 지표 | 설명 | 목표 |
| :--- | :--- | :--- |
| EX (Execution Accuracy) | 생성된 SQL이 실제 DB에서 올바른 값을 반환하는지 측정 | MVP ≥ 80% / Phase 2 ≥ 90% |
| EM (Exact Match) | 생성 쿼리 완전 일치 | ≥ 70% |
| VES (Valid Efficiency Score) | 쿼리 실행 효율성 | P95 < 3초 |

```python
# tests/e2e/test_nl2sql_accuracy.py
class TestNL2SQLAccuracy:
    """NL2SQL E2E 정확도 테스트"""

    def test_execution_accuracy(self):
        """EX: 실행 결과값 일치율"""
        benchmark = NL2SQLBenchmark(test_set="datanexus_test_queries.json")
        results = benchmark.run(vanna_client)

        # MVP 기준: §5.3 Stage 4 품질 게이트 EX ≥ 80% (0.80)
        assert results.execution_accuracy >= 0.80
        assert results.exact_match_accuracy >= 0.70

    def test_query_efficiency(self):
        """VES: 쿼리 응답 시간"""
        test_queries = load_test_queries()
        response_times = []

        for query in test_queries:
            start = time.time()
            result = vanna_client.generate_and_execute(query)
            response_times.append(time.time() - start)

        p95 = np.percentile(response_times, 95)
        assert p95 < 3.0, f"P95 응답시간 {p95:.2f}초 > 3초"
```

##### 5.3.4.2 온톨로지 커버리지(OCA) 측정

**목적:** 사용자 질의의 핵심 용어가 온톨로지와 잘 매핑되는지 평가

```python
# tests/e2e/test_ontology_coverage.py
# [Phase 2] OCA 측정 — MVP에서는 이 테스트를 skip 또는 warning으로 처리
# 또는 @pytest.mark.phase2 데코레이터 사용
class TestOntologyCoverage:
    """온톨로지 커버리지 E2E 테스트"""

    def test_entity_resolution_accuracy(self):
        """OCA: 엔티티 매핑 정확도"""
        test_queries = [
            ("지난달 순매출", ["순매출", "기간"]),
            ("VIP 고객의 주문 현황", ["VIP고객", "주문"]),
            ("A공장 생산량", ["A공장", "생산량"])
        ]

        total_entities = 0
        matched_entities = 0

        for query, expected_entities in test_queries:
            for entity in expected_entities:
                total_entities += 1
                if entity_resolver.resolve(entity) is not None:
                    matched_entities += 1

        oca = matched_entities / total_entities
        assert oca >= 0.90, f"OCA {oca:.1%} < 90%"
```

#### 5.3.5 테스트 자동화 파이프라인

CI/CD 파이프라인에 통합하여 매 배포 전 품질 게이트를 자동 검증합니다.

```yaml
# .github/workflows/test_pipeline.yml
name: DataNexus Quality Gate

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Unit Tests
        run: pytest tests/unit/ -v --cov=datanexus --cov-fail-under=90
      - name: Check Router Accuracy
        run: python -m datanexus.router benchmark --threshold 0.95

 integration-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    services:
      dozerdb:
        image: dozerdb/dozerdb:latest
      qdrant:
        image: qdrant/qdrant:latest
    steps:
      - name: Run Integration Tests
        run: pytest tests/integration/ -v
      - name: Verify SKOS Compatibility
        run: python -m datanexus.skos validate --coverage-threshold 0.95

 cq-validation:
    needs: integration-tests
    steps:
      - name: Run CQ Validation
        run: |
          python -m datanexus.cq validate \
            --config competency_questions.yaml \
            --critical-threshold 1.0 \
            --overall-threshold 0.80

 e2e-evaluation:
    needs: cq-validation
    steps:
      - name: Run E2E Benchmark
        run: |
          python -m datanexus.benchmark run \
            --test-set production_queries.json \
            --ex-threshold 0.80 \
            --p95-threshold 3.0
```

#### 5.3.6 테스트 품질 게이트 요약

| 단계 | 품질 게이트 | 통과 기준 | 실패 시 조치 |
| :--- | :--- | :--- | :--- |
| **Stage 1** | Router Accuracy | ≥ 95% | 템플릿 추가/분류기 재학습 |
| **Stage 1** | Schema Compliance | ≥ 90% | 동의어 사전 확장 |
| **Stage 2** | SKOS Coverage | ≥ 95% | 매핑 테이블 보완 |
| **Stage 2** | Sync Integrity | 100% | 파이프라인 디버깅 |
| **Stage 3** | Critical CQ Pass | 100% | 온톨로지 보완 필수 |
| **Stage 3** | Overall CQ Pass | ≥ 80% (Phase 1) | 온톨로지 확장 검토 |
| **Stage 4** | EX Accuracy | MVP ≥ 80% / Phase 2 ≥ 90% | Few-shot 예제 추가 |
| **Stage 4** | P95 Response | < 3초 | 인덱스/캐시 최적화 |

### 5.4 Multi-Agent 평가 프레임워크 (SEOCHO)

SEOCHO 프로젝트의 `feature-kgbuild` 브랜치에서 구현된 체계적인 GraphRAG 평가 프레임워크입니다.

#### 5.4.1 평가 아키텍처 개요

```txt
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SEOCHO Evaluation Framework                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Macro Experiments (M1~M4)                        │   │
│  │            시스템 레벨 비교 - 전체 파이프라인 성능 평가              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Ablation Study (A1~A6)                           │   │
│  │           컴포넌트 레벨 분석 - 개별 모듈 기여도 측정                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Metrics Collection                               │   │
│  │  AnswerRelevance | Hallucination | RoutingAccuracy | ContextPrecision│   │
│  │                  ConflictResolutionScore                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Opik Integration                                 │   │
│  │              Trace Export | Dataset Management | Dashboard           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 5.4.2 Macro Experiments (시스템 레벨 비교)

전체 시스템 구성별 성능을 비교하여 최적의 아키텍처를 검증합니다.

| 실험 ID | 구성 요소 | 목적 | 예상 결과 |
|---------|----------|------|----------|
| **M1** | LPG + RDF + HYBRID + Manager | Full System 성능 측정 | Baseline (최고 성능) |
| **M2** | LPG + RDF + HYBRID + Single Agent | Manager Agent 효과 검증 | M1 대비 -5~10% |
| **M3** | LPG + HYBRID (no RDF) | 온톨로지/RDF 기여도 측정 | M1 대비 -10~15% |
| **M4** | RDF + HYBRID (no LPG) | 구조화된 LPG 기여도 측정 | M1 대비 -15~20% |

```python
# evaluation/experiments/macro_experiments.py
class MacroExperiments:
    """시스템 레벨 Macro 실험 정의"""
    
    EXPERIMENTS = {
        "M1": {
            "name": "Full System with Manager",
            "components": ["lpg", "rdf", "hybrid"],
            "agent_type": "hierarchical",
            "description": "모든 검색 방식 + 계층적 에이전트"
        },
        "M2": {
            "name": "Full System Single Agent",
            "components": ["lpg", "rdf", "hybrid"],
            "agent_type": "single",
            "description": "모든 검색 방식 + 단일 에이전트"
        },
        "M3": {
            "name": "LPG + Hybrid (No Ontology)",
            "components": ["lpg", "hybrid"],
            "agent_type": "hierarchical",
            "description": "RDF/온톨로지 제외"
        },
        "M4": {
            "name": "RDF + Hybrid (No LPG)",
            "components": ["rdf", "hybrid"],
            "agent_type": "hierarchical",
            "description": "LPG 구조화 데이터 제외"
        }
    }
    
    def run_experiment(self, experiment_id: str, dataset: str) -> ExperimentResult:
        config = self.EXPERIMENTS[experiment_id]
        agent = self._create_agent(config)
        results = self._evaluate(agent, dataset)
        return ExperimentResult(
            experiment_id=experiment_id,
            metrics=results,
            config=config
        )
```

#### 5.4.3 Ablation Study (컴포넌트 레벨 분석)

개별 검색 방식의 기여도를 측정하여 최적 조합을 도출합니다.

> **📌 Ablation Study 해석 한계 및 교호작용 분석:**
> 기존 기여도 분석(`A4 - A2 = LPG 기여도`)은 주효과(main effect)만 추정한다. 두 컴포넌트가 함께 작동할 때 발생하는 시너지 또는 간섭(교호작용, interaction effect)은 별도 분석이 필요하다.
>
> **교호작용 계산식:** `Interaction(A×B) = AB조합 - A단독 - B단독 + Baseline`
>
> | 교호작용 | 계산 | 양수일 때 의미 | 음수일 때 의미 |
> | :--- | :--- | :--- | :--- |
> | LPG × RDF | A4 - A1 - A2 + A3 | LPG+RDF 시너지 → 하이브리드 정당화 | LPG+RDF 간섭 → 중복 정보로 혼란 |
> | LPG × HYBRID | A5 - A1 - A3 + A3 | 구조화+벡터 보완 효과 | 구조화 결과가 벡터 결과와 충돌 |
> | RDF × HYBRID | A6 - A2 - A3 + A3 | 시맨틱+벡터 보완 효과 | verbose 컨텍스트 중복 |
>
> **해석 기준:** |값| > 0.05이면 실질적 교호작용으로 판단. 이 임계값은 Phase 2 반복 실험에서 통계적으로 재설정한다.
>
> **통계적 한계:** 현재 설계는 반복 없는 단일 실행(unreplicated 2^k factorial)이다. 교호작용 값의 방향성(시너지/간섭)은 판단할 수 있으나, p-value 기반 유의성 주장은 불가하다. Phase 2에서 실험별 최소 3회 반복을 도입하여 ANOVA 기반 유의성 검정을 추가할 계획이다.

| 실험 ID | 구성 | 분석 목적 |
|---------|------|----------|
| **A1** | LPG Only | LPG 단독 성능 |
| **A2** | RDF Only | RDF 단독 성능 |
| **A3** | HYBRID Only | 벡터 검색 단독 성능 |
| **A4** | LPG + RDF | 그래프 조합 성능 |
| **A5** | LPG + HYBRID | LPG + 벡터 조합 |
| **A6** | RDF + HYBRID | RDF + 벡터 조합 |

```python
# evaluation/experiments/ablation_study.py
class AblationStudy:
    """컴포넌트 레벨 Ablation 실험"""
    
    COMBINATIONS = {
        "A1": ["lpg"],
        "A2": ["rdf"],
        "A3": ["hybrid"],
        "A4": ["lpg", "rdf"],
        "A5": ["lpg", "hybrid"],
        "A6": ["rdf", "hybrid"]
    }
    
    def run_ablation(self, dataset: str) -> Dict[str, AblationResult]:
        results = {}
        for ablation_id, components in self.COMBINATIONS.items():
            agent = self._create_ablated_agent(components)
            metrics = self._evaluate(agent, dataset)
            results[ablation_id] = AblationResult(
                ablation_id=ablation_id,
                components=components,
                metrics=metrics
            )
        return results
    
    def analyze_contributions(self, results: Dict) -> ContributionAnalysis:
        """각 컴포넌트의 주효과(main effect) 기여도 분석
        
        ⚠️ 해석 한계 (아래 analyze_interaction_effects 참조):
        이 방법은 각 컴포넌트의 단독 기여도(주효과)만 추정한다.
        LPG와 RDF가 함께 있을 때 발생하는 시너지(교호작용 효과)는
        이 계산에 포함되지 않는다. 따라서 아래 결과를 "LPG가 X%p를
        기여한다"고 단정하면 안 되며, "RDF가 고정된 조건에서 LPG를
        추가하면 약 X%p 변화가 관찰된다" 수준으로 해석해야 한다.
        """
        # A4 - A2 = LPG 기여도 (RDF 고정)
        # A4 - A1 = RDF 기여도 (LPG 고정)
        # etc.
        return ContributionAnalysis(
            lpg_contribution=results["A4"].score - results["A2"].score,
            rdf_contribution=results["A4"].score - results["A1"].score,
            hybrid_contribution=results["A5"].score - results["A1"].score
        )
    
    def analyze_interaction_effects(self, results: Dict) -> InteractionAnalysis:
        """컴포넌트 간 교호작용(interaction effect) 분석
        
        2-factor 실험 설계에서 교호작용은 두 요인의 조합 효과가
        각 요인의 주효과 합과 다른 정도를 측정한다.
        
        교호작용 = AB_조합 - A_단독 - B_단독 + Baseline
        
        양수: 시너지 (함께 쓰면 개별 합보다 좋다)
        음수: 간섭 (함께 쓰면 개별 합보다 나쁘다)
        0 근처: 독립 (서로 영향 없이 합산됨)
        
        예) LPG×RDF 교호작용이 양수이면, "LPG+RDF 하이브리드가
            15~20% 좋다"는 주장이 단순 합산이 아닌 시너지 효과로
            뒷받침된다.
        """
        # Baseline: 아무 그래프 검색 없이 벡터만 사용한 경우
        baseline = results["A3"].score
        
        # --- LPG × RDF 교호작용 ---
        # A4(LPG+RDF) - A1(LPG) - A2(RDF) + A3(Baseline)
        lpg_rdf_interaction = (
            results["A4"].score
            - results["A1"].score
            - results["A2"].score
            + baseline
        )
        
        # --- LPG × HYBRID 교호작용 ---
        # A5(LPG+HYBRID) - A1(LPG) - A3(HYBRID) + Baseline_none
        # Baseline_none이 없으므로 A3을 공유 Baseline으로 사용
        lpg_hybrid_interaction = (
            results["A5"].score
            - results["A1"].score
            - results["A3"].score
            + baseline
        )
        
        # --- RDF × HYBRID 교호작용 ---
        rdf_hybrid_interaction = (
            results["A6"].score
            - results["A2"].score
            - results["A3"].score
            + baseline
        )
        
        # --- 3-way 교호작용 (M1 Full System 필요) ---
        # Full(M1) - A4 - A5 - A6 + A1 + A2 + A3
        # ※ M1은 Macro 실험이라 agent_type이 다를 수 있음 → 주의
        three_way = None  # M1 결과가 있을 때만 계산
        
        return InteractionAnalysis(
            lpg_rdf=InteractionEffect(
                name="LPG × RDF",
                value=lpg_rdf_interaction,
                interpretation=self._interpret(lpg_rdf_interaction)
            ),
            lpg_hybrid=InteractionEffect(
                name="LPG × HYBRID",
                value=lpg_hybrid_interaction,
                interpretation=self._interpret(lpg_hybrid_interaction)
            ),
            rdf_hybrid=InteractionEffect(
                name="RDF × HYBRID",
                value=rdf_hybrid_interaction,
                interpretation=self._interpret(rdf_hybrid_interaction)
            ),
            three_way=three_way,
            methodology_note=(
                "교호작용 분석은 2^k Factorial Design의 간소화 버전이다. "
                "엄밀한 통계적 유의성 검정을 위해서는 동일 실험을 최소 "
                "3회 반복(replicate)하여 분산을 추정해야 한다. 현재 설계는 "
                "반복 없는 단일 실행(unreplicated)이므로, 교호작용 값은 "
                "방향성 판단 용도로만 활용하고 p-value 기반 유의성 주장은 "
                "하지 않는다. Phase 2에서 반복 실험을 도입하여 통계적 "
                "검정력을 확보할 계획이다."
            )
        )
    
    @staticmethod
    def _interpret(interaction_value: float) -> str:
        """교호작용 값의 실무적 해석"""
        if interaction_value > 0.05:
            return "SYNERGY: 조합 효과가 개별 합보다 크다 — 하이브리드 정당화"
        elif interaction_value < -0.05:
            return "INTERFERENCE: 조합 시 오히려 성능 저하 — 원인 분석 필요"
        else:
            return "INDEPENDENT: 컴포넌트가 독립적으로 기여 — 단순 합산 모델 적합"
    
    def analyze_cost_efficiency(self, results: Dict) -> CostEfficiencyAnalysis:
        """KVCache 비용 효율성 분석 (KGC2026 인사이트 반영)
        
        LPG/RDF 각 검색 방식이 Generation Stage에 주입하는
        컨텍스트의 토큰 비용 대비 답변 품질 효율성을 비교합니다.
        """
        cost_efficiency = {}
        for ablation_id, result in results.items():
            # Context Token Efficiency = 품질 점수 / 프롬프트 토큰 수
            cte = result.score / result.prompt_tokens if result.prompt_tokens > 0 else 0
            # KVCache Cost = 프롬프트 토큰 × API 단가 (캐시 미스분만 과금)
            kvcache_cost = (
                result.cache_creation_tokens * self.PRICE_PER_CREATION_TOKEN
                + result.cache_read_tokens * self.PRICE_PER_READ_TOKEN
                + result.uncached_tokens * self.PRICE_PER_INPUT_TOKEN
            )
            cost_efficiency[ablation_id] = CostEfficiencyResult(
                ablation_id=ablation_id,
                context_token_efficiency=cte,
                kvcache_cost_per_query=kvcache_cost,
                avg_prompt_tokens=result.prompt_tokens,
                avg_context_tokens=result.context_tokens,
                quality_score=result.score
            )
        
        # Quality-Cost Pareto Frontier 계산
        pareto_front = self._compute_pareto_frontier(cost_efficiency)
        
        return CostEfficiencyAnalysis(
            per_experiment=cost_efficiency,
            pareto_frontier=pareto_front,
            lpg_vs_rdf_cte_ratio=(
                cost_efficiency["A1"].context_token_efficiency
                / cost_efficiency["A2"].context_token_efficiency
                if cost_efficiency["A2"].context_token_efficiency > 0 else float('inf')
            ),
            optimal_combination=pareto_front[0].ablation_id  # 파레토 최적점
        )
```

#### 5.4.4 신규 평가 메트릭

기존 NL2SQL 평가 지표에 Multi-Agent 시스템 특화 메트릭을 추가합니다.

| 메트릭 | 유형 | 설명 | 측정 방법 | 목표 기준 |
|--------|------|------|----------|----------|
| **AnswerRelevance** | LLM | 응답이 질의에 적절한지 | LLM-as-a-Judge | ≥ 4.0/5.0 |
| **Hallucination** | LLM | 환각/허구 정보 포함 여부 | LLM 기반 팩트체크 | ≤ 5% |
| **RoutingAccuracy** | Custom | 올바른 도구/에이전트 선택률 | Ground Truth 비교 | ≥ 95% |
| **ContextPrecision** | Custom | 검색된 컨텍스트 품질 | Relevance 점수 | ≥ 0.85 |
| **ConflictResolutionScore** | Custom | Hierarchy of Truth 준수율 | 충돌 해결 정확도 | ≥ 95% |
| **ContextTokenEfficiency** | Cost | 토큰 대비 답변 품질 효율 (§5.4.4.1) | Score / prompt_tokens | LPG ≥ RDF |
| **KVCacheCostPerQuery** | Cost | 쿼리당 KVCache 비용 (§5.4.4.1) | Opik 토큰 추적 | 전월 대비 감소 |
| **QualityCostParetoScore** | Cost | 비용-품질 파레토 효율성 (§5.4.4.1) | 파레토 프론티어 거리 | ≥ 0.8 |

```python
# evaluation/metrics/custom_metrics.py
class RoutingAccuracyMetric:
    """에이전트 라우팅 정확도 측정"""
    
    def evaluate(self, traces: List[AgentTrace], ground_truth: List[str]) -> float:
        correct = 0
        total = len(traces)
        
        for trace, expected in zip(traces, ground_truth):
            selected_agent = trace.router_decision.selected_agent
            if selected_agent == expected:
                correct += 1
                
        return correct / total if total > 0 else 0.0


class ConflictResolutionScoreMetric:
    """Hierarchy of Truth 준수율 측정"""
    
    def evaluate(self, supervisor_results: List[SupervisorResult]) -> float:
        compliant = 0
        total_conflicts = 0
        
        for result in supervisor_results:
            if result.conflicts_detected > 0:
                total_conflicts += result.conflicts_detected
                if result.resolution_method == "hierarchy_of_truth":
                    # 우선순위 규칙 준수 여부 확인
                    if self._verify_hierarchy_compliance(result):
                        compliant += result.conflicts_detected
                        
        return compliant / total_conflicts if total_conflicts > 0 else 1.0
    
    def _verify_hierarchy_compliance(self, result: SupervisorResult) -> bool:
        """Hierarchy of Truth 우선순위 검증"""
        for resolution in result.resolutions:
            winner = resolution.selected_source
            losers = resolution.rejected_sources
            winner_priority = self.HIERARCHY[winner.type]
            
            for loser in losers:
                if self.HIERARCHY[loser.type] > winner_priority:
                    return False  # 낮은 우선순위가 선택됨
        return True


class HallucinationMetric:
    """환각 탐지 메트릭 (LLM-as-a-Judge)"""
    
    def evaluate(self, responses: List[str], contexts: List[str]) -> float:
        hallucination_count = 0
        
        for response, context in zip(responses, contexts):
            prompt = f"""
            다음 응답이 주어진 컨텍스트에서 지원되지 않는 정보를 포함하는지 평가하세요.
            
            컨텍스트: {context}
            응답: {response}
            
            환각 여부 (YES/NO):
            """
            
            result = self.llm.generate(prompt)
            if "YES" in result.upper():
                hallucination_count += 1
                
        return hallucination_count / len(responses) if responses else 0.0
```

##### 5.4.4.1 Context Token Efficiency 메트릭 (KGC2026 인사이트 반영)

> **📌 출처:** 정이태, "Mastering Graph Agents: Unifying LPG & RDF Workflows with Opik for Financial GraphRAG" (KGC2026 발표)
> **핵심 인사이트:** LPG와 RDF가 잘하는 것이 따로 있으며, '잘한다'의 기준은 단순 정확도뿐 아니라 Generation Stage에서 Agent에게 제공하는 프롬프트 비용(KVCache) 실무 관점까지 포함해야 한다.

LPG와 RDF는 동일한 비즈니스 질의에 대해 서로 다른 형태의 컨텍스트를 생성합니다. LPG는 Cypher 쿼리 결과로 구조화된 compact한 응답을 반환하는 반면, RDF 트리플은 시맨틱 추론에 강하지만 verbose한 컨텍스트를 생성할 수 있습니다. 이 차이는 API 비용과 KVCache 효율성에 직접적 영향을 미칩니다.

**메트릭 정의:**

| 메트릭 | 계산식 | 측정 단위 | 비교 기준 |
| :--- | :--- | :--- | :--- |
| **CTE (Context Token Efficiency)** | AnswerRelevance Score / context_tokens | 점수/토큰 | A1 vs A2 vs A4 간 비교 |
| **KVCache Cost per Query** | (cache_creation × $rate₁) + (cache_read × $rate₂) + (uncached × $rate₃) | USD/query | 실험별 절대 비용 비교 |
| **Quality-Cost Pareto Score** | 파레토 프론티어까지의 정규화 거리 (0~1) | 무차원 | 1.0 = 파레토 최적 |

**측정 파이프라인:**

```python
# evaluation/metrics/cost_efficiency_metrics.py
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class CostEfficiencyResult:
    ablation_id: str
    context_token_efficiency: float  # CTE = score / context_tokens
    kvcache_cost_per_query: float    # USD per query
    avg_prompt_tokens: int
    avg_context_tokens: int          # LPG/RDF 컨텍스트 토큰만 분리 측정
    quality_score: float

class ContextTokenEfficiencyMetric:
    """LPG/RDF 컨텍스트의 토큰 효율성 측정
    
    KGC2026 발표에서 제시된 KVCache 실무 관점을 DataNexus
    Ablation 실험에 적용합니다.
    """
    
    # Anthropic Claude API 요금 기준 (2026.02 기준)
    PRICE_PER_INPUT_TOKEN = 0.000003      # $3/MTok (uncached)
    PRICE_PER_CREATION_TOKEN = 0.00000375  # $3.75/MTok (cache write)
    PRICE_PER_READ_TOKEN = 0.0000003      # $0.30/MTok (cache read)
    
    def evaluate(self, traces: List[AgentTrace]) -> Dict[str, CostEfficiencyResult]:
        """Ablation 실험별 비용 효율성 평가"""
        results = {}
        
        for trace in traces:
            # Opik Trace에서 토큰 사용량 추출
            token_usage = self._extract_token_usage(trace)
            
            # CTE 계산: 품질 점수 / 컨텍스트 토큰 수
            cte = (
                trace.answer_relevance_score / token_usage.context_tokens
                if token_usage.context_tokens > 0 else 0
            )
            
            # KVCache 비용 계산
            kvcache_cost = (
                token_usage.cache_creation_tokens * self.PRICE_PER_CREATION_TOKEN
                + token_usage.cache_read_tokens * self.PRICE_PER_READ_TOKEN
                + token_usage.uncached_tokens * self.PRICE_PER_INPUT_TOKEN
            )
            
            results[trace.experiment_id] = CostEfficiencyResult(
                ablation_id=trace.experiment_id,
                context_token_efficiency=cte,
                kvcache_cost_per_query=kvcache_cost,
                avg_prompt_tokens=token_usage.total_prompt_tokens,
                avg_context_tokens=token_usage.context_tokens,
                quality_score=trace.answer_relevance_score
            )
        
        return results
    
    def _extract_token_usage(self, trace: AgentTrace) -> TokenUsage:
        """Opik Trace에서 LPG/RDF별 컨텍스트 토큰 분리 추출
        
        Agent별 tool_call 결과의 토큰 수를 분리 측정:
        - Graph Agent (LPG): Cypher 결과 토큰
        - Graph Agent (RDF): SPARQL/Triple 결과 토큰
        - Vector Agent: 벡터 검색 결과 토큰
        """
        context_tokens = 0
        for step in trace.steps:
            if step.agent_type in ["graph_lpg", "graph_rdf", "vector"]:
                context_tokens += step.output_tokens
        
        return TokenUsage(
            total_prompt_tokens=trace.total_prompt_tokens,
            context_tokens=context_tokens,
            cache_creation_tokens=trace.cache_creation_input_tokens,
            cache_read_tokens=trace.cache_read_input_tokens,
            uncached_tokens=trace.total_prompt_tokens - trace.cache_read_input_tokens
        )
    
    def compute_pareto_frontier(
        self, results: Dict[str, CostEfficiencyResult]
    ) -> List[CostEfficiencyResult]:
        """비용-품질 파레토 프론티어 계산
        
        X축: KVCache Cost (낮을수록 좋음)
        Y축: Quality Score (높을수록 좋음)
        파레토 최적: 비용을 더 줄이면 품질이 떨어지는 지점
        """
        points = sorted(results.values(), key=lambda r: r.kvcache_cost_per_query)
        frontier = []
        max_quality = -1
        
        for point in points:
            if point.quality_score > max_quality:
                frontier.append(point)
                max_quality = point.quality_score
        
        return frontier
```

**Ablation 실험별 기대 비용-품질 프로파일:**

| 실험 ID | 구성 | 예상 컨텍스트 특성 | CTE 가설 |
|---------|------|------------------|----------|
| **A1** | LPG Only | Compact (Cypher 결과: 테이블/JSON) | 높음 (적은 토큰으로 구조화된 답변) |
| **A2** | RDF Only | Verbose (Triple 열거, 추론 체인) | 낮음 (시맨틱 풍부하나 토큰 다량 소비) |
| **A3** | HYBRID Only | 중간 (청크 기반 문서 검색) | 중간 |
| **A4** | LPG + RDF | 복합 (구조 + 시맨틱 병합) | A1, A2의 가중 평균 부근 |
| **A5** | LPG + HYBRID | LPG compact + 문서 보강 | A1보다 낮으나 품질 상승 |
| **A6** | RDF + HYBRID | RDF verbose + 문서 중복 가능 | 최저 CTE 위험 (토큰 최다) |

**Opik 대시보드 확장:**

| 패널 | 시각화 | 용도 |
|------|--------|------|
| **CTE Comparison** | A1~A6 막대 그래프 (CTE 값) | LPG vs RDF 토큰 효율성 즉시 비교 |
| **Cost-Quality Scatter** | X: KVCache Cost, Y: Quality Score | 파레토 프론티어 시각화 |
| **Token Breakdown** | Stacked Bar (LPG/RDF/Vector 컨텍스트) | 실험별 토큰 구성 분석 |
| **Cost Trend** | 시계열 라인차트 (일/주별) | KVCache 비용 추이 모니터링 |

#### 5.4.5 Opik 연동 (LLM Observability)

Opik(Comet ML)과 연동하여 실험 결과를 추적하고 관리합니다.

```python
# evaluation/integrations/opik_integration.py
from opik import Opik

class OpikEvaluationTracker:
    """Opik 기반 실험 추적"""
    
    def __init__(self, project_name: str = "datanexus-eval"):
        self.opik = Opik(project_name=project_name)
        self.cost_metric = ContextTokenEfficiencyMetric()  # §5.4.4.1
        
    def log_experiment(self, experiment: ExperimentResult):
        """실험 결과 로깅 (품질 + 비용 메트릭 통합)"""
        self.opik.log({
            "experiment_id": experiment.experiment_id,
            "metrics": experiment.metrics.to_dict(),
            "cost_metrics": {
                "context_token_efficiency": experiment.cost_metrics.cte,
                "kvcache_cost_per_query": experiment.cost_metrics.kvcache_cost,
                "avg_context_tokens": experiment.cost_metrics.avg_context_tokens,
                "quality_cost_pareto_score": experiment.cost_metrics.pareto_score,
            } if experiment.cost_metrics else {},
            "config": experiment.config,
            "timestamp": experiment.timestamp
        })
        
    def export_traces(self, trace_ids: List[str], output_path: str):
        """트레이스 Export"""
        traces = self.opik.get_traces(trace_ids)
        with open(output_path, "w") as f:
            json.dump(traces, f, indent=2)
            
    def create_dataset(self, name: str, queries: List[str], ground_truths: List[str]):
        """평가 데이터셋 생성"""
        dataset = self.opik.create_dataset(
            name=name,
            data=[
                {"query": q, "ground_truth": gt}
                for q, gt in zip(queries, ground_truths)
            ]
        )
        return dataset.id
```

**Opik 대시보드 활용:**

| 기능 | 설명 | 용도 |
|------|------|------|
| **Trace Viewer** | 에이전트 실행 체인 시각화 | 디버깅, 병목 분석 |
| **Metrics Dashboard** | 실험별 메트릭 비교 차트 | 성능 추이 모니터링 |
| **Dataset Manager** | 평가 데이터셋 버전 관리 | 재현 가능한 평가 |
| **A/B Comparison** | 실험 간 직접 비교 | 아키텍처 결정 |
| **Cost-Quality Analysis** | CTE/KVCache 비용-품질 파레토 차트 (§5.4.4.1) | LPG vs RDF 토큰 효율성 비교 |

#### 5.4.6 평가 품질 게이트 (SEOCHO 확장)

| 단계 | 품질 게이트 | 통과 기준 | 실패 시 조치 |
| :--- | :--- | :--- | :--- |
| **Macro** | M1 vs M2 차이 | ≤ 10% | Manager 로직 검토 |
| **Macro** | M1 vs M3 차이 | ≥ 10% | 온톨로지 기여도 검증 완료 |
| **Ablation** | A4 > A1 + A2 | Synergy 확인 (교호작용 > 0.05) | 조합 효과 검증 — `analyze_interaction_effects()` 참조 |
| **Metrics** | RoutingAccuracy | ≥ 95% | Router 분류기 재학습 |
| **Metrics** | ConflictResolutionScore | ≥ 95% | Hierarchy 로직 검토 |
| **Metrics** | Hallucination Rate | ≤ 0.05 (ratio) | 컨텍스트 품질 개선 |
| **Cost** | CTE (A1 vs A2 비교) | LPG CTE ≥ RDF CTE | RDF 컨텍스트 압축 전략 검토 |
| **Cost** | KVCache Cost 추이 | 전월 대비 증가 ≤ 10% | 프롬프트 최적화 + 캐시 인식 프루닝 강화 |
| **Cost** | Quality-Cost Pareto Score | ≥ 0.8 | 비용 대비 품질 저하 구성 제거 검토 |

---

> **📌 메뉴 구조 참조:** 사용자 메뉴(§6.6) 및 관리자 메뉴(§6.7)는 [PRD_06_Requirements_Roadmap_final.md](PRD_06_Requirements_Roadmap_final.md)를 참조하세요.

---

### 5.5 에러 처리 및 Fallback 전략

> **⚠️ 에러 처리 구체화 미흡 (리뷰 보고서 §1-4)**

기존 §5.2의 Error Taxonomy는 분류만 있고 대응 전략이 부재합니다. 아래에 에러 유형별 구체적 처리 흐름을 정의합니다.

#### 5.5.1 NL2SQL 에러 처리 흐름

```txt
[SQL 생성 실패]
    ├─→ Syntax Error → Vanna 재시도 (max 2회, 다른 프롬프트)
    │       └─→ 재시도 실패 → "질문을 다시 표현해주세요" + 유사 질문 제안
    ├─→ Schema Linking 실패 → DataHub에서 유사 테이블/컬럼 검색
    │       └─→ 후보 발견 → "혹시 [후보]를 말씀하시나요?" 확인 질문
    │       └─→ 후보 없음 → "해당 데이터를 찾을 수 없습니다" + 카탈로그 검색 안내
    ├─→ Execution Timeout (>30초) → 쿼리 취소 + 집계 범위 축소 제안
    └─→ Permission Denied → "접근 권한이 없는 데이터입니다" + 권한 요청 안내
```

#### 5.5.2 RAG 검색 에러 처리 흐름

```txt
[문서 검색 실패]
    ├─→ Empty Results → 검색어 확장 (동의어 기반) 재시도
    │       └─→ 재시도 실패 → "관련 문서를 찾을 수 없습니다" + 검색 키워드 제안
    ├─→ Low Relevance (score < 0.6) → 결과 제공 + "관련도가 낮을 수 있습니다" 경고
    └─→ ApeRAG 서비스 장애 → NL2SQL만으로 부분 응답 + "문서 검색 일시 중단" 알림
```

#### 5.5.3 Agent 간 통신 에러 처리

| 에러 유형 | 감지 방법 | Fallback 전략 | 사용자 안내 |
|----------|----------|--------------|-----------|
| Graph Agent 타임아웃 | 30초 초과 | Vector Agent 결과만으로 응답 | "그래프 검색이 지연되어 문서 기반으로 답변합니다" |
| Supervisor 충돌 해결 실패 | ConflictResolutionScore < 0.5 | 가장 높은 우선순위 소스만 사용 | "복수 소스 간 정보가 상이하여 가장 신뢰도 높은 결과를 제공합니다" |
| 전체 Agent 장애 | 모든 Agent 응답 없음 | 기본 LLM 응답 (컨텍스트 없이) | "시스템 일시 장애로 일반적인 답변만 가능합니다" |

---

### 5.6 성능 벤치마크 기준

> **⚠️ 성능 벤치마크 구체화 미흡 (리뷰 보고서 §1-5)**

| 지표 | 측정 방법 | MVP 기준 | Phase 2 기준 | 측정 도구 |
|------|----------|---------|-------------|----------|
| **응답 시작 시간** | 첫 SSE 이벤트까지 | ≤ 2초 | ≤ 1초 | Opik Trace |
| **전체 응답 시간 (P95)** | 마지막 SSE 이벤트까지 | ≤ 5초 | ≤ 3초 | Opik Trace |
| **SQL 생성 시간** | Vanna generate_sql 호출 시간 | ≤ 3초 | ≤ 2초 | Vanna Metrics |
| **그래프 쿼리 시간** | Cypher 실행 시간 | ≤ 2초 | ≤ 1초 | Neo4j Metrics |
| **RAG 검색 시간** | ApeRAG API 응답 시간 | ≤ 2초 | ≤ 1.5초 | ApeRAG Metrics |
| **동시 사용자** | 성능 저하 없는 최대 동시 접속 | 50명 | 200명 | k6/Locust |
| **메모리 사용량** | Agent 서비스 컨테이너 기준 | ≤ 4GB | ≤ 8GB | Prometheus |

#### 5.6.1 NL2SQL Baseline 정확도 컨텍스트 (외부 벤치마크)

> **📌 배경:** DataNexus의 EX(Execution Accuracy) 목표(MVP ≥ 80%, Phase 2 ≥ 90%)가 현실적인지 판단하려면 업계 baseline을 이해해야 한다. Snowflake가 공개한 내부 벤치마크 결과와 Vanna AI 커뮤니티 실측값을 종합하여 아래 표로 정리한다.

| 조건 | 정확도 | 출처 |
|------|--------|------|
| GPT-4o 단독 (RAG 없음, 스키마만 제공) | ~51% | Snowflake 내부 벤치마크 (Cortex Analyst Behind the Scenes) |
| RAG 기반 Text-to-SQL (Q-SQL 쌍 + DDL + 문서) | ~70-75% | MITB For All (2025.06), Vanna AI 실측 |
| Snowflake Cortex Analyst (Semantic View + RAG + Multi-Agent) | ~85-90% (추정) | Snowflake 공식 블로그 |
| **DataNexus 목표 (온톨로지 + RAG + Multi-Agent)** | **≥ 80% (MVP) / ≥ 90% (Phase 2)** | **본 PRD** |

**시사점:**
- LLM 단독으로는 51%에 불과하므로, RAG 없는 NL2SQL은 프로덕션 불가. DataNexus가 Vanna RAG를 채택한 핵심 근거임
- Vanna RAG 적용만으로 20%p 이상 개선 가능하며, DataNexus의 온톨로지 컨텍스트 주입(§4.3)은 추가 10-15%p 향상 예상
- MVP 80% 목표는 RAG + 온톨로지 조합 시 달성 가능한 현실적 수준
- Phase 2 목표 90%는 Tool Memory 자동 학습(§3.10) + Few-shot 확대(§4.2.4) + 온톨로지 고도화 전제

**Ablation 실험 연계:**
- 실험 A1(온톨로지 제거)에서 정확도 하락폭이 15-20%p면, 온톨로지 기여도가 입증됨
- RAG 단독 baseline(~70%)과 비교하여 온톨로지 추가 효과를 정량 측정
- 경쟁 솔루션 정확도 비교는 [부록 B.8.5](./PRD_Appendix_AB_final.md) 참조

> **📌 참고:** Training 데이터 포맷 및 관리 전략은 [PRD_03 §4.2.4](./PRD_03_Data_Pipeline_final.md) 참조

---

### 5.7 외부 RAG 벤치마킹 전략 (AutoRAG-Research)

> **오버엔지니어링 주의 (리뷰 보고서 §3-4 연장):**
> AutoRAG-Research 프레임워크의 직접 통합(설치, 플러그인 개발, PostgreSQL+VectorChord 스택 추가)은 Phase 1 MVP 범위에서 **명시적으로 제외**합니다. MVP 파이프라인이 안정화되지 않은 상태에서 외부 벤치마크를 돌려도 의미 있는 비교가 불가능하며, 커스텀 플러그인 개발 공수가 핵심 기능 개발을 저해합니다.

**참조:** https://github.com/NomaDamas/AutoRAG-Research (Apache-2.0, v0.0.2)

#### 5.7.1 Phase 1 (MVP): 설계 참고 자료 활용

AutoRAG-Research가 구현한 SOTA 파이프라인의 아키텍처와 논문 레퍼런스를 SEOCHO 설계 시 참고합니다. 별도 설치나 통합 없이 코드 리딩과 논문 참조 수준으로만 활용합니다.

| AutoRAG-Research 파이프라인 | 참고 논문 | SEOCHO 설계 시사점 |
|---------------------------|----------|-------------------|
| MAIN-RAG (Multi-Agent Filtering) | ACL 2025 | Router + Supervisor 패턴의 필터링 전략 비교. SEOCHO의 Hierarchy of Truth 충돌 해결과 MAIN-RAG의 다중 에이전트 필터링 접근법 간 차이점 분석 |
| IRCoT (Interleaving Retrieval with CoT) | ACL 2023 | Multi-hop Inference 설계 시 검색-추론 인터리빙 패턴 참고. SEOCHO의 Graph + SQL 결합 쿼리에 CoT 기반 중간 검색 단계 적용 가능성 검토 |
| ET2RAG (Majority Voting on Context Subsets) | Preprint 2025 | 컨텍스트 서브셋 다수결 투표 방식을 Supervisor의 다중 소스 응답 신뢰도 평가에 참고 |
| HyDE (Hypothetical Document Embeddings) | ACL 2023 | 온톨로지 기반 Taxonomy Injection과 HyDE의 가상 문서 생성 접근법 간 쿼리 확장 효과 비교 |
| Hybrid RRF / Hybrid CC | - | ApeRAG 벡터/그래프 하이브리드 검색의 융합 전략 설계 시 RRF vs Convex Combination 트레이드오프 참고 |

**활용 방법:** AutoRAG-Research GitHub 레포지토리의 `autorag_research/` 디렉토리에서 해당 파이프라인 구현 코드를 리뷰하고, SEOCHO 설계 문서(`.claude/DESIGN-*.md`)에 참고 사항을 기록합니다.

**금지 사항 (Phase 1):**
- AutoRAG-Research 패키지 설치 금지
- PostgreSQL + VectorChord 별도 스택 구성 금지
- 커스텀 플러그인 개발 착수 금지
- 벤치마크 데이터셋(BEIR, RAGBench 등) 수집/실행 금지

#### 5.7.2 Phase 2 (안정화 이후): 정량 벤치마킹 도입

Phase 2.0에서 DataNexus의 핵심 파이프라인(NL2SQL, 하이브리드 검색, 멀티에이전트 라우팅)이 품질 기준선(EX ≥ 90%, P95 < 3s — §5.1 Phase 2 목표 기준)을 달성한 이후에 AutoRAG-Research를 활용한 정량 비교를 시작합니다.

**Phase 2 도입 전제조건:**
- Stage 4 E2E 품질 게이트 통과 (§5.3.6)
- 내부 벤치마크 기준선 확립 (EX, VES, QVT 측정 완료)
- DataNexus 파이프라인의 API 인터페이스 안정화

**Phase 2 벤치마킹 순서:**

| 순서 | 작업 | 데이터셋 | 목적 | 예상 공수 |
|------|------|---------|------|-----------|
| 1 | AutoRAG-Research 환경 구축 | BEIR (scifact) | 프레임워크 동작 확인 + 기준선 | 3일 |
| 2 | MrTyDi 한국어 검색 평가 | MrTyDi (ko) | 한국어 검색 성능 객관적 측정 | 3일 |
| 3 | RAGBench E2E 평가 | RAGBench | 검색+생성 품질 종합 비교 | 5일 |
| 4 | datanexus-hybrid-search 플러그인 | BEIR, RAGBench | ApeRAG 하이브리드 검색 vs SOTA 비교 | 2주 |

**Phase 3+ 확장 (선택):**
- datanexus-seocho-rag 플러그인: SEOCHO 멀티에이전트 E2E RAG vs MAIN-RAG 비교
- BRIGHT 추론 집약형 벤치마크: Multi-hop Inference 품질 평가
- Open-RAGBench 멀티모달: ApeRAG MinerU 파싱 품질 평가

#### 5.7.3 품질 게이트 연동 (Phase 2+)

AutoRAG-Research 메트릭을 DataNexus 내부 품질 지표와 교차 검증합니다.

| DataNexus 내부 지표 | AutoRAG-Research 메트릭 | 교차 검증 목적 |
|--------------------|----------------------|---------------|
| EX Accuracy (§5.1) | nDCG@10 + ROUGE-L | 내부 측정치의 외부 데이터셋 대비 일반화 가능성 확인 |
| Hallucination Rate (§5.1) | BERTScore-F1 | 환각 탐지 기준의 객관성 검증 |
| Query Router Accuracy (§5.1) | 커스텀 메트릭 플러그인 | MAIN-RAG 대비 라우팅 효율 비교 |
