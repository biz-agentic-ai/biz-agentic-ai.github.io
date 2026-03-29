"""
YouTube 처리 모듈.
yt-dlp로 메타데이터·자막을 추출하고,
ffmpeg로 썸네일을 캡처해서 static/images/curations/ 에 저장한다.
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path

import yt_dlp

# 프로젝트 루트 기준 경로
PROJECT_ROOT = Path(__file__).resolve().parents[2]
IMAGES_DIR = PROJECT_ROOT / 'static' / 'images' / 'curations'
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

MAX_THUMBNAILS = 5


def process(url: str) -> dict:
    """
    YouTube URL에서 메타데이터, 자막, 썸네일을 추출한다.

    Returns:
        {
            "title": str,
            "description": str,
            "channel": str,
            "duration": int,          # 초
            "subtitles": str,         # 자막 전문 (없으면 "")
            "thumbnail_paths": list[str],  # Hugo 기준 경로
            "url": str,
        }
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        meta = _extract_metadata(url, tmpdir)
        subtitles = _extract_subtitles(url, tmpdir)
        thumbnail_paths = _capture_thumbnails(url, meta, tmpdir)

    return {
        'title': meta.get('title', ''),
        'description': (meta.get('description') or '')[:2000],
        'channel': meta.get('uploader', ''),
        'duration': meta.get('duration', 0),
        'subtitles': subtitles,
        'thumbnail_paths': thumbnail_paths,
        'url': url,
    }


def _extract_metadata(url: str, tmpdir: str) -> dict:
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'outtmpl': os.path.join(tmpdir, '%(id)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info or {}


def _extract_subtitles(url: str, tmpdir: str) -> str:
    """자동 생성 자막 우선, 없으면 업로더 자막을 시도한다."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['ko', 'en'],
        'subtitlesformat': 'vtt',
        'outtmpl': os.path.join(tmpdir, 'sub'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # 다운로드된 .vtt 파일 찾기
    for lang in ['ko', 'en']:
        for suffix in [f'.{lang}.vtt', f'.{lang}-orig.vtt']:
            vtt_path = Path(tmpdir) / f'sub{suffix}'
            if vtt_path.exists():
                return _vtt_to_text(vtt_path.read_text(encoding='utf-8'))

    return ''


def _vtt_to_text(vtt: str) -> str:
    """VTT 형식에서 순수 텍스트만 추출한다."""
    lines = vtt.splitlines()
    text_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('WEBVTT') or '-->' in line:
            continue
        if re.match(r'^\d+$', line):
            continue
        # HTML 태그 제거
        clean = re.sub(r'<[^>]+>', '', line)
        if clean:
            text_lines.append(clean)

    # 중복 제거 (연속 중복 자막)
    deduped = []
    prev = ''
    for line in text_lines:
        if line != prev:
            deduped.append(line)
            prev = line

    return ' '.join(deduped)[:6000]


def _capture_thumbnails(url: str, meta: dict, tmpdir: str) -> list[str]:
    """
    ffmpeg로 영상에서 썸네일을 캡처한다.
    챕터가 있으면 챕터 기반, 없으면 균등 분할로 최대 5장.
    캡처된 이미지를 static/images/curations/ 에 복사하고 Hugo 경로를 반환한다.
    """
    video_id = meta.get('id', 'video')
    duration = meta.get('duration', 0)

    if not duration or duration < 10:
        return []

    # 캡처 시점 결정
    chapters = meta.get('chapters') or []
    if chapters:
        timestamps = [c['start_time'] + 5 for c in chapters[:MAX_THUMBNAILS]]
    else:
        count = min(MAX_THUMBNAILS, max(1, duration // 120))
        step = duration / (count + 1)
        timestamps = [step * (i + 1) for i in range(count)]

    # 비디오 다운로드 (최저 화질)
    video_path = os.path.join(tmpdir, f'{video_id}.mp4')
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'worst[ext=mp4]/worst',
        'outtmpl': video_path,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception:
        return []

    if not os.path.exists(video_path):
        return []

    hugo_paths = []
    for idx, ts in enumerate(timestamps):
        filename = f'{video_id}_{idx + 1:02d}.jpg'
        dest_path = IMAGES_DIR / filename
        cmd = [
            'ffmpeg', '-y', '-ss', str(int(ts)),
            '-i', video_path,
            '-frames:v', '1',
            '-q:v', '2',
            str(dest_path),
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        if result.returncode == 0 and dest_path.exists():
            hugo_paths.append(f'/images/curations/{filename}')

    return hugo_paths
