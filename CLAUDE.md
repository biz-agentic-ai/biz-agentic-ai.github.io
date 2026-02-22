# DataNexus Blog Source

Hugo 기반 블로그 프로젝트 (테마: PaperMod)

## 배포 규칙

**DOCS 폴더는 퍼블릭 레포에 절대 커밋하지 않는다.**
- `DOCS/`는 `.gitignore`에 등록되어 있다.
- `git add .`, `git add -A` 사용 금지 — 반드시 파일을 지정해서 `git add`한다.
- 커밋 전 `git status`에서 `DOCS/` 파일이 staged 되어 있지 않은지 확인한다.
- DOCS 폴더가 실수로 추적되면 `git rm -r --cached DOCS/`로 즉시 제거한다.

## 마크다운 작성 규칙

### 볼드체 + 한글 조사

Hugo Goldmark 렌더러에서 `**볼드**` 뒤에 한글이 바로 오면 볼드가 깨질 수 있다.
CJK 확장이 활성화되어 있지만, 안전을 위해 볼드 뒤 한글 조사 앞에 공백을 넣는다.

```markdown
# 좋음
**신뢰도(confidence)** 가 대표적이다.

# 나쁨
**신뢰도(confidence)**가 대표적이다.
```
