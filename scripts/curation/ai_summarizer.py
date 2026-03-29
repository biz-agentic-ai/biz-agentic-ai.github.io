"""
Gemini 2.5 Flash 기반 AI 요약 모듈.
입력 타입별로 프롬프트를 분기하고, junho-humanizer 문체 규칙을 내장한다.

환경변수:
    GEMINI_API_KEY: Google Gemini API 키
"""

import json
import os
import re
import textwrap

import google.generativeai as genai

MODEL_NAME = 'gemini-2.5-flash'

# junho-humanizer 핵심 규칙을 Gemini 프롬프트에 내장
STYLE_RULES = textwrap.dedent("""
## 이준호 스타일 글쓰기 규칙 (반드시 준수)

### 어조
- 서술형 종결(~다/~했다/~이다). 존댓말 아님.
- 친근하면서 전문적인 톤. 동료 엔지니어에게 설명하듯 작성.
- 가벼운 자조적 유머 허용 (과하지 않게).

### 어휘
- 기술 용어(NL2SQL, GraphRAG, DDL, API 등)는 영어 그대로 사용.
- 구어체 연결 허용: "~인데", "~하는데", "파보니".

### 절대 금지 표현
- "결론적으로", "요약하자면", "핵심은", "즉"
- "게임 체인저", "혁신적", "놀랍게도", "드디어", "사실"
- "~는 여기서 출발했다", "방어선은 N가지다", "이를 위해", "이에 따라"
- 느낌표(!) 와 이모지 사용 금지.
- em dash(—) 금지. 하이픈(-)을 사용한다.

### 절대 금지 구조
- 번호 나열: "첫째, 둘째, 셋째…"
- "~에 대해 알아보겠습니다" 식 서론.
- "결론적으로~"로 시작하는 마무리 단락.

### 문장 리듬
- 5~15자 짧은 문장과 40~60자 긴 문장을 불규칙하게 섞어 쓰기.
- 접속사("또한", "그러나", "따라서") 없이 맥락으로 이어가기.

### 내용 밀도
- 추상 설명 대신 구체적 예시/숫자 사용.
- 동일 단어 3회 이상 반복 금지.
- 경력 연수 직접 언급 금지.
- 구체적 회사명 대신 업종으로 표현. ("롯데" → "유통사")

### 구조
- 도입은 개념 정의 대신 구체적 상황/문제로 시작.
- 결론은 짧게. 다음 주제 예고 한 줄이면 충분.
""").strip()


def _configure():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise EnvironmentError('GEMINI_API_KEY 환경변수가 설정되지 않았습니다.')
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)


def _call(model, prompt: str) -> dict:
    """Gemini를 호출하고 JSON 결과를 파싱한다."""
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type='application/json',
            temperature=0.7,
        ),
    )
    text = response.text.strip()
    # 코드 블록 제거
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return json.loads(text)


def _output_schema() -> str:
    return textwrap.dedent("""
    출력은 반드시 다음 JSON 형식이어야 한다:
    {
      "title": "포스트 제목 (한국어, 60자 이내)",
      "summary": "한 줄 요약 (한국어, 150자 이내)",
      "body": "본문 마크다운 (이준호 스타일, 한국어 1500~3000자)",
      "insights": ["핵심 인사이트 1", "핵심 인사이트 2", "핵심 인사이트 3"],
      "tags": ["태그1", "태그2", "태그3", "태그4", "태그5"]
    }
    """).strip()


# ── 입력 타입별 프롬프트 ──────────────────────────────────────────────────────

def summarize_single_url(source: dict) -> dict:
    """urls_only 1개: 단일 소스 요약."""
    model = _configure()
    prompt = f"""
{STYLE_RULES}

---

아래 웹 콘텐츠를 읽고 블로그 큐레이션 포스트를 작성하라.
독자는 데이터 엔지니어, AI 개발자, 기술 기획자다.

## 소스 정보
- URL: {source.get('url', '')}
- 제목: {source.get('title', '')}
- 설명: {source.get('description', '')}

## 본문/자막 내용
{source.get('body_text') or source.get('subtitles', '')}

---

{_output_schema()}
"""
    return _call(model, prompt)


def summarize_multiple_urls(sources: list[dict]) -> dict:
    """urls_only N개: 묶음 비교·요약."""
    model = _configure()
    sources_text = ''
    for i, s in enumerate(sources, 1):
        sources_text += f"""
### 소스 {i}
- URL: {s.get('url', '')}
- 제목: {s.get('title', '')}
- 설명: {s.get('description', '')}
- 내용: {(s.get('body_text') or s.get('subtitles', ''))[:2000]}
"""

    prompt = f"""
{STYLE_RULES}

---

아래 여러 소스를 비교·분석해서 하나의 블로그 큐레이션 포스트를 작성하라.
각 소스의 공통점, 차이점, 시사점을 중심으로 구성한다.
독자는 데이터 엔지니어, AI 개발자, 기술 기획자다.

{sources_text}

---

{_output_schema()}
"""
    return _call(model, prompt)


def summarize_mixed(sources: list[dict], comment: str) -> dict:
    """mixed: URL 요약 + 작성자 코멘트 반영."""
    model = _configure()
    sources_text = ''
    for i, s in enumerate(sources, 1):
        sources_text += f"""
### 소스 {i}
- URL: {s.get('url', '')}
- 제목: {s.get('title', '')}
- 내용: {(s.get('body_text') or s.get('subtitles', ''))[:2000]}
"""

    prompt = f"""
{STYLE_RULES}

---

아래 소스와 작성자 코멘트를 바탕으로 블로그 큐레이션 포스트를 작성하라.
작성자 코멘트의 관점과 의견을 본문에 자연스럽게 녹여낸다.
독자는 데이터 엔지니어, AI 개발자, 기술 기획자다.

## 작성자 코멘트
{comment}

## 소스
{sources_text}

---

{_output_schema()}
"""
    return _call(model, prompt)


def summarize_text_only(text: str) -> dict:
    """text_only: 텍스트 자체를 구조화."""
    model = _configure()
    prompt = f"""
{STYLE_RULES}

---

아래 텍스트를 블로그 포스트 형태로 구조화하라.
URL 없이 텍스트만 입력된 경우이므로, 텍스트의 내용과 의도를 살려서
독자가 읽기 좋은 형태로 재구성한다.
독자는 데이터 엔지니어, AI 개발자, 기술 기획자다.

## 입력 텍스트
{text}

---

{_output_schema()}
"""
    return _call(model, prompt)


# ── 디스패처 ──────────────────────────────────────────────────────────────────

def summarize(parsed_input: dict, sources: list[dict]) -> dict:
    """
    입력 타입에 따라 적절한 요약 함수를 호출한다.

    Args:
        parsed_input: input_parser.parse_input() 결과
        sources: 수집된 소스 데이터 리스트 (url_type, 본문 등 포함)

    Returns:
        {"title", "summary", "body", "insights", "tags"}
    """
    input_type = parsed_input['input_type']
    comment = parsed_input.get('comment', '')

    if input_type == 'text_only':
        return summarize_text_only(comment)
    elif input_type == 'urls_only':
        if len(sources) == 1:
            return summarize_single_url(sources[0])
        else:
            return summarize_multiple_urls(sources)
    else:  # mixed
        return summarize_mixed(sources, comment)
