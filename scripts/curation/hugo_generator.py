"""
Hugo 마크다운 생성 모듈.
Jinja2 템플릿으로 content/curations/YYYY-MM-DD-{slug}.md 파일을 생성한다.
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from slugify import slugify

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = PROJECT_ROOT / 'templates'
OUTPUT_DIR = PROJECT_ROOT / 'content' / 'curations'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _make_slug(title: str, date_str: str) -> str:
    """제목으로 Hugo 파일명용 slug를 생성한다."""
    slug = slugify(title, allow_unicode=False, max_length=50)
    if not slug:
        slug = 'curation'
    return f'{date_str}-{slug}'


def generate(
    ai_result: dict,
    parsed_input: dict,
    sources: list[dict],
    thumbnail_paths: list[str] | None = None,
) -> str:
    """
    Hugo 마크다운 파일을 생성하고 파일 경로를 반환한다.

    Args:
        ai_result: ai_summarizer.summarize() 결과 (title, summary, body, insights, tags)
        parsed_input: input_parser.parse_input() 결과
        sources: 수집된 소스 데이터 리스트
        thumbnail_paths: YouTube 썸네일 Hugo 경로 리스트

    Returns:
        생성된 파일의 절대 경로
    """
    now = datetime.now(timezone.utc)
    date_str = now.strftime('%Y-%m-%d')
    datetime_str = now.strftime('%Y-%m-%dT%H:%M:%S+00:00')

    title = ai_result.get('title', '큐레이션')
    slug = _make_slug(title, date_str)
    filename = f'{slug}.md'
    output_path = OUTPUT_DIR / filename

    # source_url 리스트 구성
    source_urls = [s.get('url', '') for s in sources if s.get('url')]
    if not source_urls and parsed_input['input_type'] == 'text_only':
        source_urls = []

    # source_type 판별
    url_types = list({s.get('url_type', 'webpage') for s in sources})
    source_type = url_types[0] if len(url_types) == 1 else 'mixed'

    # 이미지 경로: YouTube 썸네일 우선, 없으면 og_image
    images = thumbnail_paths or []
    if not images:
        for s in sources:
            og = s.get('og_image', '')
            if og:
                images.append(og)
                break

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template('curation_post.md.j2')

    content = template.render(
        title=title,
        date=datetime_str,
        summary=ai_result.get('summary', ''),
        tags=ai_result.get('tags', []),
        source_urls=source_urls,
        source_type=source_type,
        input_type=parsed_input['input_type'],
        body=ai_result.get('body', ''),
        insights=ai_result.get('insights', []),
        images=images,
        comment=parsed_input.get('comment', ''),
        cover_image=images[0] if images else '',
    )

    output_path.write_text(content, encoding='utf-8')
    return str(output_path)
