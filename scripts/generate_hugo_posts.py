#!/usr/bin/env python3
"""
Hugo Post Generator
AI 처리 결과를 Hugo 포스트 형식으로 변환하는 스크립트
"""

import os
import json
import yaml
import frontmatter
import markdown
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HugoPostGenerator:
    """Hugo 포스트 생성기"""
    
    def __init__(self, output_dir: str = "ai-engine/output", posts_dir: str = "content/posts"):
        self.output_dir = Path(output_dir)
        self.posts_dir = Path(posts_dir)
        self.posts_dir.mkdir(parents=True, exist_ok=True)
        
    def load_processed_content(self) -> List[Dict[str, Any]]:
        """AI 처리된 콘텐츠를 로드"""
        processed_files = []
        
        if not self.output_dir.exists():
            logger.warning(f"Output directory {self.output_dir} does not exist")
            return processed_files
            
        for file_path in self.output_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    processed_files.append(content)
                    logger.info(f"Loaded processed content from {file_path}")
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
                
        return processed_files
    
    def generate_frontmatter(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Hugo 포스트의 Front Matter 생성"""
        # 기본 메타데이터
        frontmatter_data = {
            'title': content.get('title', 'Untitled Post'),
            'date': content.get('created_date', datetime.now().isoformat()),
            'lastmod': datetime.now().isoformat(),
            'draft': False,
            'description': content.get('summary', '')[:160],  # SEO를 위한 설명
            'tags': content.get('tags', []),
            'categories': content.get('categories', ['AI', 'Automation']),
            'author': 'Biz Agentic AI',
            'layout': 'post',
            'toc': True,
            'comments': True,
            'share': True,
            'featured': False,
            'weight': 1
        }
        
        # SEO 최적화
        if content.get('keywords'):
            frontmatter_data['keywords'] = content['keywords']
            
        # 이미지가 있는 경우
        if content.get('featured_image'):
            frontmatter_data['image'] = content['featured_image']
            
        # 원본 소스 정보
        if content.get('source'):
            frontmatter_data['source'] = content['source']
            
        return frontmatter_data
    
    def generate_post_content(self, content: Dict[str, Any]) -> str:
        """포스트 본문 내용 생성"""
        post_content = []
        
        # 요약 섹션
        if content.get('summary'):
            post_content.append("## 요약\n")
            post_content.append(content['summary'])
            post_content.append("\n\n")
        
        # 주요 내용
        if content.get('content'):
            post_content.append("## 주요 내용\n")
            post_content.append(content['content'])
            post_content.append("\n\n")
        
        # 키워드 및 태그
        if content.get('keywords'):
            post_content.append("## 키워드\n")
            keywords_text = ", ".join(content['keywords'])
            post_content.append(f"**{keywords_text}**\n\n")
        
        # 카테고리
        if content.get('categories'):
            post_content.append("## 카테고리\n")
            categories_text = ", ".join(content['categories'])
            post_content.append(f"**{categories_text}**\n\n")
        
        # 원본 소스 정보
        if content.get('source'):
            post_content.append("## 출처\n")
            post_content.append(f"- **원본**: {content['source']}\n")
            if content.get('source_date'):
                post_content.append(f"- **날짜**: {content['source_date']}\n")
            post_content.append("\n")
        
        # AI 처리 정보
        post_content.append("---\n")
        post_content.append("*이 포스트는 AI가 자동으로 생성한 요약본입니다.*\n")
        post_content.append(f"*생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        return "".join(post_content)
    
    def sanitize_filename(self, title: str) -> str:
        """파일명으로 사용할 수 있도록 제목을 정리"""
        # 특수문자 제거 및 공백을 하이픈으로 변경
        import re
        filename = re.sub(r'[^\w\s-]', '', title.lower())
        filename = re.sub(r'[-\s]+', '-', filename)
        return filename.strip('-')
    
    def generate_post(self, content: Dict[str, Any]) -> str:
        """단일 포스트 생성"""
        try:
            # Front Matter 생성
            frontmatter_data = self.generate_frontmatter(content)
            
            # 포스트 내용 생성
            post_content = self.generate_post_content(content)
            
            # 파일명 생성
            title = frontmatter_data['title']
            date_str = frontmatter_data['date'][:10]  # YYYY-MM-DD
            filename = f"{date_str}-{self.sanitize_filename(title)}.md"
            
            # 포스트 파일 경로
            post_path = self.posts_dir / filename
            
            # Front Matter와 내용을 결합
            post = frontmatter.Post(post_content, **frontmatter_data)
            
            # 파일 저장
            with open(post_path, 'w', encoding='utf-8') as f:
                frontmatter.dump(post, f)
            
            logger.info(f"Generated post: {post_path}")
            return str(post_path)
            
        except Exception as e:
            logger.error(f"Error generating post for {content.get('title', 'Unknown')}: {e}")
            return None
    
    def validate_post_quality(self, content: Dict[str, Any]) -> bool:
        """포스트 품질 검증"""
        # 최소 길이 검증
        if not content.get('summary') or len(content['summary']) < 50:
            logger.warning(f"Post {content.get('title', 'Unknown')} has insufficient summary")
            return False
        
        # 제목 검증
        if not content.get('title') or len(content['title']) < 5:
            logger.warning(f"Post {content.get('title', 'Unknown')} has invalid title")
            return False
        
        # 카테고리 검증
        if not content.get('categories'):
            logger.warning(f"Post {content.get('title', 'Unknown')} has no categories")
            return False
        
        return True
    
    def generate_all_posts(self) -> List[str]:
        """모든 처리된 콘텐츠를 포스트로 변환"""
        processed_contents = self.load_processed_content()
        generated_posts = []
        
        logger.info(f"Found {len(processed_contents)} processed contents")
        
        for content in processed_contents:
            # 품질 검증
            if not self.validate_post_quality(content):
                logger.warning(f"Skipping low-quality content: {content.get('title', 'Unknown')}")
                continue
            
            # 포스트 생성
            post_path = self.generate_post(content)
            if post_path:
                generated_posts.append(post_path)
        
        logger.info(f"Successfully generated {len(generated_posts)} posts")
        return generated_posts
    
    def cleanup_old_posts(self, days: int = 30):
        """오래된 포스트 정리 (선택사항)"""
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        for post_file in self.posts_dir.glob("*.md"):
            try:
                file_time = post_file.stat().st_mtime
                if file_time < cutoff_date:
                    post_file.unlink()
                    logger.info(f"Cleaned up old post: {post_file}")
            except Exception as e:
                logger.error(f"Error cleaning up {post_file}: {e}")

def main():
    """메인 실행 함수"""
    logger.info("Starting Hugo post generation...")
    
    # 생성기 초기화
    generator = HugoPostGenerator()
    
    # 포스트 생성
    generated_posts = generator.generate_all_posts()
    
    # 결과 출력
    if generated_posts:
        logger.info(f"Successfully generated {len(generated_posts)} posts:")
        for post in generated_posts:
            logger.info(f"  - {post}")
    else:
        logger.info("No posts were generated")
    
    # 오래된 포스트 정리 (선택사항)
    # generator.cleanup_old_posts()
    
    logger.info("Hugo post generation completed")

if __name__ == "__main__":
    main()
