# DataNexus PRD — Navigation Index

---

## Core PRD Documents

| # | File | Sections | Lines | Summary |
|---|------|----------|-------|---------|
| 01 | [PRD_01_Overview_Architecture_final.md](./PRD_01_Overview_Architecture_final.md) | §1–2 | 265 | 프로젝트 개요, 시스템 아키텍처, Agent Teams vs SEOCHO 구분, DozerDB Multi-DB 매핑 (Agent Studio 상세 → PRD_02 §3.5) |
| 02 | [PRD_02_Core_Features_Agent_final.md](./PRD_02_Core_Features_Agent_final.md) | §3 | 827 | 핵심 기능, SEOCHO Agent 설계, 자율성-통제 균형, NL2SQL 스키마 검증, MVP 범위 축소, **§3.9 Dashboard Promotion & 자동화 보고 (Shaper 연동)**, **§3.9.7 Promotion Lineage**, **§3.9.8 Glossary-Dashboard Staleness 감지**, **§3.9.9 양방향 컨텍스트 보존**, **§3.11 구조화된 분석 워크플로우 (alive-analysis 통합)** |
| 03 | [PRD_03_Data_Pipeline_final.md](./PRD_03_Data_Pipeline_final.md) | §4.1–4.3 | 369 | 데이터 파이프라인, Phase 0.5 데이터 준비 체크리스트 (§4.2.1), MVP 용어집 (§4.2.2), Few-shot 품질 기준 (§4.2.3), **동기화 장애 F-6 (Dashboard Staleness) 추가** |
| 04a | [PRD_04a_Ontology_Core_final.md](./PRD_04a_Ontology_Core_final.md) | §4.4–4.5, §4.6–4.8 | 1,280 | 온톨로지 방어 로직, 실무 대응, SKOS 호환성, 유통 표준 온톨로지, SKOS-DataHub 매핑, 품질 지표 통합 |
| 04b | [PRD_04b_Ontology_Extended_final.md](./PRD_04b_Ontology_Extended_final.md) | §4.3.5–4.3.8 | 330 | 온톨로지 품질 검증, Entity Resolution, DataHub→Vanna 동기화, 품질 향상 효과 |
| 04c | [PRD_04c_Ontology_Future_final.md](./PRD_04c_Ontology_Future_final.md) | §4.3.9–4.3.10 | 1,002 | **[Phase 2+/3 R&D]** 외부 데이터 자동 구축, Graphiti 시간 인식 KG, 에이전트 메모리, 컨텍스트 보존 |
| 05 | [PRD_05_Evaluation_Quality_final.md](./PRD_05_Evaluation_Quality_final.md) | §5 | 994 | 평가 체계, 에러 핸들링 플로차트, 성능 벤치마크 |
| 06 | [PRD_06_Requirements_Roadmap_final.md](./PRD_06_Requirements_Roadmap_final.md) | §6–10 | 334 | 아래 상세 참조 ↓ |
| 07 | [PRD_07_UI_Design_final.md](./PRD_07_UI_Design_final.md) | §11.1–11.16 | 1,167 | UI/UX 디자인 요구사항 (디자인 철학, 컴포넌트, QA 체크리스트), §11.15.7 Skill 기반 검증, §11.16 Skill 통합 가이드 — 구현 코드는 Design_System_Implementation_Guide로 분리 |

### PRD_06 상세 섹션 (§6–10)

| Section | Title | 주요 내용 |
|---------|-------|----------|
| §6 | 기능 요구사항 (Functional Requirements) | FR-CAT(카탈로그), FR-NL2(자연어 질의), FR-RAG(문서 Q&A), FR-SEC(보안), FR-OPS(운영), FR-AGT(에이전트), **FR-DSH(대시보드 & 보고)**, 사용자/관리자 메뉴(§6.6–6.7) |
| §7 | 기대 효과 (Expected Benefits) | §7.1 핵심 Top 7 (정량 목표 테이블), §7.2 영역별 상세 (온톨로지/플랫폼/품질/개발환경/SEOCHO) |
| §8 | 관련 리소스 URL | 핵심 프레임워크, 데이터 거버넌스, Vanna AI, 온톨로지, GraphRAG, Graphiti 참고 링크 |
| §9 | 로드맵 (Roadmap) | Phase별 개발 일정, 품질 목표, 주요 마일스톤 |
| §10 | 제외 항목 및 향후 검토 | 제외 기술, 향후 검토 필요 사항 |

## Appendices

| # | File | Sections | Lines | Summary |
|---|------|----------|-------|---------|
| A-B | [PRD_Appendix_AB_final.md](./PRD_Appendix_AB_final.md) | App A–B | 363 | 용어집(A), 기술 조사 결과 — DataHub Glossary, ApeRAG, DozerDB Fabric, Vanna 2.0(B) |
| C-E | [PRD_Appendix_CDE_final.md](./PRD_Appendix_CDE_final.md) | App C–E | 188 | API 명세, 데이터 모델, 테스트 케이스 |
| F | [PRD_Appendix_F_final.md](./PRD_Appendix_F_final.md) | App F | 762 | 기술 구현 명세 — 프로젝트 구조, 기술 스택, 서비스 인터페이스, DDL, Docker, requirements.txt |
| G-H | [PRD_Appendix_GH_final.md](./PRD_Appendix_GH_final.md) | App G–H | 398 | 평가 데이터셋, 배포 가이드 |

---

## Companion Documents

| Document | Lines | Description |
|----------|-------|-------------|
| [Implementation_Strategy_final.md](./Implementation_Strategy_final.md) | 1,700+ | 구현 전략 (원본 §1–10 + Cowork §11, Worktree §12, Cross-Review §13, CLAUDE.md §14, 외부 컨텍스트 §15, 컨텍스트 보존 §16, 개발 환경 보안 §17, KanVibe 태스크 관리 §18, CI/CD AI 리뷰 §19, 컨테이너 격리 §20, Skills & Commands §21, Prompt Caching §22, **alive-analysis 분석 통합 §23**) |
| [Implementation_Guide_final.md](./Implementation_Guide_final.md) | 1,600+ | 구현 가이드 Step-by-Step (원본 Part 1–6 + Claude Ecosystem Part 7 + KanVibe STEP 23 + **alive-analysis STEP 24**) — Part 7 포맷 복구 완료 |
| [Design_System_Implementation_Guide_final.md](./Design_System_Implementation_Guide_final.md) | 1,375 | UI/UX 디자인 시스템 구현 가이드 — CSS 토큰, React 컴포넌트, Tailwind 설정, Custom Hooks, Skill CLI (PRD_07에서 분리) |
| [CLAUDE_md_Template_final.md](./CLAUDE_md_Template_final.md) | 483 | Claude Code 세션 시 자동 로딩되는 프로젝트 규칙 템플릿 |

---

## Section Quick Lookup

> 💡 어떤 섹션이 어디에 있는지 빠르게 찾기 위한 전체 맵

| §번호 | 제목 | 파일 |
|-------|------|------|
| §1 | 제품 개요 (Product Overview) | PRD_01 |
| §2 | 시스템 아키텍처 (System Architecture) | PRD_01 |
| §3 | 핵심 기능 상세 (Key Features) | PRD_02 |
| **§3.9** | **Dashboard Promotion & 자동화 보고 (Shaper 연동)** | **PRD_02** |
| **§3.9.7** | **Promotion Lineage 관리 (SQL Drift 방지)** | **PRD_02** |
| **§3.9.8** | **Glossary-Dashboard 정합성 (Staleness 감지)** | **PRD_02** |
| **§3.9.9** | **양방향 컨텍스트 보존 (Dashboard → Chat 복귀)** | **PRD_02** |
| **§3.11** | **구조화된 분석 워크플로우 (alive-analysis 통합)** | **PRD_02** |
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
| KanVibe 태스크 관리 (칸반 보드) | Strategy §18 | Guide STEP 23, CLAUDE.md |
| NL2SQL / Vanna | PRD_02 §3 | PRD_03 §4.1, PRD_05 §5 |
| **Dashboard Promotion / Shaper BI** | **PRD_02 §3.9 (§3.9.7 Lineage, §3.9.8 Staleness, §3.9.9 컨텍스트 보존)** | **PRD_01 §1 (컴포넌트), PRD_03 §4.3.1.1 (F-6), PRD_06 §6.5.2 (FR-DSH), Appendix_AB §B.9, Appendix_F §F.3.6-F.3.7** |
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
| alive-analysis 분석 워크플로우 | PRD_02 §3.11 (§3.11.1-3.11.7) | PRD_01 §1 (컴포넌트), PRD_05 §5.1.5 (메트릭 매핑), PRD_06 §8.12/§9/§10, Strategy §23, Guide STEP 24, CLAUDE.md analysis-workflow.md |
| ALIVE 루프 (Ask→Look→Investigate→Voice→Evolve) | PRD_02 §3.11.2 | Strategy §23.3, CLAUDE.md analysis-workflow.md |
| 4단계 메트릭 분류 (North Star→Diagnostic) | PRD_05 §5.1.5 | PRD_02 §3.11.4, Strategy §23.4 |

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
| KanVibe 태스크 관리 통합 | KanVibe Adoption Review | Strategy §18, Guide STEP 23, CLAUDE.md |
| 세션 내 컨텍스트 보존 전략 | OpenClaw 코드 분석 | PRD_04c §4.3.10.10, Strategy §16, CLAUDE.md agent-routing |
| UI UX Pro Max Skill 통합 가이드 | v2.0 Skill 분석 | PRD_07 §11.16 |
| Pencil.dev 에이전틱 캔버스 | Mobiinside 사례 분석 | PRD_07 보강 §11.2.7, §11.5, §11.14 |
| Skill 실행 계획/Design Decision Priority/KPI | 통합 실행 계획서 | PRD_07 §11.16.9-13 |
| **Shaper 대시보드 & 자동화 보고 통합** | **Shaper 기술 조사 + GeekNews 분석** | **PRD_01 §1, PRD_02 §3.9, PRD_06 §6.5.2/§8.10/§9, Appendix_AB §B.9, Appendix_F** |
| **alive-analysis 구조화된 분석 통합** | **alive-analysis v1.1 레포 분석** | **PRD_01 §1, PRD_02 §3.11, PRD_05 §5.1.5, PRD_06 §8.12/§9/§10, Strategy §23, Guide STEP 24, CLAUDE.md** |

---

## Reading Order (추천)

**처음 읽는 경우:**
1. PRD_01 → PRD_02 → PRD_03 → PRD_06 (전체 그림 파악)
2. PRD_04a → PRD_04b → PRD_05 (기술 상세)
3. PRD_07 (UI/UX 요구사항) → Design_System_Implementation_Guide (구현 상세)

**개발 시작 시:**
1. Implementation_Guide Part 1–6 → Part 7 (STEP 23 KanVibe 포함)
2. Implementation_Strategy §1–10 → §11–14 → §18 (KanVibe)
3. PRD_03 Phase 0.5 체크리스트 §4.2.1 (가장 먼저 실행)
4. 데이터 분석 워크플로우 필요 시: Implementation Guide STEP 24 (alive-analysis 설정)

**온톨로지 작업 시:**
1. PRD_04a (Core) → PRD_04b (Extended MVP) → Appendix_F → PRD_03 (용어집)
2. Phase 2+ 검토 시: PRD_04c (Future)
