#!/usr/bin/env python3
"""
Notification System
파이프라인 실행 결과를 다양한 채널로 알림을 보내는 스크립트
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NotificationSender:
    """알림 발송기"""
    
    def __init__(self):
        self.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        self.discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        self.email_config = self._get_email_config()
        
    def _get_email_config(self) -> Dict[str, str]:
        """이메일 설정 가져오기"""
        return {
            'smtp_server': os.getenv('SMTP_SERVER'),
            'smtp_port': os.getenv('SMTP_PORT', '587'),
            'smtp_username': os.getenv('SMTP_USERNAME'),
            'smtp_password': os.getenv('SMTP_PASSWORD'),
            'from_email': os.getenv('FROM_EMAIL'),
            'to_email': os.getenv('TO_EMAIL')
        }
    
    def send_slack_notification(self, message: str, status: str = 'info') -> bool:
        """Slack 알림 발송"""
        if not self.slack_webhook_url:
            logger.warning("Slack webhook URL not configured")
            return False
        
        try:
            # 상태에 따른 색상 설정
            color_map = {
                'success': '#36a64f',  # 초록색
                'failure': '#ff0000',  # 빨간색
                'warning': '#ffa500',  # 주황색
                'info': '#0000ff'      # 파란색
            }
            
            payload = {
                "attachments": [
                    {
                        "color": color_map.get(status, '#0000ff'),
                        "title": f"Biz Agentic AI Pipeline - {status.upper()}",
                        "text": message,
                        "footer": "Biz Agentic AI Automation System",
                        "ts": int(datetime.now().timestamp())
                    }
                ]
            }
            
            response = requests.post(
                self.slack_webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Slack notification sent successfully")
                return True
            else:
                logger.error(f"Failed to send Slack notification: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")
            return False
    
    def send_discord_notification(self, message: str, status: str = 'info') -> bool:
        """Discord 알림 발송"""
        if not self.discord_webhook_url:
            logger.warning("Discord webhook URL not configured")
            return False
        
        try:
            # 상태에 따른 색상 설정 (Discord는 10진수 색상 코드 사용)
            color_map = {
                'success': 0x36a64f,  # 초록색
                'failure': 0xff0000,  # 빨간색
                'warning': 0xffa500,  # 주황색
                'info': 0x0000ff      # 파란색
            }
            
            payload = {
                "embeds": [
                    {
                        "color": color_map.get(status, 0x0000ff),
                        "title": f"Biz Agentic AI Pipeline - {status.upper()}",
                        "description": message,
                        "footer": {
                            "text": "Biz Agentic AI Automation System"
                        },
                        "timestamp": datetime.now().isoformat()
                    }
                ]
            }
            
            response = requests.post(
                self.discord_webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 204:  # Discord는 성공 시 204 반환
                logger.info("Discord notification sent successfully")
                return True
            else:
                logger.error(f"Failed to send Discord notification: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Discord notification: {e}")
            return False
    
    def send_email_notification(self, subject: str, message: str) -> bool:
        """이메일 알림 발송"""
        if not all(self.email_config.values()):
            logger.warning("Email configuration incomplete")
            return False
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # 이메일 메시지 생성
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from_email']
            msg['To'] = self.email_config['to_email']
            msg['Subject'] = subject
            
            # HTML 형식의 메시지 본문
            html_message = f"""
            <html>
            <body>
                <h2>Biz Agentic AI Pipeline Notification</h2>
                <p>{message}</p>
                <hr>
                <p><small>Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_message, 'html'))
            
            # SMTP 서버 연결 및 발송
            server = smtplib.SMTP(
                self.email_config['smtp_server'],
                int(self.email_config['smtp_port'])
            )
            server.starttls()
            server.login(
                self.email_config['smtp_username'],
                self.email_config['smtp_password']
            )
            
            text = msg.as_string()
            server.sendmail(
                self.email_config['from_email'],
                self.email_config['to_email'],
                text
            )
            server.quit()
            
            logger.info("Email notification sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
            return False
    
    def generate_pipeline_message(self, status: str, job_results: Optional[Dict[str, str]] = None) -> str:
        """파이프라인 메시지 생성"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if status == 'success':
            message = f"✅ **파이프라인 실행 성공**\n\n"
            message += f"📅 실행 시간: {timestamp}\n"
            message += f"🎯 상태: 모든 단계가 성공적으로 완료되었습니다.\n"
            message += f"🌐 사이트: https://biz-agentic-ai.github.io\n\n"
            
            if job_results:
                message += "**작업 결과:**\n"
                for job, result in job_results.items():
                    emoji = "✅" if result == "success" else "❌"
                    message += f"{emoji} {job}: {result}\n"
                    
        elif status == 'failure':
            message = f"❌ **파이프라인 실행 실패**\n\n"
            message += f"📅 실행 시간: {timestamp}\n"
            message += f"🚨 상태: 하나 이상의 단계에서 오류가 발생했습니다.\n\n"
            
            if job_results:
                message += "**실패한 작업:**\n"
                for job, result in job_results.items():
                    if result == "failure":
                        message += f"❌ {job}: 실패\n"
                        
            message += "\n🔧 **권장 조치:**\n"
            message += "1. GitHub Actions 로그를 확인하세요\n"
            message += "2. 에러 메시지를 분석하세요\n"
            message += "3. 필요한 경우 수동으로 재실행하세요\n"
            
        else:
            message = f"ℹ️ **파이프라인 상태 알림**\n\n"
            message += f"📅 시간: {timestamp}\n"
            message += f"📊 상태: {status}\n"
            
        return message
    
    def send_notification(self, status: str, job_results: Optional[Dict[str, str]] = None, 
                         channels: List[str] = None) -> Dict[str, bool]:
        """알림 발송 (모든 채널)"""
        if channels is None:
            channels = ['slack', 'discord']  # 기본 채널
        
        message = self.generate_pipeline_message(status, job_results)
        results = {}
        
        # 각 채널로 알림 발송
        for channel in channels:
            if channel == 'slack':
                results['slack'] = self.send_slack_notification(message, status)
            elif channel == 'discord':
                results['discord'] = self.send_discord_notification(message, status)
            elif channel == 'email':
                subject = f"Biz Agentic AI Pipeline - {status.upper()}"
                results['email'] = self.send_email_notification(subject, message)
            else:
                logger.warning(f"Unknown notification channel: {channel}")
                results[channel] = False
        
        return results

def parse_job_results(job_results_str: str) -> Dict[str, str]:
    """작업 결과 문자열을 파싱"""
    if not job_results_str:
        return {}
    
    results = {}
    try:
        # JSON 형식으로 파싱 시도
        results = json.loads(job_results_str)
    except json.JSONDecodeError:
        # 단순 키=값 형식으로 파싱
        for item in job_results_str.split(','):
            if '=' in item:
                key, value = item.split('=', 1)
                results[key.strip()] = value.strip()
    
    return results

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description='Send pipeline notifications')
    parser.add_argument('--status', required=True, 
                       choices=['success', 'failure', 'warning', 'info'],
                       help='Pipeline status')
    parser.add_argument('--job-results', type=str, default='',
                       help='Job results in JSON format or key=value pairs')
    parser.add_argument('--channels', nargs='+', 
                       choices=['slack', 'discord', 'email'],
                       default=['slack', 'discord'],
                       help='Notification channels')
    
    args = parser.parse_args()
    
    logger.info(f"Starting notification for status: {args.status}")
    
    # 알림 발송기 초기화
    sender = NotificationSender()
    
    # 작업 결과 파싱
    job_results = parse_job_results(args.job_results)
    
    # 알림 발송
    results = sender.send_notification(
        status=args.status,
        job_results=job_results,
        channels=args.channels
    )
    
    # 결과 출력
    logger.info("Notification results:")
    for channel, success in results.items():
        status = "✅ Success" if success else "❌ Failed"
        logger.info(f"  {channel}: {status}")
    
    # 실패한 채널이 있으면 종료 코드 1 반환
    if not all(results.values()):
        sys.exit(1)

if __name__ == "__main__":
    main()
