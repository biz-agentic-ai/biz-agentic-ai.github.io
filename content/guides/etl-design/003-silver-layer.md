---
title: "3. Silver 레이어 - Bronze를 분석 가능한 상태로 올린다"
date: 2026-02-22T12:00:00+09:00
draft: false
summary: "Bronze에 쌓아둔 원본 데이터를 정제하고 표준화한다. 타입을 맞추고, 컬럼명을 통일하고, 중복을 제거한다. dbt로 이 과정을 SQL 모델로 정의한다."
categories: ["ETL 설계"]
tags: ["etl", "silver", "data-cleaning"]
series: ["etl-design-guide"]
series_order: 3
weight: 2
author: "Junho Lee"
ShowToc: true
---

{{< colab "https://colab.research.google.com/github/biz-agentic-ai/biz-agentic-ai.github.io/blob/main/notebooks/etl-003-silver-layer.ipynb" >}}

## Bronze 데이터를 바로 쓰면 생기는 일

[2편]({{< ref "002-bronze-layer" >}})에서 Bronze에 원본을 있는 그대로 적재했다. 변환 없이. 그 원칙은 맞다. 문제는 Bronze 데이터가 분석에 쓸 수 있는 상태가 아니라는 것이다.

jaffle_shop의 `bronze.orders`를 보자. `order_date` 컬럼이 VARCHAR로 들어와 있다. 날짜 함수를 쓸 수 없다. `status` 컬럼에는 `returned`, `return_pending`, `completed`, `placed`, `shipped`가 섞여 있는데, 어느 값이 최종 상태인지 스키마만 봐서는 모른다.

`bronze.payments`의 `amount` 컬럼은 센트 단위 정수다. 달러로 바꾸려면 100으로 나눠야 한다. 이걸 분석할 때마다 매번 나누는 건 실수를 부르는 구조다.

Silver는 이런 문제를 한 번에 정리하는 레이어다. 타입을 맞추고, 컬럼명을 통일하고, 단위를 변환한다. 비즈니스 로직은 아직 넣지 않는다. "분석에 쓸 수 있는 깨끗한 상태"를 만드는 게 Silver의 역할이다.

## Silver에서 하는 일, 안 하는 일

경계가 중요하다. Silver에서 비즈니스 로직을 넣기 시작하면 Bronze와 Silver를 나눈 의미가 사라진다.

**Silver에서 하는 일:**

- 타입 캐스팅 - VARCHAR를 DATE, INTEGER를 DECIMAL로
- 컬럼명 표준화 - `user_id`와 `userId`를 `user_id`로 통일
- 단위 변환 - 센트를 달러로, 밀리초를 초로
- 중복 제거 - 같은 레코드가 두 번 적재된 경우
- NULL 처리 - 빈 문자열을 NULL로 통일

**Silver에서 안 하는 일:**

- KPI 계산 - 매출, 마진율 같은 비즈니스 지표
- 테이블 조인 - 주문과 고객을 합쳐서 하나의 뷰로 만드는 것
- 집계 - GROUP BY로 요약하는 것

조인과 집계는 Gold의 몫이다. Silver는 개별 테이블 단위로 정제만 한다.

## dbt가 필요한 이유

[1편]({{< ref "001-medallion-architecture" >}})에서 dbt를 도구로 소개했다. 왜 SQL 파일을 직접 실행하지 않고 dbt를 쓰는가.

SQL 파일을 하나씩 실행하면 처음엔 문제가 없다. Silver 테이블이 5개, 10개로 늘어나면 상황이 달라진다. 어떤 테이블이 어떤 Bronze 테이블에 의존하는지, 어떤 순서로 실행해야 하는지, 마지막 실행이 언제인지 추적이 안 된다.

dbt는 이걸 해결한다. SQL 파일 하나가 하나의 모델이다. 모델 간 의존 관계를 `ref()` 함수로 선언하면 dbt가 실행 순서를 알아서 정한다. 변환 로직이 SQL 파일에 남으니 Git으로 이력 추적도 된다.

## dbt 프로젝트 세팅

Colab에서 dbt 프로젝트를 만든다.

```python
!pip install -q duckdb dbt-core dbt-duckdb

import os

# dbt 프로젝트 디렉토리 구조 생성
os.makedirs('jaffle_shop/models/staging', exist_ok=True)
os.makedirs('jaffle_shop/models/marts', exist_ok=True)
```

dbt 설정 파일을 만든다. DuckDB를 데이터베이스로 쓰도록 지정한다.

```python
%%writefile jaffle_shop/dbt_project.yml
name: 'jaffle_shop'
version: '1.0.0'
profile: 'jaffle_shop'

model-paths: ["models"]
```

```python
%%writefile jaffle_shop/profiles.yml
jaffle_shop:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: /content/warehouse.duckdb
```

## Silver 모델 작성

dbt에서는 `models/staging/` 디렉토리에 Silver 레이어 모델을 둔다. `stg_` 접두어가 staging(=Silver)을 뜻한다.

### stg_orders

```python
%%writefile jaffle_shop/models/staging/stg_orders.sql
with source as (
    select * from bronze.orders
),

cleaned as (
    select
        id as order_id,
        user_id as customer_id,
        cast(order_date as date) as order_date,
        status
    from source
)

select * from cleaned
```

Bronze의 `id`를 `order_id`로 바꿨다. 여러 테이블을 조인할 때 `id`만으로는 어느 테이블의 ID인지 알 수 없으니까. `user_id`도 `customer_id`로 바꿔서 의미를 명확히 했다. `order_date`를 DATE로 캐스팅했다.

### stg_customers

```python
%%writefile jaffle_shop/models/staging/stg_customers.sql
with source as (
    select * from bronze.customers
),

cleaned as (
    select
        id as customer_id,
        first_name,
        last_name
    from source
)

select * from cleaned
```

### stg_payments

```python
%%writefile jaffle_shop/models/staging/stg_payments.sql
with source as (
    select * from bronze.payments
),

cleaned as (
    select
        id as payment_id,
        order_id,
        payment_method,
        amount / 100.0 as amount_dollars
    from source
)

select * from cleaned
```

`amount`를 100으로 나눠서 달러 단위로 바꿨다. 컬럼명도 `amount_dollars`로 변경해서 단위가 뭔지 이름에서 바로 읽힌다.

## dbt 실행

```python
!cd jaffle_shop && dbt run --select staging.*
```

dbt가 `stg_orders`, `stg_customers`, `stg_payments` 세 모델을 실행한다. 각각 DuckDB에 뷰로 생성된다.

## 결과 확인

```python
import duckdb

conn = duckdb.connect('warehouse.duckdb')

# Silver 레이어 확인
conn.execute("SELECT * FROM stg_orders LIMIT 5").fetchdf()
```

```python
# 타입 확인 — order_date가 DATE로 바뀌었는가
conn.execute("""
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'stg_orders'
""").fetchdf()
```

```python
# payments의 amount가 달러 단위로 변환되었는가
conn.execute("SELECT * FROM stg_payments LIMIT 5").fetchdf()
```

Bronze에서는 VARCHAR였던 `order_date`가 DATE로 바뀌었다. `amount`가 센트에서 달러로 변환됐다. 컬럼명이 통일됐다. 이게 Silver다.

## CTE 패턴

위 SQL에서 반복적으로 쓰인 패턴이 있다. `with source as (...), cleaned as (...) select * from cleaned`. dbt 커뮤니티에서 널리 쓰이는 CTE(Common Table Expression) 패턴이다.

```sql
with source as (
    -- 1단계: Bronze에서 원본을 가져온다
    select * from bronze.orders
),

cleaned as (
    -- 2단계: 정제 로직을 적용한다
    select
        id as order_id,
        cast(order_date as date) as order_date
    from source
)

-- 3단계: 최종 결과를 반환한다
select * from cleaned
```

`source` → `cleaned` → `select`. 각 단계가 뭘 하는지 이름에서 읽힌다. 정제 로직이 복잡해지면 CTE를 더 추가하면 된다. `renamed`, `filtered`, `deduplicated` 같은 이름으로 단계를 나누는 팀도 있다.

## 중복 제거 패턴

Bronze에 같은 레코드가 두 번 들어오는 경우가 있다. 소스 시스템에서 데이터를 다시 보냈거나, 증분 적재 로직에 버그가 있었거나. Silver에서 이걸 잡아야 한다.

```sql
with source as (
    select * from bronze.orders
),

deduplicated as (
    select
        *,
        row_number() over (
            partition by id
            order by _loaded_at desc
        ) as row_num
    from source
),

cleaned as (
    select
        id as order_id,
        user_id as customer_id,
        cast(order_date as date) as order_date,
        status
    from deduplicated
    where row_num = 1
)

select * from cleaned
```

`row_number()`로 같은 `id`가 여러 개 있으면 가장 최근에 적재된 것만 남긴다. [2편]({{< ref "002-bronze-layer" >}})에서 추가한 `_loaded_at` 메타데이터 컬럼이 여기서 쓰인다.

## Silver를 함부로 바꾸면 Gold가 깨진다

Gold 모델은 Silver 테이블의 컬럼명, 타입, 단위를 믿고 쓴다. `stg_orders`의 `order_date`가 DATE라는 전제로 Gold에서 날짜 함수를 쓰고 있는데, 누군가 Silver에서 컬럼명을 `ordered_at`으로 바꾸면 Gold 모델이 전부 에러를 뱉는다.

컬럼을 추가하는 건 괜찮다. 기존 컬럼의 이름이나 타입을 바꾸는 게 위험하다. dbt의 `ref()` 함수가 의존 관계를 추적하니까 어디가 영향 받는지는 확인할 수 있다.

## 실무 참고: Airflow에서 dbt 실행

Airflow에서 dbt를 실행하는 방법은 여러 가지다. 가장 간단한 건 `BashOperator`로 `dbt run`을 호출하는 것이고, 더 정교하게 하려면 `cosmos` 라이브러리를 쓴다.

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='silver_transformation',
    schedule='0 6 * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    # Bronze 적재 완료를 기다린 뒤 Silver 변환 실행
    run_staging = BashOperator(
        task_id='dbt_run_staging',
        bash_command='cd /opt/dbt/jaffle_shop && dbt run --select staging',
    )

    # dbt test로 Silver 데이터 품질 검증
    test_staging = BashOperator(
        task_id='dbt_test_staging',
        bash_command='cd /opt/dbt/jaffle_shop && dbt test --select staging',
    )

    run_staging >> test_staging
```

`dbt run` 다음에 `dbt test`를 건다. Silver 변환이 끝나면 바로 품질 검증을 돌린다. 테스트가 실패하면 Gold 변환으로 넘어가지 않는다. 불량 데이터가 Gold까지 올라가는 걸 막는 구조다.

`cosmos` 라이브러리를 쓰면 dbt 모델 하나하나를 Airflow 태스크로 분리할 수 있다. `stg_orders`가 실패해도 `stg_customers`는 독립적으로 성공 처리된다. 모델이 수십 개로 늘어나면 이 세분화가 의미 있어진다.

다음 글에서는 SCD(Slowly Changing Dimension)를 다룬다. 고객의 주소가 바뀌었을 때 과거 주소를 어떻게 보존하는가. Type 1, 2, 3의 차이와 선택 기준.

{{< colab "https://colab.research.google.com/github/biz-agentic-ai/biz-agentic-ai.github.io/blob/main/notebooks/etl-003-silver-layer.ipynb" >}}
