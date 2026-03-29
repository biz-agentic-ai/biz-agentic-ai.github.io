"""
웹페이지 본문 추출 모듈.
requests + BeautifulSoup + readability로 본문과 메타 태그를 수집한다.
"""

import requests
from bs4 import BeautifulSoup
from readability import Document

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}
TIMEOUT = 15


def scrape(url: str) -> dict:
    """
    URL에서 본문과 메타 정보를 추출한다.

    Args:
        url: 스크랩할 웹페이지 URL

    Returns:
        {
            "title": str,
            "description": str,
            "og_image": str,
            "body_text": str,
            "url": str,
        }
    """
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    html = resp.text

    # readability로 본문 추출
    doc = Document(html)
    readable_html = doc.summary()
    readable_soup = BeautifulSoup(readable_html, 'lxml')
    body_text = readable_soup.get_text(separator='\n', strip=True)

    # 메타 태그 추출
    soup = BeautifulSoup(html, 'lxml')
    title = _meta(soup, 'og:title') or _meta(soup, 'title') or doc.title() or ''
    description = _meta(soup, 'og:description') or _meta(soup, 'description') or ''
    og_image = _meta(soup, 'og:image') or ''

    return {
        'title': title.strip(),
        'description': description.strip(),
        'og_image': og_image.strip(),
        'body_text': body_text[:8000],  # Gemini 컨텍스트 절약
        'url': url,
    }


def scrape_txt(url: str) -> dict:
    """
    텍스트 파일 URL에서 내용을 직접 가져온다.
    """
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    text = resp.text

    return {
        'title': url.split('/')[-1],
        'description': '',
        'og_image': '',
        'body_text': text[:8000],
        'url': url,
    }


def _meta(soup: BeautifulSoup, name: str) -> str:
    """og: 속성 또는 name 속성으로 메타 태그 값을 가져온다."""
    tag = soup.find('meta', property=name)
    if tag and tag.get('content'):
        return tag['content']
    tag = soup.find('meta', attrs={'name': name})
    if tag and tag.get('content'):
        return tag['content']
    if name == 'title':
        t = soup.find('title')
        if t:
            return t.get_text()
    return ''
