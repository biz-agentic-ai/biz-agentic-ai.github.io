"""
큐레이션 자동 발행 파이프라인 엔트리포인트.

흐름:
  Sheets 미처리 행 읽기
  → input_parser (URL + 코멘트 분리)
  → url_classifier (youtube/webpage/txt)
  → 수집 (youtube_processor / web_scraper)
  → ai_summarizer (Gemini 2.5 Flash)
  → hugo_generator (마크다운 파일 생성)
  → Sheets 상태 업데이트
"""

import logging
import sys

from input_parser import parse_input
from sheets_client import get_pending_rows, mark_done, mark_error
from url_classifier import classify_url
from web_scraper import scrape, scrape_txt
from youtube_processor import process as process_youtube
from ai_summarizer import summarize
from hugo_generator import generate

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
log = logging.getLogger(__name__)


def _collect_source(url: str) -> dict:
    """URL 타입에 따라 소스 데이터를 수집하고 url_type 필드를 추가한다."""
    url_type = classify_url(url)
    log.info('  수집: %s (%s)', url, url_type)

    if url_type == 'youtube':
        data = process_youtube(url)
    elif url_type == 'txt':
        data = scrape_txt(url)
    else:
        data = scrape(url)

    data['url_type'] = url_type
    return data


def _process_row(row: dict) -> str:
    """
    단일 행을 처리하고 생성된 파일 경로를 반환한다.
    실패 시 예외를 raise한다.
    """
    raw = row['raw']
    log.info('처리 시작: %s', raw[:80])

    parsed = parse_input(raw)
    log.info('  입력 타입: %s, URL %d개', parsed['input_type'], len(parsed['urls']))

    sources: list[dict] = []
    thumbnail_paths: list[str] = []

    if parsed['input_type'] != 'text_only':
        for url in parsed['urls']:
            source = _collect_source(url)
            sources.append(source)
            if source.get('url_type') == 'youtube':
                thumbnail_paths.extend(source.get('thumbnail_paths', []))

    log.info('  AI 요약 시작')
    ai_result = summarize(parsed, sources)

    log.info('  Hugo 파일 생성 중')
    output_path = generate(ai_result, parsed, sources, thumbnail_paths)

    log.info('  완료: %s', output_path)
    return output_path


def run() -> int:
    """파이프라인 실행. 처리된 행 수를 반환한다."""
    log.info('=== 큐레이션 파이프라인 시작 ===')

    pending = get_pending_rows()
    log.info('미처리 행: %d개', len(pending))

    if not pending:
        log.info('처리할 항목 없음. 종료.')
        return 0

    success_count = 0
    for row in pending:
        row_index = row['row_index']
        try:
            _process_row(row)
            mark_done(row_index)
            success_count += 1
        except Exception as e:
            reason = str(e)[:200]
            log.error('행 %d 처리 실패: %s', row_index, reason)
            try:
                mark_error(row_index, reason)
            except Exception as mark_err:
                log.error('Sheets 오류 기록 실패: %s', mark_err)

    log.info('=== 완료: %d/%d 성공 ===', success_count, len(pending))
    return success_count


if __name__ == '__main__':
    processed = run()
    # 처리된 항목이 없으면 exit code 0 유지 (변경사항 없음을 CI에 알림)
    sys.exit(0)
