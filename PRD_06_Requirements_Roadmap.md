## 6. 기능 요구사항 (Functional Requirements)

DataNexus가 충족해야 할 구체적인 기능적 요구사항을 카테고리별로 정리합니다.

### 6.1 데이터 카탈로그 (FR-CAT)

| ID | 요구사항 | 설명 | 우선순위 |
|----|----------|------|----------|
| FR-CAT-01 | 통합 메타데이터 저장 | 다양한 소스(RDBMS, 파일, NoSQL, API)의 메타데이터를 DataHub에 통합 저장 | Critical |
| FR-CAT-02 | 메타데이터 수집 커넥터 | 커스텀 소스 플러그인 개발 가능한 유연한 Ingestion SDK/API 제공 | High |
| FR-CAT-03 | 데이터 검색 및 조회 | 이름, 설명, 태그, 컬럼명 검색 + 한글 초성 매치, 부분 문자열, 정규식 지원 | Critical |
| FR-CAT-04 | 데이터 계보 시각화 | 인터랙티브 Lineage 그래프 (노드 펼치기/숨기기, 단계/관계 필터) | High |
| FR-CAT-05 | Business Glossary | 용어 사전 관리, 데이터자산 연결, UI 검색 지원 | Critical |
| FR-CAT-06 | 메타데이터 변경 추적 | MCL(Metadata Change Log) 기반 변경 이력 기록 및 알림 | Medium |
| FR-CAT-07 | 접근권한 표기 | 민감정보 컬럼 아이콘/경고 표시, 자동 마스킹 연계 | High |

### 6.2 자연어 질의 (FR-NL2)

| ID | 요구사항 | 설명 | 우선순위 |
|----|----------|------|----------|
| FR-NL2-01 | NL2SQL 질의 응답 | 자연어 → SQL 변환, 복잡한 집계/조인/필터 의도 파악 | Critical |
| FR-NL2-02 | 실시간 응답 | 수초 내 응답 개시, 스트리밍 부분 결과 표시 | Critical |
| FR-NL2-03 | 대화 맥락 유지 | 후속 질문 시 이전 대화 컨텍스트 반영 | High |
| FR-NL2-04 | 시각화 기능 | 표 + 차트(막대/선/파이) 자동 생성, CSV 다운로드 | High |
| FR-NL2-05 | 다중 데이터소스 조인 | 교차 시스템 분석 (메모리 조인 또는 통합뷰 활용) | Medium |
| FR-NL2-06 | 파생 계산 지원 | 기간 증감율, 전년 동기 대비 등 비정형 요청 처리 | Medium |
| FR-NL2-07 | 정확도 검증 | SQL 에러/의미착오 탐지, 2-3회 재시도 후 실패 안내 | High |
| FR-NL2-08 | SQL 가시화 | "쿼리 보기" 토글로 생성된 SQL 코드 열람 가능 | Medium |

### 6.3 문서 Q&A (FR-RAG)

| ID | 요구사항 | 설명 | 우선순위 |
|----|----------|------|----------|
| FR-RAG-01 | 지식문서 관리 | 사업보고서, 정책문서, 기술스펙 등 업로드 및 메타정보 관리 | Critical |
| FR-RAG-02 | 자연어 문서 질의 | 관련 문서 검색 → 원문 기반 답변 + 출처 링크 표시 | Critical |
| FR-RAG-03 | 하이브리드 검색 | 벡터 임베딩 + 키워드 검색 결합, 다중 단락 참조 | High |
| FR-RAG-04 | 대용량 문서 처리 | 자동 chunking, 요약본 생성, 전체 개요/세부 질문 대응 | High |
| FR-RAG-05 | 멀티모달 답변 | 표 데이터 읽기, 이미지 OCR 기반 텍스트 설명 | Medium |
| FR-RAG-06 | 문서 업데이트 | 선택적 재색인 API/UI, 변경 이력 관리 | Medium |
| FR-RAG-07 | 지식 검증 | 룰 기반 검증, 사용자 피드백 수집 및 개선 반영 | Low |

### 6.4 보안 및 거버넌스 (FR-SEC)

| ID | 요구사항 | 설명 | 우선순위 |
|----|----------|------|----------|
| FR-SEC-01 | SSO 통합 인증 | OAuth/OIDC 기반 사용자 인증, 역할/그룹 정보 세션 연계 | Critical |
| FR-SEC-02 | Row-level Security | 사용자별 데이터 필터링, Vanna SQLTool에 권한 내재화 | Critical |
| FR-SEC-03 | 권한 기반 문서 접근 | ApeRAG에서 권한 없는 문서 검색 결과 배제 | High |
| FR-SEC-04 | Audit Logging | 질문, 접근 데이터, 응답 시간 등 주요 활동 로그 기록 | Critical |
| FR-SEC-05 | 쿼리 감사 추적 | 사용자별 쿼리 이력 조회, 컴플라이언스 대응 | High |
| FR-SEC-06 | 사용량 제한 | 쿼리 속도 제한(Rate Limit), 초과 시 경고 표시 | Medium |

### 6.5 시스템 운영 (FR-OPS)

| ID | 요구사항 | 설명 | 우선순위 |
|----|----------|------|----------|
| FR-OPS-01 | 수평 확장성 | Kubernetes HPA 기반 백엔드 컴포넌트 확장 | High |
| FR-OPS-02 | 쿼리 캐시 | 반복 질문 성능 향상을 위한 결과 캐싱 | Medium |
| FR-OPS-03 | 장애 격리 | 컴포넌트간 loosely coupled 설계, 부분 장애 시 영향 최소화 | High |
| FR-OPS-04 | 헬스체크 | 서비스별 헬스체크 및 자동 재시작(Failover) | High |
| FR-OPS-05 | 환경 유연성 | 클라우드/온프레미스 모두 지원, 컨테이너화 배포 | Medium |
| FR-OPS-06 | 장시간 작업 지수 백오프 | ETL, 대용량 데이터 처리, 복잡한 빌드 등 장시간 작업에 대해 지수 백오프(1분→2분→4분→8분) 방식의 상태 확인 전략 적용. 토큰 절약 및 병렬 작업 효율성 향상 | Medium |

### 6.5.1 에이전트 오케스트레이션 (FR-AGT)

> **📌 출처:** PRD_02 §3.1~3.6의 핵심 에이전트 기능을 기능 요구사항으로 정의합니다.

| ID | 요구사항 | 설명 | 우선순위 | 관련 PRD_02 |
|----|----------|------|----------|-------------|
| FR-AGT-01 | Query Router | 질의 유형(NL2SQL/GraphRAG/Vector/Hybrid)을 자동 분류하여 적절한 에이전트로 라우팅 | Critical | §3.4 |
| FR-AGT-02 | Hierarchy of Truth | 다중 소스 결과 충돌 시 Ontology > Structured > Vector > Web 우선순위 기반 해결 | Critical | §3.5.3 |
| FR-AGT-03 | Supervisor 통합 | 다중 에이전트 결과를 병합하고 ConflictResolutionScore를 산출 | High | §3.5.3 |
| FR-AGT-04 | Agent Studio UI | 에이전트 실행 흐름 시각화, 디버그 뷰, 신뢰도 점수 표시 | High | §3.5.4 |
| FR-AGT-05 | 자율성-통제 균형 | 에이전트별 자율성 수준(5단계)을 설정하고 Human-in-the-loop 제어 | Medium | §3.6 |
| FR-AGT-06 | Taxonomy Injection | ApeRAG 검색 시 DataHub Glossary 기반 온톨로지 컨텍스트 자동 주입 | High | §3.1 |

> **📌 개발 도구 관련 요구사항 이관 안내:**
> 기존 FR-OPS-06(cc-safe 명령어 감사), FR-OPS-07(컨텍스트 윈도우 모니터링)은 Claude Code 개발 환경 전용 요구사항으로,
> [Implementation_Strategy.md §17](./Implementation_Strategy.md)로 이관되었습니다. 제품(SEOCHO) 런타임 FR과 혼동되지 않도록 분리합니다.

### 6.6 사용자 메뉴 (User Menu)

> **📌 출처:** PRD_05에서 이관 (평가 섹션과 분리)

| 대분류 | 중분류 | 기능 설명 | 핵심 기술 |
| :--- | :--- | :--- | :--- |
| 홈 | 대시보드 | 메뉴 진입화면, 주요 지표 현황 | PostgreSQL, Redis |
| 홈 | Chat/Search | 자연어 질의 → 데이터 조회/분석 | SEOCHO, ApeRAG, Vanna AI |
| 카탈로그 | 통합 검색 | 테이블/컬럼/용어 통합 검색 | DataHub API, Gemini |
| 카탈로그 | 비즈니스 용어집 | 표준 용어 정의 조회 (온톨로지) | DataHub Glossary |
| 카탈로그 | 데이터 리니지 | 데이터 흐름 및 의존관계 시각화 | DataHub Lineage API |

### 6.7 관리자 메뉴 (Admin Menu)

| 대분류 | 중분류 | 기능 설명 | 핵심 기술 | Phase |
| :--- | :--- | :--- | :--- | :--- |
| 데이터 소스 | DB 연결 관리 | DM DB 접속 정보 등록, 연결 테스트 | Admin API, Credential Vault | Phase 1 |
| 데이터 소스 | 메타데이터 수집 | DataHub Ingestion 실행/스케줄 관리 | DataHub Ingestion Framework | Phase 1 |
| 온톨로지 | 용어집 관리 | Glossary Term CRUD, 계층 관리 | DataHub GraphQL API | Phase 1 |
| 온톨로지 | 테이블/컬럼 매핑 | Glossary Term ↔ 테이블/컬럼 연결 | DataHub addTerms Mutation | Phase 1 |
| 온톨로지 | 품질 검증 | 정의 충돌, 동의어 중복, 순환 참조 검증 및 **온톨로지 품질 지표 대시보드** | Validation Engine, **Graph Data Science, LLM-as-a-Judge** | Phase 1 (기본) / Phase 2 (대시보드) |
| **온톨로지** | **CQ 관리** | **적합성 질문 정의, 검증 시뮬레이션** | **CQ Validator, LLM** | **Phase 0.5** |
| **온톨로지** | **스키마 검토 큐** | **REVIEW 상태 트리플 검토 및 처리** | **Schema Enforcer** | **Phase 1** |
| **온톨로지** | **버전 관리** | **변경 이력 조회, 롤백, 스냅샷 관리** | **Version Manager, DataHub Timeline API** | **Phase 2** |
| **온톨로지** | **표준 호환** | **SKOS Export/Import, 외부 온톨로지 관리** | **SKOS Exporter/Importer** | **Phase 1.5** |
| **온톨로지** | **초안 검토** | **LLM 생성 초안 검토/승인/거부** | **Draft Review Manager** | **Phase 1** |
| RAG 관리 | Training Data | DDL/Documentation/SQL 학습 데이터 조회/편집 | Vanna AI API | Phase 1 |
| RAG 관리 | 동기화 관리 | DataHub → Vanna 동기화 실행/모니터링 | Sync Pipeline, Celery | Phase 1 |
| **라우팅** | **Cypher 템플릿** | **템플릿 라이브러리 관리, 패턴 추가/편집** | **Template Engine** | **Phase 1** |
| **라우팅** | **라우팅 로그** | **질의 라우팅 이력, 분류 정확도 분석** | **Query Classifier** | **Phase 2** |
| 시스템 | 사용자 관리 | 사용자/그룹 권한 관리 | Keycloak / LDAP | Phase 1 |
| 시스템 | 모니터링 | 시스템 상태, 쿼리 로그 조회 | Prometheus, Grafana | Phase 1 |
| **시스템** | **마이그레이션** | **DataHub 업그레이드 호환성 관리** | **Migration Manager** | **Phase 1.5+** |
| **품질** | **테스트 대시보드** | **4단계 품질 게이트 현황, 테스트 결과 조회** | **Test Framework, pytest** | **Phase 1** |
| **품질** | **벤치마크 관리** | **E2E 벤치마크 실행, 정확도 추이 분석** | **NL2SQL Benchmark** | **Phase 2** |

> **📌 개발 도구 전용 관리 기능:**
> Claude Code 환경 관련 관리 기능(개발 환경 감사, 컨텍스트 모니터링)은 [Implementation_Strategy.md §17](./Implementation_Strategy.md)에서 관리합니다.

---

## 7. 기대 효과 (Expected Benefits)

### 7.1 핵심 기대 효과 (Top 7)

| # | 효과 | 정량 목표 | 근거 |
|---|------|-----------|------|
| 1 | **NL2SQL 품질 향상** | EX 정확도 80%+ (MVP), 90%+ (Phase 2) | 온톨로지-RAG 통합, 미적용 대비 +15-20%p |
| 2 | **Time-to-Market 단축** | 구축 시간 50% 이상 단축 | 검증된 엔진(ApeRAG) 기반 |
| 3 | **라우팅 정확도 보장** | RoutingAccuracy 95%+ (MVP) | Query Router Agent 결정론적 라우팅 |
| 4 | **멀티테넌시 즉시 구현** | Neo4j Enterprise 불필요 | DozerDB Multi-DB 그룹사별 데이터 격리 |
| 5 | **배포 품질 보장** | MVP: 2단계(Unit+E2E) 100%, Phase 2: 4단계 전체 100% | §5.1 Phase별 게이트 적용 — MVP는 Stage 1+4 필수 |
| 6 | **온톨로지 운영 비용 절감** | 70% 절감 | 증분 업데이트, LLM 초안 생성 (구축 공수 60%↓) |
| 7 | **환각 감소** | Hallucination Rate ≤ 5% | LLM-as-a-Judge + Hierarchy of Truth |

### 7.2 영역별 상세 기대 효과

**온톨로지:**
- Multi-hop 추론 정확도 향상 — 세분화된 관계 표현으로 환각 위험 최소화
- 지식 그래프 품질 보장 — 스키마 강제성으로 비표준 엔티티 유입 차단
- 비즈니스 적합성 사전 검증 — CQ 기반 검증으로 구축 후 전면 수정 리스크 제거
- 표준 호환성 확보 — SKOS 기반 Export/Import로 외부 온톨로지 활용 및 장기 확장성
- 품질 가시화 — 구조적, 의미적, 기능적 품질 지표로 관리 신뢰도 향상
- 비즈니스 용어 일관성 — DataHub Glossary 기반 전사 표준 용어 통일 및 자동 적용

**플랫폼 · 운영:**
- 운영 효율화 — 관리자 UI 셀프서비스 온톨로지 관리, IT 개입 최소화
- 지속적 품질 개선 — 온톨로지 업데이트 시 자동 RAG 재학습
- 플랫폼 안정성 — DataHub 업그레이드 호환성 전략으로 무중단 유지보수
- 문서+DB 통합 분석 — "계약서 내용과 실제 매출 비교" 같은 복합 질의 처리

**품질 · CI/CD:**
- 정량적 품질 관리 — EX 80%+ (MVP), CQ Pass Rate 80%+ 등 명확한 기준 수립
- CI/CD 통합 — 자동화된 테스트 파이프라인으로 지속적 품질 모니터링

**개발환경:**
- 개발 환경 안전성 — cc-safe 기반 승인 명령어 감사로 위험한 자동 승인 사전 차단
- 세션 효율성 — /context 모니터링으로 컨텍스트 윈도우 최적화, MCP 과잉 활성화 방지
- 장시간 작업 효율 — 지수 백오프 전략으로 ETL/빌드 시 토큰 소비 최대 60% 절감

**SEOCHO Agent:**
- Agent 투명성 향상 — Visual Debugging으로 사고 과정 실시간 확인, 문제 파악 시간 80%↓
- 충돌 해결 자동화 — Hierarchy of Truth 기반 ConflictResolutionScore 95%+
- 체계적 품질 검증 — Macro/Ablation 실험 프레임워크로 아키텍처 결정 근거 명확화
- Observability 강화 — Opik/OpenAI Trace 연동으로 운영 중 실시간 성능 모니터링
- 개발 생산성 향상 — CLI 도구 표준화로 인덱싱/평가/Export 작업 자동화

---

## 8. 관련 리소스 URL

### 8.1 핵심 프레임워크
- ApeRAG: https://github.com/apecloud/ApeRAG
  - Production-ready GraphRAG with multi-modal indexing, AI agents, MCP support
  - DeepRAG로 리브랜딩 진행 중
- DozerDB: https://dozerdb.org/ (v5.26.3.0, Neo4j Core 5.26.3 호환)
  - Neo4j Community Edition에 Enterprise 기능 추가 오픈소스 플러그인
  - Multi-DB 지원, Fabric은 로드맵
- Vanna AI: https://vanna.ai/
  - ✅ **Vanna 2.0 신규 적용:** Agent-based API, User-aware, Streaming 아키텍처
  - Row-level Security, Audit Logs 내장으로 엔터프라이즈 요구사항 충족
  - DataNexus는 Vanna 2.0으로 신규 구축 (마이그레이션 불필요)
- SEOCHO: https://github.com/tteon/seocho (MIT License)
  - Ontology + Knowledge Graph 기반 GraphRAG 프레임워크
  - **main 브랜치:** Agent Studio + 통합 프레임워크 (21 commits)
  - **feature-kgbuild 브랜치:** GraphRAG Evaluation Framework (Macro/Ablation)
  - **graphrag-dev 브랜치:** GraphRAG 코어 개발
  - **master 브랜치:** Data Lineage 기반 초기 설계
  - Agent Studio URL: `http://localhost:8501`
  - API Server URL: `http://localhost:8001/docs`

### 8.2 데이터 거버넌스
- DataHub: https://datahubproject.io/
  - kafka-setup 버그 수정 포함
- DataHub Glossary API: https://docs.datahub.com/docs/api/tutorials/terms
- DataHub GlossaryTerm Schema: https://docs.datahub.com/docs/generated/metamodel/entities/glossaryterm
- Qdrant: https://qdrant.tech/

### 8.3 Vanna AI Training 참고
- Vanna Training Guide: https://vanna.ai/docs/train/
- Vanna + Qdrant: https://qdrant.tech/documentation/frameworks/vanna-ai/

### 8.4 온톨로지 엔지니어링 참고
- Competency Questions Survey: https://link.springer.com/chapter/10.1007/978-3-031-47262-6_3
- Knowledge Graph Change Language (KGCL): https://github.com/INCATools/kgcl
- IncRML (Incremental KG Construction): https://www.semantic-web-journal.net/content/incrml-incremental-knowledge-graph-construction-heterogeneous-data-sources
- Schema Validation for Graph Databases: https://hal.science/hal-02138771/document

### 8.5 표준 및 호환성 참고
- SKOS (Simple Knowledge Organization System): https://www.w3.org/2004/02/skos/
- SKOS Reference: https://www.w3.org/TR/skos-reference/
- FIBO (Financial Industry Business Ontology): https://spec.edmcouncil.org/fibo/
- Schema.org: https://schema.org/
- RDFLib (Python): https://rdflib.readthedocs.io/
- SHACL Validation: https://www.w3.org/TR/shacl/

### 8.6 테스트 및 품질 관리 참고
- pytest: https://docs.pytest.org/
- pytest-cov (Coverage): https://pytest-cov.readthedocs.io/
- NL2SQL360 Benchmark: https://arxiv.org/abs/2407.04255
- Great Expectations (Data Validation): https://greatexpectations.io/
- Hypothesis (Property-based Testing): https://hypothesis.readthedocs.io/
- GitHub Actions: https://docs.github.com/en/actions
- **cc-safe (Claude Code 승인 명령어 감사)**: https://github.com/ykdojo/claude-code-tips
  - `.claude/settings.json`의 위험 패턴(`rm -rf`, `sudo`, `curl | sh`) 자동 감지 도구

### 8.7 외부 데이터 수집 및 GraphRAG 참고
- Neo4j GraphRAG Python Package: https://github.com/neo4j/neo4j-graphrag-python
- Neo4j GraphRAG ToolsRetriever 공식 문서: https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html
- ToolsRetriever 소개 블로그: https://neo4j.com/blog/developer/introducing-toolsretriever-graphrag-python-package/
- GraphRAG ToolsRetriever 실습 코드: https://github.com/gongwon-nayeon/graphrag-tools-retriever
- Neo4j GraphRAG 파이썬 패키지 가이드북 (WikiDocs): https://wikidocs.net/book/16760
- Text2CypherRetriever 가이드: https://medium.com/neo4j/effortless-rag-with-text2cypherretriever-cb1a781ca53c

### 8.8 시간 인식 지식그래프 및 에이전트 메모리
- Graphiti (Zep): https://github.com/getzep/graphiti
- Graphiti 공식 문서: https://help.getzep.com/graphiti/getting-started/welcome
- Zep 논문 (arXiv): https://arxiv.org/abs/2501.13956
  - "Zep: A Temporal Knowledge Graph Architecture for Agent Memory"
- Graphiti Agent Tutorial (gongwon-nayeon): https://github.com/gongwon-nayeon/graphiti-agent-tutorial
- YouTube 튜토리얼: https://m.youtube.com/watch?v=y_s7T9GEfKg
- LangGraph + Graphiti 통합 가이드: https://help.getzep.com/graphiti/integrations/lang-graph-agent
- Graphiti MCP 서버: https://github.com/getzep/graphiti/tree/main/mcp_server
- Neo4j 블로그 - Graphiti 소개: https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/
- OpenClaw 컨텍스트 보존 8가지 기법 (코드 분석): https://codepointerko.substack.com/p/openclaw-ai-8
- OpenClaw GitHub 소스:
  - agent-runner.ts: https://github.com/openclaw/openclaw/blob/v2026.2.1/src/auto-reply/reply/agent-runner.ts
  - compact.ts: https://github.com/openclaw/openclaw/blob/v2026.2.1/src/agents/pi-embedded-runner/compact.ts
  - memory-flush.ts: https://github.com/openclaw/openclaw/blob/v2026.2.1/src/auto-reply/reply/memory-flush.ts
  - context-window-guard.ts: https://github.com/openclaw/openclaw/blob/v2026.2.1/src/agents/context-window-guard.ts
  - pruner.ts: https://github.com/openclaw/openclaw/blob/v2026.2.1/src/agents/pi-extensions/context-pruning/pruner.ts

---

## 9. 로드맵 (Roadmap)

### 9.1 Phase별 개발 일정

| Phase | 기간 | 핵심 목표 | 주요 산출물 |
|-------|------|----------|------------|
| **Phase 0.5** | 2026 Q1 | CQ 기반 검증 프레임워크 구축 | CQ 템플릿, 검증 파이프라인 |
| **Phase 1.0** | 2026 Q1-Q2 | 핵심 기능 MVP | 관계 세분화, 스키마 강제성, Query Router, LLM Drafting, 컨텍스트 윈도우 가드, 도구 결과 가드, **cc-safe 명령어 감사 통합, /context 모니터링 기준선 설정** |
| **Phase 1.5** | 2026 Q2 | 표준 호환성 확보 | DataHub synonyms 마이그레이션, SKOS 호환 레이어, GS1/GoodRelations Import |
| **Phase 2.0** | 2026 Q2-Q3 | 자동화 고도화 | Query Log 자동 수집, 온톨로지 버전 관리 UI, 캐시 인식 프루닝, 앞/뒤 콘텐츠 보존, **장시간 작업 지수 백오프 자동화**, **AutoRAG-Research 기반 외부 RAG 벤치마킹 도입 (MrTyDi-ko, RAGBench) (§5.7)** |
| **Phase 3.0** | 2026 Q4+ | 확장성 강화 | DozerDB Fabric, OWL/RDF 호환, 전문 추론 엔진 |
| **R&D** | 지속 | 미래 기술 탐색 | LLM 자동 관계 추천, Federated Ontology, 세션 컨텍스트 보존 고도화 (OpenClaw 적응) |

### 9.2 Phase별 품질 목표

> **📌 단일 SSOT:** 품질 지표의 유일한 정식(canonical) 출처는 **[PRD_04a §4.8](./PRD_04a_Ontology_Core.md)**입니다. [PRD_05 §5.1](./PRD_05_Evaluation_Quality.md)은 §4.8을 미러링하며 Phase별 상세를 제공합니다. 수치가 상이한 경우 §4.8이 우선합니다. 아래는 로드맵 맥락의 요약입니다.

| Phase | EX (정확도) | CQ Pass Rate | Schema Compliance | 비고 |
|-------|------------|--------------|-------------------|------|
| Phase 1 | 80% | 80% | 90% | MVP 기준 |
| Phase 2 | 90% | 95% | 95% | 안정화 (PRD_04a §4.8 SSOT 기준) |
| Phase 3 | 95% | 95% | 98% | **잠정 목표** — 정식 확정 시 PRD_04a §4.8에 추가 필요 |

### 9.3 주요 마일스톤

```txt
2026 Q1 ──┬── Phase 0.5: CQ 프레임워크 구축
          └── Phase 1.0 착수: 핵심 기능 개발

2026 Q2 ──┬── Phase 1.0 완료: MVP 릴리스
          ├── Phase 1.5: 표준 호환성 (GS1/GoodRelations)
          └── Phase 2.0 착수: 자동화 고도화

2026 Q3 ──┬── Phase 2.0 완료: 버전 관리 UI
          └── Phase 3.0 착수: 확장성 강화

2026 Q4+ ─┬── Phase 3.0: DozerDB Fabric, OWL 호환
          └── R&D: Federated Ontology
```

### 9.4 전략적 타이밍 및 방어선 전략

> **⚠️ 전략 근거 — PRD_01 §1 "전략적 포지셔닝" 연계**

로드맵의 Phase 설계는 단순한 기능 개발 순서가 아니라, **초지능 전환기의 포지셔닝 골든타임**(향후 24개월)에 맞춘 전략적 타이밍 설계이다.

**핵심 원칙: 데이터 축적 속도 > 모델 일반화 속도**

Non-verifiable domain과 Proprietary Data에 기반한 DataNexus의 방어선은 영구적이지 않다. 범용 모델이 도메인 특화 영역까지 일반화하는 속도를 DataNexus의 데이터 축적 속도가 지속적으로 앞서야 방어선이 유효하다. 이를 위해 각 Phase는 다음과 같은 축적 루프를 조기에 가동하도록 설계되었다:

| Phase | 축적 루프 가동 목표 | 방어선 기여 |
|-------|-------------------|------------|
| **Phase 0.5–1.0** | 온톨로지 + NL2SQL 핵심 루프 | 도메인 전문가의 용어 정제 → 쿼리 정확도 개선 → 사용 확대의 선순환 시작 |
| **Phase 1.5–2.0** | Query Log 자동 수집 + 표준 호환 | 실사용 패턴 기반 자동 학습으로 축적 속도 가속 |
| **Phase 3.0** | Graphiti 시간축 메모리 | Episode 기반 실시간 지식 축적 → 범용 모델이 접근 불가능한 시간적 맥락 확보 |

**타이밍 리스크:** Phase 1.0 MVP가 2026 Q2를 초과하면, 데이터 축적 루프 가동이 늦어져 방어선 구축 시간이 부족해질 수 있다. 따라서 Phase 0.5-1.0 일정은 **Hard Deadline**으로 관리한다.

---

## 10. 제외 항목 및 향후 검토 사항

### 10.1 제외 기술
- Neo4j CE/EE: DozerDB로 대체
- mcp-neo4j: ApeRAG Native MCP Server 사용
- n8n: LangGraph로 구현

### 10.2 향후 검토 필요
- DozerDB Fabric 지원: 크로스 DB 쿼리 필요 시 검토 → 부록 B.1 참조
- Query Log 자동 수집: 실제 사용 쿼리를 자동 수집하여 Sample SQL로 학습하는 기능 (Phase 2) → 부록 B.2 참조
- 온톨로지 버전 관리: Glossary Term 변경 이력 추적 및 롤백 기능 → 부록 B.3 참조
- OWL/RDF 표준 호환: DataHub Glossary를 OWL Ontology로 내보내기/가져오기 기능 → 부록 B.4 참조
- 자동 관계 추천: LLM 기반 Glossary Term 간 관계 자동 제안 기능 → 부록 B.5 참조
- DataHub synonyms 필드 요청: 커뮤니티에 feature request 제출됨, 추후 공식 지원 시 마이그레이션 검토 → 부록 B.6 참조
- **전문 추론 엔진 도입:** OWL 기반 Reasoner(예: HermiT, Pellet) 도입 검토 → Phase 3+ 장기 과제
- **Federated Ontology:** 그룹사별 분산 온톨로지 연합 질의 → DozerDB Fabric과 연계 검토
- **Multi-Language 온톨로지:** 다국어 레이블(Label) 및 정의(Definition) 관리 (글로벌 확장 시)
- **AutoRAG-Research 정량 벤치마킹:** NomaDamas/AutoRAG-Research 프레임워크를 활용한 SOTA RAG 파이프라인 대비 DataNexus 성능 정량 비교. Phase 1에서는 설계 참고 자료로만 활용, Phase 2 품질 기준선 달성 후 MrTyDi(한국어 검색), RAGBench(E2E RAG) 벤치마킹 실시 → PRD_05 §5.7 참조

---
