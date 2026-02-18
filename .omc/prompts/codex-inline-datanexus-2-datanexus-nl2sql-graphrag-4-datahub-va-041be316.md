DataNexus 블로그 포스트 2편의 아키텍처를 리뷰해줘.

DataNexus는 온톨로지 기반 NL2SQL + GraphRAG 데이터 에이전트 플랫폼이다.
4개의 오픈소스를 조합해서 만든다: DataHub + Vanna 2.0 + ApeRAG + DozerDB

리뷰 관점:
1. 이 4개 컴포넌트 조합의 아키텍처적 강점과 약점
2. 컴포넌트 간 연결 구조 (DataHub MCL → DozerDB 동기화 → Vanna RAG Store 갱신 → ApeRAG Taxonomy 참조)의 건전성
3. 멀티테넌시 전략 (DozerDB Multi-DB 기반 격리)의 적절성
4. 잠재적 아키텍처 리스크나 병목 지점
5. 개선 제안

블로그 포스트 원문을 context_files로 첨부한다.