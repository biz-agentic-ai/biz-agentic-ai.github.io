# DataNexus Design System Implementation Guide

> **📌 본 문서는 PRD_07_UI_Design_final.md에서 정의된 디자인 요구사항의 구현 가이드입니다.**
> 디자인 철학, 요구사항, 와이어프레임은 PRD_07_UI_Design_final.md를 참조하세요.

---

## PRD 교차 참조

| 구현 가이드 섹션 | PRD_07 원본 섹션 | 내용 |
|-----------------|-----------------|------|
| IG-1.1 | §11.2.1 | 컬러 팔레트 CSS Variables |
| IG-1.2 | §11.2.2 | 타이포그래피 CSS |
| IG-1.3 | §11.2.3 | 그림자 및 애니메이션 토큰 |
| IG-1.4 | §11.2.4 | Dark Mode 컬러 토큰 |
| IG-1.5 | §11.2.6 | z-index 토큰 CSS |
| IG-1.6 | §11.2.7.2 | 디자인 토큰 JSON 스키마 |
| IG-2.1 | §11.4.1 | Chat Input Component |
| IG-2.2 | §11.4.2 | Streaming Response Hook |
| IG-3 | §11.5 | Frontend 프로젝트 구조 |
| IG-4 | §11.6 | Tailwind CSS 설정 |
| IG-5.1 | §11.7 | 접근성 Reduced Motion CSS |
| IG-6 | §11.10 | CSS 2026 신기능 탐색 |
| IG-7 | §11.15.6 | Chrome DevTools MCP QA |
| IG-8 | §11.16 | UI UX Pro Max Skill 구현 |
| IG-9 | 보강 사항 | 구현 상세 보강 |

---

## 목차

- [IG-1. CSS 디자인 토큰 구현](#ig-1-css-디자인-토큰-구현)
  - [IG-1.1 컬러 팔레트 CSS Variables](#ig-11-컬러-팔레트-css-variables)
  - [IG-1.2 타이포그래피 CSS](#ig-12-타이포그래피-css)
  - [IG-1.3 그림자 및 애니메이션 토큰](#ig-13-그림자-및-애니메이션-토큰)
  - [IG-1.4 Dark Mode 컬러 토큰](#ig-14-dark-mode-컬러-토큰)
  - [IG-1.5 z-index 토큰 CSS](#ig-15-z-index-토큰-css)
  - [IG-1.6 디자인 토큰 JSON 스키마](#ig-16-디자인-토큰-json-스키마)
- [IG-2. React 컴포넌트 레퍼런스](#ig-2-react-컴포넌트-레퍼런스)
  - [IG-2.1 Chat Input Component](#ig-21-chat-input-component)
  - [IG-2.2 Streaming Response Hook](#ig-22-streaming-response-hook)
- [IG-3. Frontend 프로젝트 구조](#ig-3-frontend-프로젝트-구조)
- [IG-4. Tailwind CSS 설정](#ig-4-tailwind-css-설정)
- [IG-5. 접근성 구현](#ig-5-접근성-구현)
  - [IG-5.1 Reduced Motion CSS](#ig-51-reduced-motion-css)
- [IG-6. CSS 2026 신기능 기술 탐색 노트](#ig-6-css-2026-신기능-기술-탐색-노트)
- [IG-7. Chrome DevTools MCP 런타임 자동 QA](#ig-7-chrome-devtools-mcp-런타임-자동-qa)
- [IG-8. UI UX Pro Max Skill 구현 가이드](#ig-8-ui-ux-pro-max-skill-구현-가이드)
  - [IG-8.1 설치](#ig-81-설치)
  - [IG-8.2 DataNexus 커스텀 추론 실행](#ig-82-datanexus-커스텀-추론-실행)
  - [IG-8.3 페이지별 오버라이드 생성](#ig-83-페이지별-오버라이드-생성)
  - [IG-8.4 Agent Teams 워크플로우 구현](#ig-84-agent-teams-워크플로우-구현)
  - [IG-8.5 유지보수 및 업데이트](#ig-85-유지보수-및-업데이트)
  - [IG-8.6 실행 단계 로드맵](#ig-86-실행-단계-로드맵)
  - [IG-8.7 빠른 참조 명령어](#ig-87-빠른-참조-명령어)
  - [IG-8.8 검증 실행 스크립트](#ig-88-검증-실행-스크립트)
- [IG-9. 보강 사항: 구현 상세](#ig-9-보강-사항-구현-상세)
  - [IG-9.1 Pencil.dev MCP 에이전틱 캔버스](#ig-91-pencildev-mcp-에이전틱-캔버스)
  - [IG-9.2 Two-Way Sync 양방향 동기화](#ig-92-two-way-sync-양방향-동기화)
  - [IG-9.3 .pen 파일 Git 운영 규칙](#ig-93-pen-파일-git-운영-규칙)
  - [IG-9.4 Design as Code 구현](#ig-94-design-as-code-구현)
  - [IG-9.5 도구 간 워크플로우 확장](#ig-95-도구-간-워크플로우-확장)

---

## IG-1. CSS 디자인 토큰 구현

### IG-1.1 컬러 팔레트 CSS Variables

> PRD_07 §11.2.1 참조

DataNexus 디자인 시스템의 기본 컬러 팔레트를 CSS Custom Properties로 구현합니다. Primary Deep Slate(신뢰/전문성), Accent Sapphire Blue(인텔리전스/신뢰), Semantic Colors를 포함합니다.

```css
:root {
  /* Primary - Deep Slate (신뢰/전문성) */
  --color-primary-50: #f8fafc;
  --color-primary-100: #f1f5f9;
  --color-primary-200: #e2e8f0;
  --color-primary-300: #cbd5e1;
  --color-primary-400: #94a3b8;
  --color-primary-500: #64748b;
  --color-primary-600: #475569;
  --color-primary-700: #334155;
  --color-primary-800: #1e293b;
  --color-primary-900: #0f172a;
  --color-primary-950: #020617;

  /* Accent - Sapphire Blue (인텔리전스/신뢰) */
  --color-accent-50: #eff6ff;
  --color-accent-100: #dbeafe;
  --color-accent-200: #bfdbfe;
  --color-accent-300: #93c5fd;
  --color-accent-400: #60a5fa;
  --color-accent-500: #3b82f6;
  --color-accent-600: #2563eb;
  --color-accent-700: #1d4ed8;
  --color-accent-800: #1e40af;
  --color-accent-900: #1e3a8a;

  /* Semantic Colors */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #f43f5e;
}
```

---

### IG-1.2 타이포그래피 CSS

> PRD_07 §11.2.2 참조

DataNexus의 프리미엄 타이포그래피 시스템을 구현합니다. Outfit(헤드라인), Plus Jakarta Sans(본문), JetBrains Mono(코드/SQL) 3종 폰트를 사용합니다.

```css
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --font-display: 'Outfit', sans-serif;      /* 헤드라인 */
  --font-body: 'Plus Jakarta Sans', sans-serif; /* 본문 */
  --font-code: 'JetBrains Mono', monospace;  /* 코드/SQL */
}
```

**Type Scale:**

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| Display XL | 48px | 600 | Hero 섹션 |
| Display | 36px | 600 | 페이지 제목 |
| H1 | 30px | 600 | 섹션 헤더 |
| H2 | 24px | 600 | 카드 제목 |
| Body | 16px | 400 | 기본 본문 |
| Caption | 12px | 500 | 레이블, 힌트 |

---

### IG-1.3 그림자 및 애니메이션 토큰

> PRD_07 §11.2.3 참조

절제된 그림자(Subtle Shadows)와 부드러운 전환 효과를 위한 토큰을 구현합니다. Duration 토큰은 300ms 초과 장식적 애니메이션을 금지하는 안티패턴 규칙(§11.1.2)과 연계됩니다.

```css
:root {
  /* Subtle, refined shadows */
  --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.06);
  --shadow-md: 0 4px 6px rgba(15, 23, 42, 0.05);
  --shadow-lg: 0 10px 15px rgba(15, 23, 42, 0.04);
  --shadow-accent: 0 4px 14px rgba(59, 130, 246, 0.25);

  /* Timing Functions */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);

  /* Duration */
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 400ms;
}
```

---

### IG-1.4 Dark Mode 컬러 토큰

> PRD_07 §11.2.4 참조

다크모드 전환 시 사용되는 시맨틱 컬러 토큰을 구현합니다. Tailwind의 `darkMode: 'class'` 설정과 함께 사용됩니다.

```css
.dark {
  --bg-primary: var(--color-primary-950);
  --bg-secondary: var(--color-primary-900);
  --bg-tertiary: var(--color-primary-800);
  --bg-surface: var(--color-primary-800);
  --text-primary: var(--color-primary-50);
  --text-secondary: var(--color-primary-300);
  --text-muted: var(--color-primary-500);
  --border-default: var(--color-primary-700);
  --border-subtle: var(--color-primary-800);
  --accent-on-dark: var(--color-accent-400);
}
```

**Light/Dark 대비 비율 검증 테이블:**

| 용도 | Light | Dark | 대비 비율 |
|------|-------|------|----------|
| **ë°°ê²½ (Primary)** | #ffffff | #020617 | - |
| **본문 텍스트** | #334155 | #f8fafc | 16.1:1 / 15.4:1 |
| **보조 텍스트** | #64748b | #cbd5e1 | 4.6:1 / 7.5:1 |
| **Accent 텍스트** | #2563eb | #60a5fa | 4.7:1 / 6.3:1 |

---

### IG-1.5 z-index 토큰 CSS

> PRD_07 §11.2.6 참조

DataNexus의 다수 오버래핑 레이어(Navigation Bar, Chat 패널, SQL 사이드바, 모달, 토스트, 드롭다운 등)를 관리하기 위한 z-index 토큰 시스템을 구현합니다. 임의 z-index 값 사용을 금지합니다.

```css
:root {
  /* z-index Token System — 반드시 이 토큰만 사용 */
  --z-base: 0;           /* 기본 콘텐츠 레이어 */
  --z-dropdown: 100;     /* 드롭다운 메뉴, 자동완성, 컨텍스트 메뉴 */
  --z-sticky: 200;       /* 테이블 sticky 헤더, Navigation Bar */
  --z-overlay: 300;      /* 사이드바 오버레이 (Tablet 모드), 딤드 배경 */
  --z-modal: 400;        /* 모달 다이얼로그, 확인 팝업 */
  --z-toast: 500;        /* 토스트 알림 (항상 모달 위) */
  --z-tooltip: 600;      /* 툴팁 (최상위 레이어) */
}
```

**사용 규칙:**
- 모든 z-index는 반드시 위 토큰 변수를 참조해야 합니다. 하드코딩된 숫자값(예: `z-index: 9999`) 사용을 금지합니다.
- 동일 레벨 내 세분화가 필요한 경우 `calc(var(--z-modal) + 1)` 형태로 사용합니다.
- Tailwind 설정에서도 동일한 토큰을 확장합니다 (§11.6 참조).

**레이어 맵 (DataNexus 주요 컴포넌트):**

| 컴포넌트 | z-index 토큰 | 비고 |
|----------|-------------|------|
| 페이지 콘텐츠 | `--z-base` | 기본 레이어 |
| 자동완성 드롭다운 | `--z-dropdown` | Chat 입력 자동완성, Admin 필터 |
| Navigation Bar | `--z-sticky` | backdrop-blur 포함 |
| 결과 테이블 sticky 헤더 | `--z-sticky` | 첫 번째 행 고정 |
| 사이드바 오버레이 (Tablet) | `--z-overlay` | 딤드 배경 포함 |
| SQL 상세 패널 모달 | `--z-modal` | 전체 화면 SQL 에디터 |
| 토스트 알림 | `--z-toast` | 우측 상단 고정 |
| 차트 호버 툴팁 | `--z-tooltip` | 최상위 |

---

### IG-1.6 디자인 토큰 JSON 스키마

> PRD_07 §11.2.7.2 참조

디자인 토큰의 Single Source of Truth로 사용되는 JSON 스키마와 빌드 파이프라인을 구현합니다. tokens.json에서 CSS Variables와 Tailwind Config를 자동 생성합니다.

**Phase 1 (MVP): JSON 기반 Single Source of Truth + Pencil.dev**

```txt
design-tokens/
├── tokens.json          # 마스터 토큰 정의 (색상, 타이포, 간격, 그림자, z-index)
├── build.js             # JSON → CSS Variables + Tailwind Config 변환 스크립트
└── SYNC-CHECKLIST.md    # Figma + Pencil 동기화 체크리스트
```

```json
// design-tokens/tokens.json (예시)
{
  "color": {
    "primary": {
      "50": { "value": "#f8fafc" },
      "900": { "value": "#0f172a" }
    },
    "accent": {
      "500": { "value": "#3b82f6" }
    }
  },
  "z-index": {
    "base": { "value": "0" },
    "dropdown": { "value": "100" },
    "sticky": { "value": "200" },
    "overlay": { "value": "300" },
    "modal": { "value": "400" },
    "toast": { "value": "500" },
    "tooltip": { "value": "600" }
  }
}
```

**Phase 1~2 도구 도입 로드맵: 자동화 파이프라인 + Pencil MCP 통합**

| 도구 | 역할 | 도입 시점 |
|------|------|----------|
| **Pencil.dev** | IDE 내 디자인 → React 코드 변환, MCP 기반 AI 에이전트 통합 | Phase 1 (즉시) |
| **Tokens Studio** (Figma Plugin) | Figma Variables ↔ JSON 양방향 동기화 | Phase 2 초기 |
| **Style Dictionary** (Amazon) | JSON → CSS/Tailwind/iOS/Android 멀티 플랫폼 빌드 | Phase 2 중반 |
| **CI 파이프라인** | PR 시 tokens.json + `.pen` 파일 변경 감지 → 자동 빌드 + 토큰 일관성 검증 | Phase 2 후반 |

**디자인 동기화 체크리스트 (Phase 1):**
- [ ] tokens.json 변경 시 Figma Local Styles 업데이트
- [ ] tokens.json 변경 시 Pencil.dev 프로젝트 내 토큰 반영 확인
- [ ] Figma 변경 시 tokens.json에 역반영
- [ ] `.pen` 파일에서 생성된 React 코드가 tokens.json의 CSS 변수를 참조하는지 검증
- [ ] 매 Sprint 종료 시 Code ↔ Figma ↔ Pencil 토큰 일치 검증
- [ ] 신규 토큰 추가 시 tokens.json + Figma + Pencil + Tailwind Config 동시 반영

---

## IG-2. React 컴포넌트 레퍼런스

### IG-2.1 Chat Input Component

> PRD_07 §11.4.1 참조

DataNexus Chat UI의 핵심 입력 컴포넌트를 구현합니다. 디자인 시스템의 컬러 토큰, 그림자, 애니메이션 토큰을 활용하며, lucide-react SVG 아이콘을 사용합니다.

```tsx
// components/chat/ChatInput.tsx
import { useState, useCallback } from 'react';
import { Send, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading?: boolean;
}

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
  const [value, setValue] = useState('');

  const handleSubmit = useCallback(() => {
    if (value.trim() && !isLoading) {
      onSend(value.trim());
      setValue('');
    }
  }, [value, isLoading, onSend]);

  return (
    <div className="relative group">
      <div className={cn(
        "flex items-end gap-3 p-4",
        "bg-white dark:bg-primary-900",
        "border border-primary-200 dark:border-primary-700",
        "rounded-2xl shadow-sm",
        "transition-all duration-250",
        "focus-within:border-accent-300 focus-within:shadow-md"
      )}>
        <Sparkles className="w-5 h-5 text-accent-500" />

        <textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit();
            }
          }}
          placeholder="데이터에 대해 무엇이든 물어보세요..."
          className="flex-1 resize-none bg-transparent focus:outline-none"
        />

        <button
          onClick={handleSubmit}
          disabled={!value.trim() || isLoading}
          className={cn(
            "w-10 h-10 rounded-xl",
            "bg-gradient-to-br from-accent-500 to-accent-600",
            "text-white shadow-accent",
            "hover:shadow-accent-hover hover:-translate-y-0.5",
            "disabled:opacity-50"
          )}
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
```

---

### IG-2.2 Streaming Response Hook

> PRD_07 §11.4.2 참조

SSE(Server-Sent Events) 기반 스트리밍 응답을 처리하는 React Custom Hook을 구현합니다. NL2SQL 백엔드 API와 연동하여 실시간 응답 스트리밍을 지원합니다.

```tsx
// hooks/useStreamingChat.ts
import { useState, useCallback, useRef } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  isStreaming?: boolean;
}

export function useStreamingChat(apiUrl: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content,
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    const assistantMessage: Message = {
      id: crypto.randomUUID(),
      role: 'assistant',
      content: '',
      isStreaming: true,
    };

    setMessages(prev => [...prev, assistantMessage]);

    try {
      abortControllerRef.current = new AbortController();

      const response = await fetch(`${apiUrl}/api/v1/query/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: content }),
        signal: abortControllerRef.current.signal,
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder('utf-8', { stream: true });

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n').filter(line => line.startsWith('data: '));

          for (const line of lines) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.content) {
                setMessages(prev =>
                  prev.map(msg =>
                    msg.id === assistantMessage.id
                      ? { ...msg, content: msg.content + data.content }
                      : msg
                  )
                );
              }
            } catch (e) {
              console.warn('SSE JSON parse error:', e, 'raw:', line);
            }
          }
        }
      }

      setMessages(prev =>
        prev.map(msg =>
          msg.id === assistantMessage.id
            ? { ...msg, isStreaming: false }
            : msg
        )
      );
    } catch (error) {
      console.error('Chat error:', error);
      // TODO: PRD_05 §5.5 에러 처리 전략 반영 필요
      // - 사용자에게 에러 메시지 표시 (setMessages로 에러 메시지 추가)
      // - isStreaming 상태 해제 (현재 finally에서 isLoading만 해제)
      setMessages(prev =>
        prev.map(msg =>
          msg.isStreaming ? { ...msg, isStreaming: false, content: msg.content || '오류가 발생했습니다. 다시 시도해 주세요.' } : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  }, [apiUrl]);

  return { messages, isLoading, sendMessage };
}
```

---

## IG-3. Frontend 프로젝트 구조

> PRD_07 §11.5 참조

DataNexus Frontend의 디렉토리 구조를 정의합니다. Next.js App Router 기반으로 구성되며, Pencil.dev 디자인 파일과 디자인 토큰 관리 디렉토리를 포함합니다.

```txt
frontend/
├── src/
│   ├── app/                          # Next.js App Router
│   │   ├── (dashboard)/
│   │   │   ├── page.tsx              # 홈 대시보드
│   │   │   ├── chat/page.tsx         # Chat UI
│   │   │   ├── catalog/page.tsx      # 데이터 카탈로그
│   │   │   └── admin/                # Admin 페이지들
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/                       # 기본 UI (shadcn/ui 기반)
│   │   ├── chat/                     # Chat 컴포넌트
│   │   ├── dashboard/                # 대시보드 컴포넌트
│   │   └── admin/                    # Admin 컴포넌트
│   ├── hooks/                        # 커스텀 훅
│   ├── lib/                          # 유틸리티
│   └── stores/                       # 상태 관리 (Zustand)
├── design/                           # §11.2.7 Pencil.dev 디자인 파일 (Git 관리)
│   ├── dashboard-executive.pen       # CEO/CFO Executive Dashboard
│   ├── dashboard-comparative.pen     # 마케터 Comparative Analysis
│   ├── dashboard-drilldown.pen       # MD/상품기획 Drill-Down Analytics
│   ├── chat-interface.pen            # Chat UI (§11.3.2)
│   ├── search-cmdK.pen              # Cmd+K 자연어 검색 UI
│   ├── components-library.pen        # 공통 컴포넌트 라이브러리
│   └── README.md                     # Pencil.dev 워크플로우 가이드
├── design-tokens/                    # §11.2.7 디자인 토큰 관리
│   ├── tokens.json                   # 마스터 토큰 정의
│   ├── build.js                      # JSON → CSS/Tailwind 변환
│   └── SYNC-CHECKLIST.md            # Figma + Pencil 동기화 체크리스트
├── tailwind.config.ts
└── package.json
```

**design/ 디렉토리 규칙:**
- `.pen` 파일은 Pencil.dev의 오픈 JSON 포맷으로 저장되며, Git diff/merge가 가능합니다.
- 파일명은 `[페이지명]-[레이아웃 스타일].pen` 형식을 따릅니다.
- PR에 `.pen` 파일 변경이 포함된 경우, 해당 컴포넌트의 React 코드도 함께 업데이트해야 합니다.
- Figma에서 확정된 디자인은 Pencil.dev로 복사-붙여넣기 후 `.pen` 파일로 커밋합니다.

---

## IG-4. Tailwind CSS 설정

> PRD_07 §11.6 참조

DataNexus 디자인 시스템의 토큰을 Tailwind CSS 설정으로 구현합니다. 컬러 팔레트, 폰트 패밀리, 그림자, 애니메이션, z-index 토큰을 모두 포함합니다.

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: 'class',
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['Outfit', 'sans-serif'],
        body: ['Plus Jakarta Sans', 'sans-serif'],
        code: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        primary: {
          50: '#f8fafc', 100: '#f1f5f9', 200: '#e2e8f0',
          300: '#cbd5e1', 400: '#94a3b8', 500: '#64748b',
          600: '#475569', 700: '#334155', 800: '#1e293b',
          900: '#0f172a', 950: '#020617',
        },
        accent: {
          50: '#eff6ff', 100: '#dbeafe', 200: '#bfdbfe',
          300: '#93c5fd', 400: '#60a5fa', 500: '#3b82f6',
          600: '#2563eb', 700: '#1d4ed8', 800: '#1e40af',
          900: '#1e3a8a',
        },
        success: '#10b981',
        warning: '#f59e0b',
        error: '#f43f5e',
      },
      boxShadow: {
        'accent': '0 4px 14px rgba(59, 130, 246, 0.25)',
        'accent-hover': '0 8px 20px rgba(59, 130, 246, 0.35)',
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.3s ease-out',
        'shimmer': 'shimmer 2s linear infinite',
      },
      zIndex: {
        'base': '0',
        'dropdown': '100',
        'sticky': '200',
        'overlay': '300',
        'modal': '400',
        'toast': '500',
        'tooltip': '600',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('tailwindcss-animate'),
  ],
};

export default config;
```

---

## IG-5. 접근성 구현

### IG-5.1 Reduced Motion CSS

> PRD_07 §11.7 참조

사용자의 모션 감소 설정을 존중하는 CSS를 구현합니다. `prefers-reduced-motion` 미디어 쿼리를 통해 모든 애니메이션과 전환 효과를 비활성화합니다.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## IG-6. CSS 2026 신기능 기술 탐색 노트

> PRD_07 §11.10 참조

> **📌 본 섹션은 요구사항이 아닌 기술 탐색 노트입니다.** 도입 여부는 Phase 2+ 안정화 확인 후 별도 ADR(Architecture Decision Record)로 결정합니다.

아래 CSS 신기능들은 Chrome 135+에서 지원되기 시작한 실험적 기능입니다. DataNexus의 타겟 브라우저(Chrome 130+)가 해당 버전에 도달하는 Phase 2(2026 Q2-Q3) 이후 안정화를 확인한 뒤 선택적으로 도입합니다.

| 기능 | 도입 시점 | 적용 후보 | 기대 효과 |
|------|----------|----------|----------|
| **appearance: base-select** | Phase 2+ (안정화 후) | Admin 폼 단순 셀렉트 | JS 의존 제거, 네이티브 접근성 확보 |
| **sibling-index()** | Phase 2+ (안정화 후) | 결과 목록 순차 애니메이션 | nth-child 하드코딩 제거 |
| **@starting-style** | Phase 2+ (안정화 후) | 모달/드롭다운 진입 효과 | keyframe 선언 없이 entry 전환 가능 |
| **Typed attr()** | Phase 3 (실험적) | Agent Studio 노드 동적 색상 | data-* → CSS 직접 참조 |
| **::scroll-marker** | Phase 3 (실험적) | Chat 히스토리 탐색 | JS 스크롤 핸들러 제거 |
| **scroll-state query** | Phase 3 (실험적) | 카탈로그 수평 스크롤 | 스크롤 위치 기반 조건부 스타일링 |

---

## IG-7. Chrome DevTools MCP 런타임 자동 QA

> PRD_07 §11.15.6 참조

AI 에이전트가 실제 브라우저에서 런타임 UI 상태를 직접 검사하여, 정적 분석(ESLint)으로 잡을 수 없는 렌더링/인터랙션 버그를 자동 탐지합니다. Chrome DevTools MCP([GitHub](https://github.com/anthropics/anthropic-quickstarts/tree/main/chrome-devtools-mcp-server))를 활용합니다.

**전제 조건:** Chrome 브라우저가 `--remote-debugging-port=9222`로 실행되어야 합니다. CI 환경에서는 Headless Chrome + Puppeteer로 구성합니다.

**자동 검증 항목:**

| # | 검증 항목 | 대응 QA 항목 | DevTools MCP 실행 방법 |
|---|----------|-------------|----------------------|
| D-1 | **콘솔 에러 0건** | 전체 | Console API로 error/warning 수집, 0건 확인 |
| D-2 | **Accessibility 감사** | A-1, A-2, A-4 | Accessibility audit 트리거, WCAG AA 위반 0건 |
| D-3 | **뷰포트 순회 검증** | R-1~R-4 | Device emulation: 1440px → 1280px → 768px → 375px 자동 순회 |
| D-4 | **Skeleton UI 렌더 확인** | P-1, S-1 | Network throttling (Slow 3G) + DOM 스냅샷에서 Skeleton 존재 확인 |
| D-5 | **에러 상태 렌더 확인** | S-3 | Network intercept로 500 응답 강제 → Error UI 렌더 확인 |
| D-6 | **클릭 요소 cursor 검증** | I-1 | DOM 쿼리: `button, a, [role="button"], [onclick]`에 `cursor: pointer` 적용 확인 |
| D-7 | **First Contentful Paint** | 성능 기준 | Performance.mark 기반 프로파일링, FCP ≤ 2s 확인 |

**워크플로우 통합:**

```txt
[정적 분석 (기존)]                    [런타임 분석 (★ 신규)]
ESLint 커스텀 규칙                    Chrome DevTools MCP
├─ z-index 하드코딩 검출              ├─ D-1: 콘솔 에러 검사
├─ 이모지 아이콘 검출                 ├─ D-2: 접근성 감사
├─ 색상 하드코딩 검출                 ├─ D-3: 4개 뷰포트 순회
└─ P-7 디자인-코드 동기화             ├─ D-4: Skeleton UI 확인
                                      ├─ D-5: 에러 상태 확인
         ↓                            ├─ D-6: cursor:pointer 확인
    정적 통과 필수 ──→ 런타임 검증 ──→ └─ D-7: FCP 성능 확인
                                              ↓
                                      Guardian Hook 최종 판정
```

> **💡 TIP:** Phase 1에서는 백엔드 중심 개발이므로 미적용합니다. Phase 2의 Agent Studio UI 개발 착수 시 활성화하세요. CI/CD 파이프라인에서는 GitHub Actions + Headless Chrome으로 D-1~D-7 항목을 PR 체크에 통합합니다.

---

## IG-8. UI UX Pro Max Skill 구현 가이드

### IG-8.1 설치

> PRD_07 §11.16.2 참조

UI UX Pro Max Skill을 DataNexus 프로젝트에 설치하고 초기 디자인 시스템을 생성합니다.

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

**MASTER.md 초기 생성 후 수동 검증:**

`--design-system --persist` 명령으로 MASTER.md를 생성한 후, 아래 항목이 DataNexus PRD §11과 일치하는지 수동 검증합니다. Skill의 추론 엔진은 범용 B2B SaaS 팔레트를 추천할 가능성이 있으므로, DataNexus 커스텀 값과의 불일치를 초기에 포착하여 오버라이드하는 것이 중요합니다.

| 검증 항목 | 기대값 | 불일치 시 조치 |
|-----------|--------|---------------|
| STYLE | Minimalism & Swiss Style (Luxury Minimalism variant) | MASTER.md STYLE 섹션 수동 수정 |
| Primary Color | #0f172a (Deep Slate 900) | tokens.json 값으로 오버라이드 |
| Accent Color | #3b82f6 (Sapphire Blue 500) | tokens.json 값으로 오버라이드 |
| Typography | Outfit / Plus Jakarta Sans / JetBrains Mono | MASTER.md TYPOGRAPHY 섹션 수동 수정 |
| Anti-patterns | AI 퍼플/핑크, 네온, 이모지 아이콘 포함 여부 | §11.1.2 목록과 일치하도록 보완 |

> **핵심 원칙:** tokens.json이 Single Source of Truth이며, MASTER.md는 Skill이 생성한 "추천"이다. 불일치 시 tokens.json이 항상 우선한다. (§11.16.9 Design Decision Priority 참조)

**CLAUDE.md 규칙 파일 배치 (Context-as-Code 정렬):**

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

### IG-8.2 DataNexus 커스텀 추론 실행

> PRD_07 §11.16.3 참조

UI UX Pro Max의 100개 산업별 추론 규칙을 활용하여 DataNexus 전용 디자인 시스템을 생성합니다.

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

### IG-8.3 페이지별 오버라이드 생성

> PRD_07 §11.16.4 참조

DataNexus의 각 주요 페이지를 구현할 때, MASTER.md를 기본으로 하되 페이지별 특성에 맞는 오버라이드를 생성합니다.

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

### IG-8.4 Agent Teams 워크플로우 구현

> PRD_07 §11.16.7 참조

UI UX Pro Max Skill을 Claude Code Agent Teams 워크플로우에 통합합니다. Teammate별 역할 분담, Pencil MCP 서버 기반 확장 워크플로우, CLAUDE.md 규칙 배치를 포함합니다.

**CLAUDE.md 규칙 (frontend/):**

```markdown
## UI UX Pro Max Skill 규칙

1. 모든 UI 구현 작업 시작 전 `design-system/MASTER.md`를 먼저 읽을 것
2. 페이지별 오버라이드 파일이 있으면 MASTER.md보다 우선 적용
3. 새 컴포넌트 개발 시 `--domain style` + `--domain ux` 검색 실행
4. PR 제출 전 §11.15.7 U-1~U-7 항목 확인
5. 안티패턴 위반 시 즉시 수정 (AI 퍼플/핑크, 네온, 이모지 아이콘 등)
   <!-- 안티패턴 SSOT: §11.1.2 (43-69행 + 보강 1782-1798행) -->
6. tokens.json이 MASTER.md보다 우선한다 (§11.16.9 Design Decision Priority)
7. Skill 검증 결과는 .claude/execution/ui-qa-log.md에 기록
```

**Pencil MCP 서버 기반 UI Teammate 확장 워크플로우:**

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

**Worktree 매핑 상세:**

```
main
  +-- worktree/ui-teammate/              # UI Teammate ì "ìš© Worktree
  |     +-- design/                      # .pen 파일 독점 관리
  |     +-- design-system/               # MASTER.md + pages/ 관리
  |     +-- src/components/              # React 컴포넌트 구현
  |     +-- [Skill 활용] 구현 전 --design-system 실행
  |     +-- [Skill 활용] 페이지별 --page 오버라이드 참조
  |
  +-- worktree/qa-teammate/              # QA Teammate ì "ìš© Worktree
        +-- [Skill 활용] --domain ux 안티패턴 검증
        +-- [Skill 활용] Pre-delivery 체크리스트 실행
        +-- .claude/execution/ui-qa-log.md 갱신
```

**Guardian Hook 연동:**

`.claude/execution/ui-qa-log.md`에 Skill 검증 결과를 자동 기록합니다. Context-as-Code 자동 축적 원칙(CLAUDE.md 템플릿 §축적 규칙)에 따라:

| 축적 단계 | 조건 | 대상 파일 |
|----------|------|----------|
| 자동 기록 | Skill 검증 실행 시 | `execution/ui-qa-log.md` |
| 안티패턴 등록 | 동일 위반 3건 누적 시 | `domains/frontend-ui.md` 안티패턴 섹션 (§11.1.2 43-69행 + 보강 1782-1798행과 동기화 필요) |
| 불변 규칙 승격 | 10건+ 누적 시 Distill 리뷰 | `foundation/ui-design-system.md` |

---

### IG-8.5 유지보수 및 업데이트

> PRD_07 §11.16.8 참조

UI UX Pro Max Skill의 지속적인 유지보수 및 업데이트 절차를 정의합니다.

| 항목 | 주기 | 담당 | 방법 |
|------|------|------|------|
| **Skill 버전 업데이트** | 월 1회 | FE 리드 | `uipro update` 실행, CHANGELOG 확인 |
| **MASTER.md 갱신** | Sprint 시작 시 | UI Teammate | `--design-system --persist` 재실행 |
| **페이지 오버라이드 갱신** | 페이지 리디자인 시 | UI Teammate | 해당 `--page` 재실행 |
| **tokens.json과 동기화** | 토큰 변경 시 | FE 리드 | SYNC-CHECKLIST.md 실행 + Skill 재검증 |
| **추론 규칙 커스텀** | 분기 1회 | FE 리드 | ui-reasoning.csv에 DataNexus 전용 규칙 추가 검토 |

---

### IG-8.6 실행 단계 로드맵

> PRD_07 §11.16.10 참조

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

### IG-8.7 빠른 참조 명령어

> PRD_07 §11.16.14 참조

UI UX Pro Max Skill의 주요 CLI 명령어를 빠르게 참조할 수 있는 목록입니다.

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

### IG-8.8 검증 실행 스크립트

> PRD_07 §11.15.7 참조

UI 구현 전 및 PR 제출 시, UI UX Pro Max Skill의 디자인 시스템 생성기를 활용하여 DataNexus의 디자인 표준 준수 여부를 자동 검증합니다.

**검증 항목:**

| # | 검증 항목 | 기준 | 확인 방법 |
|---|----------|------|----------|
| U-1 | **디자인 시스템 생성** | DataNexus용 MASTER.md 존재 및 최신 상태 | `design-system/MASTER.md` 파일 확인 |
| U-2 | **컬러 팔레트 일치** | Deep Slate + Sapphire Blue 팔레트 사용 | `--domain color` 검색 결과와 tokens.json 교차 검증 |
| U-3 | **타이포그래피 일치** | Outfit + Plus Jakarta Sans + JetBrains Mono 사용 | `--domain typography` 검색으로 확인 |
| U-4 | **안티패턴 위반 0건** | AVOID 섹션의 모든 항목 미적용 확인 | `--design-system` 출력의 AVOID와 코드 비교 (안티패턴 SSOT: §11.1.2 43-69행 + 보강 1782-1798행) |
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

## IG-9. 보강 사항: 구현 상세

### IG-9.1 Pencil.dev MCP 에이전틱 캔버스

> PRD_07 보강 §11.2.7.1 MCP 참조

Pencil.dev의 MCP(Model Context Protocol) 기반 에이전틱 캔버스 아키텍처를 구현합니다. AI 에이전트가 디자인 캔버스를 직접 읽고 조작할 수 있는 환경을 제공합니다.

**MCP 통합 구조:**

```txt
Claude Code Agent Teams
  |
  +-- UI Teammate (Pencil MCP Client)
  |     |
  |     +-- read_canvas()     : 캔버스 요소/레이어 구조 조회
  |     +-- place_element()   : 벡터 요소 배치/수정
  |     +-- update_style()    : CSS 속성/디자인 토큰 적용
  |     +-- generate_code()   : 캔버스 → React/TSX 코드 변환
  |     |
  |     +-- Pencil MCP Server (로컬 실행)
  |           |
  |           +-- .pen 파일 (JSON 기반, Git 관리)
  |           +-- tokens.json 참조
  |           +-- design-system/MASTER.md 참조
  |
  +-- QA Teammate
  |     +-- .pen diff 검증 + §11.15 체크리스트
  |
  +-- Backend Teammate
        +-- API 스키마 변경 시 UI Teammate에 컨텍스트 전달
```

**에이전틱 캔버스 워크플로우:**

| 단계 | 사용자 액션 | AI 에이전트 동작 | 산출물 |
|------|-----------|-----------------|--------|
| 1. 프롬프트 | `Cmd+K` → 자연어 명령 입력 | MCP를 통해 캔버스 시각적 맥락 인지 | - |
| 2. 디자인 생성 | 명령 확인 | 벡터 요소 직접 배치, 레이아웃 구성 | .pen 파일 변경 |
| 3. 코드 변환 | "React 컴포넌트로 구현해 줘" | 캔버스 구조 분석 → TSX + Tailwind 생성 | .tsx 파일 생성 |
| 4. 미세 조정 | 레이어 패널/속성 편집기로 수동 편집 | - (토큰 비용 절약) | .pen 파일 갱신 |
| 5. 커밋 | `Cmd+S` → Git commit | - | .pen + .tsx 동시 커밋 |

**프롬프트 예시 (DataNexus 맥락):**

```bash
# Executive Dashboard KPI 카드 생성
"이 캔버스에 CEO용 KPI 요약 카드 4개를 Grid 레이아웃으로 배치해 줘.
각 카드에는 지표명, 현재값, 전월 대비 변화율, 미니 스파크라인 영역이 포함되어야 해.
§11.2.1 컬러 팔레트와 §11.2.2 타이포그래피를 준수해."

# 기존 컴포넌트 시각화 (Code-to-Design)
"src/components/chat/MessageBubble.tsx를 캔버스에 시각화해 줘.
코드의 props와 스타일을 분석해서 캔버스 요소로 변환해."
```

**Figma → Pencil.dev 데이터 전송 절차:**

**1단계: 환경 준비**

| 항목 | 요구 사항 | 확인 방법 |
|------|----------|----------|
| Pencil 확장 설치 | Cursor 확장 프로그램 메뉴에서 설치 | Extensions 패널 확인 |
| Claude Code CLI | 시스템 설치 + 인증 완료 | `claude --version` 실행 |
| MCP 서버 활성화 | Cursor 설정 > Tools & MCP > Pencil 서버 활성 | 녹색 상태 확인 |
| .pen 파일 생성 | 프로젝트 루트 또는 `design/` 디렉토리에 생성 | 캔버스 렌더링 확인 |

**2단계: 디자인 이식**

| 작업 | 절차 | 주의 사항 |
|------|------|----------|
| 프레임/컴포넌트 복사 | Figma에서 선택 → `Cmd+C` → Pencil 캔버스에서 `Cmd+V` | 레이어 계층 구조, 오토 레이아웃 속성 보존 (1px 정확도) |
| 이미지 에셋 | Figma에서 이미지를 SVG로 Export 후 별도 Import | 래스터 이미지 직접 복사 미지원 (현재 제약) |
| 디자인 토큰 | Figma의 CSS 변수/토큰 표를 프롬프트에 텍스트로 입력 | AI가 해석하여 Pencil 내 디자인 변수로 자동 등록 |
| 복잡한 Auto Layout | 전환 후 일부 미세 조정 필요 | 단순 레이아웃은 정확, 중첩 Auto Layout은 수동 보정 |

**3단계: 코드 생성**

캔버스 요소 선택 → `Cmd+K` → 구체적 기술 스택 명시 → AI가 프로젝트 컨벤션 참조하여 코드 생성.

```bash
# 권장 프롬프트 패턴
"이 [컴포넌트명]을 Tailwind CSS와 TypeScript를 사용하는 React 컴포넌트로 구현해 줘.
design-system/MASTER.md의 규칙을 준수하고, tokens.json의 CSS 변수를 참조해."
```

**Pencil.dev 운영 제약 사항:**

| 항목 | 상세 |
|------|------|
| **자동 저장 미지원** | 현재 자동 저장 기능 없음. 작업 중 `Cmd+S` 수동 저장 필수. Git 커밋 주기적 실행 권장 |
| **이미지 직접 복사 불가** | Figma 래스터 이미지는 직접 복사 불가. SVG 변환 또는 별도 Import 필요 |
| **MCP 서버 연결 실패 시** | Cursor 재시작 또는 Claude CLI 로그인 상태 재확인으로 해결 |
| **.pen 파일 위치** | 반드시 소스 코드와 동일한 워크스페이스 내 위치해야 AI가 파일 간 관계 인지 가능 |

---

### IG-9.2 Two-Way Sync 양방향 동기화

> PRD_07 보강 §11.5 참조

Pencil.dev의 Design-to-Code 및 Code-to-Design 양방향 동기화 워크플로우를 구현합니다. 코드에서 시작된 변경 사항을 시각적으로 검증하고, 디자인과 코드의 일관성을 유지합니다.

**Design-to-Code (디자인 → 코드):**

```txt
.pen 캔버스 디자인 완료
  → Cmd+K: "React 컴포넌트로 구현"
  → AI가 캔버스 시각적 구조 분석
  → .tsx 파일 생성 (tokens.json CSS 변수 참조)
  → Git commit (.pen + .tsx 동시)
```

**Code-to-Design (코드 → 디자인):**

```txt
기존 React 컴포넌트 파일 지정
  → AI가 코드의 props, 스타일, 레이아웃 분석
  → 캔버스 위에 시각적 요소로 변환/재현
  → 캔버스에서 시각적 수정 (레이아웃, 간격, 색상 등)
  → Cmd+K: "원본 코드를 수정 사항에 맞춰 업데이트해 줘"
  → .tsx 파일 업데이트 + .pen 파일 갱신
```

**Code-to-Design 활용 시나리오:**

| 시나리오 | 절차 | 기대 효과 |
|---------|------|----------|
| 코드 리뷰 시 시각적 검증 | PR의 .tsx 변경 → 캔버스로 불러와 시각 확인 | 코드만으로 파악 어려운 레이아웃 문제 사전 발견 |
| 기존 컴포넌트 리디자인 | 현재 코드 → 캔버스 시각화 → 수정 → 코드 역반영 | 디자인 도구 전환 없이 IDE 내에서 리디자인 완료 |
| 디자인 시스템 감사 | 전체 컴포넌트 → 캔버스 일괄 시각화 → 토큰 일관성 확인 | Sprint 종료 시 디자인-코드 불일치 자동 탐지 |

---

### IG-9.3 .pen 파일 Git 운영 규칙

> PRD_07 보강 §11.5.2 참조

`.pen` 파일의 Git 기반 버전 관리 및 브랜치 전략을 구현합니다. `.pen` 파일은 JSON 기반 텍스트 데이터로 구성되어 Git의 텍스트 기반 Diff/Merge가 완벽히 작동합니다.

**브랜치 전략과 디자인 실험:**

```txt
main
  +-- feature/dashboard-v2        # 코드 + 디자인 함께 브랜치
  |     +-- design/dashboard-executive.pen  (실험적 레이아웃)
  |     +-- src/components/dashboard/       (대응 코드)
  |     +-- PR: .pen diff + .tsx diff 동시 리뷰
  |
  +-- feature/chat-redesign       # 독립적 디자인 실험
        +-- design/chat-interface.pen       (새로운 대화 UI)
        +-- src/components/chat/            (대응 코드)
```

**Git 운영 원칙:**

| 원칙 | 설명 | 근거 |
|------|------|------|
| **동시 커밋** | .pen 파일 변경과 대응 React 코드를 반드시 같은 커밋에 포함 | 코드 롤백 시 디자인도 함께 롤백되는 완벽한 동기화 보장 |
| **PR 디자인 리뷰** | .pen diff를 PR에 포함하여 디자인 변경 사항을 코드 리뷰와 동일 수준으로 검토 | 디자인 투명성 확보, 변경 추적 가능 |
| **브랜치별 독립 실험** | Git 브랜치에서 디자인 실험을 독립적으로 진행, merge 시점에 통합 | Worktree 병렬 개발(Implementation Strategy §15 STEP 20)과 연계 |
| **Worktree 매핑** | Agent Teams Teammate별 Worktree에 담당 .pen 파일 배치 | UI Teammate가 design/ 하위 파일을 독점 관리 |

---

### IG-9.4 Design as Code 구현

> PRD_07 보강 §11.14.0 참조

DataNexus의 "Design as Code" 원칙을 구현합니다. 디자인을 단순한 시각적 산출물이 아닌 코드의 한 형태로 취급하며, 소프트웨어 공학의 버전 관리 원칙을 디자인 영역으로 확장합니다.

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
Foundation (불변 규칙)         →    tokens.json (Single Source of Truth)
                                    design-system/MASTER.md (디자인 시스템)

Domain (도메인 규칙)           →    design/[페이지명].pen (페이지별 디자인)
                                    design-system/pages/*.md (페이지별 오버라이드)

Execution (런타임 컨텍스트)    →    .pen diff in PR (디자인 리뷰 컨텍스트)
                                    Sticky Notes (AI 에이전트 지시 사항)
```

**Sticky Notes를 활용한 AI 컨텍스트 전달:**

Pencil.dev 캔버스에 배치하는 Sticky Notes는 Agent Teams의 컨텍스트 전달 메커니즘으로 활용됩니다.

| Sticky Note 유형 | 용도 | 예시 |
|-----------------|------|------|
| **AI 지시 사항** | UI Teammate에게 구현 방향 전달 | "이 카드는 §11.9 차트 매핑의 Sparkline 패턴을 적용할 것" |
| **팀 소통** | 디자인 의도/제약 사항 공유 | "CEO 리뷰 피드백: KPI 카드 간격을 16px → 24px로 확대" |
| **QA 체크포인트** | 검증 포인트 명시 | "다크 모드에서 §11.2.4 대비 비율 4.5:1 확인 필요" |

---

### IG-9.5 도구 간 워크플로우 확장

> PRD_07 보강 §11.2.7.1 참조

기존 3단계 워크플로우를 4단계(기획 → 디자인 시스템 → 에이전틱 캔버스 → 검증)로 확장한 통합 워크플로우 다이어그램입니다.

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

**디자인 도구 삼원 체계: Figma + Pencil.dev + UI UX Pro Max Skill:**

| 역할 | 도구 | 용도 | 산출물 |
|------|------|------|--------|
| **탐색/기획** | **Figma** | 초기 스타일 가이드, 브레인스토밍, 이해관계자 리뷰 | Figma 파일 (클라우드) |
| **디자인 인텔리전스** | **UI UX Pro Max Skill** | 산업별 디자인 시스템 자동 생성, 스타일/컬러/타이포 추론 | design-system/MASTER.md, pages/*.md |
| **구현 가속** | **Pencil.dev** | IDE 내 디자인 -> React 코드 변환, 컴포넌트 프로토타이핑 | `.pen` 파일 (Git 관리) |
| **토큰 관리** | **tokens.json** | Single Source of Truth (색상, 타이포, 간격, z-index) | CSS Variables + Tailwind Config (build.js 자동 생성 — 본 문서 내 코드는 예시) |
