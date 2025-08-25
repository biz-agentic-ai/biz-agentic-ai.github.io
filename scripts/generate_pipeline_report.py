#!/usr/bin/env python3
"""
Pipeline Report Generator
자동화 파이프라인의 실행 결과를 분석하고 리포트를 생성하는 스크립트
"""

import os
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PipelineReporter:
    """파이프라인 리포트 생성기"""
    
    def __init__(self, data_dir: str = "data", reports_dir: str = "reports"):
        self.data_dir = Path(data_dir)
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
    def collect_pipeline_metrics(self) -> Dict[str, Any]:
        """파이프라인 메트릭 수집"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'data_collection': {},
            'ai_processing': {},
            'post_generation': {},
            'deployment': {},
            'overall': {}
        }
        
        # 데이터 수집 메트릭
        metrics['data_collection'] = self._collect_data_collection_metrics()
        
        # AI 처리 메트릭
        metrics['ai_processing'] = self._collect_ai_processing_metrics()
        
        # 포스트 생성 메트릭
        metrics['post_generation'] = self._collect_post_generation_metrics()
        
        # 배포 메트릭
        metrics['deployment'] = self._collect_deployment_metrics()
        
        # 전체 메트릭
        metrics['overall'] = self._calculate_overall_metrics(metrics)
        
        return metrics
    
    def _collect_data_collection_metrics(self) -> Dict[str, Any]:
        """데이터 수집 메트릭 수집"""
        metrics = {
            'new_items_count': 0,
            'total_items_count': 0,
            'success_rate': 0.0,
            'error_count': 0,
            'last_collection_time': None
        }
        
        try:
            # 데이터 수집 로그 파일 확인
            log_file = self.data_dir / "collection_log.json"
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                    
                if isinstance(log_data, list) and log_data:
                    latest_log = log_data[-1]
                    metrics['new_items_count'] = latest_log.get('new_items', 0)
                    metrics['total_items_count'] = latest_log.get('total_items', 0)
                    metrics['success_rate'] = latest_log.get('success_rate', 0.0)
                    metrics['error_count'] = latest_log.get('errors', 0)
                    metrics['last_collection_time'] = latest_log.get('timestamp')
                    
        except Exception as e:
            logger.error(f"Error collecting data collection metrics: {e}")
            
        return metrics
    
    def _collect_ai_processing_metrics(self) -> Dict[str, Any]:
        """AI 처리 메트릭 수집"""
        metrics = {
            'processed_items_count': 0,
            'success_rate': 0.0,
            'average_processing_time': 0.0,
            'error_count': 0,
            'last_processing_time': None
        }
        
        try:
            # AI 처리 로그 파일 확인
            log_file = Path("ai-engine/logs/processing_log.json")
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                    
                if isinstance(log_data, list) and log_data:
                    latest_log = log_data[-1]
                    metrics['processed_items_count'] = latest_log.get('processed_items', 0)
                    metrics['success_rate'] = latest_log.get('success_rate', 0.0)
                    metrics['average_processing_time'] = latest_log.get('avg_processing_time', 0.0)
                    metrics['error_count'] = latest_log.get('errors', 0)
                    metrics['last_processing_time'] = latest_log.get('timestamp')
                    
        except Exception as e:
            logger.error(f"Error collecting AI processing metrics: {e}")
            
        return metrics
    
    def _collect_post_generation_metrics(self) -> Dict[str, Any]:
        """포스트 생성 메트릭 수집"""
        metrics = {
            'generated_posts_count': 0,
            'quality_score': 0.0,
            'success_rate': 0.0,
            'error_count': 0,
            'last_generation_time': None
        }
        
        try:
            # 포스트 디렉토리 확인
            posts_dir = Path("content/posts")
            if posts_dir.exists():
                # 최근 24시간 내 생성된 포스트 수
                cutoff_time = datetime.now() - timedelta(hours=24)
                recent_posts = 0
                total_posts = 0
                
                for post_file in posts_dir.glob("*.md"):
                    total_posts += 1
                    file_time = datetime.fromtimestamp(post_file.stat().st_mtime)
                    if file_time > cutoff_time:
                        recent_posts += 1
                
                metrics['generated_posts_count'] = recent_posts
                metrics['total_posts_count'] = total_posts
                
        except Exception as e:
            logger.error(f"Error collecting post generation metrics: {e}")
            
        return metrics
    
    def _collect_deployment_metrics(self) -> Dict[str, Any]:
        """배포 메트릭 수집"""
        metrics = {
            'deployment_success': False,
            'deployment_time': None,
            'build_time': 0.0,
            'site_url': None
        }
        
        try:
            # GitHub Actions 로그에서 배포 정보 확인
            # 실제 구현에서는 GitHub API를 사용하여 더 정확한 정보를 가져올 수 있음
            metrics['site_url'] = "https://biz-agentic-ai.github.io"
            
        except Exception as e:
            logger.error(f"Error collecting deployment metrics: {e}")
            
        return metrics
    
    def _calculate_overall_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """전체 메트릭 계산"""
        overall = {
            'total_execution_time': 0.0,
            'overall_success_rate': 0.0,
            'total_errors': 0,
            'pipeline_health': 'unknown'
        }
        
        # 전체 에러 수 계산
        total_errors = (
            metrics['data_collection'].get('error_count', 0) +
            metrics['ai_processing'].get('error_count', 0) +
            metrics['post_generation'].get('error_count', 0)
        )
        overall['total_errors'] = total_errors
        
        # 전체 성공률 계산
        success_rates = [
            metrics['data_collection'].get('success_rate', 0.0),
            metrics['ai_processing'].get('success_rate', 0.0),
            metrics['post_generation'].get('success_rate', 0.0)
        ]
        overall['overall_success_rate'] = sum(success_rates) / len(success_rates) if success_rates else 0.0
        
        # 파이프라인 건강도 평가
        if overall['overall_success_rate'] >= 0.95 and total_errors == 0:
            overall['pipeline_health'] = 'excellent'
        elif overall['overall_success_rate'] >= 0.90 and total_errors <= 1:
            overall['pipeline_health'] = 'good'
        elif overall['overall_success_rate'] >= 0.80 and total_errors <= 3:
            overall['pipeline_health'] = 'fair'
        else:
            overall['pipeline_health'] = 'poor'
            
        return overall
    
    def generate_daily_report(self) -> str:
        """일일 리포트 생성"""
        metrics = self.collect_pipeline_metrics()
        
        # 리포트 파일명
        date_str = datetime.now().strftime('%Y-%m-%d')
        report_file = self.reports_dir / f"pipeline_report_{date_str}.json"
        
        # 리포트 저장
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Generated daily report: {report_file}")
        return str(report_file)
    
    def generate_summary_report(self, days: int = 7) -> str:
        """요약 리포트 생성"""
        summary = {
            'period': f"Last {days} days",
            'generated_date': datetime.now().isoformat(),
            'daily_reports': [],
            'summary_metrics': {}
        }
        
        # 일일 리포트 수집
        cutoff_date = datetime.now() - timedelta(days=days)
        for report_file in self.reports_dir.glob("pipeline_report_*.json"):
            try:
                file_date_str = report_file.stem.split('_')[-1]
                file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
                
                if file_date >= cutoff_date:
                    with open(report_file, 'r', encoding='utf-8') as f:
                        report_data = json.load(f)
                        summary['daily_reports'].append(report_data)
                        
            except Exception as e:
                logger.error(f"Error reading report {report_file}: {e}")
        
        # 요약 메트릭 계산
        if summary['daily_reports']:
            summary['summary_metrics'] = self._calculate_summary_metrics(summary['daily_reports'])
        
        # 요약 리포트 저장
        summary_file = self.reports_dir / f"summary_report_{days}days.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Generated summary report: {summary_file}")
        return str(summary_file)
    
    def _calculate_summary_metrics(self, daily_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """요약 메트릭 계산"""
        summary = {
            'total_executions': len(daily_reports),
            'average_success_rate': 0.0,
            'total_errors': 0,
            'total_posts_generated': 0,
            'average_processing_time': 0.0
        }
        
        if not daily_reports:
            return summary
        
        # 평균 성공률
        success_rates = [report['overall']['overall_success_rate'] for report in daily_reports]
        summary['average_success_rate'] = sum(success_rates) / len(success_rates)
        
        # 전체 에러 수
        total_errors = sum(report['overall']['total_errors'] for report in daily_reports)
        summary['total_errors'] = total_errors
        
        # 생성된 포스트 수
        total_posts = sum(report['post_generation']['generated_posts_count'] for report in daily_reports)
        summary['total_posts_generated'] = total_posts
        
        return summary
    
    def generate_health_check_report(self) -> Dict[str, Any]:
        """건강도 체크 리포트 생성"""
        metrics = self.collect_pipeline_metrics()
        
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'overall_health': metrics['overall']['pipeline_health'],
            'success_rate': metrics['overall']['overall_success_rate'],
            'total_errors': metrics['overall']['total_errors'],
            'recommendations': []
        }
        
        # 권장사항 생성
        if health_report['overall_health'] == 'poor':
            health_report['recommendations'].append("파이프라인에 심각한 문제가 있습니다. 즉시 점검이 필요합니다.")
        
        if metrics['overall']['total_errors'] > 0:
            health_report['recommendations'].append("에러가 발생했습니다. 로그를 확인하여 문제를 해결하세요.")
        
        if metrics['overall']['overall_success_rate'] < 0.90:
            health_report['recommendations'].append("성공률이 낮습니다. 파이프라인 설정을 점검하세요.")
        
        if not health_report['recommendations']:
            health_report['recommendations'].append("파이프라인이 정상적으로 작동하고 있습니다.")
        
        return health_report

def main():
    """메인 실행 함수"""
    logger.info("Starting pipeline report generation...")
    
    # 리포트 생성기 초기화
    reporter = PipelineReporter()
    
    # 일일 리포트 생성
    daily_report = reporter.generate_daily_report()
    logger.info(f"Daily report: {daily_report}")
    
    # 요약 리포트 생성
    summary_report = reporter.generate_summary_report(days=7)
    logger.info(f"Summary report: {summary_report}")
    
    # 건강도 체크 리포트 생성
    health_report = reporter.generate_health_check_report()
    logger.info(f"Health check: {health_report['overall_health']}")
    
    # 권장사항 출력
    for recommendation in health_report['recommendations']:
        logger.info(f"Recommendation: {recommendation}")
    
    logger.info("Pipeline report generation completed")

if __name__ == "__main__":
    main()
