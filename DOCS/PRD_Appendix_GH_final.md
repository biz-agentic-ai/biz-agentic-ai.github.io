## 부록 G: 유통/물류 표준 온톨로지 Seed 예시 (GS1/GoodRelations)

### G.1 DataHub Glossary YAML 예시 (GS1/GoodRelations 핵심 클래스)

```yaml
version: 1
source: DataNexus_GS1_Importer
owners:
  - "urn:li:corpuser:admin"

nodes:
  - name: "GS1_Core"
    display_name: "GS1 유통 표준 온톨로지"
    description: "GS1 Web Vocabulary 및 GoodRelations 기반의 유통/물류 표준 용어집"
    knowledge_links:
      - label: "GS1 Web Vocab"
        url: "https://www.gs1.org/voc/"

terms:
  - name: "GS1_Product"
    display_name: "상품 (Product)"
    parentNode: "GS1_Core"
    description: "판매 또는 배송을 위해 제공되는 물리적 제품 또는 서비스. (참조: gs1:Product)"
    customProperties:
      synonyms: "['제품', '물품', 'Item', 'Merchandise', 'Goods']"
      skos_concept: "gs1:Product"
      source_affinity: "하이브리드"
      domain: "Retail"

  - name: "GS1_GTIN"
    display_name: "국제 거래 단품 식별 코드 (GTIN)"
    parentNode: "GS1_Core"
    description: "상품을 고유하게 식별하는 13자리 또는 14자리 코드. (참조: gs1:gtin)"
    customProperties:
      synonyms: "['바코드', '상품코드', 'EAN', 'UPC']"
      skos_concept: "gs1:gtin"
      relation_type: "identifierOf"  # GTIN은 Product의 식별자
    relatedTerms:
      - "GS1_Product"  # HasA/identifierOf 관계 (IsA가 아님 - GTIN은 Product의 종류가 아니라 식별자임)

  - name: "GR_Offering"
    display_name: "판매 제안 (Offering)"
    parentNode: "GS1_Core"
    description: "특정 상품을 특정 가격과 조건으로 판매하겠다는 제안. (참조: gr:Offering)"
    customProperties:
      synonyms: "['딜', '오퍼', 'Sales Offer', '프로모션']"
      skos_concept: "gr:Offering"
    relatedTerms:
      - "GS1_Product"
```

### G.2 DataHub Ingestion Recipe 예시

```yaml
source:
  type: "datahub-business-glossary"
  config:
    file: "./gs1_ontology.yaml"
    enable_patch: true

sink:
  type: "datahub-rest"
  config:
    server: "http://localhost:8080"
    token: "${DATAHUB_ACCESS_TOKEN}"
```

```bash
datahub ingest -c ingestion_recipe.yaml
```

### G.3 CQ 테스트 케이스 매트릭스 (Seed 검증)

| CQ 유형 | 자연어 질문 | 검증 대상 온톨로지 경로 | 성공 기준 |
| :--- | :--- | :--- | :--- |
| FCQ | 특정 상품의 바코드(GTIN) 정보가 정의되어 있는가? | `GS1_Product` → `GS1_GTIN` | GTIN 용어 존재 및 Product와 연결 |
| RCQ | 판매 제안(Offering)에는 어떤 상품이 포함되는가? | `GR_Offering` → `GS1_Product` | Offering 조회 시 Product 연결 확인 |
| VCQ | ‘오퍼’로 검색해도 ‘판매 제안’을 찾을 수 있는가? | `GR_Offering.customProperties.synonyms` | 동의어 매칭으로 Offering 검색 가능 |
| SCQ | 이 온톨로지는 전자상거래/리테일을 다루는가? | `GS1_Product.customProperties.domain` | domain 값이 Retail/E-commerce |

### G.4 CQ 검증 자동화 코드 (Pytest 예시)

```python
import pytest
import yaml

@pytest.fixture
def ontology():
    with open("gs1_ontology.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def test_fcq_gtin_exists(ontology):
    """GTIN 용어 존재 및 Product와의 식별자 관계 검증"""
    terms = ontology["terms"]
    gtin = next((t for t in terms if t["name"] == "GS1_GTIN"), None)
    assert gtin is not None, "GS1_GTIN 용어가 누락되었습니다."
    # GTIN은 Product의 식별자이므로 relatedTerms로 연결됨 (IsA가 아님)
    assert "GS1_Product" in gtin.get("relatedTerms", []), "GTIN이 Product와 연결되지 않았습니다."

def test_vcq_synonym_resolution(ontology):
    target_query = "오퍼"
    terms = ontology["terms"]
    found = None
    for term in terms:
        synonyms = term.get("customProperties", {}).get("synonyms", "")
        if isinstance(synonyms, str) and target_query in synonyms:
            found = term["name"]
            break
    assert found == "GR_Offering", f"'{target_query}' 검색 시 GR_Offering이 매핑되어야 합니다."

def test_rcq_offering_has_product(ontology):
    terms = ontology["terms"]
    offering = next((t for t in terms if t["name"] == "GR_Offering"), None)
    assert offering is not None, "GR_Offering 용어가 누락되었습니다."
    assert "GS1_Product" in offering.get("relatedTerms", []), "Offering-Product 관계가 누락되었습니다."
```

---

## 부록 H: SEOCHO CLI Reference

SEOCHO 프로젝트(`feature-kgbuild` 브랜치)에서 제공하는 CLI 도구 명세입니다.

### H.1 인덱싱 CLI (Indexing)

데이터 소스를 벡터 인덱스와 그래프 데이터베이스에 적재합니다.

```bash
# 전체 인덱스 빌드
docker exec agent-jupyter-container python -m src.cli.index --all

# 벡터 인덱스만 빌드 (LanceDB/FAISS)
docker exec agent-jupyter-container python -m src.cli.index --lancedb

# 그래프 인덱스만 빌드 (Neo4j)
docker exec agent-jupyter-container python -m src.cli.index --neo4j
```

**명령어 옵션:**

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--all` | 모든 인덱스 빌드 (LanceDB + Neo4j) | - |
| `--lancedb` | 벡터 인덱스만 빌드 | - |
| `--neo4j` | 그래프 인덱스만 빌드 | - |
| `--source` | 데이터 소스 경로 | `/workspace/data/` |
| `--config` | 설정 파일 경로 | `config.yaml` |
| `--force` | 기존 인덱스 덮어쓰기 | `false` |

**환경 변수:**

```bash
# 필수
OPENAI_API_KEY=sk-...

# 데이터베이스 (Docker 환경 기본값)
NEO4J_URI=bolt://graphrag-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
LANCEDB_PATH=/workspace/data/lancedb
```

### H.2 평가 CLI (Evaluation)

Macro/Ablation 실험 및 메트릭 측정을 실행합니다.

```bash
# Macro 실험 실행 (M1~M4)
docker exec agent-jupyter-container python -m src.cli.evaluate --macro

# Ablation 실험 실행 (A1~A6)
docker exec agent-jupyter-container python -m src.cli.evaluate --ablation

# 특정 모드만 실행
docker exec agent-jupyter-container python -m src.cli.evaluate --modes lpg,hybrid

# 전체 실험 실행
docker exec agent-jupyter-container python -m src.cli.evaluate --all
```

**명령어 옵션:**

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--macro` | Macro 실험 (M1~M4) 실행 | - |
| `--ablation` | Ablation 실험 (A1~A6) 실행 | - |
| `--modes` | 특정 검색 모드 조합 (콤마 구분) | `lpg,rdf,hybrid` |
| `--all` | 모든 실험 실행 | - |
| `--dataset` | 평가 데이터셋 경로 | `datasets/eval.json` |
| `--output` | 결과 출력 경로 | `results/` |
| `--verbose` | 상세 로깅 | `false` |

**실험 설정 파일 예시 (`config/experiments.yaml`):**

```yaml
macro_experiments:
  M1:
    components: [lpg, rdf, hybrid]
    agent_type: hierarchical
  M2:
    components: [lpg, rdf, hybrid]
    agent_type: single
  M3:
    components: [lpg, hybrid]
    agent_type: hierarchical
  M4:
    components: [rdf, hybrid]
    agent_type: hierarchical

ablation_experiments:
  A1: [lpg]
  A2: [rdf]
  A3: [hybrid]
  A4: [lpg, rdf]
  A5: [lpg, hybrid]
  A6: [rdf, hybrid]

metrics:
  - answer_relevance
  - hallucination
  - query_router_accuracy
  - context_precision
  - conflict_resolution_score
  - context_token_efficiency    # §5.4.4.1 CTE (KGC2026 인사이트)
  - kvcache_cost_per_query      # §5.4.4.1 KVCache 비용
  - quality_cost_pareto_score   # §5.4.4.1 파레토 효율성

thresholds:
  query_router_accuracy: 0.95
  conflict_resolution_score: 0.95
  hallucination_rate: 0.05
  quality_cost_pareto_score: 0.80  # 파레토 최적 대비 80% 이상
  kvcache_cost_monthly_increase: 0.10  # 전월 대비 10% 이내 증가
```

### H.3 데이터 Export CLI

Opik 트레이스 및 데이터셋을 Export합니다.

```bash
# 트레이스 Export
docker exec agent-jupyter-container python -m src.cli.export --traces

# 데이터셋 Export
docker exec agent-jupyter-container python -m src.cli.export --datasets

# 특정 기간 트레이스 Export
docker exec agent-jupyter-container python -m src.cli.export --traces \
    --start-date 2026-01-01 \
    --end-date 2026-01-31
```

**명령어 옵션:**

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--traces` | Opik 트레이스 Export | - |
| `--datasets` | 모든 데이터셋 Export | - |
| `--output` | 출력 디렉토리 | `exports/` |
| `--format` | 출력 형식 (`json`, `csv`, `parquet`) | `json` |
| `--start-date` | 시작 일자 (YYYY-MM-DD) | - |
| `--end-date` | 종료 일자 (YYYY-MM-DD) | - |

### H.4 Docker 환경 설정

SEOCHO 컨테이너 환경 구성을 위한 명령어입니다.

```bash
# 전체 스택 시작
docker-compose up -d --build

# 개별 서비스 시작
docker-compose up -d neo4j opik

# Neo4j 플러그인 설치 (APOC, GDS)
./setup_neo4j_plugins.sh

# Opik 설정
./setup-docker-and-opik.sh

# 로그 확인
docker-compose logs -f agent-service
```

**Docker Compose 서비스 구성:**

| 서비스 | 포트 | 설명 |
|--------|------|------|
| `graphrag-neo4j` | 7474, 7687 | Neo4j/DozerDB |
| `agent-service` | 8001 | FastAPI Agent Server |
| `agent-studio` | 8501 | Streamlit UI |
| `opik` | 5173 | LLM Observability |
| `lancedb` | - | 벡터 데이터베이스 (Volume) |

### H.5 개발 환경 CLI

로컬 개발 환경 구성을 위한 명령어입니다.

```bash
# 가상환경 생성 및 의존성 설치
./setup.sh

# 또는 수동 설치
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 테스트 실행
pytest tests/ -v --cov=src

# 코드 품질 검사
make lint

# 전체 빌드
make build
```

**Makefile 타겟:**

| 타겟 | 설명 |
|------|------|
| `make build` | Docker 이미지 빌드 |
| `make up` | 컨테이너 시작 |
| `make down` | 컨테이너 중지 |
| `make test` | 테스트 실행 |
| `make lint` | 코드 품질 검사 |
| `make index` | 인덱스 빌드 |
| `make evaluate` | 평가 실행 |
| `make clean` | 임시 파일 정리 |

### H.6 CLI 사용 예시 (E2E 워크플로우)

전체 평가 파이프라인 실행 예시:

```bash
#!/bin/bash
# evaluate_pipeline.sh

set -e

echo "🔧 Step 1: 환경 설정"
docker-compose up -d

echo "📊 Step 2: 인덱스 빌드"
docker exec agent-jupyter-container python -m src.cli.index --all

echo "🧪 Step 3: Macro 실험 실행"
docker exec agent-jupyter-container python -m src.cli.evaluate --macro \
    --dataset datasets/production_queries.json \
    --output results/macro_$(date +%Y%m%d)/

echo "🔬 Step 4: Ablation 실험 실행"
docker exec agent-jupyter-container python -m src.cli.evaluate --ablation \
    --output results/ablation_$(date +%Y%m%d)/

echo "📤 Step 5: 결과 Export"
docker exec agent-jupyter-container python -m src.cli.export --traces \
    --output exports/traces_$(date +%Y%m%d).json

echo "✅ 평가 완료!"
echo "결과 확인: results/ 디렉토리"
echo "Opik 대시보드: http://localhost:5173"
```

### H.7 CLI 출력 형식

**평가 결과 JSON 스키마:**

```json
{
  "experiment_id": "M1",
  "timestamp": "2026-02-03T10:30:00Z",
  "config": {
    "components": ["lpg", "rdf", "hybrid"],
    "agent_type": "hierarchical"
  },
  "metrics": {
    "answer_relevance": 4.2,
    "hallucination_rate": 0.03,
    "query_router_accuracy": 0.92,
    "context_precision": 0.87,
    "conflict_resolution_score": 0.96,
    "execution_accuracy": 0.85,
    "p95_response_time_ms": 1850
  },
  "cost_metrics": {
    "context_token_efficiency": 0.0042,
    "kvcache_cost_per_query_usd": 0.0087,
    "avg_context_tokens": 1024,
    "avg_prompt_tokens": 3200,
    "cache_hit_rate": 0.78,
    "quality_cost_pareto_score": 0.85,
    "token_breakdown": {
      "lpg_context_tokens": 380,
      "rdf_context_tokens": 0,
      "vector_context_tokens": 644
    }
  },
  "quality_gates": {
    "query_router_accuracy": {"threshold": 0.95, "passed": false},
    "conflict_resolution_score": {"threshold": 0.95, "passed": true},
    "hallucination_rate": {"threshold": 0.05, "passed": true}
  },
  "note": "아래는 Quality Gate 부분 실패 예시입니다 (query_router_accuracy 0.92 < 임계값 0.95):",
  "summary": {
    "total_queries": 500,
    "successful": 485,
    "failed": 15,
    "avg_latency_ms": 1234
  }
}
```

---

### H.8 Opik Cost-Quality Analysis 대시보드 설정 (KGC2026 인사이트 반영)

> **📌 출처:** 정이태, "Mastering Graph Agents: Unifying LPG & RDF Workflows with Opik for Financial GraphRAG" (KGC2026)
> **목적:** LPG/RDF 컨텍스트의 토큰 비용 대비 답변 품질 효율성을 Opik 대시보드에서 시각화
> **참조:** PRD_05 §5.4.4.1 Context Token Efficiency 메트릭 정의

#### H.8.1 커스텀 패널 구성

Opik 프로젝트 `datanexus-eval`에 아래 4개 커스텀 패널을 추가합니다.

| 패널 ID | 패널명 | 차트 유형 | X축 | Y축 | 필터 |
|---------|--------|----------|-----|-----|------|
| **CQ-01** | CTE Comparison | Grouped Bar | Ablation ID (A1~A6) | CTE (score/token) | experiment_type = "ablation" |
| **CQ-02** | Cost-Quality Scatter | Scatter Plot | kvcache_cost_per_query (USD) | answer_relevance | 최근 30일 |
| **CQ-03** | Token Breakdown | Stacked Bar | Ablation ID (A1~A6) | context_tokens (LPG/RDF/Vector) | experiment_type = "ablation" |
| **CQ-04** | KVCache Cost Trend | Time Series Line | 일/주별 timestamp | avg kvcache_cost_per_query | 최근 90일 |

#### H.8.2 Opik 메트릭 로깅 스키마

Ablation 실험 실행 시 Opik에 전송하는 cost_metrics 데이터 구조:

```python
# evaluation/integrations/opik_cost_panels.py
COST_METRICS_SCHEMA = {
    "context_token_efficiency": {
        "type": "float",
        "description": "AnswerRelevance / context_tokens",
        "unit": "score/token",
        "panel": "CQ-01"
    },
    "kvcache_cost_per_query_usd": {
        "type": "float",
        "description": "cache_creation × rate + cache_read × rate + uncached × rate",
        "unit": "USD",
        "panel": "CQ-02, CQ-04"
    },
    "quality_cost_pareto_score": {
        "type": "float",
        "description": "파레토 프론티어 대비 정규화 거리 (0~1)",
        "unit": "dimensionless",
        "panel": "CQ-02"
    },
    "token_breakdown": {
        "type": "object",
        "properties": {
            "lpg_context_tokens": {"type": "int", "panel": "CQ-03"},
            "rdf_context_tokens": {"type": "int", "panel": "CQ-03"},
            "vector_context_tokens": {"type": "int", "panel": "CQ-03"}
        }
    }
}
```

#### H.8.3 대시보드 레이아웃

```txt
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Opik: Cost-Quality Analysis Dashboard                       │
├────────────────────────────────────┬────────────────────────────────────────┤
│  [CQ-01] CTE Comparison            │  [CQ-02] Cost-Quality Scatter          │
│                                    │                                        │
│  ▐▐▐▐▐  A1 (LPG)     ← 높은 CTE │  ●A1    ●A5      ← 파레토 프론티어   │
│  ▐▐▐    A2 (RDF)     ← 낮은 CTE │     ●A4                               │
│  ▐▐▐▐   A3 (HYBRID)              │  ●A2       ●A3                        │
│  ▐▐▐▐▐  A4 (LPG+RDF)            │        ●A6                             │
│  ▐▐▐▐▐▐ A5 (LPG+HYB)            │  Cost →              Quality ↑         │
│  ▐▐▐    A6 (RDF+HYB) ← 최저 CTE │                                        │
├────────────────────────────────────┼────────────────────────────────────────┤
│  [CQ-03] Token Breakdown           │  [CQ-04] KVCache Cost Trend            │
│                                    │                                        │
│  A1 ████████░░░░░░ LPG only       │     ╱‾‾╲                               │
│  A2 ░░░░░░████████ RDF only       │  ──╱    ╲──── target                  │
│  A3 ░░░░░░░░▓▓▓▓▓▓ Vector only   │ ╱         ╲──                         │
│  A4 ████████████████ LPG+RDF      │                                        │
│  A5 ████████▓▓▓▓▓▓ LPG+Vector    │  Week 1  Week 2  Week 3  Week 4       │
│  A6 ░░░░░░████████▓▓▓▓ RDF+Vec   │                                        │
│                                    │  ── Actual  ---- Target               │
│  ████ LPG  ████ RDF  ▓▓▓▓ Vector │                                        │
└────────────────────────────────────┴────────────────────────────────────────┘
```

#### H.8.4 알림 규칙 (Alert Rules)

| 알림 ID | 조건 | 심각도 | 조치 |
|---------|------|--------|------|
| **COST-ALERT-01** | CTE(A1) < CTE(A2) (LPG가 RDF보다 비효율적) | Warning | LPG Cypher 결과 포맷 검토 |
| **COST-ALERT-02** | KVCache Cost 주간 증가 > 20% | SEV-3 | 캐시 미스 원인 조사 (§22.3) |
| **COST-ALERT-03** | Quality-Cost Pareto Score < 0.6 | SEV-2 | 현재 구성 비용 대비 품질 급락, 아키텍처 재검토 |
| **COST-ALERT-04** | 단일 실험의 avg_context_tokens > 5,000 | Warning | 컨텍스트 프루닝 전략 강화 (§4.3.10.10.3) |

#### H.8.5 도입 체크리스트

| 구현 항목 | 담당 | 예상 공수 | 우선순위 |
|----------|------|-----------|---------|
| Opik 프로젝트에 cost_metrics 스키마 등록 | Backend Core | 0.5일 | 높음 |
| CQ-01~CQ-04 커스텀 패널 생성 | Backend Core | 1일 | 높음 |
| ContextTokenEfficiencyMetric 클래스 구현 (§5.4.4.1) | Agent Logic | 2일 | 높음 |
| Ablation 실험 파이프라인에 cost_metrics 로깅 연동 | Backend Core | 1일 | 높음 |
| 알림 규칙 (COST-ALERT-01~04) 설정 | DevOps | 0.5일 | 중간 |
| **합계** | | **5일** | |

---

**참고:** 본 CLI 명세는 SEOCHO 프로젝트 `feature-kgbuild` 브랜치 (https://github.com/tteon/seocho/tree/feature-kgbuild) 기준입니다. 최신 버전은 GitHub 리포지토리를 참조하세요.
