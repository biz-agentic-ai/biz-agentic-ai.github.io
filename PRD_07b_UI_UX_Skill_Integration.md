# PRD_07b: UI UX Pro Max Skill 통합 상세 가이드

> ⚠️ 본 문서는 [PRD_07_UI_Design.md](./PRD_07_UI_Design.md)에서 분리된 UI UX Pro Max Skill 통합 상세 가이드입니다.
> 원본 PRD_07의 §11.1~§11.15 및 보강 사항 섹션을 전제로 합니다.

**PRD_07 ↔ PRD_07b 섹션 매핑:**

| PRD_07b 섹션 | 관련 PRD_07 섹션 | 관계 |
|-------------|-----------------|------|
| §11.15.7 | §11.15 QA 체크리스트 | 확장 (Skill 기반 검증 추가) |
| §11.16.1~4 | §11.2.7.1 디자인 도구 | 삼원 체계 확장 |
| §11.16.5 | §11.2.7 디자인 토큰 관리 | tokens.json SSOT 규칙 보강 |
| §11.16.6 | §11.15 QA 체크리스트 | UX 가이드라인 교차 참조 |
| §11.16.9 | §11.14 Design as Code | Design Decision Priority 확장 |

---

## 11.15.7 UI UX Pro Max Skill 기반 디자인 검증

> **참고:** 본 섹션은 PRD_07의 §11.15 QA 체크리스트의 확장으로, Skill 통합 맥락에서 참조됩니다.

UI 구현 전 및 PR 제출 시, UI UX Pro Max Skill의 디자인 시스템 생성기를 활용하여 DataNexus의 디자인 표준 준수 여부를 자동 검증합니다.

**검증 항목:**

| # | 검증 항목 | 기준 | 확인 방법 |
|---|----------|------|----------|
| U-1 | **디자인 시스템 생성** | DataNexus용 MASTER.md 존재 및 최신 상태 | `design-system/MASTER.md` 파일 확인 |
| U-2 | **컬러 팔레트 일치** | Deep Slate + Sapphire Blue 팔레트 사용 | `--domain color` 검색 결과와 tokens.json 교차 검증 |
| U-3 | **타이포그래피 일치** | Outfit + Plus Jakarta Sans + JetBrains Mono 사용 | `--domain typography` 검색으로 확인 |
| U-4 | **안티패턴 위반 0건** | AVOID 섹션의 모든 항목 미적용 확인 | `--design-system` 출력의 AVOID와 코드 비교 (안티패턴 SSOT: PRD_07 §11.1.2 43-68행 + 보강 1173-1189행) |
| U-5 | **Pre-delivery 체크리스트** | Skill 생성 체크리스트 전 항목 통과 | `--design-system` 출력의 PRE-DELIVERY CHECKLIST |
| U-6 | **스택 가이드라인 준수** | React + shadcn/ui + Tailwind 스택 규칙 적용 | `--stack react` 결과와 코드 비교 |
| U-7 | **차트 유형 적합성** | §11.9 매핑과 Skill 차트 추천 일치 | `--domain chart` 검색으로 교차 확인 |

**검증 실행 스크립트:**

```bash
# DataNexus 디자인 시스템 생성 및 검증
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "B2B enterprise data analytics SaaS dashboard" \
  --design-system -p "DataNexus" -f markdown

# 페이지별 오버라이드 생성
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "B2B enterprise data analytics SaaS dashboard" \
  --design-system --persist -p "DataNexus" --page "chat"

python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "B2B enterprise data analytics SaaS dashboard" \
  --design-system --persist -p "DataNexus" --page "dashboard"

# 세부 검색: DataNexus 스타일 적합성 확인
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "minimalism enterprise" --domain style
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "executive dashboard" --domain chart
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "animation accessibility z-index" --domain ux
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "form validation responsive" --stack react
```

---

## 11.16 UI UX Pro Max Skill 통합 가이드

### 11.16.1 개요

[UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (v2.0+)는 AI 기반 디자인 인텔리전스 스킬로, DataNexus의 UI 개발 파이프라인에 통합하여 디자인 시스템 자동 생성, 스타일 추론, 안티패턴 검증을 자동화합니다.

#### Skill 역량-PRD 대응 섹션 매핑

UI UX Pro Max v2.0+의 핵심 역량과 DataNexus PRD 기존 규정의 상세 매핑입니다.

| Skill 역량 | 규모 | DataNexus 활용 지점 | PRD 대응 섹션 |
|-----------|------|---------------------|---------------|
| 산업별 추론 규칙 | 100개 | B2B Enterprise, SaaS, Trading Dashboard 카테고리 적용 | §11.16.3 |
| UI 스타일 DB | 67개 | Minimalism & Swiss Style (Luxury Minimalism variant) 매칭 | §11.16.5 |
| 컬러 팔레트 DB | 96개 | Deep Slate + Sapphire Blue 팔레트 교차 검증 | §11.15.7 U-2 |
| 폰트 페어링 DB | 57개 | Outfit + Plus Jakarta Sans + JetBrains Mono 검증 | §11.15.7 U-3 |
| BI/Analytics 대시보드 스타일 | 10개 | 역할별 대시보드(CEO, 마케터, MD, 운영자, 분석가) 매핑 | §11.16.5 |
| UX 가이드라인 | 99개 | PRD §11.15 QA 체크리스트와 교차 참조 | §11.16.6 |
| 차트 유형 DB | 25개 | §11.9 데이터 시각화 디자인 가이드와 교차 확인 | §11.15.7 U-7 |

#### 통합 목적 상세화 (측정 지표 포함)

| 목적 | 기대 효과 | 측정 지표 |
|------|----------|----------|
| **디자인 시스템 자동 생성** | B2B 엔터프라이즈에 최적화된 스타일/컬러/타이포 자동 추론 | 디자인 토큰 불일치 0건/Sprint |
| **안티패턴 사전 방지** | 100개 산업별 규칙으로 AI 퍼플/핑크, 네온, 과도한 애니메이션 자동 차단 (안티패턴 정의: PRD_07 §11.1.2) | 안티패턴 위반 0건/PR |
| **Pre-delivery 자동 검증** | cursor:pointer, hover 전환, 접근성, SVG 아이콘 등 25개+ 항목 자동 체크 | QA 체크리스트 통과율 95%+ |
| **Claude Code Agent 연동** | Skill 모드로 자동 활성화, Agent Teams 워크플로우와 직접 통합 | UI 컴포넌트 개발 시간 30% 단축 |

---

### 11.16.2 설치

**Claude Code (프로젝트 루트에서):**

```bash
# 방법 1: Claude Marketplace
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill

# 방법 2: CLI
npm install -g uipro-cli
cd datanexus/frontend
uipro init --ai claude
```

**설치 후 디렉토리 구조:**

```txt
datanexus/frontend/
+-- .claude/skills/ui-ux-pro-max/     # Skill 파일
|   +-- scripts/
|   |   +-- search.py                 # BM25 + 추론 엔진
|   |   +-- core.py                   # 검색 엔진 코어
|   |   +-- design_system.py          # 디자인 시스템 생성기
|   +-- data/
|   |   +-- styles.csv                # 67개 UI 스타일 DB
|   |   +-- colors.csv                # 96개 컬러 팔레트 DB
|   |   +-- typography.csv            # 57개 폰트 페어링 DB
|   |   +-- ui-reasoning.csv          # 100개 산업별 추론 규칙
|   |   +-- ux-guidelines.csv         # 99개 UX 가이드라인
|   |   +-- charts.csv                # 25개 차트 유형 DB
|   |   +-- stacks/react.csv          # React 스택 가이드라인
|   +-- SKILL.md
+-- design-system/                    # Skill이 생성하는 디자인 시스템
|   +-- MASTER.md                     # Global Source of Truth
|   +-- pages/
|       +-- chat.md                   # Chat UI 오버라이드
|       +-- dashboard.md              # Dashboard 오버라이드
|       +-- admin.md                  # Admin 오버라이드
+-- design-tokens/                    # 기존 토큰 관리 (§11.2.7)
+-- design/                           # 기존 Pencil.dev 파일 (§11.5)
```

#### MASTER.md 초기 생성 후 수동 검증

`--design-system --persist` 명령으로 MASTER.md를 생성한 후, 아래 항목이 DataNexus PRD §11과 일치하는지 수동 검증합니다. Skill의 추론 엔진은 범용 B2B SaaS 팔레트를 추천할 가능성이 있으므로, DataNexus 커스텀 값과의 불일치를 초기에 포착하여 오버라이드하는 것이 중요합니다.

| 검증 항목 | 기대값 | 불일치 시 조치 |
|-----------|--------|---------------|
| STYLE | Minimalism & Swiss Style (Luxury Minimalism variant) | MASTER.md STYLE 섹션 수동 수정 |
| Primary Color | #0f172a (Deep Slate 900) | tokens.json 값으로 오버라이드 |
| Accent Color | #3b82f6 (Sapphire Blue 500) | tokens.json 값으로 오버라이드 |
| Typography | Outfit / Plus Jakarta Sans / JetBrains Mono | MASTER.md TYPOGRAPHY 섹션 수동 수정 |
| Anti-patterns | AI 퍼플/핑크, 네온, 이모지 아이콘 포함 여부 | §11.1.2 목록과 일치하도록 보완 |

> **핵심 원칙:** tokens.json이 Single Source of Truth이며, MASTER.md는 Skill이 생성한 "추천"이다. 불일치 시 tokens.json이 항상 우선한다. (§11.16.9 Design Decision Priority 참조)

#### CLAUDE.md 규칙 파일 배치 (Context-as-Code 정렬)

```txt
datanexus/
+-- .claude/
|   +-- rules/datanexus.md                    # 기존 프로젝트 규칙 (변경 없음)
|   +-- foundation/
|   |   +-- ui-design-system.md               # [신규] MASTER.md 참조 불변 규칙
|   +-- domains/
|   |   +-- frontend-ui.md                    # [신규] UI 구현 도메인 규칙 (§11.16.7 규칙)
|   +-- execution/
|       +-- ui-qa-log.md                      # [신규] Skill 검증 결과 자동 기록
+-- frontend/
    +-- .claude/skills/ui-ux-pro-max/         # Skill 설치 위치 (변경 없음)
    +-- design-system/                        # Skill 생성 디자인 시스템 (변경 없음)
    +-- design-tokens/tokens.json             # Single Source of Truth (변경 없음)
    +-- design/                               # Pencil.dev 파일 (변경 없음)
```

**Context-as-Code 3-Tier 매핑:**

| Tier | 파일 | 내용 | 변경 주기 |
|------|------|------|----------|
| **Foundation** | `foundation/ui-design-system.md` | "tokens.json이 MASTER.md보다 우선", "안티패턴 위반 즉시 수정" 등 불변 원칙 | 거의 변경 없음 |
| **Domain** | `domains/frontend-ui.md` | §11.16.7 규칙 7개, 안티패턴 누적 기록 | 안티패턴 발견 시 추가 |
| **Execution** | `execution/ui-qa-log.md` | Skill 검증 실행 결과, 위반 사항 기록 | 매 PR 검증 시 갱신 |

---

### 11.16.3 DataNexus 커스텀 추론 규칙

UI UX Pro Max의 100개 산업별 추론 규칙 중 DataNexus에 적용되는 핵심 규칙입니다.

**매핑되는 카테고리:**

| UI UX Pro Max 카테고리 | DataNexus 적용 페이지 | 추론 규칙 활용 |
|-----------------------|---------------------|---------------|
| **B2B Enterprise** | 전체 플랫폼 공통 | 패턴, 안티패턴, 컬러 무드 |
| **SaaS** | Chat UI, 검색 UI | 스타일 우선순위, 이펙트 |
| **Trading Dashboard** | Executive/Comparative Dashboard | 차트 유형, 데이터 밀도 |
| **Data Analytics** | Drill-Down, Real-Time Monitoring | 레이아웃 패턴, 인터랙션 |

**DataNexus 전용 디자인 시스템 생성:**

```bash
# 마스터 디자인 시스템 생성 + 영속화
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "B2B enterprise data analytics SaaS dashboard luxury minimalism" \
  --design-system --persist -p "DataNexus"
```

**예상 출력 (MASTER.md):**

```txt
+----------------------------------------------------------------------------------------+
|  TARGET: DataNexus - RECOMMENDED DESIGN SYSTEM                                         |
+----------------------------------------------------------------------------------------+
|                                                                                        |
|  PATTERN: Data-Dense Dashboard + Trust & Authority                                     |
|     Conversion: Data-driven with trust elements                                        |
|     CTA: Role-based dashboard entry, NL search bar above fold                          |
|     Sections:                                                                          |
|       1. Role-based Dashboard                                                          |
|       2. NL Query Interface                                                            |
|       3. Results (Chart + Table)                                                       |
|       4. AI Insights Panel                                                             |
|       5. Admin/Catalog                                                                 |
|                                                                                        |
|  STYLE: Minimalism & Swiss Style (Luxury Minimalism variant)                           |
|     Keywords: Clean lines, purposeful whitespace, refined typography, data-focused      |
|     Best For: Enterprise apps, dashboards, documentation                               |
|     Performance: Excellent | Accessibility: WCAG AA                                    |
|                                                                                        |
|  COLORS:                                                                               |
|     Primary:    #0f172a (Deep Slate 900) -> #f8fafc (50)                                |
|     Accent:     #3b82f6 (Sapphire Blue 500)                                            |
|     CTA:        #2563eb (Blue 600)                                                     |
|     Background: #ffffff (Light) / #020617 (Dark)                                       |
|     Text:       #334155 (Slate 700) / #f8fafc (Slate 50 dark)                          |
|     Semantic:   Success #10b981 | Warning #f59e0b | Error #f43f5e                      |
|     Notes: Deep Slate conveys trust/professionalism, Sapphire Blue for intelligence    |
|                                                                                        |
|  TYPOGRAPHY: Outfit / Plus Jakarta Sans / JetBrains Mono                               |
|     Mood: Professional, modern, data-friendly                                          |
|     Best For: Enterprise SaaS, data platforms, analytics dashboards                    |
|     Google Fonts: fonts.google.com/share?selection.family=Outfit|Plus+Jakarta+Sans      |
|                                                                                        |
|  KEY EFFECTS:                                                                          |
|     Subtle shadows (§11.2.3) + Smooth transitions (150-300ms) + Skeleton loading       |
|                                                                                        |
|  AVOID (Anti-patterns):                                                                |
|     Neon/fluorescent colors + AI purple/pink gradients + Parallax/scroll jacking       |
|     + Animations > 300ms + Emojis as UI icons + Auto-play video/sound                  |
|     + Spinner-only loading + Arbitrary z-index + Infinite scroll on data tables         |
|                                                                                        |
|  PRE-DELIVERY CHECKLIST:                                                               |
|     [ ] No emojis as icons (use SVG: lucide-react)                                     |
|     [ ] cursor-pointer on all clickable elements                                       |
|     [ ] Hover states with smooth transitions (150-300ms)                               |
|     [ ] Light mode: text contrast 4.5:1 minimum (WCAG AA)                              |
|     [ ] Dark mode: text contrast 4.5:1 minimum (WCAG AA)                               |
|     [ ] Focus states visible for keyboard nav (focus-visible)                          |
|     [ ] prefers-reduced-motion respected                                               |
|     [ ] Responsive: 1440px, 1280px, 768px, 375px (§11.8)                               |
|     [ ] Skeleton UI for all loading states (no spinners)                               |
|     [ ] z-index tokens only (§11.2.6)                                                  |
|     [ ] Design tokens from tokens.json (no hardcoded colors)                           |
|                                                                                        |
+----------------------------------------------------------------------------------------+
```

---

### 11.16.4 페이지별 오버라이드 워크플로우

DataNexus의 각 주요 페이지를 구현할 때, MASTER.md를 기본으로 하되 페이지별 특성에 맞는 오버라이드를 적용합니다.

**오버라이드 생성:**

```bash
# Chat UI 오버라이드
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "B2B enterprise data analytics chat NL query" \
  --design-system --persist -p "DataNexus" --page "chat"

# Executive Dashboard 오버라이드
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "executive dashboard KPI C-suite summary" \
  --design-system --persist -p "DataNexus" --page "dashboard-executive"

# Comparative Analysis 오버라이드
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "comparative analysis side-by-side data comparison" \
  --design-system --persist -p "DataNexus" --page "dashboard-comparative"

# Drill-Down Analytics 오버라이드 (MD/상품기획)
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "drill-down analytics detailed exploration hierarchical data" \
  --design-system --persist -p "DataNexus" --page "dashboard-drilldown"

# Real-Time Monitoring 오버라이드 (운영자)
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "real-time monitoring operations live data stream alerts" \
  --design-system --persist -p "DataNexus" --page "dashboard-realtime"

# Admin 오버라이드
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "admin panel data management enterprise" \
  --design-system --persist -p "DataNexus" --page "admin"
```

**확장된 디렉토리 구조:**

```txt
design-system/
+-- MASTER.md                         # Global Source of Truth
+-- pages/
    +-- chat.md                       # Chat UI 오버라이드
    +-- dashboard-executive.md        # Executive Dashboard (CEO/CFO)
    +-- dashboard-comparative.md      # Comparative Analysis (마케터)
    +-- dashboard-drilldown.md        # Drill-Down Analytics (MD/상품기획)
    +-- dashboard-realtime.md         # Real-Time Monitoring (운영자)
    +-- admin.md                      # Admin 오버라이드
```

**구현 시 컨텍스트 프롬프트:**

```txt
나는 DataNexus의 [페이지명] 페이지를 구현하고 있습니다.
design-system/MASTER.md를 읽어주세요.
design-system/pages/[페이지명].md가 존재하면 해당 규칙을 우선 적용해주세요.
존재하지 않으면 MASTER.md 규칙만 사용해주세요.
스택은 React + shadcn/ui + Tailwind CSS입니다.
이제 코드를 생성해주세요.
```

---

### 11.16.5 BI/Analytics Dashboard 스타일 매핑

UI UX Pro Max Skill의 10개 BI/Analytics Dashboard 스타일과 DataNexus §11.12.3 역할별 대시보드의 매핑입니다.

| DataNexus 역할 | DataNexus 레이아웃 스타일 | UI UX Pro Max 대시보드 스타일 | Skill 검색 키워드 |
|---------------|------------------------|----------------------------|------------------|
| CEO/CFO | Executive Dashboard | Executive Dashboard (#3) | `"executive dashboard C-suite"` |
| 마케터 | Comparative Analysis | Comparative Analysis Dashboard (#6) | `"comparative analysis side-by-side"` |
| MD/상품기획 | Drill-Down Analytics | Drill-Down Analytics (#5) | `"drill-down analytics exploration"` |
| 운영자 | Real-Time Monitoring | Real-Time Monitoring (#4) | `"real-time monitoring operations"` |
| 분석가 | (§11.12.3 확장) | Data-Dense Dashboard (#1) | `"data-dense analytics complex"` |

---

### 11.16.6 UX 가이드라인 교차 참조

UI UX Pro Max Skill의 99개 UX 가이드라인 중 DataNexus PRD 기존 규정과 교차하는 항목입니다.

| UX 가이드라인 (Skill) | DataNexus PRD 대응 섹션 | 비고 |
|-----------------------|----------------------|------|
| `cursor-pointer on clickable` | §11.15.1 I-1 | 동일 규칙 |
| `Hover transitions 150-300ms` | §11.15.1 I-2, §11.2.3 Duration 토큰 | Duration 범위 일치 |
| `focus-visible for keyboard` | §11.15.1 I-3, §11.7 접근성 | WCAG AA 준수 |
| `prefers-reduced-motion` | §11.15.2 A-5, §11.7 모션 감소 | 동일 구현 |
| `No emoji as icons` | §11.15.4 P-3, §11.3.5 아이콘 전략 | lucide-react 통일 |
| `WCAG AA contrast 4.5:1` | §11.15.2 A-1/A-2, §11.2.4 대비 비율 | Light/Dark 모두 적용 |
| `Skeleton loading` | §11.15.4 P-1, §11.3.3 Loading 상태 | Spinner 금지 |
| `z-index token system` | §11.15.4 P-2, §11.2.6 z-index 토큰 | 하드코딩 금지 |

---

### 11.16.7 Claude Code Agent Teams 통합

UI UX Pro Max Skill은 Claude Code의 Skill 모드로 자동 활성화됩니다. Agent Teams 워크플로우에서의 사용 패턴입니다.

**Teammate별 활용:**

| Teammate | 역할 | Skill 활용 방법 |
|----------|------|----------------|
| **UI Teammate** | 프론트엔드 구현 | 구현 전 `--design-system` 실행, MASTER.md 참조하여 코드 생성 |
| **QA Teammate** | 품질 검증 | `--domain ux` 검색으로 안티패턴 검증, Pre-delivery 체크리스트 실행 |
| **Design Teammate** | 디자인 탐색 | `--domain style`, `--domain color`, `--domain typography` 검색으로 대안 탐색 |

#### Pencil MCP 서버 기반 UI Teammate 확장 워크플로우

UI Teammate가 Pencil MCP 서버를 통해 수행하는 상세 워크플로우입니다.

**UI Teammate 전체 사이클:**

```txt
[태스크 수신]
  → design-system/MASTER.md 읽기
  → design-system/pages/[해당 페이지].md 존재 시 오버라이드 적용
  → design/[해당 페이지].pen 열기 (또는 생성)
  |
  +-- [디자인 단계]
  |   → Cmd+K: AI 프롬프트로 레이아웃 생성
  |   → MCP를 통해 캔버스 요소 직접 배치/조작
  |   → 수동 편집: 미세 픽셀 조정, 텍스트 변경 (토큰 비용 절약)
  |   → Sticky Note: QA 체크포인트 및 구현 메모 배치
  |   → Cmd+S: 수동 저장
  |
  +-- [코드 생성 단계]
  |   → Cmd+K: "React + shadcn/ui + Tailwind 컴포넌트로 구현"
  |   → AI가 캔버스 시각적 구조 + 프로젝트 컨벤션 참조
  |   → .tsx 파일 생성 (tokens.json CSS 변수 사용)
  |   → §11.16 Skill 검증: --design-system 출력과 교차 확인
  |
  +-- [커밋 단계]
      → .pen + .tsx 동시 Git commit
      → PR 생성: .pen diff + .tsx diff 포함
      → QA Teammate에게 §11.15 체크리스트 실행 요청
```

**MCP 기반 실시간 데이터 연결:**

Pencil.dev MCP는 외부 데이터 소스와의 연결을 지원하여, 실제 데이터를 캔버스에 실시간 반영하는 동적 프로토타이핑이 가능합니다. DataNexus의 NL2SQL 결과를 직접 시각화하는 통합 시뮬레이션 환경으로 발전할 수 있는 토대입니다.

| 연결 대상 | 용도 | 도입 시점 |
|----------|------|----------|
| **tokens.json** | 토큰 변경 시 캔버스 디자인 실시간 반영 | **Phase 1** (즉시) |
| **DataNexus API** | NL2SQL 쿼리 결과를 캔버스 차트에 실시간 반영 | Phase 2 후반 |
| **Playwright** | 캔버스 디자인과 실제 렌더링 결과 비교 검증 | Phase 2 (§11.15.6 연계) |

#### CLAUDE.md 규칙 (frontend/)

```markdown
## UI UX Pro Max Skill 규칙

1. 모든 UI 구현 작업 시작 전 `design-system/MASTER.md`를 먼저 읽을 것
2. 페이지별 오버라이드 파일이 있으면 MASTER.md보다 우선 적용
3. 새 컴포넌트 개발 시 `--domain style` + `--domain ux` 검색 실행
4. PR 제출 전 §11.15.7 U-1~U-7 항목 확인
5. 안티패턴 위반 시 즉시 수정 (AI 퍼플/핑크, 네온, 이모지 아이콘 등)
   <!-- 안티패턴 SSOT: PRD_07 §11.1.2 (43-68행 + 보강 1173-1189행) -->
6. tokens.json이 MASTER.md보다 우선한다 (§11.16.9 Design Decision Priority)
7. Skill 검증 결과는 .claude/execution/ui-qa-log.md에 기록
```

#### Worktree 매핑 상세

Agent Teams의 Worktree 병렬 개발(Implementation Strategy §15 STEP 20)과 연계한 UI UX Pro Max Skill 활용 패턴입니다.

```
main
  +-- worktree/ui-teammate/              # UI Teammate 전용 Worktree
  |     +-- design/                      # .pen 파일 독점 관리
  |     +-- design-system/               # MASTER.md + pages/ 관리
  |     +-- src/components/              # React 컴포넌트 구현
  |     +-- [Skill 활용] 구현 전 --design-system 실행
  |     +-- [Skill 활용] 페이지별 --page 오버라이드 참조
  |
  +-- worktree/qa-teammate/              # QA Teammate 전용 Worktree
        +-- [Skill 활용] --domain ux 안티패턴 검증
        +-- [Skill 활용] Pre-delivery 체크리스트 실행
        +-- .claude/execution/ui-qa-log.md 갱신
```

#### Guardian Hook 연동

`.claude/execution/ui-qa-log.md`에 Skill 검증 결과를 자동 기록합니다. Context-as-Code 자동 축적 원칙(CLAUDE.md 템플릿 §축적 규칙)에 따라:

| 축적 단계 | 조건 | 대상 파일 |
|----------|------|----------|
| 자동 기록 | Skill 검증 실행 시 | `execution/ui-qa-log.md` |
| 안티패턴 등록 | 동일 위반 3건 누적 시 | `domains/frontend-ui.md` 안티패턴 섹션 (PRD_07 §11.1.2 43-68행 + 보강 1173-1189행과 동기화 필요) |
| 불변 규칙 승격 | 10건+ 누적 시 Distill 리뷰 | `foundation/ui-design-system.md` |

---

### 11.16.8 유지보수 및 업데이트

| 항목 | 주기 | 담당 | 방법 |
|------|------|------|------|
| **Skill 버전 업데이트** | 월 1회 | FE 리드 | `uipro update` 실행, CHANGELOG 확인 |
| **MASTER.md 갱신** | Sprint 시작 시 | UI Teammate | `--design-system --persist` 재실행 |
| **페이지 오버라이드 갱신** | 페이지 리디자인 시 | UI Teammate | 해당 `--page` 재실행 |
| **tokens.json과 동기화** | 토큰 변경 시 | FE 리드 | SYNC-CHECKLIST.md 실행 + Skill 재검증 |
| **추론 규칙 커스텀** | 분기 1회 | FE 리드 | ui-reasoning.csv에 DataNexus 전용 규칙 추가 검토 |

---

### 11.16.9 Design Decision Priority (디자인 결정 우선순위)

디자인 결정에서 복수의 소스 간 충돌이 발생할 경우, 아래 우선순위를 적용합니다.

```
[최고 우선] tokens.json (Single Source of Truth)
     |
     v
[2순위] design-system/MASTER.md (Skill 생성 + 수동 오버라이드)
     |
     v
[3순위] design-system/pages/*.md (페이지별 오버라이드)
     |
     v
[4순위] UI UX Pro Max Skill 실시간 검색 결과
     |
     v
[최저] Skill 기본 추론 (범용 B2B SaaS 추천값)
```

**핵심 원칙:** Skill의 추론 엔진은 "추천"이지 "강제"가 아니다. DataNexus의 Refined Intelligence 철학과 Deep Slate + Sapphire Blue 팔레트는 tokens.json에서 관리되며, Skill이 다른 값을 추천하더라도 tokens.json이 항상 우선한다.

**SEOCHO Hierarchy of Truth(PRD_02 §3.5.3)와의 관계:**

프로덕션 런타임에서 온톨로지-RAG 충돌 해결에 사용되는 Hierarchy of Truth 패턴에서 영감을 받아, 디자인 영역에도 동일한 "최고 신뢰 소스를 우선한다"는 원칙을 적용한 것이다. 두 체계는 독립적으로 운영된다.

| 영역 | 최고 우선 소스 | 충돌 해결 기준 |
|------|--------------|---------------|
| **온톨로지-RAG (PRD_04a §4.4)** | DBA Agent 검증 + Ontology Schema | ConflictResolutionScore |
| **디자인 결정 (§11.16.9)** | tokens.json + PRD §11 디자인 철학 | 소스 우선순위 계층 |

---

### 11.16.10 실행 단계 로드맵

UI UX Pro Max Skill 통합을 7일 이내에 완료하기 위한 단계별 실행 계획입니다. 각 Phase는 이전 Phase의 완료를 전제합니다.

#### Phase A: 설치 및 초기 설정 (Day 1)

| Step | 작업 | 실행 명령 | 완료 기준 |
|------|------|----------|----------|
| A-1 | Skill 설치 | `uipro init --ai claude` | `.claude/skills/ui-ux-pro-max/` 존재 |
| A-2 | Python 의존성 확인 | `python3 --version` | 3.x 확인 |
| A-3 | MASTER.md 생성 | `--design-system --persist -p "DataNexus"` | `design-system/MASTER.md` 생성 |
| A-4 | 수동 검증 | §11.16.2 설치 후 검증 체크리스트 실행 (136행) | 5개 항목 전부 PASS 또는 오버라이드 완료 |
| A-5 | CLAUDE.md 규칙 추가 | `.claude/domains/frontend-ui.md` 생성 | 7개 규칙 배치 완료 |

#### Phase B: 페이지별 오버라이드 생성 (Day 2-3)

| Step | 대상 페이지 | 역할 매핑 | 오버라이드 파일 |
|------|-----------|----------|---------------|
| B-1 | Chat UI | 전체 사용자 | `pages/chat.md` |
| B-2 | Executive Dashboard | CEO/CFO | `pages/dashboard-executive.md` |
| B-3 | Comparative Analysis | 마케터 | `pages/dashboard-comparative.md` |
| B-4 | Drill-Down Analytics | MD/상품기획 | `pages/dashboard-drilldown.md` |
| B-5 | Real-Time Monitoring | 운영자 | `pages/dashboard-realtime.md` |
| B-6 | Admin | 관리자 | `pages/admin.md` |

#### Phase C: Agent Teams 워크플로우 통합 (Day 4-5)

| Step | 작업 | 대상 | 완료 기준 |
|------|------|------|----------|
| C-1 | Teammate 역할 배정 확인 | UI / QA / Design Teammate | §11.16.7 역할 테이블 적용 |
| C-2 | 컨텍스트 프롬프트 표준화 | UI Teammate | §11.16.4 프롬프트 템플릿 공유 |
| C-3 | Worktree 매핑 설정 | 전체 Teammate | Worktree별 Skill 활용 패턴 확인 |

#### Phase D: 검증 파이프라인 구축 (Day 6-7)

| Step | 작업 | 실행 방법 | 완료 기준 |
|------|------|----------|----------|
| D-1 | 세부 검색 검증 | `--domain style/chart/ux`, `--stack react` | 4개 도메인 검색 결과 확인 |
| D-2 | §11.15.7 U-1~U-7 검증 | 검증 실행 스크립트 1회 실행 | 7개 항목 전부 PASS |
| D-3 | Guardian Hook 연동 | `execution/ui-qa-log.md` 초기화 | 자동 기록 경로 확인 |

#### Phase E: 유지보수 체계 수립 (지속)

기존 §11.16.8 유지보수 테이블을 준수하되, 아래 추가 관찰 지점을 Sprint 회고 시 점검합니다.

| 관찰 지점 | 주기 | 대상 | 판단 기준 |
|----------|------|------|----------|
| MASTER.md 최신 상태 | Sprint 시작 시 | FE 리드 | 파일 수정 일자가 직전 Sprint 이내 |
| tokens.json-MASTER.md 불일치 | 토큰 변경 시 | FE 리드 | diff 결과 0건 |
| Skill 검색 결과 품질 | 분기 1회 | FE 리드 | 검색 결과와 PRD 규정의 일치율 90%+ |

---

### 11.16.11 성공 기준

UI UX Pro Max Skill 통합의 효과를 정량적으로 평가하기 위한 기준입니다.

| 지표 | 목표치 | 측정 방법 | 측정 시점 |
|------|--------|----------|----------|
| 디자인 토큰 불일치 | 0건/Sprint | tokens.json vs 실제 코드 diff 분석 | Sprint 종료 시 |
| 안티패턴 위반 | 0건/PR | §11.15.7 U-4 체크리스트 (안티패턴 정의: PRD_07 §11.1.2) | PR 리뷰 시 |
| QA 체크리스트 통과율 | 95%+ | §11.15.7 U-1~U-7 전 항목 | PR 리뷰 시 |
| UI 컴포넌트 개발 시간 | 30% 단축 (vs Skill 미사용) | Sprint Velocity 비교 | Phase 1.0 완료 후 |
| MASTER.md 최신 상태 유지 | Sprint 시작 시 갱신 완료 | 파일 수정 일자 확인 | Sprint 시작 시 |

> **주의:** UI 컴포넌트 개발 시간 30% 단축 목표는 Phase 1.0 완료 후 Skill 사용/미사용 비교 측정을 통해 검증합니다. 초기에는 학습 곡선으로 인해 단축 효과가 제한적일 수 있으며, Phase 1.5 이후 안정화가 예상됩니다.

---

### 11.16.12 리스크 및 대응

| Level | 리스크 | 영향 | 대응 |
|-------|--------|------|------|
| MED | Skill 추론이 DataNexus 커스텀 팔레트와 불일치 | MASTER.md에 범용 컬러 생성 | §11.16.9 Design Decision Priority 적용, tokens.json 값으로 수동 오버라이드 |
| MED | Skill v2.0 -> v3.0 Breaking Change | 디자인 시스템 파일 구조 변경 가능 | §11.16.8 월 1회 CHANGELOG 확인, MASTER.md 백업 유지 |
| LOW | Python 3.x 의존성 충돌 | search.py 실행 불가 | 가상환경 격리 또는 Docker 컨테이너 내 실행 |
| LOW | Agent Teams Experimental 상태 | Skill 모드 자동 활성화 실패 가능 | 수동 `--design-system` CLI 실행으로 Fallback |

**Implementation Strategy §9 "Risks & Mitigations"와의 연계:**

Skill 통합 리스크는 전체 프로젝트 리스크의 하위 항목으로 관리됩니다. Agent Teams Experimental 상태 리스크(Strategy §9 HIGH)와 직접 연관되며, "bkit 설계서는 단독 활용 가능" Fallback이 Skill 통합에도 동일하게 적용됩니다.

---

### 11.16.13 PRD §9 Phase별 타임라인 연계

PRD §9.1 Phase별 개발 일정과 UI UX Pro Max Skill 통합의 연계입니다.

| Phase | 기간 | UI UX Pro Max Skill 활용 | 비고 |
|-------|------|-------------------------|------|
| **Phase 0.5** | 2026 Q1 | Skill 설치, MASTER.md 생성, 기본 검증 파이프라인 구축 (§11.16.10 Phase A-D) | Hard Deadline 준수 (§9.4) |
| **Phase 1.0** | 2026 Q1-Q2 | Chat UI, Executive Dashboard 구현 시 페이지별 오버라이드 활용 | 축적 루프 가동과 동시 |
| **Phase 1.5** | 2026 Q2 | Agent Teams 워크플로우 본격 연동, QA 자동화 확대 | 표준 호환성 확보와 병행 |
| **Phase 2.0** | 2026 Q2-Q3 | 전체 페이지 오버라이드 완비, Guardian Hook 자동 검증 안정화 | 버전 관리 UI 구현과 연계 |
| **Phase 3.0** | 2026 Q4+ | ui-reasoning.csv에 DataNexus 전용 엔트리 추가, 커스텀 추론 규칙 기여 | Skill 커뮤니티 기여 검토 |

**§9.4 전략적 타이밍과의 연계:**

UI UX Pro Max Skill 통합은 Phase 0.5-1.0의 "축적 루프 조기 가동" 전략과 정렬됩니다. Skill이 자동 생성하는 MASTER.md와 페이지별 오버라이드는 UI 구현 속도를 높여 MVP 릴리스 일정(2026 Q2 Hard Deadline) 준수에 기여합니다.

---

### 11.16.14 빠른 참조 명령어

```bash
# 마스터 디자인 시스템 생성
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "B2B enterprise data analytics SaaS dashboard luxury minimalism" \
  --design-system --persist -p "DataNexus"

# 페이지별 오버라이드 생성
python3 .claude/skills/ui-ux-pro-max/scripts/search.py \
  "[키워드]" --design-system --persist -p "DataNexus" --page "[페이지명]"

# 도메인별 검색
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "[키워드]" --domain style
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "[키워드]" --domain color
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "[키워드]" --domain typography
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "[키워드]" --domain chart
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "[키워드]" --domain ux

# 스택별 가이드라인
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "[키워드]" --stack react

# Skill 업데이트
uipro update
uipro versions
```

---
