# DataNexus PRD — Navigation Index

---

## Core PRD Documents

| # | File | Sections | Lines | Summary |
|---|------|----------|-------|---------|
| 01 | [PRD_01_Overview_Architecture.md](./PRD_01_Overview_Architecture.md) | §1–2 | 265 | 프로젝트 개요, 시스템 아키텍처, Agent Teams vs SEOCHO 구분, DozerDB Multi-DB 매핑 (Agent Studio 상세 → PRD_02 §3.5) |
| 02 | [PRD_02_Core_Features_Agent.md](./PRD_02_Core_Features_Agent.md) | §3 | 374 | 핵심 기능, SEOCHO Agent 설계, 자율성-통제 균형, NL2SQL 스키마 검증, MVP 범위 축소 |
| 03 | [PRD_03_Data_Pipeline.md](./PRD_03_Data_Pipeline.md) | §4.1–4.3 | 178 | 데이터 파이프라인, Phase 0.5 데이터 준비 체크리스트 (§4.2.1), MVP 용어집 (§4.2.2), Few-shot 품질 기준 (§4.2.3) |
| 04a | [PRD_04a_Ontology_Core.md](./PRD_04a_Ontology_Core.md) | §4.4–4.5, §4.6–4.8 | 1,280 | 온톨로지 방어 로직, 실무 대응, SKOS 호환성, 유통 표준 온톨로지, SKOS-DataHub 매핑, 품질 지표 통합 |
| 04b | [PRD_04b_Ontology_Extended.md](./PRD_04b_Ontology_Extended.md) | §4.3.5–4.3.8 | 330 | 온톨로지 품질 검증, Entity Resolution, DataHub→Vanna 동기화, 품질 향상 효과 |
| 04c | [PRD_04c_Ontology_Future.md](./PRD_04c_Ontology_Future.md) | §4.3.9–4.3.10 | 1,002 | **[Phase 2+/3 R&D]** 외부 데이터 자동 구축, Graphiti 시간 인식 KG, 에이전트 메모리, 컨텍스트 보존 |
| 05 | [PRD_05_Evaluation_Quality.md](./PRD_05_Evaluation_Quality.md) | §5 | 994 | 평가 체계, 에러 핸들링 플로차트, 성능 벤치마크 |
| 06 | [PRD_06_Requirements_Roadmap.md](./PRD_06_Requirements_Roadmap.md) | §6–10 | 334 | 아래 상세 참조 ↓ |
| 07 | [PRD_07_UI_Design.md](./PRD_07_UI_Design.md) | §11.1–11.16 | 2,086 | UI/UX 디자인 시스템 (디자인 철학, 컴포넌트, QA 체크리스트), §11.15.7 Skill 기반 검증, §11.16 Skill 통합 가이드 |

### PRD_06 상세 섹션 (§6–10)

| Section | Title | 주요 내용 |
|---------|-------|----------|
| §6 | 기능 요구사항 (Functional Requirements) | FR-CAT(카탈로그), FR-NL2(자연어 질의), FR-RAG(문서 Q&A), FR-SEC(보안), FR-OPS(운영), 사용자/관리자 메뉴(§6.6–6.7) |
| §7 | 기대 효과 (Expected Benefits) | §7.1 핵심 Top 7 (정량 목표 테이블), §7.2 영역별 상세 (온톨로지/플랫폼/품질/개발환경/SEOCHO) |
| §8 | 관련 리소스 URL | 핵심 프레임워크, 데이터 거버넌스, Vanna AI, 온톨로지, GraphRAG, Graphiti 참고 링크 |
| §9 | 로드맵 (Roadmap) | Phase별 개발 일정, 품질 목표, 주요 마일스톤 |
| §10 | 제외 항목 및 향후 검토 | 제외 기술, 향후 검토 필요 사항 |

## Appendices

| # | File | Sections | Lines | Summary |
|---|------|----------|-------|---------|
| A-B | [PRD_Appendix_AB.md](./PRD_Appendix_AB.md) | App A–B | 363 | 용어집(A), 기술 조사 결과 — DataHub Glossary, ApeRAG, DozerDB Fabric, Vanna 2.0(B) |
| C-E | [PRD_Appendix_CDE.md](./PRD_Appendix_CDE.md) | App C–E | 188 | API 명세, 데이터 모델, 테스트 케이스 |
| F | [PRD_Appendix_F.md](./PRD_Appendix_F.md) | App F | 762 | 기술 구현 명세 — 프로젝트 구조, 기술 스택, 서비스 인터페이스, DDL, Docker, requirements.txt |
| G-H | [PRD_Appendix_GH.md](./PRD_Appendix_GH.md) | App G–H | 398 | 평가 데이터셋, 배포 가이드 |

---

## Companion Documents

| Document | Lines | Description |
|----------|-------|-------------|
| [Implementation_Strategy.md](./Implementation_Strategy.md) | 1,395 | 구현 전략 (원본 §1–10 + Cowork §11, Worktree §12, Cross-Review §13, CLAUDE.md §14, 외부 컨텍스트 §15, 컨텍스트 보존 §16, 개발 환경 보안 §17) |
| [Implementation_Guide.md](./Implementation_Guide.md) | 1,504 | 구현 가이드 Step-by-Step (원본 Part 1–6 + Claude Ecosystem Part 7) — Part 7 포맷 복구 완료 |
| [CLAUDE_md_Template.md](./CLAUDE_md_Template.md) | 483 | Claude Code 세션 시 자동 로딩되는 프로젝트 규칙 템플릿 |

---

## Section Quick Lookup

> 💡 어떤 섹션이 어디에 있는지 빠르게 찾기 위한 전체 맵

| §번호 | 제목 | 파일 |
|-------|------|------|
| §1 | 제품 개요 (Product Overview) | PRD_01 |
| §2 | 시스템 아키텍처 (System Architecture) | PRD_01 |
| §3 | 핵심 기능 상세 (Key Features) | PRD_02 |
| §4.1 | Data Mesh 아키텍처 | PRD_03 |
| §4.2 | 데이터 준비 + Phase 0.5 로드맵 | PRD_03 |
| §4.3.1–4.3.4 | 온톨로지-RAG 통합 파이프라인 | PRD_03 |
| §4.3.5–4.3.8 | 품질 검증, Entity Resolution, 동기화, 효과 | **PRD_04b** |
| §4.3.9–4.3.10 | 외부 데이터 자동 구축, Graphiti 시간 인식 KG | **PRD_04c** (Phase 2+/3) |
| §4.3.10.10 | 세션 내 컨텍스트 보존 전략 (OpenClaw 적응) | **PRD_04c** (Phase 2+/3) |
| §4.4 | 온톨로지 방어 로직 (관계·스키마·CQ·버전관리) | **PRD_04a** |
| §4.5 | 온톨로지 실무 대응 (SKOS·Router·LLM Drafting) | **PRD_04a** |
| §4.6 | 유통/물류 표준 온톨로지 | **PRD_04a** |
| §4.7 | SKOS-DataHub 매핑 갭 해소 (보강) | **PRD_04a** |
| §4.8 | 품질 지표 통합 정의 (보강) | **PRD_04a** |
| §5 | 평가 및 품질 관리 | PRD_05 |
| §6 | 기능 요구사항 | PRD_06 |
| §6.6–6.7 | 사용자/관리자 메뉴 구조 | PRD_06 |
| §7 | 기대 효과 | PRD_06 |
| §8 | 관련 리소스 URL | PRD_06 |
| §9 | 로드맵 | PRD_06 |
| §10 | 제외 항목 / 향후 검토 | PRD_06 |
| §11.1–11.15 | UI/UX 디자인 시스템 | PRD_07 |
| §11.15.7 | UI UX Pro Max Skill 기반 디자인 검증 | PRD_07 |
| §11.16 | UI UX Pro Max Skill 통합 가이드 | PRD_07 |

---

## Cross-Reference Quick Map

### 핵심 용어/개념 → 파일 위치

| 개념 | Primary | Related |
|------|---------|---------|
| **전략적 포지셔닝 / 방어선 전략** | **PRD_01 §1 전략적 포지셔닝** | **PRD_06 §9.4** |
| SEOCHO Agent 아키텍처 | PRD_01 §2 | PRD_02 §3 |
| Agent Teams (개발 도구) | PRD_01 §2 보강 | Strategy §12 |
| NL2SQL / Vanna | PRD_02 §3 | PRD_03 §4.1, PRD_05 §5 |
| 온톨로지 방어 로직 | PRD_04a §4.4–4.5 | Appendix_F |
| 온톨로지 확장 (Graphiti 등) | PRD_04c §4.3.9–4.3.10 | PRD_04a §4.6–4.8 |
| 세션 내 컨텍스트 보존 (OpenClaw) | PRD_04c §4.3.10.10 | PRD_05 §5.1, Strategy §16, CLAUDE.md |
| DataHub 메타데이터 | PRD_03 §4.1 | PRD_04a §4.4 |
| 품질 지표 (통합) | PRD_04a §4.8 보강 | PRD_05 §5 |
| 에러 핸들링 | PRD_05 §5 보강 | PRD_02 §3 |
| MVP 범위 | PRD_02 보강 | PRD_06 §9 |
| 로드맵 / Phase 일정 | PRD_06 §9 | PRD_03 §4.2.1 |
| 기대 효과 / KPI | PRD_06 §7 | PRD_05 §5 |
| UI/UX 디자인 | PRD_07 §11 | PRD_07 §11.16 |
| UI UX Pro Max Skill 통합 | PRD_07 §11.16 | PRD_07 §11.16.9-13 |
| Design as Code 원칙 | PRD_07 §11.14.0 | PRD_07 §11.16.9 |

### 보강 사항 위치 (Review Report / Ecosystem Analysis 반영)

| 보강 항목 | 출처 | 적용 파일 |
|-----------|------|-----------|
| **전략적 포지셔닝 (초지능 전환기 방어선)** | **AI 시장 전략 분석** | **PRD_01 §1, PRD_06 §9.4** |
| Agent Teams vs SEOCHO 용어 정리 | Review §2 | PRD_01 |
| 자율성-통제 균형 프레임워크 | Ecosystem §3 (Moltbook) | PRD_02 |
| Phase 0.5 데이터 준비 체크리스트 | Review §1 | PRD_03 |
| 오버엔지니어링 경고 접두사 | Review §2–4 | PRD_04a |
| SKOS-DataHub 필드 매핑 테이블 | Review §1 | PRD_04a |
| 품질 지표 통합 테이블 | Review §3 | PRD_04a |
| 에러 핸들링 플로차트 | Review §1 | PRD_05 |
| 성능 벤치마크 테이블 | Review §5 | PRD_05 |
| Cowork Plugin 구조 | Ecosystem §1 | Strategy §11 |
| Worktree 병렬 개발 | Ecosystem §2 (Boris #1) | Strategy §12 |
| Plan Mode Cross-Review | Ecosystem §2 (Boris #2) | Strategy §13 |
| CLAUDE.md 자동 축적 | Ecosystem §2 (Boris #3) | Strategy §14 |
| Ecosystem 통합 가이드 | Ecosystem §1–5 | Guide Part 7 |
| 세션 내 컨텍스트 보존 전략 | OpenClaw 코드 분석 | PRD_04c §4.3.10.10, Strategy §16, CLAUDE.md agent-routing |
| UI UX Pro Max Skill 통합 가이드 | v2.0 Skill 분석 | PRD_07 §11.16 |
| Pencil.dev 에이전틱 캔버스 | Mobiinside 사례 분석 | PRD_07 보강 §11.2.7, §11.5, §11.14 |
| Skill 실행 계획/Design Decision Priority/KPI | 통합 실행 계획서 | PRD_07 §11.16.9-13 |

---

## Reading Order (추천)

**처음 읽는 경우:**
1. PRD_01 → PRD_02 → PRD_03 → PRD_06 (전체 그림 파악)
2. PRD_04a → PRD_04b → PRD_05 (기술 상세)
3. PRD_07 (UI/UX)

**개발 시작 시:**
1. Implementation_Guide Part 1–6 → Part 7
2. Implementation_Strategy §1–10 → §11–14
3. PRD_03 Phase 0.5 체크리스트 §4.2.1 (가장 먼저 실행)

**온톨로지 작업 시:**
1. PRD_04a (Core) → PRD_04b (Extended MVP) → Appendix_F → PRD_03 (용어집)
2. Phase 2+ 검토 시: PRD_04c (Future)
