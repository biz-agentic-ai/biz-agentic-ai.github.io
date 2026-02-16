> **📋 오버엔지니어링 주의 (리뷰 보고서 §3-4):**
> 4단계 품질 게이트(Unit → Integration → CQ → E2E) 중 MVP에서는 **Stage 1(Unit) + Stage 4(E2E)만 필수** 적용합니다. 상세는 §5.3 참조.

## 5. 평가 및 품질 관리 (Evaluation Strategy)

### 5.1 주요 지표 (Metrics)

> **Phase 범례:** **1** = MVP 필수, 1→2 = MVP에서 도입 후 Phase 2에서 목표 상향, 1.5 = Phase 1 안정화, 2 = Phase 2 고도화, 3 = Phase 3 R&D.
> 굵은 숫자(**1**)는 §4.8 SSOT 지표. **단일 SSOT: PRD_04a §4.8이 유일한 정식(canonical) 출처이며, 본 테이블은 §4.8을 미러링합니다.** 수치가 상이한 경우 §4.8 기준이 우선합니다.

#### 5.1.1 Phase 1 MVP 필수 지표 (10개)

| 지표 | 설명 | MVP 기준 | Phase 2 목표 | Phase |
| :--- | :--- | :--- | :--- | :---: |
| **EX (Execution Accuracy)** | 실행 결과값의 일치 여부 | ≥ 80% | ≥ 90% | **1 → 2** |
| **VES (Valid Efficiency Score)** | 생성된 쿼리의 실행 효율성 | P95 < 3초 | — | **1** |
| **VPA (Validation Pass Rate)** | 품질 검증 통과율 | ≥ 95% | — | **1** |
| **CQ Pass Rate** | 적합성 질문 검증 통과율 | ≥ 80% | ≥ 95% | **1 → 2** |
| **Schema Compliance** | 스키마 강제성 준수율 (ACCEPT+REMAP) | ≥ 90% | ≥ 95% | **1 → 2** |
| **Deterministic Query Rate** | 템플릿 기반 결정론적 질의 비율 | ≥ 60% | — | **1** |
| **Routing Accuracy** | Query Router 정확도 | ≥ 95% | ≥ 97% | **1 → 2** |
| **Tool Guard Activation Rate** | 도구 결과 가드 발동 빈도 (낮을수록 양호) | < 5% | — | **1** |
| **Hallucination Rate** | 근거 없는 정보가 응답에 포함된 비율 (낮을수록 양호) | ≤ 5% (SSOT: ≤ 0.05) | ≤ 3% | **1 → 2** |
| **ConflictResolutionScore** | 다중 소스 충돌 해결 품질 | ≥ 95% | ≥ 97% | **1 → 2** |
| **Reasoning Accuracy** | 관계 기반 추론의 정확도 | ≥ 0.85 | ≥ 0.90 | **1 → 2** |

#### 5.1.2 Phase 1.5 안정화 지표 (4개)

| 지표 | 설명 | 목표 | Phase |
| :--- | :--- | :--- | :---: |
| QVT (Query Variance Testing) | 질문 표현 변화에 대한 일관성 검증 | 일관성 90% 이상 | 1.5 |
| Incremental Update Ratio | 증분 업데이트 처리 비율 | 90% 이상 | 1.5 |
| SKOS Mapping Coverage | SKOS 표준 매핑 완료율 | 95% 이상 | 1.5 |
| Draft Acceptance Rate | LLM 초안 승인율 (수정 없이) | 50% 이상 | 1.5 |

#### 5.1.3 Phase 2 고도화 지표 (5개)

| 지표 | 설명 | 목표 | Phase |
| :--- | :--- | :--- | :---: |
| OCA (Ontology Coverage) | 온톨로지 정의 용어에 대한 정확도 | 90% 이상 | 2 |
| External KG Mapping Rate | 외부 데이터 엔터티의 Glossary 매핑률 | 50% 이상 | 2 |
| ToolsRetriever Routing Accuracy | Agentic Retriever 자동 선택 정확도 | 90% 이상 | 2 |
| Context Preservation Rate | 컴팩션 후 핵심 사실 보존율 (§4.3.10.10) | 90% 이상 | 2 |
| Cache Hit Rate | LLM 프리픽스 캐시 활용률 | 70% 이상 | 2 |

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
        """각 컴포넌트의 기여도 분석"""
        # A4 - A2 = LPG 기여도 (RDF 고정)
        # A4 - A1 = RDF 기여도 (LPG 고정)
        # etc.
        return ContributionAnalysis(
            lpg_contribution=results["A4"].score - results["A2"].score,
            rdf_contribution=results["A4"].score - results["A1"].score,
            hybrid_contribution=results["A5"].score - results["A1"].score
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

#### 5.4.5 Opik 연동 (LLM Observability)

Opik(Comet ML)과 연동하여 실험 결과를 추적하고 관리합니다.

```python
# evaluation/integrations/opik_integration.py
from opik import Opik

class OpikEvaluationTracker:
    """Opik 기반 실험 추적"""
    
    def __init__(self, project_name: str = "datanexus-eval"):
        self.opik = Opik(project_name=project_name)
        
    def log_experiment(self, experiment: ExperimentResult):
        """실험 결과 로깅"""
        self.opik.log({
            "experiment_id": experiment.experiment_id,
            "metrics": experiment.metrics.to_dict(),
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

#### 5.4.6 평가 품질 게이트 (SEOCHO 확장)

| 단계 | 품질 게이트 | 통과 기준 | 실패 시 조치 |
| :--- | :--- | :--- | :--- |
| **Macro** | M1 vs M2 차이 | ≤ 10% | Manager 로직 검토 |
| **Macro** | M1 vs M3 차이 | ≥ 10% | 온톨로지 기여도 검증 완료 |
| **Ablation** | A4 > A1 + A2 | Synergy 확인 | 조합 효과 검증 |
| **Metrics** | RoutingAccuracy | ≥ 95% | Router 분류기 재학습 |
| **Metrics** | ConflictResolutionScore | ≥ 95% | Hierarchy 로직 검토 |
| **Metrics** | Hallucination Rate | ≤ 5% | 컨텍스트 품질 개선 |

---

> **📌 메뉴 구조 참조:** 사용자 메뉴(§6.6) 및 관리자 메뉴(§6.7)는 [PRD_06_Requirements_Roadmap.md](PRD_06_Requirements_Roadmap.md)를 참조하세요.

---

### 5.5 에러 처리 및 Fallback 전략 (보강: 리뷰 보고서 §1-4)

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

### 5.6 성능 벤치마크 기준 (보강: 리뷰 보고서 §1-5)

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
| Routing Accuracy (§5.1) | 커스텀 메트릭 플러그인 | MAIN-RAG 대비 라우팅 효율 비교 |
