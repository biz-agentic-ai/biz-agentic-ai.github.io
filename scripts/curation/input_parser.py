"""
입력 셀 파싱 모듈.
URL 추출 + 나머지 텍스트를 코멘트로 분리한다.
"""

import re
from typing import TypedDict

URL_PATTERN = re.compile(
    r'https?://[^\s\]\)>"\u3000-\u303f\uff00-\uffef]+'
)


class ParsedInput(TypedDict):
    input_type: str  # "urls_only" | "mixed" | "text_only"
    urls: list[str]
    comment: str


def parse_input(raw: str) -> ParsedInput:
    """
    셀 원문(raw)을 파싱해서 URL 리스트와 코멘트를 반환한다.

    Args:
        raw: Google Sheets A열 원문

    Returns:
        ParsedInput dict
    """
    raw = raw.strip()
    urls = URL_PATTERN.findall(raw)
    # URL을 원문에서 제거한 뒤 남은 텍스트를 코멘트로
    comment = URL_PATTERN.sub('', raw).strip()
    # 연속 공백/줄바꿈 정리
    comment = re.sub(r'\s+', ' ', comment).strip()

    if urls and not comment:
        input_type = "urls_only"
    elif urls and comment:
        input_type = "mixed"
    else:
        input_type = "text_only"

    return ParsedInput(input_type=input_type, urls=urls, comment=comment)
