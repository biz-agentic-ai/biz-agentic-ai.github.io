# DataNexus CLAUDE.md Template

> **Purpose:** Claude Code 세션 시작 시 자동 로딩되는 프로젝트 규칙  
> **관련 문서:** Implementation Strategy §14-18, Implementation Guide STEP 12-A

---

## Directory Structure

<!-- SSOT: Implementation_Guide STEP 5 / 본 섹션은 개요만 기술 -->

**디렉토리 구조 상세는 Implementation_Guide STEP 4-5 참조**

간략 구조:
```
.claude/
├── rules/datanexus.md        ← 이 파일의 배포 위치
├── foundation/               ← Layer 1: 불변 원칙 (모든 Teammate 공유)
│   ├── identity.md
│   ├── quality-gates.md
│   ├── schema-enforcement.md
│   └── hierarchy-of-truth.md
├── domains/                  ← Layer 2: 모듈별 전문 컨텍스트
│   ├── ontology-engine.md
│   ├── nl2sql-pipeline.md
│   ├── rag-search.md
│   └── agent-routing.md
├── hooks/                    ← KanVibe 자동 설치 (태스크 상태 추적)
│   ├── start.sh
│   └── status.sh
├── execution/                ← Layer 3: 변경 가능한 전술
│   ├── current-sprint.md
│   ├── decisions-log.md
│   ├── known-issues.md
│   ├── handoff-log.md
│   └── progress.md
└── external-docs/            ← Context7 오프라인 캐시

PROGRESS.md                   ← 프로젝트 루트: 전체 작업 현황 마스터 파일
```

상세 파일 목록 및 역할 정의는 Implementation_Guide §STEP 4-5 참조.

---

## Foundation Rules (전체 프로젝트 공통)

### Ontology Rules
- Glossary Term 이름: 한국어 우선, 영어는 synonyms(altLabel)로 관리
- Synonym 배열: 가나다순/알파벳순 정렬
- formula 필드: 파생 지표는 반드시 계산식 포함
- Predicate 수: MVP 5–7개, Phase 2에서 확장 (20+ 금지)
- 스키마 계층: MVP 2-tier (ConceptScheme → Concept), Phase 2에서 3-tier

### Forbidden Tables (NL2SQL 접근 제한)
- `SYSTEM_*`, `AUDIT_LOG*`, `_TEMP_*` 테이블: NL2SQL 접근 금지
- `ROW_LEVEL_SECURITY` 관련 테이블: User context 주입 필수
- 시스템 카탈로그 테이블: 직접 쿼리 금지

### Code Rules
- Python: 3.11+
- API endpoints: Pydantic V2 스키마 필수
- SQL 문자열: Parameter binding only (SQL injection 방지)
- Cypher 쿼리: `.cypher` 파일 관리 (인라인 금지)
- Import 순서: stdlib → third-party → local (isort 적용)
- Type hints: 모든 public function에 필수

### Agent Rules
- Router Agent: DB 직접 접근 금지 (분류만 수행)
- Graph DBA Agent: Cypher에 DELETE/DROP 포함 불가
- Supervisor: ConflictResolutionScore < 0.5 → 최고 HoT 소스만 사용
- 모든 Agent: 10K row limit 적용
- Agent Teams ≠ SEOCHO Agent (개발 도구 vs 프로덕션 런타임)

### Teammate Task Sizing (79% Rule)
에이전트가 단독으로 성공할 수 있는 크기로 태스크를 분해합니다. 복합 문제(성공률 ~23%)를 단위 작업(성공률 ~79%)으로 쪼개는 것이 핵심입니다.

| 기준 | 권장 범위 | 초과 시 조치 |
|------|-----------|-------------|
| 변경 파일 수 | 1-5개 | 태스크 재분할 |
| 변경 LOC | 300줄 이하 | 서브태스크로 분리 |
| 의존성 모듈 수 | 2개 이하 | addBlockedBy로 체이닝 |
| 예상 실행 시간 | 30분 이내 | 단계별 체크포인트 삽입 |

- 안티패턴: "온톨로지 엔진 전체 구현" (23%짜리 태스크)
- 올바른 분해: "Schema Enforcer 검증 로직" + "Cypher 템플릿 5개" + "Unit 테스트" (각각 79%짜리)
- 분해 기준: 하나의 Teammate가 하나의 커밋으로 완결할 수 있는 단위

### Prompt Token Budget (프롬프트 토큰 예산)

세션 시작 시 컨텍스트 200K 토큰 중 규칙 파일이 차지하는 비율을 관리합니다.

| 계층 | 토큰 예산 | 슬림화 원칙 |
|------|----------|------------|
| Foundation Rules (본 파일) | ≤ 3,000 tokens | 한 줄 규칙, 예시 최소화 |
| Domain Rules (4개 파일 합계) | ≤ 4,000 tokens | 안티패턴은 핵심 5개만, 외부 문서는 캐시 참조 |
| Execution Rules (런타임 로그) | ≤ 2,000 tokens | 최근 20건만 유지, 오래된 항목 아카이브 |
| MCP 서버 프롬프트 | ≤ 15,000 tokens | 활성 MCP 10개 미만 유지 |
| **총 규칙 예산** | **≤ 24,000 tokens (12%)** | 나머지 88%를 코드·대화에 할당 |

- 슬림화 점검: 월 1회 `/context` 실행 후 각 계층별 토큰 측정
- 초과 시 조치: 장황한 예시 제거, 반복 지시 통합, 미사용 도구 설명 축소
- Domain Rules 파일별 상한: 개별 1,200 tokens 초과 시 외부 문서 캐시로 분리
- CLAUDE.md 간결성 원칙: "같은 말을 반복하게 되면 그때 추가" — 과도한 선제 규칙 금지

### Session Context Strategy (세션 컨텍스트 전략)

#### HANDOFF.md 표준 템플릿
컨텍스트 사용률 70% 초과 시 아래 형식으로 HANDOFF.md를 생성하고 `/clear`로 새 세션을 시작합니다.

```
# [작업명] - Handoff Document
Created: YYYY-MM-DD HH:mm

## Goal
[현재 작업의 최종 목표 1줄]

## Current Progress
### Completed
- [완료 항목 + 커밋 해시]

### What Worked
- [효과적이었던 접근 방식]

### What Didn't Work
- [실패한 접근 + 실패 원인]

## Remaining Tasks
1. [다음 작업 구체적 명세]
2. [예상 소요 시간]

## Key Context (다음 세션 필수 로드 파일)
- @파일경로1
- @파일경로2

## Blockers
- [알려진 제약사항]
```

- 생성 타이밍: 컨텍스트 70% 초과 또는 작업 방향 전환 시
- 저장 위치: 해당 Worktree의 루트 디렉토리
- 새 세션에서: `@HANDOFF.md 이 파일을 읽고 작업을 이어가줘`로 로드

#### 대화 복제/반복제 활용 (A/B 실험용)
온톨로지 설계 방안 비교, Cypher 쿼리 최적화 비교 등에서 활용합니다.

| 명령어 | 용도 | DataNexus 활용 사례 |
|--------|------|-------------------|
| `/clone` | 현재 대화 전체 복제 | 온톨로지 스키마 A안/B안 병렬 실험 |
| `/half-clone` | 후반부만 유지 (토큰 절반) | 긴 세션의 최근 구현만 이어서 작업 |

- A/B 실험 시: `/clone` 후 각 복제본에서 다른 접근 실행 → 결과 비교 → `execution/session-log.md`에 기록
- 위험 변경 전: `/clone`으로 백업 생성 후 원본에서 실험

#### Extended Thinking 활용 (복잡한 설계 결정)
- 아키텍처 결정, HoT 계층 충돌 해결, 복잡한 디버깅에 `ultrathink` 키워드 사용
- `.claude/settings.json`에 thinking 토큰 예산 설정 가능: `"thinking": {"maxTokens": 10000}`
- Plan Mode(`Shift+Tab` 2회)와 결합하여 설계-검증 분리 워크플로우 강화

### Development Environment Safety (개발 환경 보안)

#### cc-safe 명령어 감사 (PRD §6.5 FR-OPS-06)
- 월 1회 `npx cc-safe .` 실행하여 `.claude/settings.json` 승인 명령어 감사
- 위험 패턴 감지 대상: `rm -rf`, `sudo`, `chmod 777`, `curl | sh`, `wget | bash`, `git reset --hard`, `git push --force`, `npm publish`, `docker run --privileged`
- CI/CD 파이프라인의 Quality Gate에 cc-safe 검사 포함 (Phase 1.0+)
- `--dangerously-skip-permissions` 사용 시 반드시 Docker 컨테이너 내부에서만 실행
- Graph DBA Agent의 DELETE/DROP 금지 규칙이 YOLO 모드에서 우회되지 않도록 Hook으로 이중 차단

#### /context 모니터링 기준선 (PRD §6.5 FR-OPS-07)
- 세션 시작 시 `/context` 실행하여 토큰 분포 확인
- 기준선: 활성 MCP 서버 10개 미만, 활성 도구 80개 미만
- 컨텍스트 사용률 70% 초과 시 HANDOFF.md 생성 → `/clear` → 새 세션 시작
- MCP 서버별 토큰 점유율 모니터링: 단일 MCP가 전체의 20% 초과 시 비활성화 검토
- Context7 MCP 오프라인 캐시(`external-docs/`)와 실시간 MCP 중복 방지

#### 장시간 작업 지수 백오프 (PRD §6.5 FR-OPS-08)
- ETL, 대용량 데이터 처리, 복잡한 빌드 등 30초 이상 예상 작업에 적용
- 상태 확인 간격: 1분 → 2분 → 4분 → 8분 (지수 백오프)
- `Ctrl+B`로 백그라운드 전환 후 메인 작업 계속 진행
- Agent Teams 병렬 실행 시 각 Teammate의 장시간 작업에 독립적으로 적용
- 타임아웃 한도: 최대 30분, 초과 시 작업 취소 + 원인 분석

### Quality Metrics (Single Source of Truth)

| Metric | MVP Target | Phase 2 Target |
|--------|-----------|----------------|
| Routing Accuracy | ≥ 0.95 | ≥ 0.97 |
| Hallucination Rate | ≤ 0.05 | ≤ 0.03 |
| Schema Compliance | ≥ 0.90 | ≥ 0.95 |
| CQ Pass Rate | ≥ 0.80 | ≥ 0.95 |
| EX (Execution Accuracy) | ≥ 0.80 | ≥ 0.90 |

### Performance Benchmarks

| Metric | MVP | Phase 2 |
|--------|-----|---------|
| Response start (first SSE) | ≤ 2s | ≤ 1s |
| Full response (P95) | ≤ 5s | ≤ 3s |
| SQL generation | ≤ 3s | ≤ 2s |
| Graph query | ≤ 2s | ≤ 1s |
| Concurrent users | 50 | 200 |

---

## Domain Rules (도메인별 전문 지식)

### ontology-engine.md
```
- SKOS 매핑: DataHub GlossaryTerm ↔ skos:Concept 1:1
- URN 변환: urn:li:glossaryTerm:{name} → URI
- Hierarchy: broader/narrower 양방향 동기화
- Custom Properties: synonyms[], formula, dataType 필수
- Validation: SHACL shape 적용 (Phase 2)

## 성능 안티패턴 (절대 하지 말 것)
- ❌ OPTIONAL MATCH 3중 이상 중첩 → P95 타임아웃 유발, 최대 2중까지만 허용
- ❌ MATCH (n) 전체 노드 스캔 → 반드시 레이블 + 인덱스 조건 명시
- ❌ DozerDB 트랜잭션 안에서 LLM 호출 → 트랜잭션 타임아웃, LLM 호출은 트랜잭션 외부에서
- ❌ 단일 Cypher에 UNWIND 10,000+ 행 → 배치 처리 1,000행 단위로 분할
- ❌ Multi-DB 간 Cross-database 쿼리 시도 → DozerDB는 Fabric 미지원, 앱 레벨에서 조인

## 외부 문서 참조 (Context7 MCP)
- 세션 시작 시: `use context7` → `resolve dozerdb` 실행
- DozerDB Multi-DB API 변경사항 자동 반영
- Neo4j Cypher Reference 최신 버전 참조
- 문서 버전 불일치 발견 시 execution/known-issues.md에 기록
```

### nl2sql-pipeline.md
```
- Schema Validation: Vanna SQL 생성 후 DataHub 메타데이터로 테이블/컬럼 검증
- Retry Policy: Syntax Error → max 2회 재시도 (프롬프트 변경)
- Timeout: 30초 초과 → 취소 + 좁은 집계 제안
- Few-shot: MVP 30쌍, 품질 기준: 정확한 SQL + 한국어 자연어 매칭
- 금지 패턴: SELECT *, CROSS JOIN, nested subquery 3단계 이상

## 성능 안티패턴 (절대 하지 말 것)
- ❌ Vanna training 시 DDL 전체를 한번에 주입 → 토큰 낭비, 테이블별 분할 학습 필수
- ❌ 서브쿼리 3단계 이상 중첩 → CTE(WITH 절)로 변환
- ❌ GROUP BY 없이 집계 함수 + 일반 컬럼 혼용 → SQL 에러 또는 잘못된 결과
- ❌ LIKE '%keyword%' 패턴 (leading wildcard) → Full-Text Index 또는 정확한 조건으로 대체
- ❌ 생성된 SQL에 LIMIT 없는 대용량 테이블 쿼리 → 기본 LIMIT 1000 강제 적용
- ❌ 날짜 필터 없이 시계열 테이블 전체 스캔 → 반드시 시간 범위 조건 포함

## Vanna Tool Memory ↔ Graphiti 이중 메모리 경계 (§4.3.10.10.8)
- SQL 실행 결과(질문-SQL 쌍) → Vanna Tool Memory만 저장 (Graphiti 제외)
- 비즈니스 사실/해석 패턴/KPI 정의 변경 → Graphiti만 저장 (Vanna 제외)
- SQL + 비즈니스 맥락 복합 항목 → 분할 저장: SQL은 Vanna, 맥락은 Graphiti
- 사용자 선호도 (시각화, 출력 형식) → Graphiti만 저장
- Vanna training 데이터는 tenant_id 기반 벡터 컬렉션 파티션으로 격리
- 일관성 검증: 주 1회 Vanna SQL 내 테이블명 ↔ Graphiti 엔터티 매칭율 확인 (< 80% → 알림)

## 이중 메모리 안티패턴 (절대 하지 말 것)
- ❌ 메모리 플러시 시 SQL 실행 이력을 Graphiti에도 중복 저장 → Vanna Tool Memory에만 저장 (§4.3.10.10.8.2 규칙 1)
- ❌ Vanna training에 비즈니스 해석 컨텍스트 혼합 주입 → SQL 쌍만 학습, 해석은 Graphiti (역할 분리)
- ❌ Graphiti 에피소드에 raw SQL 문자열 저장 → SQL 의도/패턴만 자연어로 요약하여 저장
- ❌ 두 저장소 간 동기화 없이 독립 운영 → 주 1회 교차 참조 검증 배치 필수
- ❌ 테넌트 간 Vanna training 데이터 공유 → 반드시 tenant_id 파티션 격리 유지

## 외부 문서 참조 (Context7 MCP)
- 세션 시작 시: `use context7` → `resolve vanna-ai` 실행
- Vanna 2.0 Agent-based API 최신 변경사항 자동 반영
- FastAPI 비동기 패턴 참조
```

### rag-search.md
```
- ApeRAG Knowledge Base: DataHub 동기화 주기 = 일 1회
- Chunk Size: 512 tokens (overlap 64)
- Retrieval: Top-K = 5, Reranking 적용
- Source Attribution: 모든 RAG 응답에 출처 명시 필수
- Permission Filter: User role 기반 문서 접근 제어

## 성능 안티패턴 (절대 하지 말 것)
- ❌ Qdrant 벡터 검색 시 limit 없는 전체 스캔 → OOM 위험, 반드시 Top-K 지정
- ❌ ApeRAG Knowledge Base 동기화 중 실시간 쿼리 병행 → 동기화 락 충돌, 비동기 큐 분리
- ❌ Chunk size 2048+ tokens → 검색 정밀도 급락, 512 tokens 유지 (overlap 64)
- ❌ Reranking 없이 벡터 유사도만으로 최종 결과 반환 → 반드시 Cross-Encoder reranking 적용
- ❌ 임베딩 모델 호출을 동기 루프 안에서 실행 → asyncio.gather로 배치 임베딩

## 외부 문서 참조 (Context7 MCP)
- 세션 시작 시: `use context7` → `resolve aperag` 실행
- ApeRAG Knowledge Base API 최신 변경사항 자동 반영
- Qdrant Client Python SDK 참조
```

### agent-routing.md
```
- Router 분류: NL2SQL / RAG / Graph / Hybrid
- Confidence Threshold: 0.7 미만 → Supervisor escalation
- Hybrid Query: Graph + SQL 결합 시 Supervisor 조율
- Fallback: 3회 실패 → "질문을 다시 표현해 주세요" + 유사 질문 제안
- Logging: 모든 라우팅 결정 Opik Trace 기록

## 성능 안티패턴 (절대 하지 말 것)
- ❌ Router가 모든 Agent를 순차 호출 후 최적 결과 선택 → 분류 후 단일 Agent만 호출
- ❌ Supervisor의 HoT 충돌 해결에서 모든 소스 재쿼리 → 캐시된 결과로 비교, 재쿼리 금지
- ❌ Agent 간 메시지에 전체 데이터셋 포함 → 요약/참조 ID만 전달, 데이터는 공유 캐시 조회
- ❌ Fallback 루프에서 동일 프롬프트 재시도 → 반드시 프롬프트 변형 (rephrasing) 후 재시도
- ❌ Opik Trace에 응답 전체 텍스트 기록 → 메타데이터만 기록, 응답 본문은 별도 스토리지
- ❌ 컨텍스트 윈도우 크기 확인 없이 에이전트 세션 시작 → 반드시 프리플라이트 가드 실행 (32K 하드 최소값, §4.3.10.10.1)
- ❌ tool_call 실패 시 결과 없이 다음 턴 진행 → 합성 플레이스홀더 주입 필수 (트랜스크립트 무결성, §4.3.10.10.2)
- ❌ 대화 히스토리를 메시지 개수로 제한 → 사용자 턴 단위로 제한 (대화 구조 보존, §4.3.10.10.5)
- ❌ 온톨로지 컨텍스트/DDL 스키마를 매 턴 재전송 → 캐시 인식 프루닝으로 캐시 히트 활용 (Phase 2, §4.3.10.10.3)
- ❌ 도구 결과 전체를 단순 truncation → 앞/뒤 보존 트리밍 적용: 앞 1500자 + 뒤 1500자 (Phase 2, §4.3.10.10.4)
- ❌ 컴팩션 시 메모리 플러시 없이 즉시 압축 → Graphiti 에피소드 커밋 후 컴팩션 진행 (Phase 3, §4.3.10.10.6)
- ❌ 대형 도구 결과를 고정 청크 크기로 분할 → 적응형 청크 비율 적용: 메시지 평균 크기 분석 (Phase 3, §4.3.10.10.7)

## 외부 문서 참조 (Context7 MCP)
- 세션 시작 시: `use context7` → `resolve langgraph` 실행
- LangGraph State Graph / Checkpointing 최신 API 자동 반영
- Opik Tracing API 참조
```

---

## Execution Rules (런타임 축적)

### partial-success-trap.md (Guardian Hook: 부분 성공 함정 감지)
```
## Partial Success Trap Detection

에이전트가 파일 여러 개를 건드려놓고 테스트는 통과하는데 
사이드이펙트가 숨어있는 "부분 성공 함정"을 구조적으로 감지합니다.

### 트리거 조건
- 단일 커밋에서 변경된 파일 > 5개
- 변경된 파일이 3개 이상의 서로 다른 디렉토리에 분산
- 테스트 통과했지만 새로 추가된 테스트가 0개

### 경고 레벨
| 조건 | 레벨 | 조치 |
|------|------|------|
| 변경 파일 6-10개 | WARNING | 변경 사유 확인 프롬프트 |
| 변경 파일 11개+ | CRITICAL | 커밋 차단 + 태스크 재분할 권고 |
| 테스트 미추가 변경 | WARNING | "새 로직에 대한 테스트가 없습니다" 경고 |
| 에이전트 "전체 리팩토링" 시도 | CRITICAL | 즉시 중단, 범위 축소 |
| 에러 해결 위해 관련 없는 파일 수정 | WARNING | git stash + 원인 재분석 |

### Format
[YYYY-MM-DD] [Teammate] [변경 파일 수] [디렉토리 수] [신규 테스트 수] [판정]

### Entries
<!-- Guardian Hook이 자동으로 아래에 추가합니다 -->
```

### known-issues.md (Guardian Hook 자동 기록 형식)
```
## Known Issues Log

### Format
[YYYY-MM-DD] [Teammate] [Error Type] [Prevention Rule]

### Entries
<!-- Guardian Hook이 자동으로 아래에 추가합니다 -->
```

### session-log.md (세션별 결정 기록 형식)
```
## Session Decision Log

### Format
[YYYY-MM-DD] [Session ID] [Decision] [Rationale] [PRD Reference]

### Entries
<!-- 각 세션 종료 시 주요 결정 사항을 기록합니다 -->
```

### progress.md (작업 진행 추적 규칙)
```
## Progress Tracking Rules

### PROGRESS.md 갱신 규칙 (모든 Teammate 필수 준수)
- 태스크 시작 시: 해당 항목 앞에 🔄 마크 추가
- 태스크 완료 시: [ ] → [x] 변경 + ✅ YYYY-MM-DD HH:mm 시각 기록
- 블로커 발생 시: 🚫 마크 + 사유 1줄 기록
- Phase별 카운터: Phase 헤더의 (n/m 완료) 숫자를 즉시 갱신
- 하루 작업 종료 시: ## Daily Summary 섹션에 요약 1줄 추가

### 갱신 타이밍
- 파일 수정/생성/삭제 등 실질적 코드 작업 완료 직후
- Git commit 직전 (commit과 PROGRESS.md 갱신을 하나의 작업 단위로 취급)
- 블로커 발견 즉시 (다른 Teammate에게 의존성 알림 역할)

### 마크 규칙
| 마크 | 의미 | 사용 시점 |
|------|------|-----------|
| 🔄 | 진행 중 | 태스크 착수 시 |
| ✅ | 완료 | 태스크 완료 시 (시각 포함) |
| 🚫 | 블로커 | 의존성/오류로 진행 불가 시 |
| ⏸️ | 보류 | 의도적으로 일시 중단 시 |

### PROGRESS.md 구조 템플릿
아래 구조를 프로젝트 루트의 PROGRESS.md에 적용합니다:

# DataNexus Progress Tracker
Last Updated: YYYY-MM-DD HH:mm KST

## Phase 0.5: Foundation Setup (n/m 완료)
- [ ] 태스크명

## Phase 1: MVP Core (n/m 완료)
- [ ] 태스크명

## Phase 1.5: 확장 (n/m 완료)
- [ ] 태스크명

## Phase 2: 고도화 (n/m 완료)
- [ ] 태스크명

## Daily Summary
- [YYYY-MM-DD] 요약 내용
```

### cc-safe-audit.md (승인 명령어 감사 기록 형식)
```
## cc-safe Audit Log

### 감사 주기
- 정기: 월 1회 첫 번째 업무일
- 수시: --dangerously-skip-permissions 사용 후 즉시

### Format
[YYYY-MM-DD] [스캔 범위] [감지 건수] [조치 사항]

### Entries
<!-- npx cc-safe . 실행 결과를 아래에 기록합니다 -->

### 위험 패턴 분류
| 등급 | 패턴 | 즉시 조치 |
|------|------|-----------|
| CRITICAL | rm -rf /, sudo rm, chmod 777 / | 즉시 제거 |
| HIGH | curl \| sh, git push --force | 팀 리뷰 후 결정 |
| MEDIUM | npm publish, docker run --privileged | 컨테이너 격리 확인 |
```

### context-monitor.md (컨텍스트 모니터링 기록 형식)
```
## Context Monitor Log

### 점검 주기
- 매 세션 시작 시 /context 실행
- 컨텍스트 사용률 70% 도달 시 경고 기록
- 월 1회 프롬프트 토큰 예산 점검 (Foundation Rules 참조)

### Format
[YYYY-MM-DD HH:mm] [사용률%] [시스템 프롬프트] [MCP] [대화 기록] [조치]

### 토큰 예산 점검 Format
[YYYY-MM-DD] [Foundation: n tokens] [Domains: n tokens] [Execution: n tokens] [MCP: n tokens] [초과 항목] [슬림화 조치]

### 기준선
| 항목 | 권장 범위 | 경고 임계값 | 조치 |
|------|-----------|------------|------|
| 활성 MCP 서버 | ≤ 10개 | > 10개 | /mcp로 비활성화 |
| 활성 도구 | ≤ 80개 | > 80개 | 미사용 MCP 제거 |
| 컨텍스트 사용률 | ≤ 70% | > 70% | HANDOFF.md + /clear |
| 단일 MCP 점유율 | ≤ 20% | > 20% | 해당 MCP 비활성화 검토 |
| 총 규칙 토큰 | ≤ 24,000 (12%) | > 24,000 | 장황한 예시 제거, 캐시 분리 |

### Entries
<!-- /context 실행 결과 중 기준선 초과 건만 기록합니다 -->
```

### handoff-log.md (HANDOFF.md 생성 이력 기록)
```
## Handoff Log

### Format
[YYYY-MM-DD HH:mm] [Teammate] [작업명] [컨텍스트 사용률] [HANDOFF 파일 경로] [다음 세션 로드 확인]

### Entries
<!-- HANDOFF.md 생성 시 자동으로 아래에 추가합니다 -->
```

---

## Accumulation Policy (축적 정책)

1. **자동 축적**: Guardian Hook 실패 시 `execution/known-issues.md`에 자동 기록
2. **수동 축적**: 세션 중 발견된 패턴을 `execution/session-log.md`에 기록
3. **승격 (Distill)**: 규칙 10개 이상 누적 시 주간 리뷰 → `foundation/` 또는 `domains/`로 승격
4. **정리**: 월간 리뷰에서 더 이상 유효하지 않은 규칙 아카이브
5. **진행 추적**: 모든 Teammate는 태스크 완료/시작/블록 시 `PROGRESS.md` 즉시 갱신
6. **안티패턴 축적**: 성능 이슈 발견 시 해당 `domains/` 파일의 안티패턴 섹션에 즉시 추가 (Implementation Strategy §15.3 참조)
7. **외부 문서 캐시**: `external-docs/` 스냅샷을 주간 갱신, 100KB 이하 유지 (Implementation Strategy §15.1 참조)
8. **명령어 감사**: 월 1회 `npx cc-safe .` 실행, 결과를 `execution/cc-safe-audit.md`에 기록 (Implementation Strategy §17.1 참조)
9. **컨텍스트 점검**: 매 세션 시작 시 `/context` 실행, 기준선 초과 시 `execution/context-monitor.md`에 기록 (Implementation Strategy §17.2 참조)
10. **장시간 작업 관리**: 30초 이상 예상 작업에 지수 백오프 적용, 비정상 종료 시 `execution/known-issues.md`에 기록 (Implementation Strategy §17.3 참조)
11. **부분 성공 감지**: 단일 커밋에서 변경 파일 5개 초과 또는 테스트 미추가 변경 시 `execution/partial-success-trap.md`에 기록, CRITICAL 레벨은 커밋 차단
12. **메타스킬 등록 (Self-Improving Context)**: 에이전트 세션에서 반복 패턴 발견 시, 그 패턴을 감지하고 기록하는 규칙 자체를 CLAUDE.md에 등록. 승격 경로: known-issues 수동 기록(2회 반복) → domains/ 안티패턴 등록(3건 누적) → Guardian Hook 자동 감지 승격(지속 발생) → foundation/ 불변 규칙 승격(Distill, 10건+)
13. **세션 종료 자기 평가**: 매 세션 종료 전, "이번 세션에서 반복된 패턴이 있었나? CLAUDE.md에 등록할 규칙이 있는가?" 확인. 신규 규칙 발견 시 `execution/session-log.md`에 기록 후 다음 리뷰에서 승격 검토
14. **KanVibe 태스크 상태 동기화**: KanVibe를 태스크 상태의 SSOT로 지정. PROGRESS.md는 `scripts/sync-progress.sh`로 KanVibe API에서 자동 생성 (Implementation Strategy §18.4 참조)
15. **KanVibe 태스크 네이밍**: 모든 태스크명에 모듈 접두사 사용 — `[Backend]`, `[Graph]`, `[RAG]`, `[Agent]`, `[Analysis]` (Implementation Strategy §18.2.2 참조)
16. **HANDOFF.md 생성 규칙**: 컨텍스트 70% 초과 또는 작업 방향 전환 시, Foundation Rules의 HANDOFF.md 표준 템플릿에 따라 생성. 새 세션 시작 전 반드시 HANDOFF.md 품질 검증 (Goal/Completed/Remaining 3섹션 필수)
17. **A/B 실험 기록**: `/clone` 또는 `/half-clone`으로 분기한 실험은 반드시 `execution/session-log.md`에 [A/B] 태그로 기록. 결정 근거와 선택된 방안을 명시
18. **프롬프트 토큰 예산 점검**: 월 1회 `/context` 실행 후 Foundation Rules의 토큰 예산 테이블 대비 초과 항목 식별. 초과 시 슬림화 조치 후 `execution/context-monitor.md`에 기록

---

## Quick Setup

```bash
# 1. 디렉토리 구조 생성
mkdir -p .claude/{rules,foundation,domains,execution,external-docs}

# 2. 이 템플릿을 규칙 파일로 복사
cp templates/CLAUDE_md_Template_final.md .claude/rules/datanexus.md

# 3. 도메인별 규칙 파일 생성 (위 Domain Rules 섹션 참조)
touch .claude/domains/{ontology-engine,nl2sql-pipeline,rag-search,agent-routing}.md

# 4. 실행 로그 초기화
echo "## Known Issues Log" > .claude/execution/known-issues.md
echo "## Session Decision Log" > .claude/execution/session-log.md
echo "## Progress Tracking Rules" > .claude/execution/progress.md
echo "## cc-safe Audit Log" > .claude/execution/cc-safe-audit.md
echo "## Context Monitor Log" > .claude/execution/context-monitor.md
echo "## Partial Success Trap Detection Log" > .claude/execution/partial-success-trap.md
echo "## Handoff Log" > .claude/execution/handoff-log.md

# 5. Foundation 규칙 파일 생성
touch .claude/foundation/{identity,quality-gates,schema-enforcement,hierarchy-of-truth}.md

# 5.5. 외부 문서 캐시 초기화 (Context7 오프라인 대비)
echo "# DozerDB API Snapshot" > .claude/external-docs/dozerdb-snapshot.md
echo "# Vanna 2.0 API Snapshot" > .claude/external-docs/vanna2-snapshot.md

# 6. KanVibe 칸반 보드 설정 (Implementation Strategy §18)
# git clone https://github.com/rookedsysc/kanvibe.git ~/kanvibe
# cd ~/kanvibe && cp .env.example .env
# .env: PORT=4885, DB_PORT=4886 설정 후 bash start.sh
# 브라우저에서 http://localhost:4885 → 프로젝트 등록 → Worktree 자동 스캔
# .claude/hooks/ 자동 설치 확인 (기존 rules/foundation/domains/execution과 충돌 없음)

# 7. PROGRESS.md 마스터 파일 초기화 (프로젝트 루트)
# ※ KanVibe 도입 후에는 sync-progress.sh로 자동 생성 (수동 편집 불필요)
cat > PROGRESS.md << 'EOF'
# DataNexus Progress Tracker
Last Updated: $(date '+%Y-%m-%d %H:%M') KST

## Phase 0.5: Foundation Setup (0/8 완료)
- [ ] 프로젝트 스캐폴딩 (FastAPI + Docker Compose)
- [ ] DozerDB 스키마 초기화
- [ ] DataHub 연동 설정
- [ ] SKOS 매핑 기초 구현
- [ ] Vanna.ai DDL 학습 파이프라인
- [ ] 기본 API 엔드포인트
- [ ] pytest fixture 셋업
- [ ] Docker Compose 구성

## Phase 1: MVP Core (0/12 완료)
- [ ] Query Router 구현 (Agent Logic)
- [ ] SchemaEnforcer 클래스 구현 (Graph Engine)
- [ ] CQ Validator 구현 (Graph Engine)
- [ ] DozerDB Cypher 템플릿 라이브러리 (Graph Engine)
- [ ] ApeRAG 연동 (RAG Pipeline)
- [ ] MinerU 문서 파싱 (RAG Pipeline)
- [ ] 벡터/그래프 하이브리드 검색 (RAG Pipeline)
- [ ] Supervisor Agent + HoT 충돌 해결 (Agent Logic)
- [ ] Graph DBA Agent (Agent Logic)
- [ ] NL2SQL Vanna 2.0 Agent 기반 (Backend Core)
- [ ] 증분 업데이트 파이프라인 (Graph Engine)
- [ ] Row-level Security 적용 (Backend Core)

## Phase 1.5: 확장 (0/4 완료)
- [ ] DataHub synonyms 마이그레이션
- [ ] SKOS Export/Import 구현
- [ ] DataHub 업그레이드 호환성 레이어
- [ ] 엔티티 정규화 파이프라인

## Phase 2: 고도화 (0/6 완료)
- [ ] Agent Studio UI 구현
- [ ] UI Design System QA + 토큰 관리
- [ ] Query Log 수집 및 분석
- [ ] 전체 통합 테스트
- [ ] Quality Gate 전 항목 통과
- [ ] CI/CD 파이프라인 구축

## Phase 3+: R&D (0/3 완료)
- [ ] 전문 추론 엔진
- [ ] Graphiti 에이전트 메모리
- [ ] 고급 시각화 대시보드

## Daily Summary
<!-- 하루 작업 종료 시 아래에 추가 -->
EOF
```
