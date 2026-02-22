---
title: "2. Bronze 레이어 - 원본을 있는 그대로 쌓는다"
date: 2026-02-22
draft: false
summary: "Bronze에 데이터를 넣는 방법은 두 가지다. 전체를 덮어쓰거나, 바뀐 것만 가져오거나. 어떤 방식을 고르느냐에 따라 파이프라인의 복잡도가 완전히 달라진다."
categories: ["ETL 설계"]
tags: ["etl", "bronze", "full-load", "incremental-load", "duckdb", "cdc"]
series: ["etl-design-guide"]
series_order: 2
weight: 2
author: "Junho Lee"
ShowToc: true
---

{{< colab "https://colab.research.google.com/github/biz-agentic-ai/biz-agentic-ai.github.io/blob/main/notebooks/etl-002-bronze-layer.ipynb" >}}

## 원본을 건드리면 돌아갈 곳이 없다

[1편]({{< ref "001-medallion-architecture" >}})에서 Bronze 레이어의 원칙을 정했다. 소스 시스템에서 가져온 데이터를 변환 없이 저장한다. 타입 캐스팅도 안 하고, 컬럼명도 안 바꾼다.

원칙은 간단한데 실제로 지키기가 어렵다. "날짜 컬럼 타입이 문자열인데 DATE로 바꿔서 넣으면 안 되나?" 같은 유혹이 생긴다. 안 된다. Bronze에서 타입을 바꾸면 원본 복원이 불가능해진다. 소스 시스템에서 `"2026-02-30"` 같은 잘못된 날짜가 넘어왔을 때, DATE로 캐스팅하면 에러가 나거나 NULL로 바뀐다. 원본이 뭐였는지 알 수 없게 된다.

Bronze는 보험이다. Silver 변환 로직에 버그가 있어도, 소스 시스템이 갑자기 스키마를 바꿔도, Bronze에서 다시 시작할 수 있다. 이 보험을 포기하면 문제가 생길 때마다 소스 시스템에서 데이터를 다시 끌어와야 한다. 소스 시스템 담당자가 협조적이라는 보장은 없다.

## Full Load와 Incremental Load

Bronze에 데이터를 넣는 방법은 크게 두 가지다.

**Full Load** 는 소스 테이블 전체를 매번 가져와서 덮어쓴다. 단순하다. 소스에 있는 그대로가 Bronze에 있으니까 정합성 고민이 없다. 대신 데이터가 커지면 비용이 늘어난다. 주문 테이블이 1억 건인데 하루에 신규 주문이 1만 건이라면, 나머지 9,999만 건은 어제와 똑같은 데이터를 매번 다시 가져오는 셈이다.

**Incremental Load** 는 마지막 적재 이후에 변경된 데이터만 가져온다. 효율적이다. 1만 건만 가져오면 된다. 대신 복잡하다. "마지막 적재 이후"를 어떻게 판단할 건지, 삭제된 데이터는 어떻게 감지할 건지 정해야 한다.

어떤 걸 쓸지는 테이블 특성에 따라 다르다.

| 구분 | Full Load | Incremental Load |
|------|-----------|------------------|
| 구현 난이도 | 낮음 | 높음 |
| 네트워크/비용 | 데이터 크기에 비례 | 변경분에 비례 |
| 삭제 감지 | 자동 (전체를 덮어쓰니까) | 별도 처리 필요 |
| 적합한 대상 | 코드 테이블, 소규모 마스터 | 대용량 트랜잭션 |

실무에서는 섞어 쓴다. 코드 테이블이나 상품 마스터처럼 건수가 적은 테이블은 Full Load로 단순하게 가져간다. 주문, 로그, 이벤트처럼 건수가 많은 테이블은 Incremental Load로 변경분만 가져간다.

## 증분의 기준을 잡는 법

Incremental Load에서 가장 중요한 건 "무엇이 변경되었는가"를 판단하는 기준이다. 흔히 쓰는 방법이 세 가지 있다.

**타임스탬프 기반.** 소스 테이블에 `updated_at` 같은 수정일시 컬럼이 있으면 가장 간단하다. 마지막 적재 시점 이후의 행만 가져온다. 조건이 하나 있다. 소스 시스템이 수정일시를 정직하게 갱신해야 한다. 데이터를 UPDATE하면서 `updated_at`을 안 바꾸는 시스템이 의외로 많다.

**자동 증가 키 기반.** `order_id`처럼 단조 증가하는 PK가 있으면 마지막으로 가져온 ID 이후의 행만 가져온다. INSERT는 잡히지만 UPDATE는 못 잡는다. 주문번호가 한 번 발행되면 바뀌지 않는 로그성 테이블에 적합하다.

**CDC(Change Data Capture).** 소스 데이터베이스의 변경 로그를 직접 읽는다. Debezium 같은 도구가 MySQL이나 PostgreSQL의 WAL(Write-Ahead Log)을 캡처해서 INSERT, UPDATE, DELETE를 전부 잡아낸다. 가장 정확하지만 인프라 구성이 필요하다.

```
타임스탬프 기반:  WHERE updated_at > '마지막 적재 시점'
자동 증가 키:    WHERE order_id > 마지막_적재_ID
CDC:            데이터베이스 변경 로그 캡처
```

## DuckDB로 두 방식을 직접 비교한다

[1편]({{< ref "001-medallion-architecture" >}})에서 세팅한 환경을 이어서 쓴다.

```python
import duckdb

conn = duckdb.connect('warehouse.duckdb')
```

### Full Load 시뮬레이션

Full Load는 간단하다. 기존 데이터를 지우고 전체를 다시 넣는다.

```python
# 소스 데이터가 변경된 상황을 시뮬레이션
# 실제로는 소스 시스템에서 SELECT * 로 전체를 가져온다

conn.execute("""
-- Full Load: 통째로 교체
CREATE OR REPLACE TABLE bronze.orders AS
SELECT *
FROM read_csv_auto(
  'https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_orders.csv'
);
""")

print("Full Load 완료:",
      conn.execute("SELECT count(*) FROM bronze.orders").fetchone()[0], "건")
```

`CREATE OR REPLACE TABLE`이 핵심이다. 매번 테이블을 새로 만든다. 이전 데이터는 사라지고 소스의 현재 상태가 그대로 들어온다.

### Incremental Load 시뮬레이션

Incremental Load는 한 단계가 더 있다. 마지막으로 가져온 지점을 기억해야 한다.

```python
# 워터마크 테이블: 마지막 적재 지점을 기록
conn.execute("""
CREATE TABLE IF NOT EXISTS bronze.watermarks (
    table_name VARCHAR PRIMARY KEY,
    last_loaded_id INTEGER,
    last_loaded_at TIMESTAMP DEFAULT current_timestamp
);
""")

# 현재 워터마크 확인
watermark = conn.execute("""
SELECT COALESCE(last_loaded_id, 0)
FROM bronze.watermarks
WHERE table_name = 'orders'
""").fetchone()

last_id = watermark[0] if watermark else 0
print(f"마지막 적재 ID: {last_id}")
```

```python
# 증분 적재: last_id 이후 데이터만 가져온다
conn.execute(f"""
INSERT INTO bronze.orders
SELECT *
FROM read_csv_auto(
  'https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_orders.csv'
)
WHERE id > {last_id};
""")

# 워터마크 갱신
conn.execute("""
INSERT OR REPLACE INTO bronze.watermarks (table_name, last_loaded_id, last_loaded_at)
SELECT 'orders', MAX(id), current_timestamp
FROM bronze.orders;
""")

print("Incremental Load 완료")
```

`watermarks` 테이블이 증분 적재의 핵심이다. 어디까지 가져왔는지를 기록해두고, 다음 적재 때 그 이후만 가져온다. 이 패턴을 **하이 워터마크(High Watermark)** 라고 부른다.

## 메타데이터 컬럼을 붙인다

Bronze에 원본 데이터만 넣으면 나중에 답이 안 나오는 질문이 생긴다. "이 데이터가 언제 적재된 건가?" "어느 소스에서 온 건가?"

원본 컬럼은 그대로 두고, 메타데이터 컬럼을 추가한다.

```python
conn.execute("""
CREATE OR REPLACE TABLE bronze.orders_with_meta AS
SELECT
    *,
    current_timestamp AS _loaded_at,
    'jaffle_shop' AS _source_system,
    'full' AS _load_type
FROM read_csv_auto(
  'https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_orders.csv'
);
""")

conn.execute("SELECT * FROM bronze.orders_with_meta LIMIT 3").fetchdf()
```

`_loaded_at`, `_source_system`, `_load_type`. 언더스코어로 시작하는 이유는 원본 컬럼과 구분하기 위해서다. 원본에 `loaded_at`이라는 컬럼이 있을 수도 있으니까.

이 메타데이터가 있으면 Silver 변환에서 문제가 생겼을 때 "언제 적재한 데이터까지는 정상이고, 이후부터 이상하다"는 식으로 범위를 좁힐 수 있다.

## 적재 패턴 정리

Bronze 적재 패턴을 정리하면 이렇다.

| 패턴 | 적용 대상 | 구현 |
|------|-----------|------|
| Full Load (덮어쓰기) | 코드 테이블, 소규모 마스터 | `CREATE OR REPLACE TABLE` |
| Full Load (스냅샷) | 일별 현황 보관이 필요한 경우 | 파티션 키로 적재일 사용 |
| Incremental (타임스탬프) | `updated_at`이 있는 테이블 | `WHERE updated_at > 워터마크` |
| Incremental (자동 증가 키) | 로그, 이벤트, 주문 | `WHERE id > 워터마크` |
| CDC | 삭제 감지가 필요한 경우 | Debezium + Kafka |

Full Load 중에 **스냅샷** 방식이 하나 더 있다. 덮어쓰기가 아니라 적재일 기준으로 매일의 전체 상태를 따로 저장하는 방식이다. 상품 마스터의 어제 상태와 오늘 상태를 비교하고 싶을 때 쓴다. 스토리지를 많이 먹지만, [1편]({{< ref "001-medallion-architecture" >}})에서 얘기했듯 클라우드 환경에서 스토리지 비용은 무시할 수 있는 수준이다.

## 실무 참고: Airflow로 Bronze 적재

Bronze 적재를 Airflow DAG으로 짜면 테이블마다 Full Load / Incremental Load를 구분해서 태스크를 나눌 수 있다.

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import duckdb

def load_full(table_name, source_url, **context):
    """Full Load: 전체 교체"""
    conn = duckdb.connect('warehouse.duckdb')
    conn.execute(f"""
        CREATE OR REPLACE TABLE bronze.{table_name} AS
        SELECT *, current_timestamp AS _loaded_at,
               '{table_name}' AS _source_system, 'full' AS _load_type
        FROM read_csv_auto('{source_url}')
    """)
    conn.close()

def load_incremental(table_name, source_url, key_column, **context):
    """Incremental Load: 워터마크 이후만"""
    conn = duckdb.connect('warehouse.duckdb')
    wm = conn.execute(f"""
        SELECT COALESCE(last_loaded_id, 0)
        FROM bronze.watermarks WHERE table_name = '{table_name}'
    """).fetchone()
    last_id = wm[0] if wm else 0

    conn.execute(f"""
        INSERT INTO bronze.{table_name}
        SELECT *, current_timestamp AS _loaded_at
        FROM read_csv_auto('{source_url}')
        WHERE {key_column} > {last_id}
    """)
    conn.close()

with DAG(
    dag_id='bronze_ingestion',
    schedule='0 5 * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    # 소규모 마스터 → Full Load
    load_customers = PythonOperator(
        task_id='load_customers_full',
        python_callable=load_full,
        op_kwargs={'table_name': 'customers', 'source_url': '...'},
    )

    # 대용량 트랜잭션 → Incremental Load
    load_orders = PythonOperator(
        task_id='load_orders_incremental',
        python_callable=load_incremental,
        op_kwargs={
            'table_name': 'orders',
            'source_url': '...',
            'key_column': 'id',
        },
    )

    # 병렬 실행 — 테이블 간 의존 관계가 없으니까
    [load_customers, load_orders]
```

소규모 마스터는 `load_full`, 대용량 트랜잭션은 `load_incremental`. 테이블 특성에 맞게 함수를 나눠서 호출한다. 테이블 간에는 의존 관계가 없으니 Airflow가 병렬로 실행한다.

다음 글에서는 Silver 레이어를 다룬다. Bronze에 쌓아둔 원본 데이터를 정제하고 표준화하는 과정이다. dbt를 본격적으로 쓰기 시작한다.

{{< colab "https://colab.research.google.com/github/biz-agentic-ai/biz-agentic-ai.github.io/blob/main/notebooks/etl-002-bronze-layer.ipynb" >}}
