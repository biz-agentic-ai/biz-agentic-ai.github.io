# DataNexus Blog Source

Hugo 기반 블로그 프로젝트 (테마: PaperMod)

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
