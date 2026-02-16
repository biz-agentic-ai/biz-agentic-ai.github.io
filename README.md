# Biz Agentic AI Personal Blog

## 프로젝트 개요

이 프로젝트는 **Biz Agentic AI Personal Blog Automation System**의 1단계 산출물로, Hugo 정적 사이트 생성기를 사용하여 구축된 개인 블로그입니다.

## 주요 특징

- 🚀 **Hugo 기반**: 빠르고 안전한 정적 사이트 생성
- 🎨 **PaperMod 테마**: 깔끔하고 모던한 디자인
- 📱 **반응형 디자인**: 모바일과 데스크톱 모두 지원
- 🔄 **자동 배포**: GitHub Actions를 통한 자동 빌드 및 배포
- 🌐 **GitHub Pages**: 무료 호스팅 서비스

## 기술 스택

- **정적 사이트 생성기**: Hugo
- **테마**: PaperMod
- **호스팅**: GitHub Pages
- **CI/CD**: GitHub Actions
- **버전 관리**: Git

## 로컬 개발 환경 설정

### 필수 요구사항

- Git
- Hugo Extended (최신 버전)

### 설치 및 실행

1. **저장소 클론**
   ```bash
   git clone https://github.com/biz-agentic-ai/biz-agentic-ai.github.io.git
   cd biz-agentic-ai.github.io
   ```

2. **Hugo 서버 실행**
   ```bash
   hugo server -D
   ```

3. **브라우저에서 확인**
   - http://localhost:1313 접속

## 사이트 구조

```
biz-agentic-ai.github.io/
├── content/           # 콘텐츠 파일들
│   ├── about.md      # About 페이지
│   └── posts/        # 블로그 포스트들
├── themes/           # Hugo 테마
│   └── PaperMod/     # PaperMod 테마
├── static/           # 정적 파일들
├── layouts/          # 레이아웃 템플릿
├── hugo.toml         # Hugo 설정 파일
└── .github/          # GitHub Actions 설정
    └── workflows/    # CI/CD 워크플로우
```

## 배포

이 사이트는 GitHub Actions를 통해 자동으로 배포됩니다:

1. `main` 브랜치에 푸시하면 자동으로 빌드 시작
2. Hugo 사이트가 빌드되어 GitHub Pages에 배포
3. https://biz-agentic-ai.github.io 에서 확인 가능

## 개발 가이드

### 새 포스트 작성

```bash
hugo new posts/새-포스트-제목.md
```

### 새 페이지 생성

```bash
hugo new 새-페이지-제목.md
```

### 테마 커스터마이징

- `themes/PaperMod/` 디렉토리에서 테마 파일 수정
- 또는 `layouts/` 디렉토리에서 오버라이드

## 프로젝트 단계

이 프로젝트는 5단계로 구성되어 있습니다:

1. **Phase 1**: 기반 환경 구축 (현재 단계) ✅
2. **Phase 2**: 데이터 수집 파이프라인
3. **Phase 3**: AI 처리 엔진
4. **Phase 4**: 자동화 파이프라인
5. **Phase 5**: 최적화 및 검증

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 연락처

- **GitHub**: [@biz-agentic-ai](https://github.com/biz-agentic-ai)

---

**프로젝트 버전**: 1.0  
**최종 업데이트**: 2025-08-21
