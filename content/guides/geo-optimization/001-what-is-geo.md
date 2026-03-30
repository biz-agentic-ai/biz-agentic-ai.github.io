---
title: "1. GEO란 무엇인가 - SEO 너머의 AI 인용 전략"
date: 2026-03-26T10:00:00+09:00
draft: false
summary: "구글 상위 10위 페이지 중 AI가 인용하는 비율은 9%에 불과하다. SEO 순위가 AI 인용을 보장하지 않는 시대, GEO의 3대 원칙과 학술 근거를 정리한다."
categories: ["GEO 최적화"]
tags: ["geo", "seo", "ai-search", "schema-org", "json-ld"]
series: ["geo-optimization-guide"]
series_order: 1
author: "Junho Lee"
ShowToc: true
---

{{< series-toc >}}

## 구글 1페이지 노출만으로 충분할 줄 알았다

SEO를 열심히 해서 구글 검색 1페이지에 올라갔다. 자연스럽게 검색 유입도 늘었다. 여기까지는 익숙한 시나리오다.

요즘 주변에서 검색하는 방식이 달라졌다. ChatGPT에 "가성비 노트북 추천해줘"라고 치고, Perplexity에서 "서울 가족여행 호텔"을 찾는다. Google AI Overview가 검색 결과 위에 답을 먼저 깔아버린다.

![검색 패러다임의 변화](/images/geo/slide_01_paradigm_shift.png)

클릭이 사라지고 있다. AI가 대신 답해주니까.

[Ahrefs 쪽 분석](https://ahrefs.com/blog/ai-search-overlap/)을 보면 AI가 인용하는 URL 중 구글 검색 상위 10위에 드는 건 **9%** 에 불과하다. SEO 상위 노출이 AI 인용을 보장하지 않는다. 별도의 최적화 레이어가 필요하다.

그게 GEO(Generative Engine Optimization)다.

## GEO는 무엇인가

ChatGPT, Perplexity, Gemini, Google AI Overview 같은 AI 검색엔진이 우리 콘텐츠를 답변에 인용하게 만드는 게 GEO다. 데이터 구조 자체를 AI가 읽기 좋게 바꾸는 작업이다.

SEO는 사람이 클릭하게 만드는 거였다. GEO는 AI가 우리를 출처로 찍게 만드는 거다.

| 구분 | SEO | GEO |
|------|-----|-----|
| 목표 | 클릭 유도 (Traffic) | AI 답변 내 인용 (Citation) |
| 신뢰 기준 | 키워드 밀도, 백링크 수 | 식별 가능성, 구조화 데이터 |
| 인식 주체 | 사람 + 검색엔진 봇 | 생성형 AI 모델 |
| 핵심 기술 | 메타태그, 콘텐츠 최적화 | JSON-LD, Schema.org, FAQ 구조화 |
| KPI | 노출 순위, CTR | 언급률, 인용 정확도 |

오해하면 안 되는 게, GEO한다고 SEO를 버리는 게 아니다. SEO 기반이 탄탄해야 GEO도 먹힌다. GEO는 그 위에 얹는 거다.

## 왜 지금인가

데이터를 보면 이미 흐름이 바뀌고 있다.

[ChatGPT WAU가 8억을 넘었다](https://openai.com/index/how-people-are-using-chatgpt/). 한국은 세계 2위 유료 구독 시장이고, 경제활동인구 셋 중 하나는 AI를 쓴다. [Gartner](https://www.gartner.com/en/newsroom/press-releases/2024-02-19-gartner-predicts-search-engine-volume-will-drop-25-percent-by-2026-due-to-ai-chatbots-and-other-virtual-agents)는 2026년까지 전통 검색량이 **25%** 줄어들 거라고 본다. [Capgemini 보고서](https://www.capgemini.com/news/press-releases/71-of-consumers-want-generative-ai-integrated-into-their-shopping-experiences/)를 보면 소비자 3분의 2 이상이 AI 추천 제품을 실제로 산다. Google 검색의 절반 이상이 **제로클릭** 으로 끝나는데, AI Overview가 깔리면 이 비율은 더 올라간다.

전환율 쪽이 더 흥미롭다. [GrackerAI 쪽 분석](https://gracker.ai/static/GEO%202026%20Data%20Sheet.Disb-CIl.pdf)을 보면 AI 검색 유입의 구매 전환율이 14.2%다. 전통 구글 검색 대비 **5배** 다. [Adobe 쪽 데이터](https://business.adobe.com/blog/the-explosive-rise-of-generative-ai-referral-traffic)에서도 AI 유입 방문당 매출이 기존보다 2.5배 이상 높게 나온다.

트래픽은 줄어드는데 AI가 골라준 결과의 전환율은 오히려 높다. 많이 노출되느냐보다, AI한테 선택되느냐가 매출을 가른다.

## GEO 3대 원칙

GEO를 적용할 때 매번 부딪히는 질문이 있다. 이 상품을 AI가 다른 것과 구분할 수 있나? 용도와 맥락을 알아채나? 그리고 읽은 다음에 출처를 달아줄 수 있는 구조인가?

![GEO 3대 원칙: Identity, Context, Citability](/images/geo/slide_02_principles.png)

### Identity - 식별 가능성

AI가 상품이나 서비스를 명확히 구분할 수 있어야 한다.

GS1 GTIN/GLN 같은 국제 표준 식별자가 핵심이다. "초코스틱 오리지널"과 "초코스틱 아몬드"를 AI가 별개 상품으로 인식하려면 각각 고유한 GTIN이 있어야 한다. 대표코드 하나로 묶어놓으면 AI는 둘을 구분하지 못한다.

### Context - 맥락 연결성

상품의 용도, 관계, 위치를 AI가 이해할 수 있어야 한다.

카테고리 계층, Variant(맛/용량/색상) 관계, 브랜드-제품-SKU 구조. 이런 맥락이 구조화되어 있어야 AI가 "20대 남성에게 어울리는 운동화"라는 질문에 적절한 상품을 연결할 수 있다.

### Citability - 인용 가능성

AI가 콘텐츠를 읽고 출처를 밝힐 수 있는 구조여야 한다.

JSON-LD, FAQ Schema, robots.txt 설정이 여기에 해당한다. 아무리 좋은 데이터라도 AI 크롤러가 접근할 수 없거나 파싱하기 어려운 구조면 AI는 그냥 넘겨버린다.

표로 보면 이렇다:

| 원칙 | 핵심 질문 | 핵심 기술 | 검증 기준 |
|------|-----------|-----------|-----------|
| Identity | AI가 이걸 다른 것과 구분하는가? | GS1 GTIN/GLN | 식별자 등록, Variant 구분 |
| Context | AI가 용도와 관계를 이해하는가? | 카테고리, 지식그래프 | 메타데이터 품질, 채널 간 정합성 |
| Citability | AI가 읽고 출처를 밝힐 수 있는가? | JSON-LD, FAQ, robots.txt | 구조화 데이터 유효성, 크롤러 접근 허용 |

## Invisible GEO vs Visible GEO

구현 방식은 두 갈래로 나뉜다.

**Invisible GEO** 는 `<head>` 태그 안의 JSON-LD다. 사용자 눈에는 안 보이지만 AI와 검색엔진이 직접 파싱한다. AI 인용률을 끌어올리는 가장 강력한 방법이다. 다만 SPA로 되어 있다면 SSR(Server-Side Rendering) 전환이 선행되어야 한다.

```html
<!-- Invisible GEO: <head> 안의 JSON-LD -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "초코스틱 오리지널",
  "gtin13": "8801234567890",
  "brand": { "@type": "Brand", "name": "K식품" },
  "offers": {
    "@type": "Offer",
    "price": 1500,
    "priceCurrency": "KRW",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

**Visible GEO** 는 `<body>` 안의 HTML 콘텐츠다. FAQ 페이지, 상품 상세 설명, 영양정보 표. 사람도 읽고 AI도 읽는다. 기술적 장벽이 낮아서 당장 시작할 수 있다.

| 항목 | Invisible GEO | Visible GEO |
|------|--------------|-------------|
| 위치 | `<head>` JSON-LD | `<body>` HTML |
| SEO 효과 | 높음 | 보통 |
| AI 인용률 | 높음 | 높음 |
| 구현 난이도 | 높음 (SSR 필요) | 낮음 |
| 사용자 경험 | 없음 (기계 전용) | 직접 노출 |

실무에서는 둘 다 쓴다. JSON-LD로 기계가 파싱하기 좋게 넣고, HTML로 사람과 AI 모두 읽을 수 있게 깔아두는 식이다.

## AI는 이미 잘 답하고 있다, 문제는 출처다

"가족 여행 호텔 추천해줘." 이 질문을 Genspark, Perplexity, ChatGPT에 동시에 던져봤다. 세 AI 모두 비슷한 답을 내놓는다. 수영장 정보, 객실 가격, 조식까지. 답변 품질은 이미 충분하다.

문제는 출처다. Genspark은 공식 사이트의 Schema 데이터를 직접 인용하고, Perplexity는 네이버 블로그와 여기어때를 긁어온다. ChatGPT는 공식 사이트를 참조하지만 구조화 데이터 없이는 정밀도가 떨어진다. 같은 호텔인데 AI마다 보여주는 가격이 다르다.

Schema가 공식 인용을 보장하진 않는다. AI가 공식 사이트를 쉽게 파싱할 수 있게 만들어서, 블로그 대비 공식 출처 선택 확률을 높이는 거다. On-Site GEO가 중요한 이유가 여기 있다.

<div class="demo-btn-group">
<a href="/demo/geo-demo-a.html" target="_blank" rel="noopener" onclick="window.open(this.href,'geo-a','width=1200,height=800,scrollbars=yes,resizable=yes');return false;" class="demo-btn demo-btn--primary"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>Demo - AI 검색 비교</a>
</div>

## 연구 결과가 말해주는 것

[Princeton대와 Georgia Tech 연구팀](https://arxiv.org/abs/2311.09735)이 만 건의 쿼리를 분석했는데, 결과가 꽤 뚜렷하다:

- 출처를 명시한 콘텐츠: AI 가시성 **+40%**
- 통계를 포함한 콘텐츠: **+30%**
- 키워드를 반복 삽입한 콘텐츠: 오히려 **-10%**

SEO에서 통하던 키워드 반복이 GEO에서는 오히려 깎인다. AI는 같은 단어가 몇 번 나왔는지가 아니라, 정보가 얼마나 체계적이고 믿을 만한지를 본다.

구조화 데이터 쪽 실증도 쌓이고 있다. [Seer Interactive 분석](https://www.seerinteractive.com/insights/how-ai-overviews-are-impacting-ctr-5-initial-takeaways)을 보면 AI Overview에 인용된 브랜드는 자연 검색 클릭률이 35% 높고, 유료 광고 클릭률은 거의 두 배까지 올랐다. [GrackerAI](https://gracker.ai/static/GEO%202026%20Data%20Sheet.Disb-CIl.pdf)에서도 구조화 데이터를 넣으면 AI Overview에 뜰 확률이 **36%** 올라간다고 나온다. [Search Engine Land](https://searchengineland.com/schema-ai-overviews-structured-data-visibility-462353)에서는 완전한 Schema를 적용한 사이트가 ChatGPT에 노출될 확률이 **80%** 라고 보도했다. 기본 Schema만 있으면 20%.

콘텐츠 최신성도 빼놓을 수 없다. Perplexity에서 높은 인용을 받은 페이지 4분의 3 이상이 한 달 이내에 업데이트된 것이었다. 석 달 넘게 손 안 댄 페이지는 밀린다.

## On-Site GEO와 Off-Site GEO

GEO는 크게 두 영역으로 나뉜다.

| 구분 | On-Site GEO | Off-Site GEO |
|------|------------|-------------|
| 정의 | 자사 사이트를 AI가 읽고 답변에 사용하게 만들기 | AI가 참고하는 외부 사이트에 브랜드 노출 |
| 핵심 기술 | JSON-LD, Schema.org, SSR, robots.txt, FAQ | Reddit, Wikipedia, 뉴스, 커뮤니티 |
| 담당 | 개발팀 / 기술 조직 | 마케팅 / PR / 브랜드 전략 |

이 시리즈에서는 **On-Site GEO** 에 집중한다. 개발자가 코드로 바로 적용할 수 있는 영역이다.

## 다음 편 예고

다음 편에서는 GEO 시스템의 실제 구조를 다룬다. 상품 데이터가 어떻게 흘러서 AI가 읽을 수 있는 형태가 되는지.
