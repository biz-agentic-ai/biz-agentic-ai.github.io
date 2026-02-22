---
title: "1. 메달리온 아키텍처 - 데이터를 세 겹으로 쌓는 이유"
date: 2026-02-22
draft: false
summary: "Bronze, Silver, Gold. 데이터를 레이어별로 나눠서 적재하면 뭐가 달라지는가. DuckDB와 dbt로 직접 구성해 본다."
categories: ["ETL 설계"]
tags: ["etl", "medallion-architecture", "duckdb", "dbt", "elt"]
series: ["etl-design-guide"]
series_order: 1
author: "Junho Lee"
ShowToc: true
---

{{< colab "https://colab.research.google.com/github/biz-agentic-ai/biz-agentic-ai.github.io/blob/main/notebooks/etl-001-medallion-architecture.ipynb" >}}

## 데이터 레이크가 늪이 되는 과정

데이터 레이크에 파일을 쏟아놓고 바로 분석하려는 팀이 있다. 처음엔 빠르다. CSV 올리고 SQL 한 줄이면 결과가 나온다.

3개월 지나면 상황이 달라진다. 누가 올린 파일인지 모른다. 원본인지 정제된 건지 구분이 안 된다. 같은 매출 테이블인데 부서마다 숫자가 다르다. 데이터 늪(data swamp)이라고 부르는 상태다.

원인은 단순하다. 원본과 가공물이 같은 공간에 섞여 있기 때문이다. 레이어를 나누면 이 문제가 풀린다.

## Bronze, Silver, Gold

메달리온 아키텍처는 데이터를 세 개의 레이어로 나눈다. Databricks가 이름을 붙여서 널리 퍼졌지만, 개념 자체는 전통 DW의 레이어드 접근과 같다.

```
소스 시스템 → [Bronze] → [Silver] → [Gold] → BI / 분석
               원본 적재    정제·표준화   비즈니스 집계
```

**Bronze** 는 원본 그대로다. 소스 시스템에서 가져온 데이터를 변환 없이 저장한다. CSV든 JSON이든 API 응답이든 있는 그대로. 데이터 계보(lineage)의 출발점이다. 여기서 뭔가를 바꾸면 원본을 잃는다.

**Silver** 는 정제와 표준화다. Bronze 데이터의 타입을 맞추고, 중복을 제거하고, 키를 통합한다. "분석에 쓸 수 있는 상태"로 만드는 레이어다. 비즈니스 로직은 아직 넣지 않는다.

**Gold** 는 비즈니스 관점의 집계다. 팩트 테이블, 차원 테이블, KPI 마트. 최종 사용자가 직접 쿼리하는 레이어다. [DW 모델링 1편]({{< ref "001-cloud-era-dw-modeling" >}})에서 다뤘던 스타스키마가 여기에 해당한다.

각 레이어의 역할이 명확하다는 게 핵심이다. Bronze에서는 절대 변환하지 않는다. Silver에서는 비즈니스 로직을 넣지 않는다. Gold에서만 비즈니스 관점의 가공이 들어간다. 이 규칙이 깨지면 레이어를 나눈 의미가 없다.

## 전통 DW 레이어와의 대응

[DW 모델링 시리즈]({{< ref "001-cloud-era-dw-modeling" >}})에서 `Raw → Staging → Integration → Mart` 구조를 다뤘다. 메달리온과 이름만 다르고 역할은 거의 같다.

| 메달리온 | 전통 DW | 하는 일 |
|---------|---------|--------|
| Bronze | Raw / Staging | 원본 적재, 변환 없음 |
| Silver | Integration (3NF / Data Vault) | 정제, 표준화, 키 통합 |
| Gold | Mart (Star Schema) | 비즈니스 집계, 분석용 |

전통 DW에서는 Staging과 Integration 사이에 ETL 서버가 무거운 변환을 처리했다. 메달리온은 ELT 패러다임이다. 일단 Bronze에 적재하고, DW 엔진 안에서 Silver와 Gold를 만든다. 변환을 별도 서버가 아니라 DW 엔진의 컴퓨팅 파워로 처리한다는 점이 다르다.

## 이 시리즈의 실습 환경

시리즈 전체에서 사용할 도구는 세 가지다. 전부 무료이고, Google Colab에서 클라우드 계정 없이 바로 돌릴 수 있다.

| 도구 | 역할 |
|------|------|
| DuckDB | 로컬 DW 엔진. Columnar Storage 기반이라 BigQuery/Snowflake와 같은 방식으로 동작한다 |
| dbt-core + dbt-duckdb | 변환 레이어. SQL로 Bronze → Silver → Gold를 정의한다 |
| Soda Core | 데이터 품질 검증. 레이어 간 품질 게이트를 건다 |

DuckDB를 고른 이유가 있다. 설치가 `pip install` 한 줄이면서, 실제 클라우드 DW와 동작 방식이 같다. Parquet, CSV를 네이티브로 읽고, SQL로 분석하고, Columnar Storage라 컬럼 기반 스캔이 된다. 로컬에서 돌리지만 클라우드 DW의 축소판이라고 보면 된다.

## 환경 세팅

Colab 셀에서 아래를 실행하면 준비 끝이다.

```python
# 도구 설치
!pip install -q duckdb dbt-core dbt-duckdb

import duckdb

# DuckDB 데이터베이스 생성
conn = duckdb.connect('warehouse.duckdb')
print(f"DuckDB {duckdb.__version__} 준비 완료")
```

## 샘플 데이터 준비

시리즈에서 사용할 샘플은 간단한 이커머스 데이터다. 주문, 고객, 상품 세 테이블. [DW 모델링 2편]({{< ref "002-oltp-vs-dw-model" >}})에서 다뤘던 구조와 같은 도메인이다.

```python
# Bronze 레이어: 원본 그대로 적재
conn.execute("""
CREATE SCHEMA IF NOT EXISTS bronze;

CREATE OR REPLACE TABLE bronze.orders AS
SELECT * FROM read_csv_auto('https://raw.githubusercontent.com/
  dbt-labs/jaffle_shop/main/seeds/raw_orders.csv');

CREATE OR REPLACE TABLE bronze.customers AS
SELECT * FROM read_csv_auto('https://raw.githubusercontent.com/
  dbt-labs/jaffle_shop/main/seeds/raw_customers.csv');

CREATE OR REPLACE TABLE bronze.payments AS
SELECT * FROM read_csv_auto('https://raw.githubusercontent.com/
  dbt-labs/jaffle_shop/main/seeds/raw_payments.csv');
""")

# 적재 확인
conn.execute("SELECT count(*) as cnt FROM bronze.orders").fetchdf()
```

Bronze에 적재했다. CSV를 읽어서 DuckDB에 넣었을 뿐, 어떤 변환도 하지 않았다. 타입 캐스팅도 안 했고, 컬럼명도 바꾸지 않았다. 이게 Bronze의 원칙이다.

```python
# Bronze 데이터 확인
conn.execute("SELECT * FROM bronze.orders LIMIT 5").fetchdf()
```

여기서 바로 분석 쿼리를 던지고 싶은 유혹이 생긴다. 참아야 한다. Bronze 데이터를 직접 분석에 쓰면 3개월 뒤에 데이터 늪에 빠진다. 다음 글에서 Bronze를 Silver로 올리는 과정을 다룬다.

## 왜 이렇게까지 나누는가

레이어를 나누면 느려지지 않냐는 질문을 받는다. 저장 공간도 더 쓰고, 변환 단계도 늘어나니까.

맞다. 대신 세 가지를 얻는다.

**재처리가 가능하다.** Silver 로직에 버그가 있으면 Bronze에서 다시 만들면 된다. 원본이 살아있으니까. Bronze 없이 Silver만 있으면 소스 시스템에서 다시 끌어와야 한다.

**문제 추적이 된다.** Gold의 숫자가 이상하면 Silver를 보고, Silver가 이상하면 Bronze를 본다. 어느 레이어에서 문제가 생겼는지 특정할 수 있다.

**역할이 분리된다.** 데이터 엔지니어는 Bronze→Silver를 책임지고, 분석 엔지니어는 Silver→Gold를 책임진다. 서로의 영역을 건드리지 않아도 된다.

클라우드 환경에서 스토리지 비용은 거의 무시할 수 있는 수준이다. 레이어를 하나 더 두는 비용보다, 데이터 늪에 빠졌을 때의 비용이 훨씬 크다.

다음 글에서는 Bronze 레이어를 본격적으로 다룬다. Full Load와 Incremental Load의 차이, 증분 적재의 기준 컬럼을 어떻게 잡는지.

{{< colab "https://colab.research.google.com/github/biz-agentic-ai/biz-agentic-ai.github.io/blob/main/notebooks/etl-001-medallion-architecture.ipynb" >}}
