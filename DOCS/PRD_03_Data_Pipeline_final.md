## 4. 데이터 파이프라인 및 거버넌스 (Data Ops & Mesh)

### 4.1 Data Mesh 아키텍처 도입
- **Human-in-the-loop:** 현업 도메인 전문가가 DataHub에서 비즈니스 용어(Glossary)와 소유권(Ownership)을 관리
- **Sync Pipeline:** DataHub 변경 사항 감지 시 ApeRAG/Vanna AI 인덱싱 파이프라인 트리거

### 4.2 데이터 준비 (Preparation)
- **초기 구축:** 사내 테이블 DDL, 메타 정보, 기존 쿼리 로그를 수집하여 초기 지식 그래프 구축
- **Few-shot 예제:** 고품질의 질문-SQL 쌍을 구축하여 프롬프트에 동적으로 삽입

### 4.2+ 데이터 준비 로드맵

> **⚠️ 데이터 준비 계획 부재 (리뷰 보고서 §1-3: 가장 시급한 보완 사항)**

기존 PRD §4.2에서 "초기 구축"과 "Few-shot 예제"를 언급하지만, 구체적 실행 계획이 부재합니다. 아래는 Phase 0.5에서 반드시 선행되어야 할 데이터 준비 로드맵입니다.

#### 4.2.1 Phase 0.5 데이터 준비 체크리스트

| 단계 | 작업 | 산출물 | 담당 | 예상 공수 |
|------|------|--------|------|----------|
| **D-1** | 대상 DM DB 목록 확정 | DB 접속 정보 시트 | DBA + 현업 | 2일 |
| **D-2** | DDL 수집 및 정제 | 테이블/컬럼 DDL 파일 | DBA | 3일 |
| **D-3** | 핵심 비즈니스 용어 20개 선정 | MVP Glossary Term 목록 | 현업 도메인 전문가 | 3일 |
| **D-4** | 기존 쿼리 로그 분석 | Top-50 빈출 쿼리 목록 | DA/DE | 5일 |
| **D-5** | 질문-SQL 쌍 30개 구축 | Few-shot Training Set | DA + 현업 | 5일 |
| **D-6** | 평가 데이터셋 구축 | eval_queries.json (50+ 쌍) | DA | 3일 |
| **D-7** | DataHub Ingestion 테스트 | Ingestion 성공 로그 | DE | 2일 |

**총 예상 공수:** 약 3주 (병렬 진행 시 2주)

#### 4.2.2 MVP Glossary Term 선정 기준

Phase 1 MVP에서는 전체 온톨로지가 아닌 **핵심 20개 용어**로 시작합니다:

```yaml
# mvp_glossary_terms.yaml
selection_criteria:
  - 현업 질문 빈도 상위 (쿼리 로그 기반)
  - 계산식이 포함된 파생 지표 (순매출, 영업이익 등)
  - 부서 간 중의성이 있는 용어 (고객, 매출 등)
  
mvp_terms:  # 아래는 예시 13개 (실제 선정 시 최소 20개로 확장)
  financial:
    - 순매출 (Net Sales)
    - 총매출 (Gross Sales)
    - 영업이익 (Operating Profit)
    - 매출원가 (COGS)
    - 반품 (Returns)
  customer:
    - VIP고객 (VIP Customer)
    - 고객유형 (Customer Type)
    - 구독 (Subscription)
  product:
    - 상품분류 (Product Category)
    - SKU
  operational:
    - 점포 (Store)
    - 주문 (Order)
    - 배송 (Delivery)
  # [TODO: Phase 0.5 D-3] 현업 협의 후 7개 이상 추가하여 최소 20개 확보
  # 후보: 할인, 에누리, 재고, 매장유형, 회원등급, 결제수단, 카테고리 등
  # 담당: 도메인 전문가 + 데이터 오너, §4.2.1 체크리스트 D-3 참조
```

#### 4.2.3 Few-shot 예제 품질 기준

| 기준 | 설명 | 최소 요건 |
|------|------|----------|
| **다양성** | 단순 조회 ~ 복합 집계 ~ 조인 질의 균형 | 각 유형 최소 5개 |
| **정확성** | DBA가 검증한 정답 SQL | 실행 결과 일치 100% |
| **현업 표현** | 실제 현업이 사용하는 자연어 표현 | 쿼리 로그 기반 |
| **온톨로지 활용** | Glossary Term이 자연어에 포함 | 70% 이상 |

#### 4.2.4 Training 데이터 포맷 및 관리 전략

##### YAML 기반 Q-SQL 쌍 관리

Few-shot training 데이터는 YAML 파일로 관리한다. JSON 대비 가독성이 높고, 멀티라인 SQL 작성이 용이하며, Git diff로 변경 추적이 직관적이다.

```yaml
# config/training_queries.yaml
# 형식: question(자연어) + answer(검증된 SQL)
# 참고: Vanna AI YAML training 패턴 (MITB For All, 2025.06)
---
- question: >
    지난 분기 VIP 고객의 월별 순매출 추이를 보여줘
  answer: |
    SELECT 
      DATE_TRUNC('month', o.order_date) AS month,
      SUM(o.amount - o.returns - o.discounts) AS net_sales
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    WHERE c.customer_type = 'VIP'
      AND o.order_date >= DATE_TRUNC('quarter', CURRENT_DATE - INTERVAL '3 months')
      AND o.order_date < DATE_TRUNC('quarter', CURRENT_DATE)
    GROUP BY 1
    ORDER BY 1;
  tags: [financial, customer, time-series]
  glossary_terms: [순매출, VIP고객]
  complexity: complex  # simple | medium | complex

- question: >
    올해 상품 카테고리별 매출 비중은?
  answer: |
    SELECT 
      p.category AS product_category,
      SUM(o.amount) AS total_sales,
      ROUND(SUM(o.amount) * 100.0 / SUM(SUM(o.amount)) OVER(), 2) AS pct
    FROM orders o
    JOIN products p ON o.product_id = p.id
    WHERE EXTRACT(YEAR FROM o.order_date) = EXTRACT(YEAR FROM CURRENT_DATE)
    GROUP BY 1
    ORDER BY 2 DESC;
  tags: [product, aggregation]
  glossary_terms: [상품분류]
  complexity: medium
```

##### DataNexus 확장 필드

Vanna 기본 포맷(question + answer)에 DataNexus 전용 필드를 추가한다:

| 필드 | 필수 | 설명 |
|------|------|------|
| `question` | Y | 현업이 실제 사용하는 자연어 표현 |
| `answer` | Y | DBA 검증 완료 SQL |
| `tags` | N | 분류 태그 (검색/필터용) |
| `glossary_terms` | N | 참조하는 온톨로지 용어 (§4.2.2 MVP Term과 매칭) |
| `complexity` | N | 난이도 (simple/medium/complex) — 평가 데이터셋 구성 시 활용 |
| `tenant_id` | N | 멀티테넌트 환경 시 테넌트 귀속 (미지정 시 공용) |

##### 학습 데이터 로드 유틸리티

```python
# src/training/loader.py
import yaml
from typing import List, Tuple
from pathlib import Path

def load_training_queries(yaml_path: str | Path) -> List[Tuple[str, str]]:
    """YAML 파일에서 Q-SQL 쌍을 로드한다.
    
    Returns:
        List of (question, sql) tuples for Vanna training
    """
    path = Path(yaml_path)
    if not path.exists():
        raise FileNotFoundError(f"Training file not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        documents = yaml.safe_load(f)
    
    if not isinstance(documents, list):
        raise ValueError("YAML content must be a list of Q-SQL documents")
    
    return [(doc['question'].strip(), doc['answer'].strip()) for doc in documents]
```

##### 파일 구조 및 도메인별 분할

training 데이터가 30쌍을 초과하면 도메인별로 YAML 파일을 분할하여 관리한다:

```
config/training/
├── financial.yaml      # 순매출, 영업이익, 매출원가 관련
├── customer.yaml       # VIP고객, 고객유형, 구독 관련
├── product.yaml        # 상품분류, SKU 관련
├── operational.yaml    # 점포, 주문, 배송 관련
└── common.yaml         # 도메인 무관 범용 질의 (테이블 목록 조회 등)
```

##### 학습 데이터 품질 게이트

| 검증 항목 | 기준 | 자동화 |
|----------|------|--------|
| SQL 구문 유효성 | 모든 SQL이 대상 DB에서 파싱 가능 | CI/CD `sqlfluff lint` |
| 실행 결과 비어있지 않음 | 최소 1행 이상 반환 | pytest fixture |
| 온톨로지 용어 매칭 | `glossary_terms` 필드의 70%가 §4.2.2 목록에 존재 | 커스텀 validator |
| 난이도 분포 | simple:medium:complex = 30:40:30 (±10%) | YAML 메타 분석 |
| 중복 질문 검출 | 코사인 유사도 > 0.9인 쌍 없음 | 임베딩 비교 스크립트 |

> **📌 참조:** NL2SQL baseline 정확도 근거는 [PRD_05 §5.6.1](./PRD_05_Evaluation_Quality_final.md) 참조. 학습 데이터 피드백 루프 설계는 [PRD_02 §3.10](./PRD_02_Core_Features_Agent_final.md) 참조 (예정).

---

### 4.3 온톨로지-RAG 통합 파이프라인
목적: 관리자가 DM(데이터 마트) DB를 지정하면, DataHub에 테이블/뷰 메타데이터가 자동 수집되고, 정의된 온톨로지(Glossary Terms)가 Vanna AI RAG에 동기화되어 NL2SQL 쿼리 품질이 향상됩니다.

#### 4.3.1 전체 플로우 개요

| 단계 | 작업 설명 | 기술 요소 |
| :--- | :--- | :--- |
| ① DB 연결 설정 | 관리자가 Admin UI에서 DM DB 접속 정보 등록 | Admin API, 암호화 Credential 저장 |
| ② 메타데이터 수집 | DataHub Ingestion으로 테이블/뷰/컬럼 자동 수집 | DataHub Ingestion Framework (YAML) |
| ③ 카탈로그 표시 | DataHub UI/API에서 수집된 객체 목록 조회 | DataHub GraphQL API |
| ④ 온톨로지 정의 | 관리자가 Glossary Term 생성 및 테이블/컬럼/세만틱 뷰 매핑 | DataHub Glossary, GraphQL Mutation |
| ⑤ 품질 검증 | 정의 충돌, 동의어 중복, 순환 참조, 고아 참조 등 검증 및 **온톨로지 자체 품질 지표(Structural/Semantic/Functional) 평가** | Validation Engine, Fuzzy Matching, **LLM-as-a-Judge, Graph Data Science** |
| ⑥ RAG 동기화 | DDL + Glossary + Sample SQL을 Vanna AI에 학습 및 ApeRAG에 Taxonomy로 주입 | Sync Pipeline, Vanna train API, ApeRAG GraphIndex, Prompt Template |
| ⑦ 질의 시 컨텍스트 활용 | 사용자 질문에 온톨로지 포함 컨텍스트로 SQL/Cypher 생성 | Vanna generate_sql, RAG Retrieval |

> **📌 파이프라인 상세 문서 위치:**
> - ①~④ 단계 상세: 본 파일 §4.3.2~4.3.4 (아래 참조)
> - ⑤~⑥ 단계 상세 (품질 검증, Entity Resolution, DataHub→Vanna 동기화): [PRD_04b_Ontology_Extended_final.md §4.3.5~4.3.8](./PRD_04b_Ontology_Extended_final.md)
> - ⑦ 단계 상세 (질의 시 컨텍스트 활용): [PRD_02_Core_Features_Agent_final.md §3.1~3.5](./PRD_02_Core_Features_Agent_final.md)

#### 4.3.1.1 동기화 장애 시나리오 및 복구 전략

> **📌 배경:** §4.3.1의 동기화 파이프라인(DataHub MCL → Kafka → DozerDB/Vanna/ApeRAG)은 "한 곳에서 용어를 고치면 네 군데가 동시에 바뀐다"는 설계다. 이 섹션은 동기화가 실패하는 현실적 시나리오와 복구 전략을 정의한다.

##### 장애 유형 분류

| 유형 | 시나리오 | 영향 | 심각도 |
| :--- | :--- | :--- | :--- |
| **F-1** | Kafka Consumer 일시 다운 | MCL 이벤트 미소비, 대상 시스템 동기화 지연 | HIGH |
| **F-2** | 부분 동기화 실패 | DozerDB 성공 + Vanna 실패 → 시스템 간 불일치 | CRITICAL |
| **F-3** | MCL 이벤트 순서 역전 | Term 생성 전에 관계 설정 이벤트 도착 → 참조 오류 | MEDIUM |
| **F-4** | 스키마 변환 오류 | Glossary Term → Vanna Documentation 변환 실패 | MEDIUM |
| **F-5** | DozerDB 용량/연결 장애 | 그래프 쓰기 실패, 온톨로지 갱신 중단 | HIGH |
| **F-6** | Glossary 변경 후 대시보드 Staleness 미감지 | 구식 SQL로 생성된 KPI가 경영진에게 보고됨 — Shaper 대시보드가 이전 Glossary 정의 기반 SQL을 계속 실행 | HIGH |

##### F-1: Kafka Consumer 다운 — 이벤트 유실 방지

Kafka Consumer Group은 오프셋 커밋 방식으로 동작한다. Consumer가 일시적으로 다운되면 이벤트가 Kafka 토픽에 남아 있고, Consumer 재기동 시 마지막 커밋된 오프셋부터 재소비한다.

```yaml
# sync_consumer_config.yaml
kafka:
  consumer:
    group_id: "datanexus-sync-consumer"
    auto_offset_reset: "earliest"         # 신규 Consumer는 처음부터 읽기
    enable_auto_commit: false             # 수동 커밋으로 처리 완료 보장
    max_poll_interval_ms: 300000          # 5분 이내 처리 못하면 리밸런스
  topic:
    name: "MetadataChangeLog_Versioned_v1"
    retention_ms: 604800000               # 7일 보관 (재처리 여유)
```

**복구 전략:**
- 수동 커밋(enable.auto.commit=false): 메시지를 처리하고 대상 시스템(DozerDB, Vanna, ApeRAG)에 반영 완료한 뒤에만 오프셋을 커밋한다. 처리 도중 Consumer가 죽으면 재기동 시 같은 메시지를 다시 받는다.
- 토픽 보관 기간 7일: Consumer가 7일 이내에 복구되면 이벤트 유실 없음.
- **모니터링:** Consumer Lag(미처리 메시지 수)를 Prometheus로 수집. Lag > 1000이면 Opik 알림 발행.

##### F-2: 부분 동기화 실패 — 정합성 보장

가장 위험한 시나리오다. DozerDB에는 반영됐는데 Vanna RAG Store에는 안 된 상태가 되면, 그래프 탐색 결과와 NL2SQL 프롬프트에 주입되는 맥락이 불일치한다.

```python
# sync/transactional_sync.py
class TransactionalSyncProcessor:
    """다중 대상 동기화의 원자성 보장
    
    Saga 패턴 적용: 각 대상별 동기화를 순차 실행하고,
    중간 실패 시 이미 완료된 동기화를 보상 트랜잭션으로 롤백한다.
    """
    
    SYNC_TARGETS = ["dozerdb", "vanna", "aperag"]
    
    def process_event(self, event: MCLEvent) -> SyncResult:
        completed = []
        
        for target in self.SYNC_TARGETS:
            try:
                self._sync_to_target(target, event)
                completed.append(target)
            except SyncError as e:
                # 실패 시: 이미 완료된 대상들에 대해 보상 트랜잭션 실행
                self._compensate(completed, event)
                # 이벤트를 Dead Letter Queue로 이동
                self._send_to_dlq(event, error=e, completed=completed)
                return SyncResult(
                    status="PARTIAL_FAILURE",
                    completed=completed,
                    failed=target,
                    error=str(e)
                )
        
        return SyncResult(status="SUCCESS", completed=completed)
    
    def _compensate(self, completed: list, event: MCLEvent):
        """보상 트랜잭션: 이미 반영된 변경을 되돌린다"""
        for target in reversed(completed):
            try:
                self._rollback_target(target, event)
            except CompensationError as ce:
                # 보상마저 실패하면 수동 개입 필요 → 알림 발행
                self._alert_manual_intervention(target, event, ce)
    
    def _send_to_dlq(self, event: MCLEvent, error, completed: list):
        """Dead Letter Queue에 실패 이벤트 저장 — 수동 재처리용"""
        self.dlq_producer.send(
            topic="datanexus-sync-dlq",
            value={
                "original_event": event.to_dict(),
                "error": str(error),
                "completed_targets": completed,
                "timestamp": datetime.utcnow().isoformat(),
                "retry_count": 0
            }
        )
```

**정합성 검증 — 주기적 Reconciliation:**

```python
# sync/reconciliation.py
class SyncReconciler:
    """DataHub ↔ DozerDB ↔ Vanna 간 정합성 주기 검증
    
    스케줄: 매일 03:00 (Ingestion 스케줄 이후)
    """
    
    def reconcile(self) -> ReconciliationReport:
        datahub_terms = self.datahub_client.get_all_glossary_terms()
        dozerdb_nodes = self.dozerdb_client.get_all_entity_nodes()
        vanna_docs = self.vanna_client.get_all_documentation()
        
        mismatches = []
        
        for term in datahub_terms:
            # DozerDB 노드 존재 여부
            node = dozerdb_nodes.get(term.urn)
            if not node or node.definition != term.definition:
                mismatches.append(Mismatch(
                    term_urn=term.urn,
                    target="dozerdb",
                    type="MISSING" if not node else "STALE"
                ))
            
            # Vanna Documentation 존재 여부
            doc = vanna_docs.get(term.urn)
            if not doc or doc.content != self._term_to_doc(term):
                mismatches.append(Mismatch(
                    term_urn=term.urn,
                    target="vanna",
                    type="MISSING" if not doc else "STALE"
                ))
        
        if mismatches:
            self._auto_repair(mismatches)
        
        return ReconciliationReport(
            total_terms=len(datahub_terms),
            mismatches_found=len(mismatches),
            auto_repaired=len([m for m in mismatches if m.repaired])
        )
```

##### F-3: MCL 이벤트 순서 역전 — 멱등성 + 타임스탬프 기반 해결

Kafka 파티션 내에서는 순서가 보장되지만, 서로 다른 엔티티의 이벤트가 다른 파티션에 있으면 순서가 뒤바뀔 수 있다. Term 생성 이벤트보다 관계 설정 이벤트가 먼저 도착하면, 아직 존재하지 않는 노드에 엣지를 만들려는 상황이 된다.

**해결:**
- 모든 동기화 작업을 멱등(idempotent)하게 구현한다. 동일 이벤트가 두 번 들어와도 결과가 같아야 한다.
- 관계 설정 이벤트가 도착했을 때 대상 노드가 없으면, 이벤트를 Retry Queue에 넣고 30초 후 재시도한다(최대 3회).
- 3회 초과 실패 시 Dead Letter Queue로 이동.

##### F-6: Glossary 변경 후 대시보드 Staleness — 구식 KPI 보고 방지

> **📌 상세 설계:** [PRD_02 §3.9.7~3.9.8](./PRD_02_Core_Features_Agent_final.md) 참조

**시나리오:** "순매출" Glossary Term의 계산식이 변경되었으나, 이미 승격된 Shaper 대시보드 5개가 이전 SQL을 계속 실행하여 경영진에게 잘못된 KPI가 보고됨.

**영향 범위:**
- Glossary 변경 → Vanna 재학습은 정상 작동 (기존 F-1~F-5 파이프라인)
- 그러나 Shaper 대시보드는 기존 파이프라인의 전파 대상에 포함되지 않음
- 대시보드 소유자가 수동으로 인지하기 전까지 구식 SQL이 계속 실행됨

**해결:**
- DashboardStalenessDetector를 기존 Kafka Consumer 체인에 핸들러로 추가 (아키텍처 변경 없음)
- Glossary Term 변경 MCL 이벤트 수신 시, 해당 Term을 참조하는 모든 DashboardLineage를 STALE로 마킹
- 대시보드 소유자에게 즉시 알림 발송 + RE_PROMOTE(재승격) 권고
- 재승격 시 기존 대시보드 ID를 유지하여 스케줄/공유 설정 보존

**복구 우선순위:**
1. STALE 마킹 + 알림 (자동, 즉시)
2. 대시보드 소유자가 Chat에서 재질의 후 RE_PROMOTE (수동, 권고)
3. 72시간 미조치 시 대시보드에 "⚠️ 데이터 정의 변경으로 정확성 미보장" 워터마크 자동 표시

##### 품질 게이트 연동

| 게이트 | 기존 기준 | 보강 |
| :--- | :--- | :--- |
| Sync Integrity (§5.3.6) | 100% | Reconciliation Report의 mismatch 수 = 0 |
| 실패 시 조치 | "파이프라인 디버깅" | DLQ 이벤트 재처리 → 실패 시 Reconciler 강제 실행 → 실패 시 수동 개입 에스컬레이션 |

**모니터링 대시보드 (Opik 연동):**

| 패널 | 메트릭 | 알림 기준 |
| :--- | :--- | :--- |
| Consumer Lag | 미처리 MCL 이벤트 수 | > 1,000: WARNING, > 5,000: CRITICAL |
| Sync Success Rate | 성공 / 전체 동기화 시도 | < 99%: WARNING, < 95%: CRITICAL |
| DLQ Depth | Dead Letter Queue 메시지 수 | > 0: WARNING (즉시 확인) |
| Reconciliation Mismatch | 일일 Reconciliation 불일치 수 | > 0: 자동 복구 후 알림 |
| P95 Sync Latency | 이벤트 발행 → 전체 동기화 완료 | > 30초: WARNING |
| Dashboard Staleness Count | STALE 상태 대시보드 수 (F-6) | > 0: WARNING, 72시간 미조치: CRITICAL |

#### 4.3.2 관리자 메뉴 설계
**A. DB 연결 관리 (Data Source Management)**

| 메뉴 항목 | UI 컴포넌트 | 기능 설명 |
| :--- | :--- | :--- |
| DB 소스 목록 | DataGrid, StatusBadge | 등록된 DM DB 목록 조회, 연결 상태 표시 (정상/오류/동기화중) |
| DB 소스 등록 | Form, Select, Input | 플랫폼 선택 (Oracle/PostgreSQL/BigQuery 등), 접속 정보 입력, 연결 테스트 |
| 스키마 선택 | TreeView, Checkbox | 수집 대상 스키마/테이블 패턴 지정 (예: MART_%, DW_%) |
| 수집 실행 | Button, ProgressBar | DataHub Ingestion 즉시 실행, 진행 상황 표시 |
| 수집 스케줄 | CronEditor, Toggle | 자동 수집 주기 설정 (매일 02:00 등) |

**B. 온톨로지 편집기 (Ontology Editor)**

| 메뉴 항목 | UI 컴포넌트 | 기능 설명 |
| :--- | :--- | :--- |
| 용어집 목록 | DataGrid, Search | Glossary Term 전체 목록, 검색/필터링 |
| 용어 생성/편집 | Form, RichTextEditor | 용어명, 정의(계산식 포함), 동의어, 관련 링크 입력 |
| 테이블/컬럼 연결 | TreeView, DragDrop | Glossary Term을 특정 테이블 또는 컬럼에 매핑 |
| 용어 계층 관리 | TreeEditor | Glossary Node(그룹) 생성 및 용어 계층화 |
| 관계 정의 | RelationEditor, Graph | IsA/HasA/RelatedTo 등 용어 간 관계 설정, 그래프 시각화 |
| 일괄 Import | FileUpload, Preview | Excel/YAML 파일로 용어 일괄 등록 |

**C. RAG 학습 관리 (RAG Training Manager)**

| 메뉴 항목 | UI 컴포넌트 | 기능 설명 |
| :--- | :--- | :--- |
| Training Data 목록 | DataGrid, Filter | Vanna AI에 학습된 데이터 목록 (DDL/Doc/SQL 구분) |
| DDL 관리 | CodeEditor, Sync | DataHub에서 추출된 DDL 확인, 수동 편집, 재학습 |
| Documentation | List, Editor | Glossary Term → Documentation 변환 결과 확인/편집 |
| Sample SQL 관리 | CodeEditor, Test | 질문-SQL 쌍 등록, SQL 실행 테스트 |
| 동기화 상태 | StatusBoard, Log | DataHub → Vanna 동기화 이력 및 상태 모니터링 |
| 수동 동기화 | Button, Confirm | 전체 또는 선택된 테이블의 RAG 데이터 즉시 동기화 |

#### 4.3.3 DataHub Ingestion 설정
관리자가 DB 소스를 등록하면 아래와 같은 YAML Recipe가 자동 생성됩니다:

```yaml
# datahub_ingestion_recipe.yaml (자동 생성 예시)
source:
 type: oracle # 또는 postgresql, bigquery, snowflake 등
 config:
    host_port: "${DB_HOST}:${DB_PORT}"
    database: "GRS_DM"
    schema_pattern:
      allow: ["MART_%", "DW_%"]
    include_tables: true
    include_views: true
    profiling:
      enabled: true # 컬럼 통계 수집
sink:
 type: datahub-rest
 config:
    server: "http://datahub-gms:8080"
```

#### 4.3.4 Glossary Term 데이터 구조
온톨로지 편집기에서 정의하는 Glossary Term의 필수/권장 필드입니다. 관계 정의 및 동의어 필드가 확장되었습니다.

⚠️ DataHub는 synonyms 필드를 공식 지원하지 않습니다. 커스텀 필드로 구현하거나 description에 포함해야 합니다.

| 필드명 | 필수 여부 | 예시 | 활용 |
| :--- | :--- | :--- | :--- |
| name | 필수 | 순매출 | Documentation 제목, Entity 이름 |
| definition | 필수 | 총매출에서 반품, 할인, 에누리를 차감한 실제 매출액 | Documentation 본문 |
| formula | 권장 | 순매출 = 총매출 - 반품 - 할인 - 에누리 | Documentation에 계산식으로 포함, **세만틱 뷰 정의** |
| synonyms (⚠️ 커스텀) | 권장 | ["Net Sales", "실매출", "넷세일즈"] | ⚠️ DataHub 미지원 — 커스텀 필드로 구현, Entity Resolution에 활용 |
| linked_columns | 권장 | GRS_DM.MART_SALES.NET_SALES_AMT | DDL-Documentation 연결 힌트 |
| domain | 선택 | Sales (영업) | RAG 검색 시 도메인 필터링, **다중 도메인 중의성 해결** |
| relatedTerms | 권장 | [{urn, relation_type}] | DataHub 공식 관계 (IsA/HasA/RelatedTo), **세분화된 관계 정의** |
| validity_period (커스텀) | 선택 | {"start": "2026-01-01", "end": "2026-12-31"} | **시간적 온톨로지 관리** |
| source_affinity (커스텀) | 선택 | "정형", "비정형", "하이브리드" | **온톨로지 기반 질의 분해 전략** |
| uri | 자동생성 | urn:li:glossaryTerm:순매출 | 공통 식별자 (Vanna+ApeRAG 통합용) |

#### 4.3.4.1 DataHub 공식 관계 유형

| 관계 유형 | DataHub 필드 | 설명 | 예시 |
| :--- | :--- | :--- | :--- |
| IsA | isRelatedTerms | 상속/일종(kind-of) 관계 | Email IsA PersonalInformation |
| HasA | hasRelatedTerms | 포함(contains) 관계 | Address HasA ZipCode |
| Values | values | 값 목록 관계 | CustomerType Values [VIP, Regular, New] |
| RelatedTo | relatedTerms | 일반 연관 관계 | 순매출 RelatedTo 반품 |

※ 출처: DataHub 공식 문서 (GlossaryTerm 메타데이터 스키마), DataHub GraphQL API
