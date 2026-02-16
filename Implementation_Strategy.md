# DataNexus Implementation Strategy

**IMPLEMENTATION STRATEGY**

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

Claude Code Agent Teams + bkit + Context-as-Code

*Ontology-Driven Autonomous Data Agent*

Platform Tech Team \| Lotte Innovate

---

> **📌 이 문서의 역할**
>
> **Implementation Strategy**는 DataNexus의 **구현 전략서**입니다.
> "왜 이 도구를 선택했는지, 어떤 조합으로 쓰는지, 리스크는 무엇인지"에 대한
> **설계 근거, 아키텍처 결정, 참조 테이블**을 담고 있습니다.
>
> | 항목 | 내용 |
> |------|------|
> | **성격** | 의사결정 문서 / 아키텍처 레퍼런스 |
> | **대상** | 의사결정자, 아키텍트, 리드 개발자 |
> | **활용 시점** | 프로젝트 킥오프, 기술 선택 논의, 설계 리뷰 시 |
> | **주요 질문** | "왜 Agent Teams인가?", "도구별 역할은?", "리스크 대응은?" |
>
> **짝꿍 문서:** [Implementation Guide](Implementation_Guide.md)
> — Strategy가 **지도(Map)**라면, Guide는 **내비게이션 안내(Turn-by-Turn)**입니다.
> Guide는 본 문서의 전략을 STEP 1~24의 복사-붙여넣기 가능한 실행 명령으로 풀어낸 문서입니다.
> 실제 개발 착수 시에는 Guide를 펼쳐놓고, 배경 이해가 필요할 때 본 문서로 돌아오세요.
>
> **참고:** 본 문서의 §12.2 매핑 테이블, §13.2 체크리스트 등은 Guide에서 자주 참조됩니다.

### 두 문서의 관계

```
┌─────────────────────────────┐        ┌─────────────────────────────┐
│  Implementation Strategy     │        │  Implementation Guide        │
│  (본 문서)                   │        │  (짝꿍 문서)                 │
│  ───────────────────────     │        │  ───────────────────────     │
│  § 1  Executive Summary      │        │  Part 1  환경 설정           │
│  § 2  Strategy Background    │        │  Part 2  설계 (Phase 0)      │
│  § 3  Tool Configuration     │◄───────│  Part 3  병렬개발 (Phase 1)  │
│  § 5  Module Mapping         │        │  Part 4  통합검증 (Phase 2)  │
│  § 6  Teams Guide            │        │  Part 5  심화적용 (Phase 3)  │
│  § 8  Context-as-Code        │◄───────│  Part 6  Reference           │
│  § 9  Risks & Mitigations    │        │  Part 7  Ecosystem           │
│  §11  Cowork Plugin          │        │                              │
│  §12  Worktree 전략          │◄───────│  Guide에서 Strategy를        │
│  §13  Cross-Review           │◄───────│  자주 참조 (← 방향)          │
│  §14  CLAUDE.md 축적         │◄───────│                              │
│                              │        │                              │
│  ★ WHY & WHAT               │        │  ★ HOW & WHEN               │
│  ★ 지도 (Map)               │        │  ★ 내비 (Turn-by-Turn)      │
└─────────────────────────────┘        └─────────────────────────────┘
```

---

**1. Executive Summary**

본 문서는 DataNexus PRD (SEOCHO Integrated)의 성공적 구현을 위한
최종 개발 전략을 정리합니다. 2026년 2월 5일 Anthropic이 Opus 4.6과 함께
공식 출시한 Agent Teams 기능을 반영하여, 기존에 검토되었던 3개 서드파티
플러그인 조합(bkit + clnode + OMC) 전략을 재평가하고 최적화된 전략을
제시합니다.

  -----------------------------------------------------------------------
  Core Strategy: bkit으로 설계하고, Context-as-Code로 컨텍스트를
  계층화하며, Agent Teams로 병렬 실행하고, Guardian/Distill 패턴으로
  품질과 지식을 자동 관리하는 구조

  -----------------------------------------------------------------------

  ---------------- --------------------------- ---------------------------
  **구분**         **기존 제안**               **최종 전략 (수정)**

  **설계 도구**    bkit (PDCA)                 bkit (PDCA) - 유지

  **에이전트       clnode (DuckDB 기반 공유    Agent Teams (네이티브) -
  조율**           메모리)                     대체

  **병렬 실행**    OMC Swarm/Ultrapilot        Agent Teams (네이티브) -
                                               대체

  **지속 실행**    OMC Ralph                   OMC Ralph - 선택적 유지
  ---------------- --------------------------- ---------------------------

**2. Strategy Change Background**

**2.1 Agent Teams: Anthropic 공식 멀티에이전트**

2026년 2월 5일, Anthropic은 Claude Opus 4.6 출시와 함께 Agent Teams를
Research Preview로 공개했습니다. 이는 여러 Claude Code 인스턴스가 하나의
팀으로 협업할 수 있는 네이티브 기능입니다.

  ------------------ ----------------------------------------------------
  **특성**           **설명**

  **Team Lead**      메인 세션이 팀을 생성하고, 작업 할당 및 결과 종합
                     담당

  **Teammate**       독립 컨텍스트 윈도우에서 작업, 상호 직접 메시징 가능

  **Shared Task      의존성(DAG) 기반 태스크 관리, 세션 간 상태 유지
  List**             

  **활성화**         CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

  **통신 방식**      TeammateTool + SendMessage (P2P 메시징, broadcast,
                     plan approval)

  **표시 모드**      In-process (기본) 또는 Split-pane (tmux/iTerm2 필요)
  ------------------ ----------------------------------------------------

**2.2 기존 제안 재평가: 왜 변경하는가**

-   **clnode** 제거: Agent Teams가 에이전트 간 컨텍스트 공유 문제를
    네이티브로 해결합니다. clnode가 DuckDB로 구현한 에이전트 메일박스를
    Agent Teams의 Shared Task List + 직접 메시징이 대체합니다. clnode는
    Star 6개의 초기 프로젝트이며, 상용 라이선스가 필요합니다.

-   **OMC Swarm/Ultrapilot** 대체: Agent Teams의 병렬 Teammate 실행이
    기능적으로 동일합니다. 네이티브 구현이 서드파티 hooks 기반보다
    안정적이며, hook 충돌 위험이 없습니다.

-   **OMC Ralph** 유지: PRD 생성 및 반복 검증 루프(완료까지 멈추지 않는
    실행)는 Agent Teams에 없는 고유 기능입니다. DataNexus의 품질 검증
    사이클에 유용합니다.

-   **bkit** 유지: PDCA 방법론 기반 설계는 Agent Teams와 경쟁하지 않고
    보완합니다. 설계(What) vs 실행(How)의 레이어가 다릅니다.

**3. Final Tool Configuration**

<!-- SSOT: 본 섹션 / 설치 방법은 Implementation_Guide STEP 1-3 참조 -->

**3.1 도구별 역할 및 시너지 (전략적 의사결정)**

각 도구의 역할을 명확히 구분하여 중복을 방지하고 시너지를 극대화합니다.

  ------------- -------------------- ------------------- -------------------
                **bkit (설계)**      **Agent Teams       **OMC Ralph
                                     (실행)**            (검증)**

  **역할**      PRD 분석,            병렬 개발, 에이전트 완료까지 지속 실행,
                PLAN.md/DESIGN.md    조율, 태스크 관리   반복 검증 루프
                생성

  **유형**      Claude Code Plugin   Claude Code Native  Claude Code Plugin

  **핵심 명령** /bkit:pdca-plan      자연어로 팀 구성    ralph: \"task\"
                /bkit:pdca-design    요청 Ctrl+T (태스크 (완료까지 자동
                /bkit:pdca-iterate   보기) Shift+Up/Down 반복)

  **필수 여부** **Required**         **Required**        **Optional**
  ------------- -------------------- ------------------- -------------------

**설치 및 환경 설정 실행 가이드는 Implementation_Guide STEP 1-3 참조**

**3.2 설치 및 환경 설정**

**Step 1: bkit 설치**

> \# Claude Code 내에서 실행
>
> /plugin marketplace add popup-studio-ai/bkit-claude-code
>
> /plugin install bkit

**Step 2: Agent Teams 활성화**

> \# 환경변수 설정 (shell profile에 추가)
>
> export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
>
> \# 또는 settings.json에 추가
>
> { \"env\": { \"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS\": \"1\" } }

**Step 3: OMC 설치 (선택)**

> \# Claude Code 내에서 실행
>
> /plugin marketplace add Yeachan-Heo/oh-my-claudecode
>
> /plugin install oh-my-claudecode

**4. Step-by-Step Execution Guide**

DataNexus PRD의 로드맵(Phase 0.5 \~ Phase 3+)에 맞춘 단계별 실행
가이드입니다.

**Phase 0: 설계 (bkit PDCA)**

  -----------------------------------------------------------------------
  도구: bkit \| 산출물: PLAN.md, DESIGN.md \| 기간: 1-2일/모듈

  -----------------------------------------------------------------------

PRD의 각 핵심 모듈을 bkit PDCA로 분해합니다. PRD의 복잡한
요구사항을 Claude Code 에이전트가 이해할 수 있는 구조화된 설계서로
변환하는 단계입니다.

  ----------------------- ----------------------- -----------------------
  **설계 대상 모듈**      **bkit 명령어**         **PRD 참조 섹션**

  온톨로지 엔진 + 스키마  /bkit:pdca-plan         §4.4.2, §4.4.2.4
  강제성                                          

  Multi-Agent             /bkit:pdca-plan         §3.5, §3.5.3 (HoT)
  Router/Supervisor                               

  하이브리드 검색         /bkit:pdca-design       §3.2, ApeRAG 연동
  (GraphRAG+Vector)                               

  NL2SQL (Vanna 2.0)      /bkit:pdca-design       부록 B.8, §3.3

  SEOCHO Agent Studio UI  /bkit:pdca-design       §2.1.6, §3.5.4

  엔티티 정규화           /bkit:pdca-design       §4.3.6.2
  파이프라인                                      
  ----------------------- ----------------------- -----------------------

**Phase 1: 스캐폴딩 + 코어 개발 (Agent Teams)**

  -----------------------------------------------------------------------
  도구: Agent Teams \| 팀 구성: Lead + 4 Teammates \| 기간: PRD Phase 0.5
  \~ Phase 1

  -----------------------------------------------------------------------

bkit이 생성한 설계서(PLAN.md, DESIGN.md)를 프로젝트 루트의 .claude/
디렉토리에 배치합니다. 모든 Teammate가 CLAUDE.md 시스템을 통해 자동으로
설계서를 참조하게 됩니다.

**Agent Team 구성 프롬프트 예시**

다음과 같은 자연어로 Team Lead에게 지시합니다:

> DataNexus 백엔드를 구현할 팀을 구성해줘:
>
> 1\. Backend Core - FastAPI 서버, 인증, Docker 인프라 구축
>
> (.claude/DESIGN-ontology.md 참조)
>
> 2\. Graph Engine - DozerDB 연동, 온톨로지 스키마 강제성,
>
> Cypher 템플릿 라이브러리 구현
>
> 3\. RAG Pipeline - ApeRAG 연동, 벡터/그래프 하이브리드 검색
>
> 4\. Agent Logic - Router/Supervisor/DBA 에이전트,
>
> Hierarchy of Truth 충돌 해결 로직
>
> 각 Teammate는 독립적으로 작업하되, 공유 태스크로 의존성을 관리해줘.

**팀 역할 매핑 (PRD → Agent Teams)**

  --------------- ------------------ ------------------ ------------------
  **Teammate**    **담당 PRD 모듈**  **핵심 산출물**    **의존성**

  **Backend       부록 F (개발       FastAPI, Docker    없음 (선행)
  Core**          가이드)            Compose, DB 스키마 

  **Graph         §4.4 온톨로지      SchemaEnforcer, CQ Backend Core
  Engine**        엔지니어링         Validator, DozerDB 
                                     연동               

  **RAG           §3.1-3.2 ApeRAG    MinerU 파싱, 벡터  Backend Core
  Pipeline**      연동               인덱스, GraphRAG   

  **Agent Logic** §3.5 Multi-Agent   Router,            Graph + RAG
                  Studio             Supervisor, HoT,   
                                     DBA Agent          
  --------------- ------------------ ------------------ ------------------

**Phase 2: 통합 + 품질 검증**

  -----------------------------------------------------------------------
  도구: bkit iterate + Agent Teams + (선택) OMC Ralph \| 기간: PRD Phase
  1.5 \~ Phase 2

  -----------------------------------------------------------------------

각 Teammate의 산출물을 통합하고, PRD §5.4의 Multi-Agent 평가
프레임워크를 실행합니다.

**품질 검증 사이클**

1.  **bkit 반복 검증:** /bkit:pdca-iterate 명령으로 설계 대비 구현
    상태를 점검합니다.

2.  **SEOCHO 평가 CLI 실행:** 부록 H의 CLI로 Macro/Ablation 실험을
    실행합니다.

> docker exec agent-jupyter-container python -m src.cli.evaluate \--all

3.  **Quality Gate 통과 확인:** PRD 정의 임계값 - Routing Accuracy ≥
    0.95, ConflictResolutionScore ≥ 0.95, Hallucination Rate ≤ 0.05

4.  **(선택) OMC Ralph 지속 실행:** Quality Gate 미달 시 ralph 루프로
    자동 수정 사이클을 돌립니다.

> ralph: \"Quality Gate 미달 항목 수정 - routing_accuracy 현재 0.93,
> 목표 0.95\"

**5. PRD Module-to-Execution Mapping**

PRD의 핵심 모듈별로 어떤 도구가 어떤 역할을 수행하는지 상세
매핑입니다.

  ------------------- ------------ ------------- ------------ ------------
  **PRD 모듈**        **Phase**    **설계        **실행       **검증**
                                   (bkit)**      (Teams)**    

  CQ 기반 검증 (§C.4) 0.5          pdca-plan     단독 세션    bkit iterate

  스키마 강제성       1            pdca-design   Graph Engine 평가 CLI
  (§4.4.2.4)                                                  

  관계 표현력         1            pdca-design   Graph Engine CQ Validator
  (§4.4.1.4)                                                  

  Router Agent        1            pdca-plan     Agent Logic  Macro 실험
  (§3.4-3.5)                                                  

  NL2SQL Vanna 2.0    1            pdca-design   Backend Core Exec
  (B.8)                                                       Accuracy

  증분 업데이트       1            pdca-design   Graph Engine bkit iterate
  (§4.4.4)                                                    

  DataHub synonyms    1.5          \-            Backend Core \-
  (B.6)                                                       

  SKOS 호환 (§4.6)    1.5          pdca-design   Graph Engine RDF Export

  Query Log 수집      2            pdca-plan     RAG Pipeline bkit iterate
  (B.2)                                                       

  Agent Studio UI     2            pdca-design   전용 FE팀    E2E 테스트
  (§2.1.6)                                                    

  UI Design System    2            -             전용 FE팀    §11.15 QA
  QA + 토큰 관리                                              체크리스트 CI
  (§11)                                                       

  전문 추론 엔진      3+           pdca-plan     Agent Logic  Ablation
  (§4.5.2.6)                                                  
  ------------------- ------------ ------------- ------------ ------------

**6. Agent Teams Practical Guide**

<!-- SSOT: 본 섹션 / 실행 방법은 Implementation_Guide "Agent Teams 실전 팁" 참조 -->

**6.1 효과적인 팀 구성 원칙 (전략적 맥락)**

팀 구성의 핵심은 독립성과 의존성의 균형입니다. DataNexus의 모듈 구조(Backend/Graph/RAG/Agent)는 자연스러운 팀 분할 경계를 제공합니다.

-   **독립적 작업 단위로 분할:** 같은 파일을 수정하는 Teammate가 없도록
    합니다. DataNexus는 Backend/Graph/RAG/Agent로 자연스럽게 분리됩니다.

-   **의존성은 Task로 명시:** Graph Engine은 Backend Core의 DB 스키마에
    의존합니다. addBlockedBy로 체이닝하면 자동으로 순서가 관리됩니다.

-   **Lead는 조율만:** Shift+Tab으로 Delegate Mode를 활성화하면 Lead가
    직접 코딩하지 않고 조율에만 집중합니다.

-   **컨텍스트 제공:** 각 Teammate에게 충분한 설계
    문서(.claude/DESIGN-\*.md)를 참조하도록 지시합니다.

**실행 세부사항은 Implementation_Guide "Agent Teams 실전 팁" 참조**

**6.2 알려진 제한사항 및 대응 (리스크 분석)**

Agent Teams의 제약사항과 완화 전략. 각 제한사항의 근본 원인과 구조적 대응 방안을 정리합니다.

  ----------------------- ----------------------- -----------------------
  **제한사항**            **영향**                **대응 방안**

  세션 재개 불가          /resume 시 Teammate     새 Teammate를
                          사라짐                  스폰하도록 Lead에 지시

  세션 종료 시 상태 휘발  컨텍스트 손실           Context-as-Code로 파일
                                                  시스템에 영속화

  태스크 상태 지연        의존 태스크가 차단됨    수동 확인 후 Lead에
                                                  상태 업데이트 요청

  중첩 팀 불가            Teammate가 하위 팀 생성 Lead가 Subagent로 추가
                          불가                    분할 가능

  토큰 비용 증가          멀티에이전트로 비용 N배 Claude Max 요금제 활용,
                                                  비핵심 작업은 단독 세션

  파일 잠금 없음          동시 수정 시            모듈별 디렉토리 분리로
                          Last-write-wins         충돌 원천 방지
  ----------------------- ----------------------- -----------------------

**7. Technology Stack Reference**

<!-- SSOT: 본 섹션 / 버전 및 URL은 공통 참조용 -->

**7.1 DataNexus 핵심 프레임워크**

  --------------- ----------------- ------------------------------------------
  **컴포넌트**    **버전**          **URL / 비고**

  **ApeRAG**      v0.5.0-alpha.14   github.com/apecloud/ApeRAG

  **DozerDB**     v5.26.3.0         dozerdb.org

  **Vanna AI**    v2.0.2            vanna.ai (Agent-based, User-Aware)

  **DataHub**     v1.3.0.1          datahubproject.io

  **SEOCHO**      feature-kgbuild   github.com/tteon/seocho
  --------------- ----------------- ------------------------------------------

**7.2 Claude Code 개발 도구**

  --------------- ------------- --------------------------------------------- ---------------------
  **도구**        **역할**      **URL**                                       **비고**

  **Agent Teams** 실행/조율     code.claude.com/docs/en/agent-teams           Anthropic 네이티브,
                                                                              Experimental

  **bkit**        설계/방법론   github.com/popup-studio-ai/bkit-claude-code   PDCA, Context
                                                                              Engineering

  **OMC**         지속 검증     github.com/Yeachan-Heo/oh-my-claudecode       Ralph 모드만 선택
                                                                              사용
  --------------- ------------- --------------------------------------------- ---------------------

이 테이블은 Strategy와 Guide 양쪽에서 공통 참조합니다.

**8. Context-as-Code: Philosophy_AI Integration**

<!-- SSOT: 본 섹션은 전략적 근거만 기술 / 실행 명령어는 Implementation_Guide STEP 4 참조 -->

Philosophy_AI(github.com/dev-whitecrow/Philosophy_AI)의 핵심 아이디어를
DataNexus 개발 워크플로우에 통합합니다. 전체 프레임워크를 도입하는 것이
아니라, DataNexus 구현에 실질적 가치를 제공하는 3가지 패턴만 선별
적용합니다.

**8.1 왜 통합하는가 (전략적 가치)**

-   **Fearless Reset (두려움 없는 리셋):** Agent Teams의 핵심 제한사항인
    \'세션 재개 불가\'를 구조적으로 해결합니다. 모든 설계 맥락이 파일
    시스템에 체계적으로 존재하면, 새 세션에서도 Teammate가 첫 마디부터
    프로젝트를 완벽히 이해합니다.

-   **Zero Fatigue (입력 피로도 제로):** 매 세션마다 PRD 컨텍스트를 반복
    설명할 필요 없이, 구조화된 파일이 자동으로 주입됩니다. bkit
    산출물(PLAN.md/DESIGN.md)의 가치가 극대화됩니다.

-   **Context-SOLID로 토큰 효율화:** SOLID 원칙을 적용한 모듈화된
    컨텍스트 파일은 필요한 정보만 선택적 로딩(ISP)되어, Agent Teams의
    토큰 비용 문제를 완화합니다.

**8.2 선별 적용: 3가지 패턴 (아키텍처 결정)**

  ------------- ------------------- ------------------- -------------------
  **Pattern**   **Philosophy_AI     **DataNexus 적용**  **효과**
                원본**                                  

  **#1 The      The_Ark/ 레이어드   .claude/ 컨텍스트를 Teammate별 필요
  Ark**         지식 아키텍처       Foundation / Domain 레이어만 로딩, 토큰
                (Foundation →       / Execution         절감
                Domains →           3계층으로 재구성    
                Execution)                              

  **#2          Guardian Agent:     PRD 설계 원칙 위반  PRD와 구현의 정합성
  Guardian**    논리적 무결성 검증, 자동 감지 Hook을    보장
                철학 간 모순/충돌   Agent Teams에 적용  
                감지                                    

  **#3          Architect Agent:    구현 중 발견된 기술 프로젝트 지식이
  Distill**     비정형 데이터를     결정 사항을         시간에 따라
                Foundation 규칙에   .claude/에 자동     축적/진화
                맞춰 정제           증류(Distill)       
  ------------- ------------------- ------------------- -------------------

**8.3 DataNexus Context Architecture**

<!-- SSOT: Implementation_Guide STEP 4-5 / 본 섹션은 전략적 맥락만 기술 -->

bkit이 생성하는 PLAN.md/DESIGN.md를 Philosophy_AI의 The Ark 패턴으로
계층화합니다. Claude Code의 .claude/ 시스템을 그대로 활용하되, 내부를
3개 레이어로 구조화합니다.

**디렉토리 구조 상세는 Implementation_Guide STEP 4-5 참조**

계층 개요:
- **foundation/** - Layer 1: 불변 원칙 (모든 Teammate 공유)
- **domains/** - Layer 2: 모듈별 전문 컨텍스트
- **execution/** - Layer 3: 변경 가능한 전술
- **rules/** - Claude Code 기본 규칙

각 파일의 역할 및 생성 명령어는 Implementation_Guide §STEP 4 참조.

**8.4 Context-SOLID Mapping**

Philosophy_AI의 Context-SOLID 원칙을 DataNexus 컨텍스트 관리에
적용합니다.

  ----------- -------------------- ---------------------------------------
  **SOLID**   **원칙**             **DataNexus 적용**

  **SRP**     파일 하나 = 의미     schema-enforcement.md는 스키마만,
              단위 하나            hierarchy-of-truth.md는 충돌 해결만 →
                                   Teammate가 필요한 파일만 로딩

  **OCP**     Foundation 보존,     PRD 핵심 원칙(foundation/)은 불변,
              Execution 확장       Sprint별 전술(execution/)은 자유 변경 →
                                   일관성 + 유연성

  **LSP**     하위가 상위를        Guardian Hook이 domains/ 구현이
              위반하지 않음        foundation/ 원칙에 위배되는지 자동 검증

  **ISP**     필요한 정보만 선택   Graph Teammate는 ontology-engine.md +
              로딩                 foundation/만, RAG는 rag-search.md +
                                   foundation/ → 컨텍스트 절약

  **DIP**     추상과 구체 분리     quality-gates.md(추상 기준)와
                                   current-sprint.md(구체 수치) 분리 →
                                   기준 변경 시 한 곳만 수정
  ----------- -------------------- ---------------------------------------

**8.5 Guardian Pattern: PRD 정합성 자동 검증**

Philosophy_AI의 Guardian Agent 패턴을 Agent Teams의 TaskCompleted Hook에
적용합니다. Teammate가 태스크를 완료 표시할 때 foundation/ 원칙 위반
여부를 자동 검증합니다.

> \# Agent Teams Hook: TaskCompleted
>
> \# exit code 2 = 완료 거부 + 피드백 전송
>
> 검증 항목:
>
> 1\. SchemaEnforcer 규칙 위반 (foundation/schema-enforcement.md)
>
> 2\. Quality Gate 임계값 충족 (foundation/quality-gates.md)
>
> 3\. HoT 충돌 해결 로직 정합성 (foundation/hierarchy-of-truth.md)
>
> 4\. 프론트엔드 규칙 준수 — FE Teammate 대상 (rules/datanexus.md §프론트엔드 규칙)
>
>    - z-index 하드코딩 없음, 이모지 아이콘 없음, 색상 하드코딩 없음
>    - §11.15 QA 체크리스트 자동 검증 항목(lint) 통과

Agent Teams의 기존 Hook 시스템(TeammateIdle, TaskCompleted)과 자연스럽게
통합됩니다. 추가 의존성이 없습니다.

**8.6 Distill Pattern: 기술 결정 자동 축적**

구현 과정에서 내린 기술 결정을 execution/decisions-log.md에 자동
기록합니다. Philosophy_AI의 Scribe Agent 패턴을 차용합니다.

-   **기록 시점:** 아키텍처 변경, 의존성 추가, API 설계 결정 시
    Teammate가 자동 기록

-   **기록 형식:** \[타임스탬프\] \[Teammate\] \[결정 사항\] \[검토
    대안\] \[선택 근거\]

-   **누적 효과:** 세션 리셋 후 새 Teammate가 과거 결정 이력을 즉시
    파악, 동일 실수 반복 방지

  -----------------------------------------------------------------------
  Philosophy_AI 통합의 핵심 가치: Agent Teams의 \'세션 휘발성\' 문제를
  구조적으로 해결. 파일 시스템이 곧 프로젝트의 영속적 기억(Persistent
  Memory)이 됩니다.

  -----------------------------------------------------------------------

**9. Risks & Mitigations**

  ----------- -------------------- -------------------- --------------------
  **Level**   **Risk**             **Impact**           **Mitigation**

  **HIGH**    Agent Teams          팀 기반 워크플로우   bkit 설계서는 Agent
              Experimental 상태 -  전체 변경            Teams 없이도 활용
              기능 변경/제거 가능                       가능. 단독 세션 +
                                                        Subagent로 Fallback

  **MED**     OMC + bkit hook 충돌 플러그인 오작동      OMC는 Ralph 모드만
                                                        선택적 사용, 문제 시
                                                        제거 가능

  **MED**     토큰 비용 초과       예산 초과            Claude Max 200
              (Agent Teams                              요금제, 비핵심
              멀티에이전트)                             작업은 단독 세션
                                                        유지

  **LOW**     기업 네트워크에서    bkit/OMC 사용 불가   Agent Teams만으로도
              Plugin 설치 제한                          핵심 실행 가능,
                                                        설계는 수동 문서로
                                                        대체
  ----------- -------------------- -------------------- --------------------

**10. Conclusion**

DataNexus PRD의 구현은 복잡한 멀티 컴포넌트 시스템(ApeRAG, DozerDB,
Vanna, DataHub, SEOCHO)의 통합을 요구합니다. 이 복잡성을 관리하기 위해
다음과 같은 최종 전략을 채택합니다:

1.  **bkit PDCA로 설계를 구조화하여** 에이전트가 PRD의 의도를 정확히
    파악할 수 있는 PLAN.md/DESIGN.md를 생성합니다.

2.  **Philosophy_AI의 Context-as-Code로 컨텍스트를 계층화하여**
    Foundation/Domain/Execution 3계층 구조가 Teammate에게 필요한 정보만
    정확히 전달합니다.

3.  **Agent Teams(네이티브)로 병렬 실행하여** Backend, Graph, RAG, Agent
    Logic 모듈을 독립 Teammate가 동시에 구현합니다.

4.  **Guardian/Distill 패턴으로 품질과 지식을 자동 관리하여** PRD 정합성
    검증과 기술 결정 축적이 세션 리셋에도 영속적으로 유지됩니다.

  -----------------------------------------------------------------------
  핵심 원칙: 네이티브 기능 우선, 서드파티는 고유 가치가 있을 때만 선택적
  사용. 설계(bkit) → 컨텍스트(Context-as-Code) → 실행(Agent Teams) →
  검증(Guardian)의 레이어를 명확히 분리.

  -----------------------------------------------------------------------

*Author: Platform Tech Team*


---

## 11. Cowork Plugin 구조 적용 (보강: Ecosystem Analysis §1)

> **신규 섹션 — Claude Cowork Plugins 구조를 DataNexus Context-as-Code에 통합**

### 11.1 Plugin 4요소 → DataNexus 매핑

| Cowork Plugin 요소 | DataNexus 대응 | 현재 상태 | 보강 필요 |
|-------------------|---------------|----------|----------|
| `skills/` | `.claude/foundation/` + `domains/` | ✅ 존재 | domain 기술을 분리된 skill 파일로 구조화 |
| `commands/` | bkit 명령어 | ⚠️ 부분 존재 | 커스텀 Slash 명령어 추가 필요 |
| `.mcp.json` | 개별 API 연동 설정 | ❌ 부재 | 통합 MCP 커넥터 설정 파일 생성 |
| `agents/` (sub-agents) | Agent Teams Teammate 정의 | ⚠️ 자연어 | 독립 에이전트 정의 파일 분리 |

### 11.2 DataNexus 커스텀 Slash 명령어

```yaml
# datanexus-data/commands.yaml
commands:
  /dn:validate-ontology:
    description: "DataHub Glossary Term 정의 충돌 검증"
    action: "python src/validators/ontology_validator.py"
    context: [foundation/schema-enforcement.md]
    
  /dn:test-nl2sql:
    description: "Few-shot 예제 기반 NL2SQL 정확도 테스트"
    action: "pytest tests/e2e/test_nl2sql_accuracy.py -v"
    context: [domains/nl2sql-pipeline.md]
    
  /dn:sync-rag:
    description: "DataHub → Vanna/ApeRAG 수동 동기화 실행"
    action: "python src/sync/manual_sync.py"
    context: [domains/rag-search.md]
    
  /dn:quality-gate:
    description: "품질 게이트 통합 실행 (Unit + E2E)"
    action: "pytest tests/ -v --tb=short"
    context: [foundation/quality-gates.md]
```

### 11.3 통합 MCP 커넥터 설정

```json
// datanexus-connectors.mcp.json
{
  "mcpServers": {
    "aperag": {
      "command": "npx",
      "args": ["-y", "@aperag/mcp-server"],
      "env": {
        "APERAG_API_URL": "${APERAG_URL}",
        "APERAG_API_KEY": "${APERAG_KEY}"
      }
    },
    "datahub": {
      "command": "python",
      "args": ["-m", "datahub.mcp_server"],
      "env": {
        "DATAHUB_GMS_URL": "${DATAHUB_URL}",
        "DATAHUB_TOKEN": "${DATAHUB_TOKEN}"
      }
    },
    "dozerdb": {
      "command": "npx",
      "args": ["-y", "@neo4j/mcp-server"],
      "env": {
        "NEO4J_URI": "${DOZERDB_URI}",
        "NEO4J_USER": "${DOZERDB_USER}",
        "NEO4J_PASSWORD": "${DOZERDB_PASSWORD}"
      }
    },
    "vanna": {
      "command": "python",
      "args": ["-m", "vanna.mcp_server"],
      "env": {
        "VANNA_API_URL": "${VANNA_URL}"
      }
    }
  }
}
```

---

## 12. Worktree 병렬 개발 전략 (보강: Boris Cherny Tip #1)

> **신규 섹션 — Git Worktree를 활용한 Agent Teams 병렬 개발**

### 12.1 Worktree 초기 설정 스크립트

```bash
#!/bin/bash
# setup_worktrees.sh - DataNexus 병렬 개발 환경 구성

MAIN_DIR=$(pwd)
BRANCH_PREFIX="feature/datanexus"

# 모듈별 Worktree 생성
git worktree add ../wt-backend  ${BRANCH_PREFIX}-backend
git worktree add ../wt-graph    ${BRANCH_PREFIX}-graph
git worktree add ../wt-rag      ${BRANCH_PREFIX}-rag
git worktree add ../wt-agent    ${BRANCH_PREFIX}-agent
git worktree add ../wt-analysis ${BRANCH_PREFIX}-analysis

echo "✅ Worktree 5개 생성 완료"
echo "   wt-backend:  FastAPI, Docker, DB 스키마"
echo "   wt-graph:    DozerDB, 온톨로지, Cypher"
echo "   wt-rag:      ApeRAG, 벡터 인덱스"
echo "   wt-agent:    SEOCHO Router, LangGraph"
echo "   wt-analysis: 평가, BigQuery, 로그 분석"
```

### 12.2 Worktree ↔ Agent Teams Teammate 매핑

| Worktree | Teammate | 담당 디렉토리 | 의존성 | 병렬 실행 |
|----------|----------|-------------|--------|----------|
| `wt-backend` | Backend Core | `src/api/`, `src/db/` | 없음 (선행) | ✅ 독립 |
| `wt-graph` | Graph Engine | `src/graph/`, `src/ontology/` | 없음 | ✅ 독립 |
| `wt-rag` | RAG Pipeline | `src/rag/`, `src/search/` | 없음 | ✅ 독립 |
| `wt-agent` | Agent Logic | `src/agents/`, `src/eval/` | Graph + RAG 완료 후 | ⚠️ addBlockedBy |
| `wt-analysis` | (수동/별도) | `analysis/`, `evaluation/` | 항상 사용 가능 | ✅ 독립 |

### 12.3 Worktree 충돌 방지 규칙

```yaml
# .claude/foundation/worktree-rules.md
rules:
  - "각 Teammate는 자신의 담당 디렉토리만 수정합니다"
  - "공유 파일(pyproject.toml, docker-compose.yaml)은 Backend Core Teammate만 수정합니다"
  - "API 인터페이스 변경 시 반드시 다른 Teammate에게 SendMessage로 알립니다"
  - "merge는 항상 main 방향으로, 순서는 backend → graph/rag → agent"
```

---

## 13. Plan Mode Cross-Review 패턴 (보강: Boris Cherny Tip #2)

> **신규 섹션 — Claude A 설계 → Claude B 검증 패턴으로 오버엔지니어링 방지**

### 13.1 Cross-Review 워크플로우

```
[Claude A: 설계자]                [Claude B: 검토자]
      │                                  │
      ├─ bkit PDCA로 PLAN.md 생성 ──────→│
      │                                  ├─ 오버엔지니어링 검토
      │                                  ├─ MVP 범위 초과 여부 확인
      │                                  ├─ 기존 PRD와의 정합성 확인
      │◀── 검토 의견 + 수정 제안 ────────┤
      │                                  │
      ├─ 수정 반영 후 DESIGN.md 생성 ──→│
      │                                  ├─ 구현 가능성 검증
      │                                  ├─ 성능 벤치마크 충족 확인
      │◀── 최종 승인 ───────────────────┤
```

### 13.2 Cross-Review 체크리스트

```markdown
## Cross-Review Checklist (Claude B 검토용)

### 오버엔지니어링 검증
- [ ] Phase 1 MVP에 불필요한 기능이 포함되어 있지 않은가?
- [ ] "데이터 플랫폼 사용자는 정확한 결과를 원한다" 원칙에 부합하는가?
- [ ] 복잡한 추상화 대신 직접적 구현이 가능한가?

### PRD 정합성 검증
- [ ] foundation/ 원칙(quality-gates.md, schema-enforcement.md)과 모순이 없는가?
- [ ] 품질 지표 수치가 PRD §4.8 통합 정의와 일치하는가?
- [ ] Agent Teams vs SEOCHO Agent 용어가 올바르게 사용되었는가?

### 구현 가능성 검증
- [ ] 외부 의존성(ApeRAG, DozerDB, Vanna) 버전 호환성이 확인되었는가?
- [ ] 성능 벤치마크(PRD §5.6) 충족이 가능한 설계인가?
- [ ] 에러 처리(PRD §5.5) 시나리오가 반영되었는가?

### 프론트엔드 품질 검증 (PRD §11 UI/UX Design System)
- [ ] PRD §11.1.2 안티패턴 위반 항목이 없는가? (네온컬러, 스피너전용 로딩, 임의 z-index 등)
- [ ] z-index가 모두 §11.2.6 토큰 변수(--z-base ~ --z-tooltip)를 참조하는가? (하드코딩 없음)
- [ ] 모든 UI 아이콘이 lucide-react SVG인가? (이모지 UI 사용 없음, §11.3.5)
- [ ] §11.9.2 차트 유형 선택 가이드에 따라 적절한 차트가 선택되었는가?
- [ ] §11.15 UI QA Pre-delivery 체크리스트 전체 항목 통과 확인
- [ ] 디자인 토큰이 §11.2.7 tokens.json과 동기화되어 있는가? (하드코딩 색상값 없음)
```

---

## 14. CLAUDE.md 자동 축적 패턴 (보강: Boris Cherny Tip #3 + Ecosystem Analysis §2)

> **신규 섹션 — 실수 발견 시 자동으로 규칙을 누적하는 패턴**

### 14.1 Guardian Hook + Auto-Accumulate

기존 §8.5 Guardian 패턴에 **자동 규칙 축적** 기능을 추가합니다:

```
[Teammate 작업 완료]
      │
      ├─ Guardian Hook 검증
      │     ├─ 통과 → 완료 처리
      │     └─ 실패 → 피드백 + 규칙 자동 기록
      │           │
      │           ▼
      │     [.claude/execution/known-issues.md에 추가]
      │     Format: [날짜] [Teammate] [실수 유형] [방지 규칙]
      │
      └─ 다음 세션에서 모든 Teammate가 known-issues.md 참조
```

### 14.2 초기 CLAUDE.md 규칙 (DataNexus 전용)

<!-- SSOT: 정식 버전은 CLAUDE_md_Template.md 참조. 본 섹션은 전략적 맥락만 기술 -->

```markdown
# .claude/rules/datanexus.md

## 온톨로지 규칙
- Glossary Term 이름은 반드시 한글 우선, 영문은 동의어로 등록
- 동의어 배열은 알파벳/가나다 순으로 정렬
- formula 필드에는 반드시 계산식을 포함 (파생 지표인 경우)

## 금지 테이블 목록
- SYSTEM_*, AUDIT_LOG*, _TEMP_* 테이블은 NL2SQL에서 접근 금지
- ROW_LEVEL_SECURITY가 설정된 테이블은 반드시 사용자 컨텍스트 주입 후 쿼리

## 코드 규칙
- Python 버전: 3.11+
- 모든 API 엔드포인트에 Pydantic V2 스키마 필수
- SQL 문자열은 반드시 파라미터 바인딩 사용 (SQL Injection 방지)
- Cypher 쿼리는 .cypher 파일로 관리 (인라인 금지)

## Agent 규칙
- Router Agent는 직접 DB 접근 불가 (분류만 담당)
- Graph DBA Agent의 Cypher에 DELETE/DROP 포함 불가
- Supervisor는 ConflictResolutionScore < 0.5일 때 가장 높은 HoT 소스만 사용

## 프론트엔드 규칙 (PRD §11 UI/UX Design System)
- 이모지를 UI 아이콘으로 사용 금지 → lucide-react SVG만 허용 (§11.3.5)
- z-index 하드코딩 금지 → --z-base ~ --z-tooltip 토큰 변수만 사용 (§11.2.6)
- 색상 하드코딩 금지 → CSS 변수(--color-*) 또는 Tailwind 클래스만 사용 (§11.2.7)
- 데이터 로딩 시 Spinner 금지 → 반드시 Skeleton UI 사용 (§11.3.3)
- 기능적 전환 외 장식적 애니메이션 금지, 최대 400ms (--duration-slow)
- 네온/형광/AI퍼플 컬러 사용 금지 → Deep Slate + Sapphire Blue 팔레트만 허용 (§11.1.2)
- 모든 클릭 가능 요소에 cursor: pointer + hover 전환(150-300ms) 필수 (§11.15)
- 차트 생성 시 §11.9.2 차트 유형 선택 가이드의 의사결정 트리 준수
```

---

## 15. 외부 컨텍스트 자동 주입 & 런타임 QA 통합 (보강: Addy Osmani Workflow 2026)

> **신규 섹션 — Context7 MCP로 외부 라이브러리 문서 자동 주입 + Chrome DevTools MCP로 런타임 UI QA 자동화**
>
> **출처:** [Addy Osmani, "My LLM coding workflow going into 2026"](https://addyosmani.com/blog/ai-coding-workflow/)
>
> Addy의 핵심 원칙: "AI에게 부분 정보로 작업시키지 마라(Don't make the AI operate on partial information)" + "에이전트에게 눈을 줘라(Give your agent eyes)"

> **📌 Phase 안내:** §15.1~15.4는 모두 **Phase 2 이후** 도입을 전제로 합니다. MVP(Phase 0.5~1.0) 단계에서는 참조만 하고, 실제 적용은 Phase 2 로드맵에서 우선순위를 재평가한 후 진행하세요. §15.4의 영향 분석 표를 함께 참조하시기 바랍니다.

### 15.1 Context7 MCP — 외부 라이브러리 문서 자동 주입

**문제:** DataNexus의 핵심 의존성(ApeRAG, DozerDB, Vanna 2.0)은 문서가 빈약하거나 빠르게 변경됩니다. 현재 `.claude/domains/` 파일은 **내부 규칙**에 집중하며, 외부 API 문서는 수동으로 붙여넣기해야 합니다. Addy가 강조하는 "context packing"의 핵심 누락 지점입니다.

**해결:** Context7 MCP(https://context7.com/)를 통합하여 세션 시작 시 외부 라이브러리의 최신 문서를 자동 주입합니다.

#### 15.1.1 MCP 설정 추가

```json
// datanexus-connectors.mcp.json에 추가 (§11.3 기존 MCP 설정 확장)
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"],
      "description": "외부 라이브러리 최신 문서 자동 주입"
    }
  }
}
```

#### 15.1.2 Teammate별 외부 문서 주입 매핑

| Teammate | 자동 주입 대상 | Context7 쿼리 예시 |
|----------|---------------|-------------------|
| **Graph Engine** | DozerDB API, Neo4j Cypher Reference | `resolve dozerdb` → Cypher 문법, Multi-DB API |
| **RAG Pipeline** | ApeRAG API, Qdrant Client Reference | `resolve aperag` → Knowledge Base API, Indexing |
| **Backend Core** | Vanna 2.0 Agent API, FastAPI Reference | `resolve vanna-ai` → Agent-based API, Training |
| **Agent Logic** | LangGraph Reference, Opik Tracing API | `resolve langgraph` → State Graph, Checkpointing |

#### 15.1.3 세션 시작 시 자동 주입 프롬프트

```markdown
# .claude/domains/에 추가할 주입 규칙 예시 (ontology-engine.md)

## 외부 문서 참조 (Context7 자동 주입)
- 세션 시작 시: `use context7` → `resolve dozerdb` 실행
- DozerDB Multi-DB API 변경사항 자동 반영
- Neo4j Cypher Reference 최신 버전 참조
- 문서 버전 불일치 발견 시 execution/known-issues.md에 기록
```

#### 15.1.4 기존 컨텍스트 구조와의 통합

```
.claude/
├── foundation/          ← 불변 원칙 (기존 유지)
├── domains/             ← 내부 규칙 + 외부 문서 참조 규칙 (확장)
│   ├── ontology-engine.md    ← + DozerDB 외부 문서 참조 규칙 추가
│   ├── nl2sql-pipeline.md    ← + Vanna 2.0 외부 문서 참조 규칙 추가
│   ├── rag-search.md         ← + ApeRAG 외부 문서 참조 규칙 추가
│   └── agent-routing.md      ← + LangGraph 외부 문서 참조 규칙 추가
├── execution/           ← 런타임 축적 (기존 유지)
└── external-docs/       ← ★ 신규: Context7 캐시 스냅샷 (선택)
    ├── dozerdb-snapshot.md   ← 주간 갱신, 오프라인 참조용
    └── vanna2-snapshot.md    ← 주간 갱신, 오프라인 참조용
```

> **💡 TIP:** Context7은 실시간 문서 조회이므로 네트워크 의존성이 있습니다. 기업 네트워크 제한 환경을 대비하여 `external-docs/` 디렉토리에 주간 스냅샷을 저장하는 것을 권장합니다.

---

### 15.2 Chrome DevTools MCP — 런타임 UI QA 자동화

**문제:** 현재 PRD §11.15 QA 체크리스트의 상당 항목(I-1 cursor 검사, A-1/A-2 색상 대비, R-1~R-4 반응형, S-1~S-4 데이터 상태)은 **수동 확인** 또는 **정적 분석(ESLint)**에 의존합니다. AI 에이전트가 실제 브라우저에서 DOM, 콘솔 에러, 네트워크 요청, 성능 트레이스를 직접 확인할 수 없어 런타임 버그를 잡지 못합니다.

**해결:** Chrome DevTools MCP(https://github.com/anthropics/anthropic-quickstarts/tree/main/chrome-devtools-mcp-server)를 Phase 2 UI QA 파이프라인에 통합합니다. Addy Osmani의 이전 팀(Google Chrome DevTools)에서 만든 도구로, "에이전트에게 눈을 준다(gives your agent eyes)".

#### 15.2.1 MCP 설정

```json
// datanexus-connectors.mcp.json에 추가
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/chrome-devtools-mcp-server"],
      "env": {
        "CHROME_REMOTE_DEBUGGING_PORT": "9222"
      },
      "description": "런타임 UI QA - DOM 검사, 콘솔 로그, 네트워크, 성능 트레이스"
    }
  }
}
```

#### 15.2.2 자동 검증 가능한 QA 항목 매핑

PRD §11.15 체크리스트 중 Chrome DevTools MCP로 자동화 가능한 항목:

| QA 항목 | 현재 확인 방법 | DevTools MCP 자동화 |
|---------|---------------|-------------------|
| I-1 `cursor: pointer` | 수동 DevTools 검사 | ✅ DOM 쿼리로 전체 클릭 요소 자동 검증 |
| A-1/A-2 색상 대비 | axe DevTools 수동 실행 | ✅ Accessibility audit 자동 트리거 |
| R-1~R-4 반응형 | 수동 브라우저 리사이즈 | ✅ Device emulation으로 4개 뷰포트 자동 순회 |
| S-1 Loading 상태 | API 지연 시뮬레이션 | ✅ Network throttling + DOM 스냅샷 |
| S-3 Error 상태 | API 에러 시뮬레이션 | ✅ Network intercept로 에러 응답 강제 |
| P-1 Skeleton UI | 네트워크 throttling | ✅ Slow 3G 모드에서 Skeleton 렌더 확인 |
| 콘솔 에러 | 수동 확인 | ✅ Console API로 에러/경고 자동 수집 |
| 성능 트레이스 | Lighthouse 수동 실행 | ✅ Performance.mark 기반 자동 프로파일링 |

#### 15.2.3 Agent Teams UI QA 워크플로우

```
[FE Teammate: 컴포넌트 구현 완료]
      │
      ├─ ESLint 커스텀 규칙 자동 실행 (정적 분석, 기존)
      │     ├─ z-index 하드코딩 검출
      │     ├─ 이모지 아이콘 검출
      │     └─ 색상 하드코딩 검출
      │
      ├─ Chrome DevTools MCP 자동 실행 (런타임 분석, ★ 신규)
      │     ├─ 1. 페이지 로드 → 콘솔 에러 0개 확인
      │     ├─ 2. Accessibility audit → WCAG AA 위반 0개 확인
      │     ├─ 3. 4개 뷰포트 순회 → 레이아웃 깨짐 0건
      │     ├─ 4. Network throttling → Skeleton UI 렌더 확인
      │     └─ 5. 성능 프로파일 → First Contentful Paint ≤ 2s
      │
      └─ Guardian Hook 통합 검증
            ├─ 정적 + 런타임 모두 통과 → 완료 처리
            └─ 실패 → known-issues.md 기록 + FE Teammate에 피드백
```

#### 15.2.4 도입 타이밍 및 Phase 매핑

| Phase | 적용 범위 | 비고 |
|-------|----------|------|
| Phase 1 (현재) | 미적용 | 백엔드 중심 개발, UI 없음 |
| **Phase 2 (UI 개발)** | **Agent Studio UI + Design System QA** | ★ 도입 시점 |
| Phase 3+ | 고급 시각화 대시보드 QA | 차트/그래프 렌더링 검증 확장 |

> **⚠️ WARNING:** Chrome DevTools MCP는 Chrome 브라우저가 `--remote-debugging-port=9222`로 실행되어야 합니다. CI/CD 환경에서는 Headless Chrome + Puppeteer로 구성합니다.

---

### 15.3 성능 안티패턴 — domains/ 규칙 파일 확장

**문제:** 현재 `.claude/domains/` 파일은 "해야 할 것(Do)"에 집중하며, Addy가 강조하는 "which naive solutions are too slow" 같은 **"하지 말아야 할 것(Don't)" 패턴**이 명시적으로 기술되어 있지 않습니다. AI 에이전트는 금지 패턴이 명시되지 않으면 성능 문제가 있는 naive 접근을 선택할 가능성이 높습니다.

**해결:** 각 domains/ 규칙 파일에 `## 성능 안티패턴 (절대 하지 말 것)` 섹션을 추가합니다.

#### 15.3.1 도메인별 안티패턴 정의

**ontology-engine.md 추가 내용:**
```markdown
## 성능 안티패턴 (절대 하지 말 것)
- ❌ OPTIONAL MATCH 3중 이상 중첩 → P95 타임아웃 유발, 최대 2중까지만 허용
- ❌ MATCH (n) 전체 노드 스캔 → 반드시 레이블 + 인덱스 조건 명시
- ❌ DozerDB 트랜잭션 안에서 LLM 호출 → 트랜잭션 타임아웃, LLM 호출은 트랜잭션 외부에서
- ❌ 단일 Cypher에 UNWIND 10,000+ 행 → 배치 처리 1,000행 단위로 분할
- ❌ Multi-DB 간 Cross-database 쿼리 시도 → DozerDB는 Fabric 미지원, 애플리케이션 레벨에서 조인
```

**nl2sql-pipeline.md 추가 내용:**
```markdown
## 성능 안티패턴 (절대 하지 말 것)
- ❌ Vanna training 시 DDL 전체를 한번에 주입 → 토큰 낭비, 테이블별 분할 학습 필수
- ❌ SELECT * 생성 → 명시적 컬럼 지정 필수 (이미 금지 패턴이나 재강조)
- ❌ 서브쿼리 3단계 이상 중첩 → CTE(WITH 절)로 변환
- ❌ GROUP BY 없이 집계 함수 + 일반 컬럼 혼용 → SQL 에러 또는 잘못된 결과
- ❌ LIKE '%keyword%' 패턴 (leading wildcard) → Full-Text Index 또는 정확한 조건으로 대체
- ❌ 생성된 SQL에 LIMIT 없는 대용량 테이블 쿼리 → 기본 LIMIT 1000 강제 적용
```

**rag-search.md 추가 내용:**
```markdown
## 성능 안티패턴 (절대 하지 말 것)
- ❌ Qdrant 벡터 검색 시 limit 없는 전체 스캔 → OOM 위험, 반드시 Top-K 지정
- ❌ ApeRAG Knowledge Base 동기화 중 실시간 쿼리 병행 → 동기화 락 충돌, 비동기 큐 분리
- ❌ Chunk size 2048+ tokens → 검색 정밀도 급락, 512 tokens 유지 (overlap 64)
- ❌ Reranking 없이 벡터 유사도만으로 최종 결과 반환 → 반드시 Cross-Encoder reranking 적용
- ❌ 임베딩 모델 호출을 동기 루프 안에서 실행 → asyncio.gather로 배치 임베딩
```

**agent-routing.md 추가 내용:**
```markdown
## 성능 안티패턴 (절대 하지 말 것)
- ❌ Router가 모든 Agent를 순차 호출 후 최적 결과 선택 → 분류 후 단일 Agent만 호출
- ❌ Supervisor의 HoT 충돌 해결에서 모든 소스 재쿼리 → 캐시된 결과로 비교, 재쿼리 금지
- ❌ Agent 간 메시지에 전체 데이터셋 포함 → 요약/참조 ID만 전달, 데이터는 공유 캐시에서 조회
- ❌ Fallback 루프에서 동일 프롬프트 재시도 → 반드시 프롬프트 변형 (rephrasing) 후 재시도
- ❌ Opik Trace에 응답 전체 텍스트 기록 → 메타데이터만 기록, 응답 본문은 별도 스토리지
```

#### 15.3.2 Guardian Hook 확장

성능 안티패턴 검증을 Guardian Hook에 추가합니다:

```
# Guardian Hook 검증 항목 추가 (§8.5 확장)

기존 검증:
  1. SchemaEnforcer 규칙 위반
  2. Quality Gate 임계값 충족
  3. HoT 충돌 해결 정합성
  4. 프론트엔드 규칙 준수

★ 추가 검증:
  5. 성능 안티패턴 위반 (domains/ 안티패턴 섹션 참조)
     - Cypher 쿼리: OPTIONAL MATCH 중첩 깊이 검사
     - SQL 생성: SELECT *, LIMIT 누락, 서브쿼리 깊이 검사
     - 벡터 검색: limit 파라미터 존재 여부 검사
     - Agent 호출: 순차 호출 패턴 감지
```

---

### 15.4 §15 도입 시 영향 분석

| 변경 사항 | 영향 범위 | 리스크 | 대응 |
|----------|----------|--------|------|
| Context7 MCP 추가 | §11.3 MCP 설정 파일 | 네트워크 의존성 | external-docs/ 오프라인 캐시 |
| Chrome DevTools MCP 추가 | Phase 2 QA 파이프라인 | Chrome 실행 필요 | CI에서 Headless Chrome 사용 |
| 성능 안티패턴 추가 | domains/ 4개 파일 | Guardian Hook 검증 부하 증가 | 정적 분석(grep 기반)으로 경량 검증 |
| external-docs/ 디렉토리 추가 | .claude/ 구조 확장 | 캐시 크기 관리 | 주간 갱신 + 100KB 이하 유지 |

---

## 16. 에이전트 세션 컨텍스트 보존 전략 (보강: OpenClaw 코드 분석)

> **신규 섹션 — OpenClaw 컨텍스트 보존 8가지 기법의 DataNexus 적응**
> Reference: https://codepointerko.substack.com/p/openclaw-ai-8
> 기술 상세: PRD_04c §4.3.10.10

### 16.1 개요

OpenClaw는 장시간 AI 에이전트 세션에서 "절대 잊지 않는" 메모리를 구현하기 위해 8가지 기법을 사용합니다. 컨텍스트를 단순한 텍스트가 아닌 핵심 자원으로 관리하며, 예방→보존→적응→최적화→견고성의 5계층 방어선을 형성합니다. 이를 DataNexus SEOCHO Agent 아키텍처에 적응시킵니다.

### 16.2 구현 우선순위

| 우선순위 | 기법 | Phase | 사유 | 예상 공수 |
|---------|------|-------|------|----------|
| **P0** | 컨텍스트 윈도우 가드 | Phase 1 (MVP) | 에이전트 안정성 기본 요소 | 2 M/D |
| **P0** | 도구 결과 가드 | Phase 1 (MVP) | 다중 에이전트 트랜스크립트 무결성 | 3 M/D |
| **P1** | 턴 기반 히스토리 제한 | Phase 2 | 장시간 분석 세션 지원 | 2 M/D |
| **P1** | 앞/뒤 콘텐츠 보존 | Phase 2 | 도구 결과 프루닝 품질 향상 | 3 M/D |
| **P1** | 캐시 인식 프루닝 | Phase 2 | 비용 최적화 핵심 (~80% 절감 추정) | 5 M/D |
| **P2** | 컴팩션 전 Graphiti 플러시 | Phase 3 | Graphiti 의존 | 5 M/D |
| **P2** | 적응형 청크 비율 | Phase 3 | 컴팩션 시스템 의존 | 3 M/D |
| **P2** | 단계적 요약 | Phase 3 | 컴팩션 시스템 의존 | 4 M/D |

**총 예상 공수:** 27 M/D (Phase 1: 5 M/D, Phase 2: 10 M/D, Phase 3: 12 M/D)

### 16.3 Phase 1 MVP 즉시 적용

Phase 1 MVP에서 컨텍스트 윈도우 가드와 도구 결과 가드를 기존 §3.6.2 `agent_permissions.yaml`과 연계하여 적용합니다.

```python
# router_agent.py — Phase 1 가드 등록
class SEOCHORouterAgent:
    def __init__(self, model_config):
        self.ctx_guard = ContextWindowGuard()  # 32K 하드 최소값
        self.ctx_guard.validate(model_config.context_tokens)
        self.tool_guard = ToolResultGuard(self.session_manager)
```

### 16.4 Agent Teams Teammate 매핑

| Teammate | 구현 대상 | Phase |
|---------|----------|-------|
| Agent Logic | 컨텍스트 윈도우 가드, 도구 결과 가드, 턴 기반 제한 | Phase 1-2 |
| Backend Core | 캐시 인식 프루닝, 앞/뒤 콘텐츠 보존 | Phase 2 |
| Graph Engine | Graphiti 메모리 플러시, 역할별 플러시 차별화 | Phase 3 |
| RAG Pipeline | 적응형 청크 비율, 단계적 요약 | Phase 3 |

### 16.5 방어선 전략 연계 (PRD_01 §1)

| 방어선 요소 | 컨텍스트 보존 기여 |
|-----------|------------------|
| 역할별 해석 차이 (5개 페르소나) | 역할별 메모리 플러시 차별화로 페르소나별 맥락 축적 가속 |
| 시간축 지식 그래프 (Graphiti) | 컴팩션 전 Graphiti 플러시로 세션 내 발견 사실의 영구 보존 |
| 비공개 운영 데이터 (DozerDB 격리) | 캐시 인식 프루닝으로 테넌트별 DDL/온톨로지 효율적 관리 |

### 16.6 §16 도입 시 영향 분석

| 추가 항목 | 영향받는 기존 섹션 | 리스크 | 대응 |
|----------|----------------|-------|------|
| 컨텍스트 윈도우 가드 | §3.6.2 agent_permissions.yaml | 모델 변경 시 임계값 재조정 | Claude Max 기준 200K 여유 |
| 도구 결과 가드 | §3.5 SEOCHO Agent 전체 | 합성 결과가 모델 혼란 유발 | 에러 메시지 명확화 |
| 캐시 인식 프루닝 | §15.1 Context7 MCP | 캐시 무효화 시점 오판 | 보수적 TTL (5분) 적용 |
| Graphiti 플러시 | §4.3.10.3 에피소드 축적 | 플러시 지연으로 체감 속도 저하 | 비동기 실행 + 3초 타임아웃 |

### 16.7 Vanna Tool Memory ↔ Graphiti 이중 메모리 구현 가이드 (v1.3 신규)

> **신규 섹션 — PRD_04c §4.3.10.10.8 구체화**
> Phase 3에서 Graphiti 메모리 플러시(§4.3.10.10.6)와 Vanna Tool Memory가 동시에 활성화될 때의 경계 관리 전략

#### 16.7.1 문제 정의

Vanna 2.0은 성공한 질문-SQL 쌍을 Qdrant 벡터스토어에 자동 학습(Tool Memory)합니다. Graphiti 메모리 플러시는 대화 중 발견된 사실·패턴을 시간축 지식그래프에 커밋합니다. **동일 정보가 두 저장소에 중복 축적되면:**

1. 스토리지 낭비 (Qdrant + Neo4j 양쪽에 유사 데이터)
2. 일관성 위험 (한쪽만 업데이트 시 정보 불일치)
3. 검색 노이즈 (유사도 검색 시 중복 결과로 Few-shot 품질 저하)

#### 16.7.2 구현 우선순위

| 우선순위 | 구현 항목 | Phase | Teammate | 예상 공수 |
|---------|---------|-------|---------|----------|
| **P0** | DualMemoryRouter 클래스 | Phase 3 | Backend Core | 3 M/D |
| **P0** | Vanna Training 테넌트 파티션 격리 | Phase 3 | Backend Core | 2 M/D |
| **P1** | 일관성 검증 배치 작업 | Phase 3 | Graph Engine | 3 M/D |
| **P1** | 역할별 메모리 라우팅 설정 | Phase 3 | Agent Logic | 2 M/D |
| **P2** | 이중 메모리 모니터링 대시보드 | Phase 3+ | Frontend | 2 M/D |

**총 예상 공수:** 12 M/D (§16.2의 Phase 3 기존 12 M/D에 추가 → Phase 3 합계 24 M/D)

#### 16.7.3 핵심 구현 패턴

```python
# dual_memory_router.py — DualMemoryRouter 핵심 로직
from enum import Enum
from dataclasses import dataclass

class MemoryDestination(Enum):
    VANNA_ONLY = "vanna"       # Qdrant 벡터스토어
    GRAPHITI_ONLY = "graphiti" # Neo4j 시간축 그래프
    SPLIT = "split"            # SQL → Vanna, 맥락 → Graphiti

@dataclass
class MemoryItem:
    type: str          # sql_execution | business_fact | sql_with_context | user_preference
    content: dict
    persona: str       # CMO | CFO | Analyst | PM | Ops
    tenant_id: str

class DualMemoryRouter:
    """§4.3.10.10.8.2 분류 규칙 구현"""
    
    ROUTING_RULES = {
        "sql_execution": MemoryDestination.VANNA_ONLY,
        "business_fact": MemoryDestination.GRAPHITI_ONLY,
        "interpretation_pattern": MemoryDestination.GRAPHITI_ONLY,
        "kpi_definition_change": MemoryDestination.GRAPHITI_ONLY,
        "sql_with_context": MemoryDestination.SPLIT,
        "user_preference": MemoryDestination.GRAPHITI_ONLY,
    }
    
    def route(self, item: MemoryItem) -> MemoryDestination:
        return self.ROUTING_RULES.get(
            item.type, MemoryDestination.GRAPHITI_ONLY
        )
    
    def split_item(self, item: MemoryItem) -> tuple:
        """SPLIT 대상 항목을 Vanna/Graphiti용으로 분리"""
        vanna_part = {
            "question": item.content["question"],
            "sql": item.content["sql"],
            "tenant_id": item.tenant_id,
        }
        graphiti_part = {
            "business_context": item.content.get("context", ""),
            "interpretation": item.content.get("interpretation", ""),
            "persona": item.persona,
            "source_description": "memory_flush_pre_compaction",
        }
        return vanna_part, graphiti_part
```

#### 16.7.4 §16.2 기존 공수표 업데이트

| 기존 Phase 3 항목 | 기존 공수 | 변경 사항 |
|-----------------|----------|----------|
| Graphiti 메모리 플러시 | 5 M/D | 유지 (DualMemoryRouter 연동만 추가) |
| 적응형 청크 비율 | 3 M/D | 유지 |
| 단계적 요약 | 4 M/D | 유지 |
| **이중 메모리 경계 관리 (신규)** | **12 M/D** | **§4.3.10.10.8 전체** |
| **Phase 3 합계** | **24 M/D** | **기존 12 + 신규 12** |

#### 16.7.5 §16.6 영향 분석 추가

| 추가 항목 | 영향받는 기존 섹션 | 리스크 | 대응 |
|----------|----------------|-------|------|
| DualMemoryRouter | §4.3.10.10.6 메모리 플러시 | 분류 오류 시 메모리 누락 | 기본값 GRAPHITI_ONLY (안전한 방향) |
| Vanna 테넌트 파티션 | Appendix B.8 Vanna 통합 | Qdrant 컬렉션 수 증가 | 테넌트당 1 컬렉션, 인덱스 최적화 |
| 일관성 검증 배치 | §4.3.5 품질 검증 파이프라인 | DataHub 스키마 변경 시 대량 무효화 | 증분 검증 (변경된 테이블만) |

---

## 17. 개발 환경 보안 및 효율성 강화 (보강: Claude Code 70 Tips 분석)

> **출처:** "Claude Code 완전 가이드: 70가지 파워 팁" (ykdojo + Ado Kukic) 분석 결과, DataNexus 프로젝트에 추가 채택 가치가 있는 3개 항목을 선별 도입합니다.
> **관련 PRD:** §6.5 FR-OPS-06, FR-OPS-07, FR-OPS-08

### 17.1 cc-safe 명령어 감사 (Command Audit)

**배경:** Claude Code의 `.claude/settings.json`에 승인된 명령어가 누적되면, `rm -rf`, `sudo`, `curl | sh` 같은 위험 패턴이 포함될 수 있습니다. 실제로 한 사용자가 `rm -rf tests/ patches/ plan/ ~/`를 승인하여 홈 디렉토리를 삭제한 사례가 보고되었습니다.

**DataNexus 적용 전략:**

DataNexus의 Guardian Hook 시스템은 **런타임** 시점의 위험 명령어를 차단하지만, cc-safe는 **사전 감사** 차원에서 이미 승인된 명령어 목록을 스캔합니다. 두 체계는 보완적으로 작동합니다:

```
┌─────────────────────────────────────────────────────────┐
│ 개발 환경 보안 2중 방어선                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [사전 감사] cc-safe                                     │
│  ─────────────────────────────────                      │
│  • .claude/settings.json 스캔                           │
│  • 위험 패턴 감지 및 리포트                              │
│  • 주기: 월 1회 + --dangerously-skip-permissions 후     │
│  • CI/CD Quality Gate 통합                              │
│        ↓                                                │
│  [런타임 차단] Guardian Hook (§8.5)                      │
│  ─────────────────────────────────                      │
│  • PreToolUse Hook으로 실행 시점 차단                    │
│  • Graph DBA Agent DELETE/DROP 금지                     │
│  • TaskCompleted 시 자동 검증                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**CI/CD 통합:**

```yaml
# .github/workflows/claude-audit.yml (§5.3.5 기존 파이프라인에 추가)
  cc-safe-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install cc-safe
        run: npm install -g cc-safe
      - name: Audit approved commands
        run: |
          npx cc-safe . --json > cc-safe-report.json
          RISKY_COUNT=$(jq '.risks | length' cc-safe-report.json)
          if [ "$RISKY_COUNT" -gt 0 ]; then
            echo "⚠️ Found $RISKY_COUNT risky approved commands"
            cat cc-safe-report.json
            exit 1
          fi
```

**도입 시점:** Phase 1.0 (MVP와 동시, 개발 환경 구축 단계)
**예상 공수:** 0.5 M/D (CI/CD 연동 포함)
**산출물:** `execution/cc-safe-audit.md` 월간 감사 기록

### 17.2 /context 컨텍스트 윈도우 모니터링

**배경:** Claude Code의 200K 토큰 컨텍스트 윈도우는 시스템 프롬프트, MCP 서버, CLAUDE.md, 대화 기록으로 채워집니다. DataNexus처럼 Context7 MCP, Chrome DevTools MCP 등 다수의 MCP를 활용하는 프로젝트에서는 MCP 서버만으로 전체의 18%를 점유할 수 있어, 세션 효율성이 급격히 저하됩니다.

**DataNexus 기준선:**

| 항목 | 권장 범위 | 경고 임계값 | 조치 |
|------|-----------|------------|------|
| 활성 MCP 서버 | 10개 이하 | 10개 초과 | `/mcp`로 비활성화 |
| 활성 도구 | 80개 이하 | 80개 초과 | 미사용 MCP 제거 |
| 컨텍스트 사용률 | 70% 이하 | 70% 초과 | HANDOFF.md 생성 + `/clear` |
| 단일 MCP 점유율 | 20% 이하 | 20% 초과 | 해당 MCP 비활성화 검토 |
| 시스템 프롬프트 비율 | 15% 이하 | 15% 초과 | CLAUDE.md 간소화 |

**Context-as-Code와의 연계:**

DataNexus의 3-tier Context-as-Code(`foundation/domains/execution/`) 구조는 ISP 원칙에 따라 Teammate별 필요한 정보만 선택 로딩하므로, CLAUDE.md 토큰 점유율을 낮게 유지합니다. /context 모니터링은 이 구조의 효과를 정량적으로 검증하는 역할도 합니다.

**도입 시점:** Phase 1.0 (세션 시작 시 자동 점검 루틴으로)
**예상 공수:** 0.5 M/D (모니터링 기준선 설정 + 기록 템플릿)
**산출물:** `execution/context-monitor.md` 모니터링 기록

### 17.3 장시간 작업 지수 백오프 전략

**배경:** DataNexus의 데이터 파이프라인 작업(DataHub에서 Vanna 동기화, ApeRAG Knowledge Base 재색인, 대용량 CSV ETL 등)은 수분에서 수십 분이 소요됩니다. 매 초마다 상태를 확인하면 토큰이 낭비되고, Agent Teams의 병렬 실행 효율이 저하됩니다.

**지수 백오프 적용 대상:**

| 작업 유형 | 예상 소요 시간 | 백오프 시작 간격 | 최대 간격 |
|----------|--------------|----------------|----------|
| DataHub Ingestion | 5-15분 | 1분 | 8분 |
| Vanna Training (DDL 학습) | 3-10분 | 1분 | 4분 |
| ApeRAG KB 재색인 | 10-30분 | 2분 | 16분 |
| DozerDB 대량 Import | 5-20분 | 1분 | 8분 |
| 전체 통합 테스트 (E2E) | 10-30분 | 2분 | 16분 |

**Agent Teams 연계:**

Agent Teams에서 Team Lead가 Backend Core에 "Vanna DDL 학습 실행"을 지시하면, Backend Core는 Ctrl+B로 백그라운드 전환 후 지수 백오프로 상태를 확인합니다. 동시에 Graph Engine과 RAG Pipeline은 독립 작업을 병렬 진행합니다. 백오프 간격 동안 절약된 토큰은 다른 Teammate의 작업에 활용됩니다.

**도입 시점:** Phase 2.0 (자동화 고도화 단계)
**예상 공수:** 1 M/D (프롬프트 패턴 정립 + Agent Teams 연동)
**산출물:** 장시간 작업 지수 백오프 프롬프트 템플릿 (`.claude/commands/`)

### 17.4 도입 시 영향 분석

| 추가 항목 | 영향받는 기존 섹션 | 리스크 | 대응 |
|----------|----------------|-------|------|
| cc-safe CI/CD 통합 | §5.3.5 테스트 파이프라인 | cc-safe npm 패키지 의존성 | 버전 고정 + 대체 수단(수동 grep) 준비 |
| /context 모니터링 | §8.5 Guardian Pattern | 세션 시작 지연 (1-2초) | 수동 실행으로 시작, Phase 2에서 자동화 |
| 지수 백오프 | §6 Agent Teams Guide | Teammate 간 동기화 타이밍 이슈 | PROGRESS.md 갱신으로 상태 공유 |
| 전체 토큰 영향 | §14 CLAUDE.md 축적 | execution/ 파일 2개 추가 (약 200 토큰) | 미미한 영향, 기준선 이내 |

### 17.5 공수 요약

| 항목 | Phase | 담당 | 공수 |
|------|-------|------|------|
| cc-safe CI/CD 통합 | Phase 1.0 | Backend Core | 0.5 M/D |
| /context 모니터링 기준선 | Phase 1.0 | Team Lead | 0.5 M/D |
| 지수 백오프 자동화 | Phase 2.0 | Team Lead | 1 M/D |

**총 예상 공수:** 2 M/D
