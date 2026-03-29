"""
URL 타입 판별 모듈.
youtube / webpage / txt 세 가지로 분류한다.
"""

import re
from urllib.parse import urlparse

YOUTUBE_PATTERNS = [
    re.compile(r'youtube\.com/watch'),
    re.compile(r'youtube\.com/shorts'),
    re.compile(r'youtu\.be/'),
    re.compile(r'youtube\.com/live'),
]


def classify_url(url: str) -> str:
    """
    URL을 youtube / txt / webpage 중 하나로 분류한다.

    Args:
        url: 분류할 URL

    Returns:
        "youtube" | "txt" | "webpage"
    """
    for pattern in YOUTUBE_PATTERNS:
        if pattern.search(url):
            return "youtube"

    parsed = urlparse(url)
    path = parsed.path.lower()
    if path.endswith('.txt') or path.endswith('.md'):
        return "txt"

    return "webpage"
