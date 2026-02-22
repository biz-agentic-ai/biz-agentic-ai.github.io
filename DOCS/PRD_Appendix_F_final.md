## 부록 F: 기술 구현 명세 (Claude Code 개발용)

### F.1 프로젝트 디렉토리 구조

```txt
datanexus/
├── backend/
│ ├── app/
│ │ ├── __init__.py
│ │ ├── main.py # FastAPI 진입점
│ │ ├── config.py # 설정 관리
│ │ ├── api/
│ │ │ ├── __init__.py
│ │ │ ├── deps.py # 의존성 주입
│ │ │ └── v1/
│ │ │ ├── __init__.py
│ │ │ ├── router.py # 라우터 집합
│ │ │ ├── query.py # 질의 처리 API
│ │ │ ├── ontology.py # 온톨로지 관리 API
│ │ │ ├── sync.py # 동기화 API
│ │ │ ├── cq.py # CQ 검증 API
│ │ │ └── benchmark.py # 벤치마크 API
│ │ ├── models/
│ │ │ ├── __init__.py
│ │ │ ├── query.py # 질의 Pydantic 모델
│ │ │ ├── ontology.py # 온톨로지 모델
│ │ │ ├── cq.py # CQ 모델
│ │ │ └── benchmark.py # 벤치마크 모델
│ │ ├── services/
│ │ │ ├── __init__.py
│ │ │ ├── query_router.py # Query Router Agent
│ │ │ ├── schema_enforcer.py # Schema Enforcer
│ │ │ ├── impact_analyzer.py # Impact Analyzer
│ │ │ ├── cq_validator.py # CQ Validator
│ │ │ ├── skos_handler.py # SKOS Import/Export
│ │ │ └── sync_pipeline.py # 동기화 파이프라인
│ │ ├── integrations/
│ │ │ ├── datahub/
│ │ │ │ ├── client.py # DataHub API
│ │ │ │ └── glossary.py # Glossary 관리
│ │ │ ├── vanna/
│ │ │ │ └── client.py # Vanna AI
│ │ │ ├── dozerdb/
│ │ │ │ └── client.py # DozerDB/Neo4j
│ │ │ ├── aperag/
│ │ │ │ └── client.py # ApeRAG
│ │ │ └── shaper/
│ │ │ ├── client.py # Shaper REST API 클라이언트
│ │ │ ├── promotion.py # Dashboard Promotion 서비스
│ │ │ └── security.py # JWT RLS 토큰 브릿지
│ │ └── db/
│ │ ├── session.py # DB 세션 관리
│ │ └── models.py # SQLAlchemy 모델
│ ├── tests/
│ │ ├── conftest.py
│ │ ├── unit/
│ │ ├── integration/
│ │ ├── cq/
│ │ └── e2e/
│ ├── alembic/
│ ├── scripts/
│ ├── requirements.txt
│ ├── requirements-dev.txt
│ └── Dockerfile
├── frontend/
│ ├── src/
│ │ ├── app/ # Next.js App Router
│ │ ├── components/
│ │ ├── lib/
│ │ └── types/
│ ├── package.json
│ └── Dockerfile
├── docker/
│ ├── docker-compose.yml
│ └── docker-compose.test.yml
├── .github/workflows/
│ └── test_pipeline.yml
├── docs/api/openapi.yaml
├── .env.example
└── README.md
```

---

### F.2 기술 스택 버전

#### F.2.1 Backend (Python)

| 카테고리 | 패키지 | 버전 | 용도 |
| :--- | :--- | :--- | :--- |
| **Framework** | fastapi | 0.109.0 | REST API |
| | uvicorn | 0.27.0 | ASGI 서버 |
| | pydantic | 2.5.3 | 데이터 검증 |
| **Database** | sqlalchemy | 2.0.25 | ORM |
| | alembic | 1.13.1 | 마이그레이션 |
| | asyncpg | 0.29.0 | PostgreSQL 비동기 |
| **AI/ML** | langchain | 0.1.4 | LLM 오케스트레이션 |
| | langgraph | 0.0.20 | 에이전트 워크플로우 |
| | vanna | 2.0.2 | NL2SQL (Agent-based API) |
| | openai | 1.10.0 | OpenAI API |
| | anthropic | 0.18.0 | Claude API |
| **Graph DB** | neo4j | 5.26.3 | DozerDB 클라이언트 |
| **Vector DB** | qdrant-client | 1.7.3 | Qdrant |
| **RDF** | rdflib | 7.0.0 | SKOS 처리 |
| | pyshacl | 0.25.0 | SHACL 검증 |
| **Task Queue** | celery | 5.3.6 | 백그라운드 작업 |
| | redis | 5.0.1 | 브로커/캐시 |
| **Testing** | pytest | 7.4.4 | 테스트 |
| | pytest-asyncio | 0.23.3 | 비동기 테스트 |

#### F.2.2 Frontend (Node.js)

| 카테고리 | 패키지 | 버전 |
| :--- | :--- | :--- |
| **Runtime** | node | 20.11.0 |
| **Framework** | next | 14.1.0 |
| | react | 18.2.0 |
| | typescript | 5.3.3 |
| **Styling** | tailwindcss | 3.4.1 |
| **State** | zustand | 4.5.0 |
| | @tanstack/react-query | 5.17.19 |
| **Chart** | recharts | 2.10.4 |

#### F.2.3 Infrastructure

| 기술 | 버전 | 용도 |
| :--- | :--- | :--- |
| PostgreSQL | 16.1 | 관계형 DB |
| Redis | 7.2 | 캐시/브로커 |
| DozerDB | 5.26.3.0 | 지식 그래프 (Neo4j 5.26.3 호환) |
| Qdrant | 1.7.4 | 벡터 검색 |
| DataHub | 1.3.0.1 | 거버넌스 |
| ApeRAG | 0.5.0-alpha.14 | GraphRAG (DeepRAG) |
| **Shaper** | **0.12.9** | **SQL 기반 대시보드 & 자동화 보고 (DuckDB 기반 BI)** |
| Docker | 24.0 | 컨테이너 |
| **KanVibe** | latest | AI 에이전트 태스크 관리 칸반 보드 (Self-hosted) |

#### F.2.4 KanVibe 개발 환경 (태스크 관리)

> **📌 상세:** Implementation Strategy §18 참조

| 기술 | 버전 | 용도 |
| :--- | :--- | :--- |
| KanVibe | latest | AI 코딩 에이전트 태스크 칸반 보드 |
| PostgreSQL (KanVibe) | 16 | KanVibe 전용 DB (포트 4886) |
| Node.js | >= 22 | KanVibe 런타임 |
| tmux / zellij | latest | 터미널 멀티플렉서 (브라우저 터미널) |

| 서비스 | 포트 | 비고 |
| :--- | :--- | :--- |
| KanVibe Web | 4885 | DataNexus 인프라 포트와 충돌 없음 |
| KanVibe PostgreSQL | 4886 | DataNexus 인프라 포트와 충돌 없음 |

> **리포지토리:** https://github.com/rookedsysc/kanvibe

---

### F.3 API 명세 (OpenAPI 3.0 요약)

#### F.3.1 Query API

| Method | Endpoint | 설명 | Request | Response |
| :--- | :--- | :--- | :--- | :--- |
| POST | `/api/v1/query` | 자연어 질의 처리 | `{question, tenant_id?, user_context?}` | `{query_id, route_type, confidence, generated_sql, result, response_time_ms}` |

#### F.3.2 Ontology API

| Method | Endpoint | 설명 |
| :--- | :--- | :--- |
| GET | `/api/v1/ontology/terms` | Term 목록 조회 |
| POST | `/api/v1/ontology/terms` | Term 생성 |
| GET | `/api/v1/ontology/terms/{urn}` | Term 상세 조회 |
| PUT | `/api/v1/ontology/terms/{urn}` | Term 수정 |
| DELETE | `/api/v1/ontology/terms/{urn}` | Term 삭제 |
| POST | `/api/v1/ontology/validate` | 품질 검증 |
| POST | `/api/v1/ontology/skos/export` | SKOS 내보내기 |
| POST | `/api/v1/ontology/skos/import` | SKOS 가져오기 |

#### F.3.3 Schema API

| Method | Endpoint | 설명 |
| :--- | :--- | :--- |
| POST | `/api/v1/schema/validate-triple` | 트리플 검증 |
| GET | `/api/v1/schema/review-queue` | 검토 대기열 조회 |
| POST | `/api/v1/schema/review-queue` | 검토 처리 |

#### F.3.4 CQ API

| Method | Endpoint | 설명 |
| :--- | :--- | :--- |
| GET | `/api/v1/cq` | CQ 목록 |
| POST | `/api/v1/cq` | CQ 생성 |
| POST | `/api/v1/cq/validate` | CQ 검증 실행 |

#### F.3.5 Sync & Benchmark API

| Method | Endpoint | 설명 |
| :--- | :--- | :--- |
| POST | `/api/v1/sync/trigger` | 동기화 실행 |
| GET | `/api/v1/sync/jobs/{id}` | 작업 상태 |
| POST | `/api/v1/benchmark/run` | 벤치마크 실행 |
| GET | `/api/v1/benchmark/results` | 결과 목록 |

#### F.3.6 Dashboard & Report API (Shaper 연동)

| Method | Endpoint | 설명 | Request | Response |
| :--- | :--- | :--- | :--- | :--- |
| POST | `/api/v1/dashboard/promote` | NL2SQL 결과를 Shaper 대시보드로 승격 | `{query_log_id, name, schedule?}` | `{dashboard_id, url, embed_code, lineage_id}` |
| GET | `/api/v1/dashboard` | 대시보드 목록 조회 | — | `{dashboards[]}` |
| GET | `/api/v1/dashboard/{id}` | 대시보드 상세 조회 | — | `{id, name, sql, chart_type, schedule, drift_status}` |
| DELETE | `/api/v1/dashboard/{id}` | 대시보드 삭제 | — | `{success}` |
| POST | `/api/v1/dashboard/{id}/embed-token` | 임베디드 JWT 토큰 생성 | `{user_context}` | `{token, expires_at}` |
| POST | `/api/v1/dashboard/{id}/report` | 즉시 리포트 생성 (PDF/CSV/Excel) | `{format, filters?}` | `{report_url, format}` |
| GET | `/api/v1/dashboard/schedules` | 예약 리포트 목록 | — | `{schedules[]}` |
| POST | `/api/v1/dashboard/{id}/schedule` | 예약 리포트 설정 | `{cron, formats[], recipients[]}` | `{schedule_id}` |

#### F.3.7 Dashboard Lineage & Staleness API (§3.9.7~3.9.9)

| Method | Endpoint | 설명 | Request | Response |
| :--- | :--- | :--- | :--- | :--- |
| GET | `/api/v1/dashboard/{id}/lineage` | 대시보드 Promotion Lineage 조회 | — | `{lineage_id, original_nl_query, drift_status, referenced_glossary_terms[], stale_reason?}` |
| GET | `/api/v1/dashboard/lineage` | 전체 Lineage 목록 (Drift 상태 필터) | `?drift_status=STALE` | `{lineages[]}` |
| POST | `/api/v1/dashboard/{id}/re-promote` | 기존 대시보드 SQL 교체 (RE_PROMOTE) | `{query_log_id}` | `{dashboard_id, new_sql_hash, drift_status: "SYNCED"}` |
| POST | `/api/v1/dashboard/{id}/return-to-chat` | Dashboard → Chat 복귀 세션 생성 | — | `{session_id, context: {original_query, drift_status, modifications?}}` |
| GET | `/api/v1/dashboard/staleness/summary` | STALE 대시보드 요약 통계 | — | `{total_stale, by_glossary_term: {term_urn: count}}` |

---

### F.4 데이터베이스 DDL

#### F.4.1 핵심 테이블

```sql
-- 테넌트 관리
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    dozerdb_database VARCHAR(100) NOT NULL,
    datahub_glossary_urn VARCHAR(200),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 질의 로그
CREATE TABLE query_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    question TEXT NOT NULL,
    route_type VARCHAR(20) NOT NULL,
    template_id VARCHAR(50),
    confidence_score DECIMAL(3,2),
    generated_sql TEXT,
    execution_success BOOLEAN,
    response_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Competency Questions
CREATE TABLE competency_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cq_id VARCHAR(50) UNIQUE NOT NULL,
    cq_type VARCHAR(10) NOT NULL CHECK (cq_type IN ('SCQ', 'FCQ', 'RCQ', 'VCQ', 'MpCQ')),
    priority VARCHAR(10) NOT NULL CHECK (priority IN ('Critical', 'High', 'Medium', 'Low')),
    question TEXT NOT NULL,
    expected_concepts JSONB DEFAULT '[]',
    expected_relationships JSONB DEFAULT '[]',
    pass_criteria JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- CQ 검증 결과
CREATE TABLE cq_validation_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    validation_run_id UUID,
    cq_id VARCHAR(50) REFERENCES competency_questions(cq_id),
    status VARCHAR(10) CHECK (status IN ('PASS', 'FAIL', 'SKIP')),
    concept_coverage DECIMAL(3,2),
    relationship_coverage DECIMAL(3,2),
    llm_score DECIMAL(3,2),
    details JSONB DEFAULT '{}',
    validated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Schema Review Queue
CREATE TABLE schema_review_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject VARCHAR(500) NOT NULL,
    predicate VARCHAR(100) NOT NULL,
    object VARCHAR(500) NOT NULL,
    subject_status VARCHAR(10),
    object_status VARCHAR(10),
    similarity_score DECIMAL(3,2),
    review_status VARCHAR(20) DEFAULT 'PENDING',
    reviewed_by VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 동기화 작업
CREATE TABLE sync_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_type VARCHAR(30) NOT NULL,
    scope VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    total_items INTEGER DEFAULT 0,
    processed_items INTEGER DEFAULT 0,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 벤치마크 결과
CREATE TABLE benchmark_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    benchmark_id VARCHAR(50) UNIQUE NOT NULL,
    test_set_name VARCHAR(100) NOT NULL,
    execution_accuracy DECIMAL(5,2),
    exact_match_accuracy DECIMAL(5,2),
    p95_response_time_ms INTEGER,
    ontology_coverage DECIMAL(5,2),
    total_queries INTEGER NOT NULL,
    passed_queries INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Cypher 템플릿
CREATE TABLE cypher_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    template_query TEXT NOT NULL,
    parameter_schema JSONB NOT NULL,
    matching_patterns JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT true,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 시스템 설정
CREATE TABLE system_config (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

### F.5 핵심 클래스 인터페이스

#### F.5.1 Enums

```python
# app/models/enums.py
from enum import Enum

class RouteType(str, Enum):
    DETERMINISTIC = "DETERMINISTIC"
    HYBRID = "HYBRID"
    PROBABILISTIC = "PROBABILISTIC"

class TripleStatus(str, Enum):
    ACCEPT = "ACCEPT"
    REMAP = "REMAP"
    REVIEW = "REVIEW"
    REJECT = "REJECT"

class TripleAction(str, Enum):
    STORE = "STORE"
    QUEUE = "QUEUE"
    DISCARD = "DISCARD"

class CQType(str, Enum):
    SCQ = "SCQ"
    FCQ = "FCQ"
    RCQ = "RCQ"
    VCQ = "VCQ"
    MpCQ = "MpCQ"

class CQStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"

class UpdateStrategy(str, Enum):
    INCREMENTAL = "INCREMENTAL"
    PARTIAL_REBUILD = "PARTIAL_REBUILD"
    FULL_REBUILD = "FULL_REBUILD"
```

#### F.5.2 Service Interfaces

```python
# app/services/interfaces.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class IQueryRouter(ABC):
    @abstractmethod
    async def classify(self, query: str, context: Optional[Dict] = None) -> Dict:
        """질의 분류 및 라우팅 결정"""
        pass

    @abstractmethod
    async def execute_template(self, template_id: str, params: Dict) -> Dict:
        """Cypher 템플릿 실행"""
        pass

class ISchemaEnforcer(ABC):
    @abstractmethod
    async def validate_triple(self, triple: Dict) -> Dict:
        """트리플 스키마 검증"""
        pass

    @abstractmethod
    async def get_review_queue(self, limit: int = 100) -> List[Dict]:
        """검토 대기열 조회"""
        pass

class IImpactAnalyzer(ABC):
    @abstractmethod
    async def analyze_change_impact(self, event: Dict) -> Dict:
        """변경 영향 분석"""
        pass

class ICQValidator(ABC):
    @abstractmethod
    async def validate(self, cq: Dict) -> Dict:
        """CQ 검증"""
        pass

    @abstractmethod
    async def validate_all(self, cq_ids: Optional[List[str]] = None) -> Dict:
        """전체 CQ 검증"""
        pass

class ISKOSHandler(ABC):
    @abstractmethod
    async def export_to_skos(self, glossary_urn: str, format: str = "turtle") -> str:
        """SKOS 내보내기"""
        pass

    @abstractmethod
    async def import_from_skos(self, rdf_content: str, target_urn: str) -> Dict:
        """SKOS 가져오기"""
        pass

class ISyncPipeline(ABC):
    @abstractmethod
    async def trigger_sync(self, scope: str, target_urns: Optional[List[str]] = None) -> str:
        """동기화 실행"""
        pass

class IDataHubClient(ABC):
    @abstractmethod
    async def get_glossary_terms(self, glossary_urn: Optional[str] = None) -> List[Dict]:
        pass

    @abstractmethod
    async def create_term(self, term_data: Dict) -> str:
        pass

class IVannaClient(ABC):
    @abstractmethod
    async def train_ddl(self, ddl: str) -> bool:
        pass

    @abstractmethod
    async def generate_sql(self, question: str) -> str:
        pass

class IDozerDBClient(ABC):
    @abstractmethod
    async def execute_cypher(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        pass
```

---

### F.6 환경 변수 템플릿

```bash
# .env.example

# Application
APP_NAME=DataNexus
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO
SECRET_KEY=change-in-production

# API Server
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=datanexus
POSTGRES_USER=datanexus
POSTGRES_PASSWORD=changeme
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_URL=redis://${REDIS_HOST}:${REDIS_PORT}/0
CELERY_BROKER_URL=redis://${REDIS_HOST}:${REDIS_PORT}/1

# DozerDB
DOZERDB_URI=bolt://localhost:7687
DOZERDB_USER=neo4j
DOZERDB_PASSWORD=changeme

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333

# DataHub
DATAHUB_GMS_URL=http://localhost:8080
DATAHUB_TOKEN=

# Vanna AI
VANNA_API_KEY=
VANNA_MODEL=gpt-4

# LLM
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
LLM_PROVIDER=openai

# Quality Gates
QG_ROUTER_ACCURACY=0.95
QG_SCHEMA_COMPLIANCE=0.90
QG_CRITICAL_CQ_PASS=1.0
QG_OVERALL_CQ_PASS=0.80
QG_EXECUTION_ACCURACY=0.85
QG_P95_RESPONSE_TIME_MS=3000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

### F.7 Docker Compose 설정

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
 backend:
    build: ../backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://datanexus:changeme@postgres:5432/datanexus
      - REDIS_URL=redis://redis:6379/0
      - DOZERDB_URI=bolt://dozerdb:7687
      - QDRANT_HOST=qdrant
      - SHAPER_BASE_URL=http://shaper:5454
      - SHAPER_JWT_SECRET=${SHAPER_JWT_SECRET:-changeme}
    depends_on:
      - postgres
      - redis
      - dozerdb
      - qdrant
      - shaper

 frontend:
    build: ../frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
    depends_on:
      - backend

 celery:
    build: ../backend
    command: celery -A app.worker worker --loglevel=info
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/1
    depends_on:
      - backend
      - redis

 postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: datanexus
      POSTGRES_USER: datanexus
      POSTGRES_PASSWORD: changeme
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U datanexus"]
      interval: 5s
      retries: 5

 redis:
    image: redis:7.2-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

 dozerdb:
    image: dozerdb/dozerdb:5.26.3
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/changeme
    volumes:
      - dozerdb_data:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7474"]
      interval: 10s
      retries: 5

 qdrant:
    image: qdrant/qdrant:v1.7.4
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

 shaper:
    image: taleshape/shaper:v0.12.9
    ports:
      - "5454:5454"
    volumes:
      - shaper_data:/data
    environment:
      - SHAPER_JWT_SECRET=${SHAPER_JWT_SECRET:-changeme}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5454/health"]
      interval: 10s
      retries: 5

volumes:
 postgres_data:
 redis_data:
 dozerdb_data:
 qdrant_data:
 shaper_data:

networks:
 default:
    name: datanexus-network
```

---

### F.8 의존성 목록

#### F.8.1 requirements.txt

```txt
# Core
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6
python-dotenv==1.0.0

# Database
sqlalchemy[asyncio]==2.0.25
alembic==1.13.1
asyncpg==0.29.0

# AI/ML
langchain==0.1.4
langchain-openai==0.0.5
langgraph==0.0.20
openai==1.10.0
anthropic==0.18.0
vanna>=2.0.0  # PRD 전체 Vanna 2.0 기준 설계 (부록 B.8 참조). 0.5.x API 비호환

# Graph/Vector
neo4j==5.15.0  # Python Driver 버전. DozerDB v5.26.3.0 서버와 호환성 검증 필요 (PRD_01 §2 참조)
qdrant-client==1.7.3

# RDF
rdflib==7.0.0
pyshacl==0.25.0

# HTTP
httpx==0.26.0
aiohttp==3.9.1

# Task Queue
celery==5.3.6
redis==5.0.1

# Utils
pyyaml==6.0.1
structlog==24.1.0
```

#### F.8.2 requirements-dev.txt

```txt
-r requirements.txt

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0
pytest-mock==3.12.0
hypothesis==6.92.2

# Code Quality
black==23.12.1
isort==5.13.2
flake8==7.0.0
mypy==1.8.0
pre-commit==3.6.0
```

---

### F.9 Claude Code 활용 가이드

#### F.9.1 Phase별 프롬프트

**Phase 1: 스캐폴딩**
```txt
"PRD 부록 F.1의 프로젝트 구조에 따라 FastAPI 백엔드를 생성해줘.
requirements.txt, Dockerfile도 포함해줘."
```

**Phase 2: 데이터베이스**
```txt
"PRD 부록 F.4의 DDL로 Alembic 마이그레이션과 SQLAlchemy 모델을 구현해줘."
```

**Phase 3: API 구현**
```txt
"PRD 부록 F.3의 API 명세로 FastAPI 라우터를 구현해줘.
Pydantic 모델도 함께 생성해줘."
```

**Phase 4: 핵심 서비스**
```txt
"PRD 부록 F.5의 인터페이스로 QueryRouter를 구현해줘.
섹션 5.3의 테스트 케이스도 함께 작성해줘."
```

**Phase 5: 통합 테스트**
```txt
"PRD 섹션 5.3의 테스트 전략으로 통합 테스트를 구현해줘.
docker-compose.test.yml 기반 테스트 환경도 구성해줘."
```

#### F.9.2 개발 명령어 참고

| 단계 | 명령어 |
| :--- | :--- |
| 프로젝트 초기화 | `mkdir -p backend/app/{api/v1,models,services,integrations,db}` |
| 의존성 설치 | `pip install -r requirements.txt` |
| DB 마이그레이션 | `alembic upgrade head` |
| 테스트 실행 | `pytest tests/ -v --cov=app` |
| Docker 실행 | `docker-compose -f docker/docker-compose.yml up -d` |
| API 문서 확인 | `http://localhost:8000/docs` |

---


#### F.9.3 실전 사용 팁 (운영 가이드)

- 병렬 작업을 적극 활용합니다: 3~5개의 git worktree를 병렬로 운영해 컨텍스트를 분리하고, 작업 전환 비용을 최소화합니다.
- 복잡한 작업은 Plan Mode로 시작합니다: 계획(설계/작업 순서/테스트 전략)을 먼저 확정한 뒤 구현을 진행하고, 흔들리면 즉시 Plan으로 복귀합니다.
- CLAUDE.md(프로젝트 규칙)를 지속적으로 업데이트합니다: 반복되는 실수/규칙/컨벤션을 축적해 품질을 안정화합니다.
- 반복 작업은 Skill/Slash Command로 표준화합니다: 하루 1회 이상 반복되는 작업은 자동화 명령으로 만들고 레포에 커밋합니다.
- 버그 수정은 로그 중심으로 위임합니다: docker logs/CI 실패 로그/재현 절차를 제공하고 “failing tests를 통과시켜라”처럼 목표를 명확히 전달합니다.
- 프롬프트 품질을 끌어올립니다: 모호함을 제거하고, “테스트 통과 전 PR 금지”, “diff로 증명” 같은 품질 게이트를 명시합니다.
- 서브에이전트를 활용해 컨텍스트를 관리합니다: 분석/리뷰/실행을 역할로 분리해 메인 컨텍스트를 얇게 유지합니다.
- 데이터/분석 CLI를 적극 연결합니다: bq 등 CLI 기반의 즉석 분석을 Skill로 만들어 개발/검증 루프를 단축합니다.

### F.10 구현 체크리스트

| 단계 | 항목 | 예상 공수 | 우선순위 |
| :--- | :--- | :--- | :--- |
| **스캐폴딩** | 프로젝트 구조 생성 | 0.5일 | P0 |
| | Dockerfile, docker-compose.yml | 0.5일 | P0 |
| | requirements.txt | 0.25일 | P0 |
| | .env.example | 0.25일 | P0 |
| **데이터베이스** | Alembic 초기화 | 0.5일 | P0 |
| | SQLAlchemy 모델 정의 | 1일 | P0 |
| | 초기 마이그레이션 | 0.5일 | P0 |
| **API Layer** | FastAPI 기본 설정 | 0.5일 | P0 |
| | Query API 구현 | 1일 | P1 |
| | Ontology API 구현 | 2일 | P1 |
| | Schema API 구현 | 1일 | P1 |
| | CQ API 구현 | 1일 | P1 |
| | Sync/Benchmark API | 1일 | P2 |
| **Services** | IQueryRouter 구현 | 3일 | P1 |
| | ISchemaEnforcer 구현 | 2일 | P1 |
| | ICQValidator 구현 | 2일 | P1 |
| | ISKOSHandler 구현 | 2일 | P2 |
| | ISyncPipeline 구현 | 2일 | P2 |
| **Integrations** | DataHub Client | 2일 | P1 |
| | Vanna Client | 1일 | P1 |
| | DozerDB Client | 1일 | P1 |
| **Testing** | Unit Tests | PRD 섹션 5.3 참조 | P1 |
| | Integration Tests | PRD 섹션 5.3 참조 | P1 |
| | E2E Tests | PRD 섹션 5.3 참조 | P2 |
| **총계** | | **약 25일** | |

**권장 진행 순서:** 스캐폴딩 → 데이터베이스 → API Layer → Services → Integrations → Testing

---

**Note:** 본 문서는 즉시 개발 착수가 가능하도록 프로젝트 구조, 의존성, OpenAPI 명세, DB DDL, 핵심 인터페이스, Docker/환경 설정을 포함합니다.

