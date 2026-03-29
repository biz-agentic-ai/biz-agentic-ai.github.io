"""
Google Sheets API 클라이언트.
미처리 행 읽기 + 처리 완료 상태 기록을 담당한다.

환경변수:
    GOOGLE_SHEETS_CREDENTIALS: 서비스 계정 JSON 문자열
    GOOGLE_SHEET_ID: 스프레드시트 ID
"""

import json
import os
from datetime import datetime, timezone
from typing import Optional

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# 데이터가 있는 시트 이름 (기본: Sheet1)
SHEET_NAME = os.environ.get('GOOGLE_SHEET_NAME', 'Sheet1')


def _get_service():
    creds_json = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
    if not creds_json:
        raise EnvironmentError('GOOGLE_SHEETS_CREDENTIALS 환경변수가 설정되지 않았습니다.')

    creds_info = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    return build('sheets', 'v4', credentials=creds)


def _sheet_id() -> str:
    sheet_id = os.environ.get('GOOGLE_SHEET_ID')
    if not sheet_id:
        raise EnvironmentError('GOOGLE_SHEET_ID 환경변수가 설정되지 않았습니다.')
    return sheet_id


def get_pending_rows() -> list[dict]:
    """
    B열이 비어 있는 행을 모두 읽어 반환한다.

    Returns:
        [{"row_index": int, "raw": str}, ...]
        row_index는 1-based (Sheets API 기준)
    """
    service = _get_service()
    sheet_id = _sheet_id()

    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=f'{SHEET_NAME}!A:C')
        .execute()
    )

    rows = result.get('values', [])
    pending = []

    for i, row in enumerate(rows):
        row_number = i + 1  # 1-based
        if not row:
            continue

        a_val = row[0].strip() if len(row) > 0 else ''
        b_val = row[1].strip() if len(row) > 1 else ''

        if not a_val:
            continue
        if b_val:  # 이미 처리됨
            continue

        pending.append({'row_index': row_number, 'raw': a_val})

    return pending


def mark_done(row_index: int, published_date: Optional[str] = None) -> None:
    """
    처리 완료 행의 B열에 "done", C열에 발행일을 기록한다.

    Args:
        row_index: 1-based 행 번호
        published_date: ISO 날짜 문자열 (없으면 오늘)
    """
    service = _get_service()
    sheet_id = _sheet_id()

    if published_date is None:
        published_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    body = {'values': [['done', published_date]]}
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=f'{SHEET_NAME}!B{row_index}:C{row_index}',
        valueInputOption='RAW',
        body=body,
    ).execute()


def mark_error(row_index: int, reason: str) -> None:
    """
    처리 실패 행의 B열에 "error: {reason}"을 기록한다.

    Args:
        row_index: 1-based 행 번호
        reason: 오류 사유 (간결하게)
    """
    service = _get_service()
    sheet_id = _sheet_id()

    error_msg = f'error: {reason[:200]}'
    body = {'values': [[error_msg]]}
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=f'{SHEET_NAME}!B{row_index}',
        valueInputOption='RAW',
        body=body,
    ).execute()
