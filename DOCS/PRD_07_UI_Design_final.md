> **📌 문서 분리 안내:** 본 파일은 UI/UX 디자인 요구사항(PRD 범위)을 정의합니다.
> 상세 CSS 변수, React TSX 코드, Tailwind 설정, Custom Hooks 등 구현 수준의 코드는
> **Design_System_Implementation_Guide_final.md**를 참조하세요.

## 11. 사용자 인터페이스 (UI/UX Design System)

### 11.1 디자인 철학 및 방향

**Design Vision: "Refined Intelligence"**

DataNexus는 **럭셔리 미니멀리즘(Luxury Minimalism)** 스타일을 채택합니다.
- 절제된 우아함과 세련된 디테일
- 데이터의 복잡성을 정제된 시각적 경험으로 승화
- 신뢰감과 전문성을 전달하는 프리미엄 인터페이스

**핵심 디자인 원칙:**

| 원칙 | 설명 |
|------|------|
| **Purposeful Minimalism** | 불필요한 요소 제거, 핵심 기능에 집중 |
| **Refined Details** | 미세한 타이포그래피, 정밀한 여백, 섬세한 인터랙션 |
| **Intelligent Hierarchy** | 명확한 시각적 위계로 정보 탐색 용이 |
| **Subtle Sophistication** | 은은한 그라데이션, 부드러운 그림자, 우아한 전환 효과 |

---

### 11.1.1 타겟 환경 및 브라우저 호환성 정책

DataNexus는 사내 엔터프라이즈 플랫폼으로, 아래 환경을 공식 지원 대상으로 합니다.

| 환경 | 지원 범위 | 비고 |
|------|----------|------|
| **Desktop Browser** | Chrome 최신 2개 버전 (130+) | 사내 표준 브라우저 |
| **Desktop Browser** | Edge Chromium 최신 2개 버전 | 보조 지원 |
| **해상도** | 1280px 이상 (데스크톱 우선) | §11.8 반응형 전략 참조 |
| **미지원** | Safari, Firefox, IE | 사내 환경 외 미지원 명시 |

**Progressive Enhancement 원칙:** CSS @supports를 통한 Feature Detection으로 신규 CSS 기능을 점진적으로 도입합니다.

---

### 11.1.2 B2B 데이터 포털 안티패턴 (Anti-patterns)

<!-- 안티패턴 SSOT: 본 섹션이 정의의 원본. UI UX Pro Max Skill 교차 검증 보강은 하단 보강 섹션 참조 -->

DataNexus UI 구현 시 **반드시 피해야 할 패턴**을 정의합니다. B2B 엔터프라이즈 데이터 플랫폼의 신뢰성과 전문성을 저해하는 요소를 명시적으로 금지합니다.

**시각 디자인 안티패턴:**

| 금지 항목 | 사유 | 대안 |
|-------------|------|------|
| **네온/형광 컬러** (Neon, Fluorescent) | 신뢰감 훼손, B2B 톤 부적합 | §11.2.1 컬러 팔레트의 Deep Slate + Sapphire Blue 사용 |
| **AI 퍼플/핑크 그라데이션** | 유행성 디자인, 데이터 플랫폼과 부조화 | 단색 Accent Blue 또는 미세 그라데이션만 허용 |
| **과도한 패럴랙스/스크롤 잭킹** | 데이터 탐색 효율 저하, 인지 부하 증가 | 네이티브 스크롤 유지, 스크롤 기반 애니메이션 금지 |
| **300ms 초과 장식적 애니메이션** | 비기능적 전환은 생산성 저해 | 기능적 전환만 허용 (§11.2.3 Duration 토큰 준수) |
| **이모지를 UI 아이콘으로 사용** | 플랫폼 간 렌더링 불일치, 비전문적 인상 | SVG 아이콘 사용 (§11.3.5 아이콘 전략 참조) |
| **자동 재생 비디오/사운드** | 엔터프라이즈 환경에서 부적절, 접근성 위반 | 사용자 명시적 재생만 허용 |

**UX 안티패턴:**

| 금지 항목 | 사유 | 대안 |
|-------------|------|------|
| **스피너 전용 로딩** (Spinner-only) | 콘텐츠 구조 예측 불가, 체감 속도 저하 | 반드시 Skeleton UI 사용 (§11.3.3 Loading 상태) |
| **임의 z-index 값** (z-index: 9999 등) | 레이어 충돌, 유지보수 불가 | z-index 토큰 시스템 사용 (§11.2.6) |
| **무한 스크롤 (데이터 테이블)** | 데이터 위치 파악 불가, 브라우저 성능 저하 | 페이지네이션 + "더 보기" 패턴 |
| **확인 없는 파괴적 액션** | 데이터 삭제/변경 실수 복구 불가 | 2단계 확인 모달 필수 |
| **모호한 에러 메시지** ("오류가 발생했습니다") | 사용자 다음 행동 안내 불가 | 구체적 원인 + 해결 방법 + 재시도 버튼 (§11.3.3 Error 상태) |
| **과도한 토스트 알림 스택** | 알림 피로도 증가 | 동시 최대 3개, 동일 유형 통합 |

---

### 11.2 디자인 시스템

#### 11.2.1 컬러 팔레트

DataNexus의 컬러 시스템은 Deep Slate(신뢰/전문성)와 Sapphire Blue(인텔리전스/신뢰)를 중심으로 구성됩니다.

**Primary - Deep Slate (신뢰/전문성):**

| 토큰 | HEX | 용도 |
|------|-----|------|
| primary-50 | #f8fafc | 밝은 배경, 호버 상태 |
| primary-100 | #f1f5f9 | 보조 배경 |
| primary-200 | #e2e8f0 | 보더, 구분선 |
| primary-300 | #cbd5e1 | 비활성 텍스트, 플레이스홀더 |
| primary-400 | #94a3b8 | 보조 텍스트 (Light) |
| primary-500 | #64748b | 중간 톤 텍스트 |
| primary-600 | #475569 | 일반 텍스트 |
| primary-700 | #334155 | 본문 텍스트 (Light Mode) |
| primary-800 | #1e293b | 강조 텍스트 |
| primary-900 | #0f172a | 가장 어두운 배경 |
| primary-950 | #020617 | Dark Mode 기본 배경 |

**Accent - Sapphire Blue (인텔리전스/신뢰):**

| 토큰 | HEX | 용도 |
|------|-----|------|
| accent-50 | #eff6ff | 액센트 밝은 배경 |
| accent-100 | #dbeafe | 액센트 보조 배경 |
| accent-200 | #bfdbfe | 액센트 보더 |
| accent-300 | #93c5fd | 액센트 비활성 |
| accent-400 | #60a5fa | 다크 모드 액센트 텍스트 |
| accent-500 | #3b82f6 | 기본 액센트 컬러 |
| accent-600 | #2563eb | CTA 버튼, 링크 |
| accent-700 | #1d4ed8 | 액센트 호버 |
| accent-800 | #1e40af | 액센트 강조 |
| accent-900 | #1e3a8a | 액센트 최어두운 톤 |

**Semantic Colors:**

| 토큰 | HEX | 용도 |
|------|-----|------|
| success | #10b981 | 성공 상태, 긍정 지표 |
| warning | #f59e0b | 경고 상태, 주의 지표 |
| error | #f43f5e | 에러 상태, 부정 지표 |

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.2.1 (CSS :root 변수 정의) 참조

#### 11.2.2 타이포그래피

**Font Selection: Premium & Distinctive**

| 용도 | 폰트 | 설명 |
|------|------|------|
| 헤드라인 (Display) | Outfit | 모던하고 기하학적인 산세리프, 대형 타이틀에 최적 |
| 본문 (Body) | Plus Jakarta Sans | 가독성 높은 산세리프, 데이터 밀집 화면에 적합 |
| 코드/SQL | JetBrains Mono | 개발자 친화적 모노스페이스, 코드 가독성 최적화 |

**Type Scale:**

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| Display XL | 48px | 600 | Hero 섹션 |
| Display | 36px | 600 | 페이지 제목 |
| H1 | 30px | 600 | 섹션 헤더 |
| H2 | 24px | 600 | 카드 제목 |
| Body | 16px | 400 | 기본 본문 |
| Caption | 12px | 500 | 레이블, 힌트 |

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.2.2 (CSS @import 및 :root 폰트 변수) 참조

#### 11.2.3 그림자 및 애니메이션

**그림자 시스템:**

| 토큰 | 설명 |
|------|------|
| shadow-sm | 미세한 그림자 (1px blur, 6% opacity) |
| shadow-md | 중간 그림자 (6px blur, 5% opacity) |
| shadow-lg | 큰 그림자 (15px blur, 4% opacity) |
| shadow-accent | 액센트 색상 그림자 (14px blur, 25% opacity, Sapphire Blue) |

**애니메이션 Duration 토큰:**

| 토큰 | 값 | 용도 |
|------|------|------|
| duration-fast | 150ms | 호버, 포커스 전환 |
| duration-normal | 250ms | 일반적인 상태 전환 |
| duration-slow | 400ms | 복잡한 레이아웃 전환 (최대 허용값) |

**Timing Function:** ease-out-expo `cubic-bezier(0.16, 1, 0.3, 1)`, ease-out-quart `cubic-bezier(0.25, 1, 0.5, 1)`

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.2.3 (CSS :root 변수 정의) 참조

### 11.2.4 Dark Mode 컬러 토큰

다크모드 전환 시 사용되는 시맨틱 컬러 토큰입니다.

**Dark Mode 대비 비율 요구사항:**

| 용도 | Light | Dark | 대비 비율 |
|------|-------|------|----------|
| **배경 (Primary)** | #ffffff | #020617 | - |
| **본문 텍스트** | #334155 | #f8fafc | 16.1:1 / 15.4:1 |
| **보조 텍스트** | #64748b | #cbd5e1 | 4.6:1 / 7.5:1 |
| **Accent 텍스트** | #2563eb | #60a5fa | 4.7:1 / 6.3:1 |

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.2.4 (CSS .dark 클래스 변수 정의) 참조

### 11.2.5 Spacing Scale

모든 여백/패딩에 4px 기반 스케일을 사용합니다.

| Token | Value | Tailwind | 용도 |
|-------|-------|----------|------|
| space-1 | 4px | p-1 | 아이콘-텍스트 간격 |
| space-2 | 8px | p-2 | 인라인 요소 간격 |
| space-4 | 16px | p-4 | 기본 패딩 |
| space-6 | 24px | p-6 | 카드 내부 패딩 |
| space-8 | 32px | p-8 | 섹션 간 간격 |
| space-12 | 48px | p-12 | 페이지 여백 |

### 11.2.6 z-index 토큰 시스템

DataNexus는 Navigation Bar(backdrop-blur), Chat 패널, SQL 사이드바, 모달, 토스트, 드롭다운 등 다수의 오버래핑 레이어를 사용합니다. 임의 z-index 값 사용을 금지하고, 아래 토큰 시스템을 필수 적용합니다.

**z-index 토큰 정의:**

| 토큰 | 값 | 용도 |
|------|------|------|
| z-base | 0 | 기본 콘텐츠 레이어 |
| z-dropdown | 100 | 드롭다운 메뉴, 자동완성, 컨텍스트 메뉴 |
| z-sticky | 200 | 테이블 sticky 헤더, Navigation Bar |
| z-overlay | 300 | 사이드바 오버레이 (Tablet 모드), 딤드 배경 |
| z-modal | 400 | 모달 다이얼로그, 확인 팝업 |
| z-toast | 500 | 토스트 알림 (항상 모달 위) |
| z-tooltip | 600 | 툴팁 (최상위 레이어) |

**사용 규칙:**
- 모든 z-index는 반드시 위 토큰 변수를 참조해야 합니다. 하드코딩된 숫자값(예: `z-index: 9999`) 사용을 금지합니다.
- 동일 레벨 내 세분화가 필요한 경우 `calc(var(--z-modal) + 1)` 형태로 사용합니다.
- Tailwind 설정에서도 동일한 토큰을 확장합니다 (§11.6 참조).

**레이어 맵 (DataNexus 주요 컴포넌트):**

| 컴포넌트 | z-index 토큰 | 비고 |
|----------|-------------|------|
| 페이지 콘텐츠 | z-base | 기본 레이어 |
| 자동완성 드롭다운 | z-dropdown | Chat 입력 자동완성, Admin 필터 |
| Navigation Bar | z-sticky | backdrop-blur 포함 |
| 결과 테이블 sticky 헤더 | z-sticky | 첫 번째 행 고정 |
| 사이드바 오버레이 (Tablet) | z-overlay | 딤드 배경 포함 |
| SQL 상세 패널 모달 | z-modal | 전체 화면 SQL 에디터 |
| 토스트 알림 | z-toast | 우측 상단 고정 |
| 차트 호버 툴팁 | z-tooltip | 최상위 |

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.2.6 (CSS :root 변수 및 Tailwind zIndex 확장) 참조

### 11.2.7 디자인 토큰 관리 및 디자인 도구 전략

디자인과 코드(CSS/Tailwind) 간 토큰 동기화 및 디자인-개발 워크플로우 통합 전략입니다.

#### 11.2.7.1 디자인 도구 삼원 체계: Figma + Pencil.dev + UI UX Pro Max Skill

DataNexus는 **탐색/기획 단계**, **디자인 인텔리전스**, **구현/코드 전환 단계**를 분리하는 삼원 디자인 도구 체제를 채택합니다.

| 역할 | 도구 | 용도 | 산출물 |
|------|------|------|--------|
| **탐색/기획** | **Figma** | 초기 스타일 가이드, 브레인스토밍, 이해관계자 리뷰 | Figma 파일 (클라우드) |
| **디자인 인텔리전스** | **UI UX Pro Max Skill** | 산업별 디자인 시스템 자동 생성, 스타일/컬러/타이포 추론 | design-system/MASTER.md, pages/*.md |
| **구현 가속** | **Pencil.dev** | IDE 내 디자인 → React 코드 변환, 컴포넌트 프로토타이핑 | `.pen` 파일 (Git 관리) |
| **토큰 관리** | **tokens.json** | Single Source of Truth (색상, 타이포, 간격, z-index) | CSS Variables + Tailwind Config (build.js 자동 생성 -- 본 문서 내 코드는 예시) |

**Pencil.dev 선택 근거:**

| 평가 항목 | Pencil.dev 장점 | DataNexus 적합성 |
|----------|----------------|-----------------|
| **IDE 통합** | VS Code/Cursor 내 캔버스, MCP 프로토콜 지원 | Claude Code Agent Teams 워크플로우와 직접 연결 |
| **Git 네이티브** | `.pen` 파일이 레포에 저장, 브랜치/머지/롤백 가능 | "Design-as-Code" -- PRD의 Single Source of Truth 원칙 부합 |
| **Figma 호환** | 복사-붙여넣기로 벡터, 스타일, 레이어 계층 보존 (1px 오차 이내) | 기존 Figma 자산 즉시 활용 가능 |
| **React 코드 생성** | HTML/CSS/React 컴포넌트 직접 출력 | shadcn/ui 기반 컴포넌트 개발 가속 |
| **컴포넌트 라이브러리** | shadcn UI, Halo, Lunaris 등 내장 | DataNexus의 shadcn/ui 기반 디자인 시스템과 즉시 호환 |

**도구 간 워크플로우:**

```txt
[1. 기획]           [2. 디자인 시스템]     [3. 구현]           [4. 검증]
  Figma          UI UX Pro Max Skill     Pencil.dev          Code Review
    |                   |                   |                   |
    +- 스타일 탐색       +- MASTER.md 생성    +- .pen 파일 생성     +- PR에 .pen diff 포함
    +- 이해관계자 리뷰   +- 페이지별 오버라이드  +- AI로 React 생성    +- tokens.json 일치 검증
    +- 확정 디자인       +- 안티패턴 자동 검증   +- 직접 조정/편집      +- §11.15 QA 체크리스트
          |             +- 컬러/폰트 추론        +- Git commit         +- §11.16 Skill 검증
          |                   |                   |
          +-- Copy & Paste -->+                   |
          |   (벡터/스타일 보존)                    |
          |                   |                   |
          +-- MASTER.md 참조 -------> 구현 시 우선 적용
```

**Pencil.dev 도입 주의사항:**

| 항목 | 상세 |
|------|------|
| **성숙도** | Early Access 단계 (2025년 설립, $1M 투자). 보조 도구로 활용하되 주요 의존성으로 삼지 않음 |
| **가격** | 현재 무료 (Early Access). Claude Code 구독 필요 ($20/월). 유료 전환 시 재평가 |
| **플랫폼** | macOS: 데스크톱 앱 + 익스텐션, Windows: 익스텐션만, Linux: 데스크톱 앱 + 익스텐션 |
| **Fallback 전략** | Pencil.dev 서비스 중단 시 Figma + 수동 코드 전환으로 원복. `.pen` 파일은 JSON 기반 오픈 포맷이므로 데이터 lock-in 위험 낮음 |
| **복잡한 Auto Layout** | Figma의 복잡한 Auto Layout 구성은 전환 후 수동 조정 필요 가능 |

#### 11.2.7.2 디자인 토큰 관리 전략

**Phase 1 (MVP): JSON 기반 Single Source of Truth + Pencil.dev**

토큰 관리 디렉토리 구조:

```txt
design-tokens/
+-- tokens.json          # 마스터 토큰 정의 (색상, 타이포, 간격, 그림자, z-index)
+-- build.js             # JSON -> CSS Variables + Tailwind Config 변환 스크립트
+-- SYNC-CHECKLIST.md    # Figma + Pencil 동기화 체크리스트
```

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.2.7.2 (tokens.json 예시 및 빌드 스크립트) 참조

**Phase 1~2 도구 도입 로드맵: 자동화 파이프라인 + Pencil MCP 통합**

| 도구 | 역할 | 도입 시점 |
|------|------|----------|
| **Pencil.dev** | IDE 내 디자인 → React 코드 변환, MCP 기반 AI 에이전트 통합 | Phase 1 (즉시) |
| **Tokens Studio** (Figma Plugin) | Figma Variables <-> JSON 양방향 동기화 | Phase 2 초기 |
| **Style Dictionary** (Amazon) | JSON → CSS/Tailwind/iOS/Android 멀티 플랫폼 빌드 | Phase 2 중반 |
| **CI 파이프라인** | PR 시 tokens.json + `.pen` 파일 변경 감지 → 자동 빌드 + 토큰 일관성 검증 | Phase 2 후반 |

**디자인 동기화 체크리스트 (Phase 1):**
- [ ] tokens.json 변경 시 Figma Local Styles 업데이트
- [ ] tokens.json 변경 시 Pencil.dev 프로젝트 내 토큰 반영 확인
- [ ] Figma 변경 시 tokens.json에 역반영
- [ ] `.pen` 파일에서 생성된 React 코드가 tokens.json의 CSS 변수를 참조하는지 검증
- [ ] 매 Sprint 종료 시 Code <-> Figma <-> Pencil 토큰 일치 검증
- [ ] 신규 토큰 추가 시 tokens.json + Figma + Pencil + Tailwind Config 동시 반영

---

### 11.3 핵심 컴포넌트 디자인

#### 11.3.1 Navigation Bar

```txt
+-----------------------------------------------------------------------------+
|                                                                             |
|   ◈ DataNexus           Catalog   Chat   Admin              🔔  👤 이준호 |
|                                                                             |
+-----------------------------------------------------------------------------+
```

> **참고:** 위 와이어프레임의 🔔, 👤 등 이모지는 **와이어프레임 플레이스홀더**입니다. 실제 구현 시 반드시 §11.3.5 아이콘 전략의 SVG 아이콘으로 대체합니다.

**스타일 특징:**
- 배경: 반투명 백드롭 블러 (`backdrop-filter: blur(20px)`)
- 로고: ◈ (Nexus 심볼 - 연결점을 상징하는 기하학적 형태)
- 네비게이션: 현재 탭에 subtle underline indicator

#### 11.3.2 Chat Interface

```txt
+-----------------------------------------------------------------------------+
|                                                                             |
|  +-----------------------------------------------------------------------+ |
|  |                      ◈ DataNexus                                      | |
|  |                  Connect. Unify. Discover.                            | |
|  |                                                                       | |
|  |              데이터에 대해 무엇이든 물어보세요                          | |
|  |                                                                       | |
|  |   +-------------------------------------------------------------+   | |
|  |   |  🔍  지난달 GRS 매출 현황을 알려줘                      ↵  |   | |
|  |   +-------------------------------------------------------------+   | |
|  +-----------------------------------------------------------------------+ |
|                                                                             |
|  +-----------------------------------------------------------------------+ |
|  | 👤 지난달 GRS 매출 현황을 알려줘                                      | |
|  +-----------------------------------------------------------------------+ |
|                                                                             |
|  +-----------------------------------------------------------------------+ |
|  | ◈ 2026년 1월 GRS 매출 현황입니다.                                     | |
|  |                                                                       | |
|  | +------------------------------------------------------------------+ | |
|  | | 항목          |    금액     |   전월대비   |   전년동기대비    | | |
|  | +---------------+-------------+--------------+-------------------+ | |
|  | | 총 매출       |  156.2억    |   +8.3%      |     +15.2%        | | |
|  | | 순 매출       |  142.8억    |   +7.9%      |     +14.1%        | | |
|  | +------------------------------------------------------------------+ | |
|  |                                                                       | |
|  | 📊 SQL 보기    📋 복사    👍 👎                                      | |
|  +-----------------------------------------------------------------------+ |
|                                                                             |
+-----------------------------------------------------------------------------+
```

> **참고:** 위 와이어프레임의 📊, 📋, 👍, 👎 등 이모지는 **와이어프레임 플레이스홀더**입니다. 실제 구현 시 §11.3.5 아이콘 전략에 따라 lucide-react SVG 아이콘으로 대체합니다.

**Chat UI 스타일 가이드:**
- 입력창: 넓은 패딩, 부드러운 radius, focus 시 accent shadow
- 메시지 버블: 사용자(오른쪽), AI(왼쪽 + 그림자)
- 차트/테이블: 부드러운 곡선, 호버 인터랙션
- 로딩: Shimmer + Typing indicator (3-dot pulse)

### 11.3.3 상태 UI 패턴 (State UI Patterns)

모든 데이터 의존 화면은 아래 5가지 상태를 반드시 처리해야 합니다.

| 상태 | 시각적 처리 | 구현 방법 |
|------|------------|----------|
| **Loading** | Skeleton Placeholder + Shimmer | 콘텐츠 영역 형태를 모방한 회색 블록 애니메이션 |
| **Empty** | 일러스트 + 안내 메시지 + CTA | 중앙 정렬, muted 톤 일러스트, 행동 유도 버튼 |
| **Error** | 에러 아이콘 + 메시지 + 재시도 | error 색상 뱃지, [다시 시도] 버튼 |
| **Permission** | 잠금 아이콘 + 권한 안내 | warning 색상, 권한 요청 경로 안내 |
| **Success** | 체크 아이콘 + 확인 메시지 | success 색상 토스트, 3초 후 자동 닫힘 |

### 11.3.4 폼 컨트롤 전략

| 컴포넌트 | 기술 선택 | 근거 |
|----------|----------|------|
| **Select (단일)** | shadcn/ui Select (Radix) | 검색 가능, 접근성 검증 완료 |
| **Multi-Select** | shadcn/ui Combobox + Badge | 태그 스타일 다중 선택 |
| **Date Picker** | shadcn/ui Calendar | 범위 선택 지원 |
| **Tree Select** | 커스텀 TreeView + Checkbox | 스키마/테이블 계층 선택에 특화 |
| **Code Editor** | Monaco Editor (SQL/Cypher) | 구문 강조, 자동 완성 |

### 11.3.5 아이콘 전략

**공식 아이콘 라이브러리: lucide-react**

DataNexus는 모든 UI 아이콘에 [Lucide](https://lucide.dev)를 사용합니다. 와이어프레임 및 PRD 문서 내 이모지(🔔, 👤, 📊 등)는 **설계 단계 플레이스홀더**이며, 실제 구현 시 반드시 lucide-react SVG 아이콘으로 대체합니다.

**아이콘 사이즈 시스템:**

| 용도 | 크기 | Tailwind Class | 사용 위치 |
|------|------|---------------|----------|
| Inline (텍스트 내) | 16px | `w-4 h-4` | 버튼 라벨 옆, 상태 표시 |
| Button (버튼 내) | 20px | `w-5 h-5` | 액션 버튼, 입력 필드 아이콘 |
| Navigation | 24px | `w-6 h-6` | Navigation Bar, 사이드바 메뉴 |
| Feature (대형) | 32px | `w-8 h-8` | Empty State 일러스트, 카드 헤더 |

**와이어프레임 → 구현 매핑:**

| 와이어프레임 이모지 | lucide-react 아이콘 | import |
|--------------------|---------------------|--------|
| 🔔 (알림) | `Bell` | `import { Bell } from 'lucide-react'` |
| 👤 (사용자) | `User` | `import { User } from 'lucide-react'` |
| 📊 (SQL 보기) | `Code` | `import { Code } from 'lucide-react'` |
| 📋 (복사) | `Copy` | `import { Copy } from 'lucide-react'` |
| 👍 (좋아요) | `ThumbsUp` | `import { ThumbsUp } from 'lucide-react'` |
| 👎 (싫어요) | `ThumbsDown` | `import { ThumbsDown } from 'lucide-react'` |
| 🔍 (검색) | `Search` | `import { Search } from 'lucide-react'` |
| 💡 (인사이트) | `Lightbulb` | `import { Lightbulb } from 'lucide-react'` |
| 🎯 (추천) | `Target` | `import { Target } from 'lucide-react'` |
| 🤖 (AI 생성) | `Sparkles` | `import { Sparkles } from 'lucide-react'` |

**아이콘 사용 규칙:**
- 모든 프로덕션 아이콘은 반드시 lucide-react에서 SVG로 렌더링합니다.
- OS/브라우저 이모지를 UI 아이콘으로 사용하는 것을 금지합니다 (플랫폼 간 렌더링 불일치, 비전문적 인상).
- 아이콘에는 반드시 `aria-label` 또는 인접 텍스트로 접근성 라벨을 제공합니다.
- strokeWidth 기본값 2를 유지하고, 일관된 시각적 무게감을 보장합니다.

---

### 11.4 React 컴포넌트 예시

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.4 참조
> (ChatInput 컴포넌트, Streaming Response Hook 등 React TSX 코드)

---

### 11.5 Frontend 프로젝트 구조

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.5 참조
> (디렉토리 트리, design/ 디렉토리 규칙, .pen 파일 관리 규칙)

---

### 11.6 Tailwind CSS 설정

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.6 참조
> (tailwind.config.ts 전체 TypeScript 코드)

---

### 11.7 접근성 (A11y) 가이드라인

| 항목 | 요구사항 | 구현 방법 |
|------|----------|-----------|
| **색상 대비** | WCAG AA 준수 (4.5:1 이상) | 모든 텍스트에 충분한 대비 |
| **키보드 네비게이션** | Tab 순서 논리적 | `tabIndex`, `focus-visible` |
| **스크린 리더** | 모든 인터랙티브 요소에 라벨 | `aria-label`, `aria-describedby` |
| **모션 감소** | 사용자 설정 존중 | `prefers-reduced-motion` |

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.7 (CSS @media prefers-reduced-motion 코드) 참조

**컴포넌트별 ARIA 패턴:**

| 컴포넌트 | ARIA 패턴 | 키보드 인터랙션 |
|----------|----------|----------------|
| **Chat Input** | role="textbox", aria-label="데이터 질의 입력" | Enter: 전송, Shift+Enter: 줄바꿈, Esc: 취소 |
| **결과 테이블** | role="table", aria-rowcount, aria-colcount | Arrow: 셀 이동, Home/End: 행 시작/끝 |
| **SQL 패널** | role="region", aria-label="생성된 SQL" | Tab: 복사 버튼 포커스, Enter: 복사 실행 |
| **사이드바 네비게이션** | role="navigation", aria-current="page" | Arrow Up/Down: 항목 이동, Enter: 선택 |
| **토스트 알림** | role="alert", aria-live="polite" | 자동 포커스 없음, 스크린 리더 자동 읽기 |
| **모달 다이얼로그** | role="dialog", aria-modal="true" | Tab: 모달 내 포커스 트랩, Esc: 닫기 |

---

### 11.8 반응형 레이아웃 전략

DataNexus는 데스크톱 우선(Desktop First) 전략을 취하되, 태블릿 화면에서의 기본 사용성을 보장합니다.

| Breakpoint | 너비 | 레이아웃 | 비고 |
|-----------|------|---------|------|
| **Desktop (기본)** | >= 1280px | 사이드바 + 메인 + 서브패널 | 전체 기능 사용 가능 |
| **Tablet** | 768-1279px | 사이드바 접힘 + 메인 확장 | Chat, 카탈로그 조회 가능 |
| **Mobile** | < 768px | 지원 안내 화면 | "데스크톱에서 접속해 주세요" 안내 |

**Chat 화면 레이아웃 기준:**
- **Desktop:** 좌측 대화 히스토리 사이드바(280px) + 중앙 Chat(flex-1) + 우측 SQL/차트 패널(400px, 토글)
- **Tablet:** 사이드바 숨김(오버레이 전환) + 중앙 Chat 전체 확장 + SQL 패널 하단 시트로 전환

**Admin 화면 레이아웃 기준:**
- **Desktop:** 좌측 Admin 메뉴(240px) + 메인 콘텐츠(flex-1) + 테이블/그리드 전체 너비 활용
- **Tablet:** 메뉴 접힘(아이콘만) + 테이블 수평 스크롤 허용

**반응형 검증 Breakpoints:** 375px, 768px, 1024px, 1280px, 1440px (§11.15 QA 체크리스트에서 검증)

---

### 11.9 데이터 시각화 디자인 가이드

Chat UI에서 AI가 생성하는 차트/테이블의 디자인 일관성을 위한 가이드입니다.

#### 11.9.1 차트 라이브러리 및 스타일

**기본 라이브러리:** Recharts (React 친화적, 선언적 API, 반응형 지원)
**보조 라이브러리:** Tremor (대시보드 차트 위젯), D3.js (복잡한 커스텀 시각화 시)

**차트 컬러 시퀀스:**

| 순서 | 색상 (Light) | 색상 (Dark) | 용도 |
|------|-------------|------------|------|
| 1 | #3b82f6 Accent Blue | #60a5fa | 주요 지표 (매출, 실적) |
| 2 | #10b981 Success Green | #34d399 | 긍정 지표 (성장률, 달성률) |
| 3 | #f59e0b Warning Amber | #fbbf24 | 주의 지표 (비용, 이탈률) |
| 4 | #f43f5e Error Rose | #fb7185 | 부정 지표 (손실, 에러율) |
| 5 | #8b5cf6 Purple | #a78bfa | 보조 비교 데이터 |
| 6 | #64748b Slate | #94a3b8 | 기준선, 전년 데이터 |
| 7 | #06b6d4 Cyan | #22d3ee | 지역/채널 구분 |
| 8 | #ec4899 Pink | #f472b6 | 세그먼트/코호트 강조 |

**차트 스타일 규칙:**
- 모서리: borderRadius 6px (바 차트), strokeWidth 2px (라인 차트)
- 그리드: strokeDasharray="3 3", 색상 primary-200 (light) / primary-700 (dark)
- 툴팁: bg-white/dark:bg-primary-800, shadow-lg, rounded-xl, 12px 패딩
- 범례: 차트 하단 중앙 정렬, Body Small 사이즈, 색상 원형 인디케이터
- 애니메이션: 초기 로드 시 0.5s ease-out 진입, prefers-reduced-motion 존중

#### 11.9.2 차트 유형 선택 가이드 (Chart Selection Matrix)

AI가 자연어 질의에서 차트를 자동 생성할 때, 데이터 특성에 따라 적절한 차트 유형을 선택하기 위한 의사결정 매트릭스입니다.

**데이터 특성 → 차트 유형 매핑:**

| 데이터 특성 | 추천 차트 | DataNexus 사용 예시 | Recharts 컴포넌트 |
|------------|----------|-------------------|------------------|
| **시계열 (1개 지표)** | Line Chart | 월별 매출 추이, 일별 방문자 수 | `<LineChart>` |
| **시계열 (2개+ 지표)** | Multi-Line / Area Chart | 채널별 매출 비교, 전년 동기 대비 | `<AreaChart>` |
| **구성 비율** | Donut Chart / Stacked Bar | 지역별 매출 비중, 카테고리별 점유율 | `<PieChart>` / `<BarChart stackId>` |
| **단일 비교 (<=7개 항목)** | Horizontal Bar Chart | Top 5 상품 매출, 팀별 KPI 달성률 | `<BarChart layout="vertical">` |
| **단일 비교 (8개+ 항목)** | Vertical Bar + 스크롤 | 월별 카테고리 매출, 대규모 비교 | `<BarChart>` |
| **분포** | Histogram / Box Plot | 주문 금액 분포, 배송 소요 시간 분포 | 커스텀 `<BarChart>` / D3.js |
| **상관관계** | Scatter Plot | 광고비 vs 전환율, 가격 vs 판매량 | `<ScatterChart>` |
| **진행률/달성률** | Gauge / Progress Bar | KPI 달성률, 목표 대비 현황 | Tremor `<ProgressCircle>` |
| **계층 구조** | Treemap | 카테고리 > 브랜드 > 상품 매출 비중 | `<Treemap>` / D3.js |
| **지리적 분포** | Choropleth Map | 지역별 매출 히트맵 | D3.js + TopoJSON |

**자동 선택 로직 (AI Agent 가이드):**

```txt
1. 시간 축 포함? -> Yes: Line/Area Chart
   +- 지표 수: 1개 -> Line, 2개+ -> Multi-Line/Area
   +- 누적 비교? -> Yes: Stacked Area

2. 비율/구성? -> Yes: Donut (<=5개 항목) / Stacked Bar (6개+)

3. 항목 간 비교? -> Yes:
   +- <=7개 -> Horizontal Bar
   +- 8개+ -> Vertical Bar + 상위 N개 표시 + "기타" 그룹핑

4. 분포 확인? -> Yes: Histogram (연속값) / Box Plot (그룹 비교)

5. 상관관계? -> Yes: Scatter Plot (+ 추세선 옵션)

6. 위 조건 미해당? -> 결과 테이블로 표시
```

#### 11.9.3 결과 테이블 스타일

- 헤더: primary-50 배경, 600 weight, 좌측 정렬 (숫자는 우측 정렬)
- 행: 호버 시 primary-50 배경, 짝수행 zebra striping 없음 (미니멀 원칙)
- 숫자 포맷: 천 단위 콤마, 소수점 2자리 (금액), 퍼센트 1자리
- 증감 표시: ▲/▼ 아이콘 + success/error 색상, 0%는 primary-500
- 오버플로: 수평 스크롤, 첫 번째 열 sticky (position: sticky; left: 0)

---

### 11.10 CSS 2026 신기능 탐색 노트

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.10 참조
> (CSS 2026 신기능 기술 탐색 노트 -- 참고용 실험적 기능 목록 및 도입 계획)

---

### 11.11 2025 글로벌 UI/UX 트렌드 반영 전략

DataNexus는 2025년 글로벌 B2B 데이터 포털의 주요 UI/UX 트렌드를 전략적으로 수용합니다.

#### 11.11.1 새로운 미니멀리즘 (Purposeful Minimalism 2.0)

**적용 방향:**
- 홈 대시보드 정제: 역할별로 3~5개 핵심 KPI 카드만 표시
- 여백 확대: 카드 간 간격을 24px → 32px로 상향
- 단일 폰트 패밀리: Plus Jakarta Sans를 본문 전용으로 통일
- 컬러 절제: 배경은 중성색(Gray 50/950), 액센트 컬러는 브랜드 블루 1종 + 상태 컬러 3종으로 제한

#### 11.11.2 AI 기반 개인화 (Hyper-Personalized Interfaces)

**적용 방향:**
- 역할 기반 홈 대시보드: CEO/CFO/마케터/MD/운영자 등 5개 역할별 기본 레이아웃 템플릿 제공
- 사용 패턴 학습: 최근 7일간 가장 많이 조회한 리포트/차트를 홈 상단에 자동 배치
- AI 추천 인사이트: 우측 패널에 이상치 탐지, 전월 대비 급변 지표, 상관관계 추천 자동 표시
- 위젯 재배치 허용: 드래그 앤 드롭으로 카드 순서 변경 가능

#### 11.11.3 다크 모드 & 멀티 테마 (Accessibility First)

**적용 방향:**
- 3종 테마 제공: Light Mode (기본), Dark Mode, High Contrast Mode [Phase 2+ -- §11.2.4에 Light/Dark 토큰 정의, High Contrast 토큰은 Phase 2에서 추가]
- 시스템 설정 연동: 사용자 OS의 테마 설정을 자동 감지 (prefers-color-scheme)
- WCAG 2.1 AA 준수: 모든 텍스트-배경 조합에서 최소 4.5:1 명도 대비 확보
- 차트 컬러 자동 조정: 다크 모드에서는 차트 색상을 자동으로 밝은 톤으로 변환

#### 11.11.4 점진적 정보 공개 (Progressive Disclosure)

**적용 방향:**
- 3단계 정보 계층: Level 1 (요약 카드) → Level 2 (차트) → Level 3 (테이블: 원본 데이터)
- 스크롤 텔링형 리포트: 중요 리포트는 타임라인 레이아웃 제공
- 맥락 기반 툴팁: 지표 옆 'i' 아이콘 호버 시 계산 로직, 데이터 소스, 업데이트 시간 표시
- 확장 가능한 카드: 카드 클릭 시 인라인 확장(Accordion)으로 세부 차트 노출

#### 11.11.5 데이터 신뢰성 & 윤리적 투명성 (Trust-Driven UI)

**적용 방향:**
- 데이터 품질 배지: 차트/테이블 우측 상단에 '실시간 | N분 전 업데이트 | 99.8% 완전성' 표시
- 소스 추적: 모든 지표에 '데이터 소스: [S3 Bucket Path]' 링크 제공
- AI 생성 표시: AI 추천 인사이트에는 'AI 생성' 배지와 '신뢰도 85%' 수치 병기
- 감사 추적: 관리자 화면에서 모든 데이터 변경 이력을 타임라인으로 시각화

---

### 11.12 AI 기반 개인화 UI 패턴

#### 11.12.1 AI 인사이트 패널 (우측 사이드바)

**레이아웃:** 화면 우측, 너비 360px (Desktop), 전체 너비 (Mobile 하단 시트), 토글 가능

**섹션 구성:**
- **섹션 1: 실시간 알림 (Alerts)** -- 이상치 탐지, 임계값 초과, 데이터 품질 저하. Error 색상(#f43f5e) 배경, Bell 아이콘
- **섹션 2: AI 발견 사항 (Insights)** -- 상관관계 발견, 트렌드 변화 포인트. Accent 색상(#3b82f6) 배경, Lightbulb 아이콘, 신뢰도 수치(%) 병기
- **섹션 3: 추천 액션 (Recommendations)** -- 재고 최적화 제안, 다음 분석 방향. Success 색상(#10b981) 배경, Target 아이콘, CTA 버튼 포함

> **참고:** 위 섹션 설명의 아이콘명은 lucide-react 기준입니다. 실제 구현 시 lucide-react 아이콘 사용: Bell, Lightbulb, Target

#### 11.12.2 자연어 검색 인터페이스 (상단 고정)

- 위치: 네비게이션 바 중앙, 전체 페이지에서 접근 가능, 너비 600px (Desktop)
- 단축키: Cmd+K (Mac) / Ctrl+K (Windows)로 포커스
- 자동완성: 입력 중 관련 리포트/지표 3개 추천 드롭다운
- 결과: 질의 → SQL 자동 생성 → 차트/테이블 렌더링 (전환 시간 2초 이내 목표)

#### 11.12.3 역할 기반 대시보드 템플릿

| 역할 | 핵심 KPI (3개) | 주요 차트 (2개) | 대시보드 레이아웃 스타일 |
|------|---------------|----------------|------------------------|
| **CEO/CFO** | 전체 매출, 영업이익률, 월간 성장률 | 월별 매출 추이, 지역별 비중 | **Executive Dashboard** |
| **마케터** | 광고 ROAS, 전환율, CAC | 채널별 성과, 캠페인 ROI | **Comparative Analysis** |
| **MD/상품기획** | 재고 회전율, 품절률, 평균 재고일 | 카테고리별 판매 추이, 재고 현황 | **Drill-Down Analytics** |
| **운영자** | 데이터 파이프라인 상태, 에러율, 지연 시간 | 시간별 처리량, 장애 로그 | **Real-Time Monitoring** |
| **분석가** [Phase 2+] | 쿼리 정확도, 데이터 커버리지, 사용 빈도 | 쿼리 성공률 추이, 데이터 소스 활용 비중 | **Drill-Down Analytics** |

**대시보드 레이아웃 스타일 상세:**

| 스타일 | 레이아웃 구조 | 특징 |
|--------|-------------|------|
| **Executive Dashboard** | 상단 KPI 카드 Row(3~5개) + 중앙 대형 차트 2개(2-column) + 하단 요약 테이블 | 한 눈에 전체 현황 파악, 스크롤 최소화 |
| **Comparative Analysis** | 상단 글로벌 필터 바 + 좌-우 분할 비교 패널 + 하단 상세 테이블 | 채널/기간/세그먼트 비교에 최적화 |
| **Drill-Down Analytics** | 상단 Treemap/계층 차트 + 클릭 시 하단 상세 확장 테이블 | 계층 탐색: 카테고리 → 브랜드 → SKU |
| **Real-Time Monitoring** | 상단 상태 인디케이터 그리드(Green/Yellow/Red) + 중앙 타임라인 차트 + 하단 로그 테이블 | 자동 갱신 (30초), 임계값 초과 시 하이라이트 |

---

### 11.13 마이크로 인터랙션 상세화

**로딩 상태 (Loading States):**
- 스켈레톤 UI: 실제 레이아웃과 동일한 회색 플레이스홀더 (Shimmer 애니메이션 2초 반복)
- 프로그레스 바: SQL 실행 중 상단에 얇은 파란색 프로그레스 바 (indeterminate 모드)
- 로딩 시간 표시: 3초 이상 걸리는 작업은 '처리 중... (N초 경과)' 카운터 표시

**데이터 업데이트 (Data Refresh):**
- 숫자 카운팅 애니메이션: KPI 카드 수치 변경 시 0.8초간 카운트업/다운 (CountUp.js)
- 차트 전환: 차트 유형 변경 시 200ms 페이드아웃 → 새 차트 300ms 페이드인
- 실시간 배지: 업데이트 직후 1초간 '방금 업데이트됨' 배지 표시 후 자동 페이드아웃

**사용자 액션 피드백:**
- 버튼 클릭: 0.15초간 scale(0.95) 애니메이션 + 리플 효과
- 토스트 알림: 우측 상단 3초간 표시 후 자동 닫힘 (스와이프 수동 닫기 가능)
- 드래그 앤 드롭: 원본 위치 점선 플레이스홀더, 드롭 가능 영역 파란색 하이라이트

---

### 11.14 Quick Wins: 즉시 적용 가능한 개선 사항

#### 11.14.0 Design as Code 원칙

DataNexus는 "Design as Code" 원칙을 채택합니다. 디자인을 단순한 시각적 산출물이 아닌 코드의 한 형태로 취급하며, 소프트웨어 공학의 버전 관리 원칙을 디자인 영역으로 확장합니다.

**원칙 정의:**

| 원칙 | 설명 | DataNexus 구현 |
|------|------|---------------|
| **디자인은 코드다** | .pen 파일은 JSON 기반 텍스트로 코드와 동일한 수준의 엄밀함으로 관리 | design/ 디렉토리의 .pen 파일이 Git 저장소에 물리적으로 위치 |
| **버전 관리 통합** | 디자인 변경도 Git commit/branch/merge/rollback 대상 | 코드 롤백 시 디자인도 함께 롤백, 특정 시점의 디자인 상태 완벽 복원 |
| **디자인 코드 리뷰** | .pen diff가 PR에 포함되어 팀원이 디자인 변경을 투명하게 검토 | §11.15 QA 체크리스트와 연계된 리뷰 프로세스 |
| **기술 부채 방지** | 디자인과 코드의 불일치를 구조적으로 제거 | 동시 커밋 원칙(§11.5.2)으로 drift 방지 |

**Context-as-Code 아키텍처와의 정렬:**

```txt
Context-as-Code 3-Tier              Design as Code 대응
------------------------------------------------------------
Foundation (불변 규칙)         ->    tokens.json (Single Source of Truth)
                                    design-system/MASTER.md (디자인 시스템)

Domain (도메인 규칙)           ->    design/[페이지명].pen (페이지별 디자인)
                                    design-system/pages/*.md (페이지별 오버라이드)

Execution (런타임 컨텍스트)    ->    .pen diff in PR (디자인 리뷰 컨텍스트)
                                    Sticky Notes (AI 에이전트 지시 사항)
```

**Sticky Notes를 활용한 AI 컨텍스트 전달:**

| Sticky Note 유형 | 용도 | 예시 |
|-----------------|------|------|
| **AI 지시 사항** | UI Teammate에게 구현 방향 전달 | "이 카드는 §11.9 차트 매핑의 Sparkline 패턴을 적용할 것" |
| **팀 소통** | 디자인 의도/제약 사항 공유 | "CEO 리뷰 피드백: KPI 카드 간격을 16px → 24px로 확대" |
| **QA 체크포인트** | 검증 포인트 명시 | "다크 모드에서 §11.2.4 대비 비율 4.5:1 확인 필요" |

---

Phase 1(2026 Q2) 내에 빠르게 구현 가능한 UI 개선 항목:

| # | Quick Win | 기존 예상 | Pencil.dev 활용 시 | 적합도 |
|---|-----------|----------|-----------------|:------:|
| 1 | **홈 대시보드 역할별 재구성** -- CEO/마케터/MD 3개 템플릿으로 분리, 초기 로그인 시 선택 모달 | 3일 | 1.5일 | 높음 |
| 2 | **자연어 검색 UI 추가** -- 상단 네비게이션에 Cmd+K 검색 바 추가 | 2일 | 1일 | 높음 |
| 3 | **데이터 품질 배지** -- 모든 차트 우측 상단에 '실시간 | N분 전' 표시 | 1일 | 0.5일 | 중간 |
| 4 | **다크 모드 MVP** -- Tailwind darkMode='class' 설정 + 기본 컬러 토큰 전환 | 2일 | 2일 | 낮음 |
| 5 | **스켈레톤 UI 적용** -- 현재 스피너를 모두 스켈레톤으로 교체 | 1일 | 0.5일 | 높음 |
| 6 | **z-index 토큰 적용** -- 기존 하드코딩 z-index를 토큰 변수로 일괄 전환 | 0.5일 | 0.5일 | - |
| 7 | **아이콘 통일** -- 이모지/혼용 아이콘을 lucide-react로 일괄 교체 | 1일 | 1일 | - |

> **Pencil.dev 적합도 기준:** 높음 = 캔버스에서 레이아웃 배치 → React 즉시 생성으로 큰 효과, 중간 = 시각적 작업에 부분적 효과, 낮음 = 토큰/코드 레벨 작업이라 효과 제한적, `-` = Pencil 무관 (코드 리팩토링)

**Pencil.dev 시범 적용 추천 순서:**

1. **#2 자연어 검색 UI** -- 단일 컴포넌트로 디자인→코드 전환 효과를 빠르게 검증 가능
2. **#1 역할별 대시보드** -- 3개 레이아웃을 캔버스에서 배치하고 React로 변환, 가장 큰 시간 절약
3. **#5 스켈레톤 UI** -- 시각적 형태 모방이 핵심이라 캔버스 작업에 적합

---

### 11.15 UI QA Pre-delivery 체크리스트

모든 UI 컴포넌트 및 페이지는 배포 전 아래 체크리스트를 통과해야 합니다. 이 체크리스트는 Pull Request 리뷰 시 필수 확인 항목입니다.

#### 11.15.1 인터랙션 품질

| # | 검증 항목 | 기준 | 확인 방법 |
|---|----------|------|----------|
| I-1 | **클릭 가능 요소에 `cursor: pointer`** | 모든 button, link, 클릭 가능 요소 | DevTools 검사 |
| I-2 | **호버 상태 전환** | 150-300ms transition, 시각적 피드백 존재 | 육안 확인 |
| I-3 | **Focus 상태 (키보드)** | `focus-visible` 스타일 적용, outline 2px 이상 | Tab 키로 탐색 |
| I-4 | **Active/Pressed 상태** | 클릭 시 scale 또는 색상 변화 피드백 | 클릭 테스트 |
| I-5 | **Disabled 상태** | opacity 0.5 + cursor: not-allowed + 기능 비활성화 | 비활성 조건 테스트 |

#### 11.15.2 접근성 (Accessibility)

| # | 검증 항목 | 기준 | 확인 방법 |
|---|----------|------|----------|
| A-1 | **색상 대비 (Light Mode)** | 텍스트-배경 4.5:1 이상 (WCAG AA) | axe DevTools / Lighthouse |
| A-2 | **색상 대비 (Dark Mode)** | 텍스트-배경 4.5:1 이상 (WCAG AA) | axe DevTools / Lighthouse |
| A-3 | **키보드 내비게이션** | Tab 순서 논리적, 모든 기능 키보드로 접근 가능 | Tab 키 순회 테스트 |
| A-4 | **스크린 리더 라벨** | 모든 인터랙티브 요소에 aria-label 또는 visible label | axe DevTools |
| A-5 | **모션 감소 존중** | `prefers-reduced-motion: reduce` 시 애니메이션 비활성화 | OS 설정 변경 후 확인 |
| A-6 | **포커스 트랩 (모달)** | 모달 열린 상태에서 Tab이 모달 내부에서만 순환 | 모달 열고 Tab 테스트 |

#### 11.15.3 반응형 & 레이아웃

| # | 검증 항목 | 기준 | 확인 방법 |
|---|----------|------|----------|
| R-1 | **Desktop (1440px)** | 모든 요소 정상 표시, 레이아웃 깨짐 없음 | 브라우저 리사이즈 |
| R-2 | **Desktop (1280px)** | 최소 지원 해상도에서 정상 동작 | 브라우저 리사이즈 |
| R-3 | **Tablet (768px)** | 사이드바 접힘, 주요 기능 사용 가능 | 브라우저 리사이즈 |
| R-4 | **Mobile (375px)** | "데스크톱 접속 안내" 화면 정상 표시 | 브라우저 리사이즈 |
| R-5 | **콘텐츠 오버플로** | 긴 텍스트 truncate/wrap 처리, 수평 스크롤 의도된 곳만 | 긴 텍스트 입력 테스트 |

#### 11.15.4 성능 & 코드 품질

| # | 검증 항목 | 기준 | 확인 방법 |
|---|----------|------|----------|
| P-1 | **Skeleton UI 사용** | 모든 데이터 로딩 영역에 Skeleton 적용 (스피너 금지) | 네트워크 throttling |
| P-2 | **z-index 토큰 사용** | 하드코딩 z-index 값 없음, 모두 토큰 변수 참조 | 코드 검색: `z-index: [0-9]` |
| P-3 | **아이콘 규격 준수** | 모든 아이콘 lucide-react SVG, 이모지 UI 사용 없음 | 코드 리뷰 |
| P-4 | **디자인 토큰 사용** | 하드코딩 색상값 없음, CSS 변수 또는 Tailwind 클래스 사용 | 코드 검색: `#[0-9a-f]{6}` |
| P-5 | **다크 모드 호환** | 모든 컴포넌트에 dark: 변수 적용, 수동 테마 전환 테스트 | 다크모드 토글 |
| P-6 | **애니메이션 Duration** | 기능적 전환만 허용, 최대 400ms (--duration-slow) 이내 | 육안 확인 |
| P-7 | **디자인-코드 동기화** | `.pen` 파일 변경 시 대응 React 코드도 함께 업데이트 | PR diff 확인: `design/*.pen` 변경 시 `src/` 변경 포함 여부 |

#### 11.15.5 데이터 상태 처리

| # | 검증 항목 | 기준 | 확인 방법 |
|---|----------|------|----------|
| S-1 | **Loading 상태** | Skeleton UI 표시 | API 지연 시뮬레이션 |
| S-2 | **Empty 상태** | 안내 메시지 + CTA 표시 | 빈 데이터 조건 |
| S-3 | **Error 상태** | 구체적 에러 메시지 + 재시도 버튼 | API 에러 시뮬레이션 |
| S-4 | **Permission 상태** | 권한 부족 안내 + 요청 경로 | 권한 없는 사용자로 테스트 |

**체크리스트 사용 방법:**
- PR 생성 시 위 체크리스트를 PR 템플릿에 포함합니다.
- 모든 항목에 체크 또는 N/A(해당 없음)를 표기해야 머지가 가능합니다.
- 자동화 가능한 항목(A-1, A-2, P-2, P-3, P-4, P-7)은 CI 파이프라인에서 lint 규칙으로 검증합니다.

#### 11.15.6 Chrome DevTools MCP 런타임 자동 QA (Phase 2+)

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.15.6 참조
> (Chrome DevTools MCP 설정, 자동 검증 항목 D-1~D-7, 워크플로우 통합 다이어그램)

#### 11.15.7 UI UX Pro Max Skill 기반 디자인 검증

> **참고:** 본 섹션은 §11.15 QA 체크리스트의 확장으로, Skill 통합 맥락에서 참조됩니다.

UI 구현 전 및 PR 제출 시, UI UX Pro Max Skill의 디자인 시스템 생성기를 활용하여 DataNexus의 디자인 표준 준수 여부를 자동 검증합니다.

**검증 항목:**

| # | 검증 항목 | 기준 | 확인 방법 |
|---|----------|------|----------|
| U-1 | **디자인 시스템 생성** | DataNexus용 MASTER.md 존재 및 최신 상태 | `design-system/MASTER.md` 파일 확인 |
| U-2 | **컬러 팔레트 일치** | Deep Slate + Sapphire Blue 팔레트 사용 | `--domain color` 검색 결과와 tokens.json 교차 검증 |
| U-3 | **타이포그래피 일치** | Outfit + Plus Jakarta Sans + JetBrains Mono 사용 | `--domain typography` 검색으로 확인 |
| U-4 | **안티패턴 위반 0건** | AVOID 섹션의 모든 항목 미적용 확인 | `--design-system` 출력의 AVOID와 코드 비교 (안티패턴 SSOT: §11.1.2) |
| U-5 | **Pre-delivery 체크리스트** | Skill 생성 체크리스트 전 항목 통과 | `--design-system` 출력의 PRE-DELIVERY CHECKLIST |
| U-6 | **스택 가이드라인 준수** | React + shadcn/ui + Tailwind 스택 규칙 적용 | `--stack react` 결과와 코드 비교 |
| U-7 | **차트 유형 적합성** | §11.9 매핑과 Skill 차트 추천 일치 | `--domain chart` 검색으로 교차 확인 |

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.15.7 (검증 실행 스크립트, bash 명령어) 참조

---

### 11.16 UI UX Pro Max Skill 통합 가이드

#### 11.16.1 개요

[UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (v2.0+)는 AI 기반 디자인 인텔리전스 스킬로, DataNexus의 UI 개발 파이프라인에 통합하여 디자인 시스템 자동 생성, 스타일 추론, 안티패턴 검증을 자동화합니다.

##### Skill 역량-PRD 대응 섹션 매핑

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

##### 통합 목적 상세화 (측정 지표 포함)

| 목적 | 기대 효과 | 측정 지표 |
|------|----------|----------|
| **디자인 시스템 자동 생성** | B2B 엔터프라이즈에 최적화된 스타일/컬러/타이포 자동 추론 | 디자인 토큰 불일치 0건/Sprint |
| **안티패턴 사전 방지** | 100개 산업별 규칙으로 AI 퍼플/핑크, 네온, 과도한 애니메이션 자동 차단 (안티패턴 정의: §11.1.2) | 안티패턴 위반 0건/PR |
| **Pre-delivery 자동 검증** | cursor:pointer, hover 전환, 접근성, SVG 아이콘 등 25개+ 항목 자동 체크 | QA 체크리스트 통과율 95%+ |
| **Claude Code Agent 연동** | Skill 모드로 자동 활성화, Agent Teams 워크플로우와 직접 통합 | UI 컴포넌트 개발 시간 30% 단축 |

---

#### 11.16.2 설치

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.16.2 참조
> (설치 명령어, 설치 후 디렉토리 구조, MASTER.md 초기 생성 및 수동 검증 절차, CLAUDE.md 규칙 파일 배치)

---

#### 11.16.3 DataNexus 커스텀 추론 규칙

UI UX Pro Max의 100개 산업별 추론 규칙 중 DataNexus에 적용되는 핵심 규칙입니다.

**매핑되는 카테고리:**

| UI UX Pro Max 카테고리 | DataNexus 적용 페이지 | 추론 규칙 활용 |
|-----------------------|---------------------|---------------|
| **B2B Enterprise** | 전체 플랫폼 공통 | 패턴, 안티패턴, 컬러 무드 |
| **SaaS** | Chat UI, 검색 UI | 스타일 우선순위, 이펙트 |
| **Trading Dashboard** | Executive/Comparative Dashboard | 차트 유형, 데이터 밀도 |
| **Data Analytics** | Drill-Down, Real-Time Monitoring | 레이아웃 패턴, 인터랙션 |

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.16.3 (bash 명령어, MASTER.md 예상 출력 예시) 참조

---

#### 11.16.4 페이지별 오버라이드 워크플로우

DataNexus의 각 주요 페이지를 구현할 때, MASTER.md를 기본으로 하되 페이지별 특성에 맞는 오버라이드를 적용합니다.

**오버라이드 디렉토리 구조:**

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

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.16.4 (오버라이드 생성 bash 명령어) 참조

---

#### 11.16.5 BI/Analytics Dashboard 스타일 매핑

UI UX Pro Max Skill의 10개 BI/Analytics Dashboard 스타일과 DataNexus §11.12.3 역할별 대시보드의 매핑입니다.

| DataNexus 역할 | DataNexus 레이아웃 스타일 | UI UX Pro Max 대시보드 스타일 | Skill 검색 키워드 |
|---------------|------------------------|----------------------------|------------------|
| CEO/CFO | Executive Dashboard | Executive Dashboard (#3) | `"executive dashboard C-suite"` |
| 마케터 | Comparative Analysis | Comparative Analysis Dashboard (#6) | `"comparative analysis side-by-side"` |
| MD/상품기획 | Drill-Down Analytics | Drill-Down Analytics (#5) | `"drill-down analytics exploration"` |
| 운영자 | Real-Time Monitoring | Real-Time Monitoring (#4) | `"real-time monitoring operations"` |
| 분석가 | (§11.12.3 확장) | Data-Dense Dashboard (#1) | `"data-dense analytics complex"` |

---

#### 11.16.6 UX 가이드라인 교차 참조

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

#### 11.16.7 Claude Code Agent Teams 통합

UI UX Pro Max Skill은 Claude Code의 Skill 모드로 자동 활성화됩니다. Agent Teams 워크플로우에서의 사용 패턴입니다.

**Teammate별 활용:**

| Teammate | 역할 | Skill 활용 방법 |
|----------|------|----------------|
| **UI Teammate** | 프론트엔드 구현 | 구현 전 `--design-system` 실행, MASTER.md 참조하여 코드 생성 |
| **QA Teammate** | 품질 검증 | `--domain ux` 검색으로 안티패턴 검증, Pre-delivery 체크리스트 실행 |
| **Design Teammate** | 디자인 탐색 | `--domain style`, `--domain color`, `--domain typography` 검색으로 대안 탐색 |

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.16.7 참조
> (Pencil MCP 서버 기반 UI Teammate 확장 워크플로우, CLAUDE.md 규칙 코드, Worktree 매핑 상세, Guardian Hook 연동)

---

#### 11.16.8 유지보수 및 업데이트

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.16.8 참조
> (유지보수 주기 테이블, 업데이트 절차)

---

#### 11.16.9 Design Decision Priority (디자인 결정 우선순위)

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

#### 11.16.10 실행 단계 로드맵

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.16.10 참조
> (Phase A-E 단계별 실행 계획, 일별 작업 테이블)

---

#### 11.16.11 성공 기준

UI UX Pro Max Skill 통합의 효과를 정량적으로 평가하기 위한 기준입니다.

| 지표 | 목표치 | 측정 방법 | 측정 시점 |
|------|--------|----------|----------|
| 디자인 토큰 불일치 | 0건/Sprint | tokens.json vs 실제 코드 diff 분석 | Sprint 종료 시 |
| 안티패턴 위반 | 0건/PR | §11.15.7 U-4 체크리스트 (안티패턴 정의: §11.1.2) | PR 리뷰 시 |
| QA 체크리스트 통과율 | 95%+ | §11.15.7 U-1~U-7 전 항목 | PR 리뷰 시 |
| UI 컴포넌트 개발 시간 | 30% 단축 (vs Skill 미사용) | Sprint Velocity 비교 | Phase 1.0 완료 후 |
| MASTER.md 최신 상태 유지 | Sprint 시작 시 갱신 완료 | 파일 수정 일자 확인 | Sprint 시작 시 |

> **주의:** UI 컴포넌트 개발 시간 30% 단축 목표는 Phase 1.0 완료 후 Skill 사용/미사용 비교 측정을 통해 검증합니다. 초기에는 학습 곡선으로 인해 단축 효과가 제한적일 수 있으며, Phase 1.5 이후 안정화가 예상됩니다.

---

#### 11.16.12 리스크 및 대응

| Level | 리스크 | 영향 | 대응 |
|-------|--------|------|------|
| MED | Skill 추론이 DataNexus 커스텀 팔레트와 불일치 | MASTER.md에 범용 컬러 생성 | §11.16.9 Design Decision Priority 적용, tokens.json 값으로 수동 오버라이드 |
| MED | Skill v2.0 -> v3.0 Breaking Change | 디자인 시스템 파일 구조 변경 가능 | §11.16.8 월 1회 CHANGELOG 확인, MASTER.md 백업 유지 |
| LOW | Python 3.x 의존성 충돌 | search.py 실행 불가 | 가상환경 격리 또는 Docker 컨테이너 내 실행 |
| LOW | Agent Teams Experimental 상태 | Skill 모드 자동 활성화 실패 가능 | 수동 `--design-system` CLI 실행으로 Fallback |

**Implementation Strategy §9 "Risks & Mitigations"와의 연계:**

Skill 통합 리스크는 전체 프로젝트 리스크의 하위 항목으로 관리됩니다. Agent Teams Experimental 상태 리스크(Strategy §9 HIGH)와 직접 연관되며, "bkit 설계서는 단독 활용 가능" Fallback이 Skill 통합에도 동일하게 적용됩니다.

---

#### 11.16.13 PRD §9 Phase별 타임라인 연계

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

#### 11.16.14 빠른 참조 명령어

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.16.14 참조
> (마스터 디자인 시스템 생성, 페이지별 오버라이드, 도메인별 검색, 스택별 가이드라인, Skill 업데이트 bash 명령어)

---

## 보강 사항

> 아래 내용은 §11.1~§11.15 보강 섹션입니다.
> §11.15.7 및 §11.16은 상단에 통합되어 있습니다.

**보강 사항 네비게이션 맵:**

본 섹션 이하의 보강 내용은 원본 섹션을 확장/대체합니다. 각 보강 블록은 원본 위치와 최신 위치를 명시합니다.

| 보강 대상 | 원본 위치 | 보강 위치 | 상태 | 내용 요약 |
|----------|----------|----------|------|----------|
| §11.1.2 | §11.1.2 본문 | 하단 보강 섹션 | 원본 유지 + 보강 추가 | 안티패턴 정의 + UI UX Pro Max Skill 교차 검증 테이블 |
| §11.2.7.1 | §11.2.7.1 본문 | §11.2.7.1 (삼원 체계로 통합) | 원본 SUPERSEDED | 이원→삼원 체계(Figma + Pencil + Skill) 확장 |
| §11.14 | §11.14 본문 | §11.14.0 (본문 통합) | 원본 유지 + 보강 추가 | Design as Code 원칙 선언 |

**읽기 가이드:**
- **상태: "원본 SUPERSEDED"** → 최신 위치만 참조
- **상태: "원본 유지 + 보강 추가"** → 원본 위치에서 기본 개념 파악 후, 보강 위치에서 추가 내용 확인

---

## §11.1.2 보강 사항: 안티패턴 교차 검증

기존 §11.1.2 B2B 데이터 포털 안티패턴에 아래 내용을 추가합니다.

**UI UX Pro Max Skill 교차 검증:**

DataNexus의 안티패턴 정의는 UI UX Pro Max Skill v2.0의 100개 산업별 추론 규칙(ui-reasoning.csv) 중 "B2B Enterprise", "SaaS", "Trading Dashboard" 카테고리의 anti_patterns 필드와 교차 검증됩니다.

| DataNexus 안티패턴 | UI UX Pro Max 대응 규칙 | 검증 방법 |
|---------------------|------------------------|-----------|
| 네온/형광 컬러 금지 | `anti_patterns: "Bright neon colors"` (B2B Enterprise) | `--design-system` 출력의 AVOID 섹션 확인 |
| AI 퍼플/핑크 그라데이션 금지 | `anti_patterns: "AI purple/pink gradients"` (Fintech, Banking) | 컬러 팔레트 검증 시 자동 경고 |
| 300ms 초과 장식적 애니메이션 금지 | `anti_patterns: "Harsh animations"` (B2B Enterprise) | UX 가이드라인 검색으로 Duration 기준 확인 |
| 이모지 UI 아이콘 금지 | Pre-delivery checklist: `"No emojis as icons (use SVG)"` | QA 체크리스트 **P-3** 항목과 연동 |

---

## §11.2.7 보강 사항: 디자인 도구 삼원 체계

> 본 보강 사항의 내용은 §11.2.7.1 본문에 삼원 체계로 직접 통합되었습니다. §11.2.7.1을 참조하세요.

---

## §11.2.7.1 보강 사항: Pencil.dev MCP 에이전틱 캔버스

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.2.7.1 보강 참조
> (MCP 에이전틱 캔버스 아키텍처, Figma→Pencil 전송 절차, 운영 제약 사항)

---

## §11.5 보강 사항: Two-Way Sync 양방향 동기화

> 📎 **구현 상세:** Design_System_Implementation_Guide_final.md §11.5 보강 참조
> (Design-to-Code / Code-to-Design 워크플로우, .pen 파일 Git 운영 규칙)

---

## §11.2.7.1 보강 사항: 도구 간 워크플로우 확장

기존 4단계 워크플로우 다이어그램을 아래로 교체합니다.

**도구 간 워크플로우 (확장):**

```txt
[1. 기획]           [2. 디자인 시스템]     [3. 에이전틱 캔버스]    [4. 검증]
  Figma          UI UX Pro Max Skill     Pencil.dev (MCP)       Code Review
    |                   |                   |                      |
    +- 스타일 탐색       +- MASTER.md 생성    +- .pen 파일 생성        +- PR에 .pen diff 포함
    +- 이해관계자 리뷰   +- 페이지별 오버라이드  +- Cmd+K AI 프롬프트     +- tokens.json 일치 검증
    +- 확정 디자인       +- 안티패턴 자동 검증   +- MCP로 요소 직접 조작   +- §11.15 QA 체크리스트
          |             +- 컬러/폰트 추론        +- Code-to-Design 역동기화+- §11.16 Skill 검증
          |                   |                +- 수동 미세 조정         |
          +-- Copy & Paste -->+                +- React 코드 생성        |
          |   (벡터/스타일 보존)                  +- Git commit             |
          |   (이미지: SVG 변환)                  +- Sticky Notes 배치      |
          |                   |                   |                      |
          +-- MASTER.md 참조 -------> 구현 시 우선 적용                   |
          |                                       |                      |
          +------------- Design as Code: .pen + .tsx 동시 커밋 ---------->+
```

---
