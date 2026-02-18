# DataNexus 빌딩 로그 - 블로그 런칭 플랜

## 현재 상태 진단

Hugo + PaperMod 블로그가 https://biz-agentic-ai.github.io 에 배포되어 있으나,
실제 포스트가 없고 README가 홈페이지에 노출되는 상태다.
GitHub Actions CI/CD는 정상 작동 중.

---

## STEP 1. hugo.toml 수정 (즉시)

현재 설정에서 아래 항목을 추가/수정한다.

```toml
baseURL = "https://biz-agentic-ai.github.io/"
languageCode = "ko"
title = "Junho Lee | DataNexus 빌딩 로그"
theme = "PaperMod"

[params]
  author = "Junho Lee"
  description = "Data & AI Architect가 온톨로지 기반 데이터 에이전트를 만드는 과정"
  ShowReadingTime = true
  ShowPostNavLinks = true
  ShowBreadCrumbs = true
  ShowCodeCopyButtons = true
  ShowToc = true
  TocOpen = false
  defaultTheme = "auto"

  [params.homeInfoParams]
    Title = "DataNexus 빌딩 로그"
    Content = "엔터프라이즈 데이터를 자연어로 탐색하는 AI 에이전트, DataNexus를 만드는 과정을 기록합니다."

  [[params.socialIcons]]
    name = "github"
    url = "https://github.com/biz-agentic-ai"

  [[params.socialIcons]]
    name = "linkedin"
    url = "https://www.linkedin.com/in/leejuno/"

[taxonomies]
  category = "categories"
  tag = "tags"
  series = "series"

[markup.goldmark.renderer]
  unsafe = true

[markup.highlight]
  codeFences = true
  guessSyntax = true
  lineNos = false
  style = "monokai"
```

---

## STEP 2. 콘텐츠 구조 설정

```
content/
├── about.md                    # About 페이지 (경력 + DataNexus 소개)
├── posts/
│   └── datanexus/              # DataNexus 빌딩 로그 시리즈
│       ├── 001-why-datanexus.md
│       ├── 002-architecture-decisions.md
│       ├── ...
│       └── (TIL 포스트들)
└── archives.md                 # 아카이브 페이지
```

---

## STEP 3. About 페이지 작성

파일: `content/about.md`

```markdown
---
title: "About"
layout: "single"
url: "/about/"
summary: "Junho Lee - Data & AI Platform Architect"
ShowToc: false
---

20년차 데이터 플랫폼 엔지니어. 애플리케이션 개발자로 시작해서 DW/BI,
Technical Lead, 컨설팅 본부장을 거쳐 지금은 AI 기반 데이터 플랫폼을 만들고 있다.

삼성전자 60TB급 DW 클라우드 마이그레이션, 54억 규모 차세대 정보계,
8억 규모 BI Agent 구축 등을 리드했고, 지금은 온톨로지 기반 NL2SQL과
GraphRAG를 결합한 DataNexus를 설계/구축 중이다.

이 블로그는 DataNexus를 만들어가는 과정에서 배운 것들을 기록한다.

## Contact

- GitHub: [@biz-agentic-ai](https://github.com/biz-agentic-ai)
- LinkedIn: [linkedin.com/in/leejuno](https://www.linkedin.com/in/leejuno/)
```

---

## STEP 4. 시리즈 구성안

시리즈명: **datanexus-building-log**

### Phase 0: 왜 만드는가 (1~2편)

| # | 제목 | 핵심 내용 |
|---|------|----------|
| 001 | 왜 DataNexus를 만드는가 | 문제 정의, Non-verifiable Domain 방어선 논리, 24개월 골든타임 |
| 002 | 아키텍처를 결정한 과정 | DataHub + Vanna + ApeRAG + DozerDB 조합에 도달하기까지의 의사결정 |

### Phase 0.5~1: 만들면서 배운 것 (TIL 시리즈, 지속)

| # | 제목 (예시) | 카테고리 |
|---|------------|---------|
| 003 | DataHub Glossary를 온톨로지로 쓸 수 있을까 | ontology |
| 004 | SKOS 호환 레이어를 왜 넣었나 | ontology |
| 005 | Vanna 2.0의 User-Aware 설계가 Row-level Security에 주는 것 | nl2sql |
| 006 | DozerDB Multi-DB로 테넌트를 격리한 이유 | architecture |
| 007 | CQ(Competency Questions)로 온톨로지를 검증하는 법 | ontology |
| 008 | Query Router: 결정론적 vs 확률론적 라우팅 | agent |
| 009 | 79% Rule - 에이전트 태스크를 쪼개는 기준 | agent |
| 010 | PRD를 17개 파일로 쪼개고 나서 생긴 일 | process |

(이후 개발 진행에 따라 TIL 추가)

### 사용할 태그 체계

```
categories: [architecture, ontology, nl2sql, agent, rag, process]
tags: [datahub, vanna, dozerdb, aperag, skos, graphrag, prd, til]
```

---

## STEP 5. 첫 포스트 (아래 별도 파일로 제공)

---

## 작성 스타일 가이드

### DO

- 문제 → 시도 → 결과/교훈 구조
- 기술 용어는 영어 그대로 (NL2SQL, GraphRAG, Ontology)
- 코드/설정/다이어그램은 필요한 만큼만
- 한 포스트 500~1000자 (TIL답게 짧게)
- "~했다", "~이다" 체 (블로그 글답게)
- 의사결정의 근거를 명시 ("A 대신 B를 선택한 이유는...")

### DON'T

- "이 글에서는 ~에 대해 알아보겠습니다" 류의 서론
- 감성적 표현 ("드디어!", "놀랍게도!")
- 결론 없는 나열
- AI가 작성한 티가 나는 균일한 문장 길이
- 이모지 남발
- 모든 걸 설명하려는 욕심 (하나의 글에 하나의 주제)

### 문체 예시 (Good)

> DozerDB의 Multi-DB 기능으로 테넌트 격리를 구현했다. Neo4j Community에서는
> 단일 DB만 지원하는데, DozerDB 플러그인을 얹으면 datahub_db, insight_kb_db를
> 별도로 운영할 수 있다. 다만 Fabric은 아직 미지원이라 크로스 DB 쿼리는 Phase 3+로 미뤘다.

### 문체 예시 (Bad)

> 안녕하세요! 오늘은 DozerDB의 놀라운 Multi-DB 기능에 대해 알아보겠습니다.
> DozerDB는 정말 강력한 도구인데요, Neo4j Community Edition의 한계를 극복할 수
> 있게 해줍니다. 자, 그럼 시작해볼까요?

---

## 실행 순서 요약

1. **hugo.toml 수정** → 사이트 메타 정보, 한국어 설정, 소셜 링크
2. **About 페이지 생성** → `content/about.md`
3. **첫 포스트 발행** → `content/posts/datanexus/001-why-datanexus.md`
4. **README 정리** → 홈에 README 대신 포스트 목록 노출되도록 확인
5. **2~3편 추가 발행** → 아키텍처 결정, 첫 TIL
6. **LinkedIn에 첫 포스트 공유** → 기술 포트폴리오 노출 시작
