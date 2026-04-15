# db

데이터베이스 접근을 추상화하는 패키지.
현재 PostgreSQL 구현체가 포함되어 있으며, 다른 DB를 추가할 때도 동일한 인터페이스를 따른다.

## 클래스 구조

```
IDB (ABC)                       # DB 인터페이스
└── PostgresqlDB                # psycopg3 기반 PostgreSQL 구현체

IDBClient (ABC)                 # DB 연결 클라이언트 인터페이스
└── PostgresqlDBClient          # 실제 psycopg3 연결 래퍼

IDBRow (ABC)                    # 쿼리 결과 행 인터페이스
└── DBRow                       # dict 기반 기본 구현체

IDBFactory (ABC)                # DB 인스턴스 생성 팩토리
└── PostgresqlDBFactory         # create_db() → PostgresqlDB 반환

IDBInfoFactory (ABC)            # DB 접속 클라이언트 생성 팩토리
└── PostgresqlDBInfoFactory     # create_db_client() → PostgresqlDBClient 반환
```

---

## 추상 팩토리 패턴

두 개의 Factory 인터페이스가 협력해 DB 객체를 완성한다.

```
IDBFactory ──────────────────── IDBInfoFactory
  create_db()                     create_db_client()
       │                                │
       ▼                                ▼
  PostgresqlDB  ◄── set_db_client ── PostgresqlDBClient
```

- `IDBInfoFactory.create_db_client()` → 접속 정보(url, user, password)로 클라이언트를 만든다.
- `IDBFactory.create_db()` → DB 객체를 만들고, 위 클라이언트를 `set_db_client()`로 주입한다.
- 호출 측은 `IDBFactory` 하나만 알면 되고, 접속 정보 소스(하드코딩, 환경변수, Secrets Manager 등)는 `IDBInfoFactory` 구현체 교체로 처리한다.

```python
# PostgresqlDBFactory 내부 동작
def create_db(self) -> IDB:
    db = PostgresqlDB()
    db.set_db_client(self._db_info_factory.create_db_client())  # InfoFactory가 클라이언트 생성
    return db
```

---

## 사용법

### 연결

```python
from python_library.db.postgresql.postgresql_db_factory import PostgresqlDBFactory
from python_library.db.postgresql.postgresql_db_info_factory import PostgresqlDBInfoFactory

url = "postgresql://127.0.0.1:15432/data_lake?sslmode=require"
db = PostgresqlDBFactory(PostgresqlDBInfoFactory(url, "user", "password")).create_db()
db.connect()
```

### 조회 (execute_query)

파라미터는 `%s` 플레이스홀더와 tuple로 전달한다.

```python
# 전체 조회
rows = db.execute_query("SELECT * FROM batch")

# 파라미터 조회
rows = db.execute_query("SELECT * FROM resource WHERE name = %s", ("lcms",))

for row in rows:
    print(row)
    update_time = row.get_as("update_time", datetime)  # 타입 변환 조회
```

### 수정 (execute_update)

```python
db.execute_update("UPDATE project SET remarks = %s WHERE id = %s", ("test3", 2))
db.commit()
```

실패 시 `rollback()`으로 트랜잭션을 되돌린다.

```python
try:
    db.execute_update(...)
    db.commit()
except Exception:
    db.rollback()
finally:
    db.disconnect()
```

---

## 설계 의도

### 인터페이스 분리

- `IDB`: SQL 실행 (`connect`, `disconnect`, `execute_query`, `execute_update`, `commit`, `rollback`)
- `IDBClient`: 연결 객체 래핑. `IDB`가 `set_db_client()`로 주입받는다.
- `IDBRow` / `DBRow`: 쿼리 결과 행 추상화. `get_as(column, type)`으로 타입 변환 조회, `get_as_or_none(column, type)`으로 null 안전 조회를 지원한다. `UUID`, `datetime` 변환이 내장되어 있다.

### 추상 팩토리 패턴

`IDBFactory`와 `IDBInfoFactory`를 분리한 이유:

- **DB 교체**: `IDBFactory` 구현체만 바꾸면 PostgreSQL → MySQL 전환 가능. 호출 측 코드 변경 없음.
- **접속 정보 소스 교체**: `IDBInfoFactory` 구현체만 바꾸면 하드코딩 → 환경변수 → AWS Secrets Manager 전환 가능.
- **조합 가능**: 두 Factory는 독립적으로 교체할 수 있어 테스트 시 Mock InfoFactory를 주입하기 쉽다.

---

## 새 DB 추가 방법

1. `db/` 하위에 새 디렉토리를 만든다 (예: `mysql/`).
2. `IDB`, `IDBClient`를 구현한다.
3. `IDBFactory`, `IDBInfoFactory`를 구현한다.
4. PostgreSQL 구현체(`db/postgresql/`)를 참고해 동일한 파일 구조로 작성한다.

---

## 의존성

- `psycopg >= 3.2.1` (optional extra `postgres`로 설치)
- `uv sync --extra postgres`
