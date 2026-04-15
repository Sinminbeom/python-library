# python-library

공통으로 사용하는 Python 핵심 라이브러리.
로깅, 데이터베이스, 클라우드 저장소, 멀티프로세싱/스레딩, 보안 등 반복 구현이 필요한 인프라 기능을 추상화해 제공한다.

> **Python >= 3.11** / 현재 버전: `pyproject.toml`의 `[project] version` 참고

---

## 패키지 구조

```
src/python_library/
├── logger/         # 구조화 로깅 (AppLogger, JobLogger)
├── db/             # DB 추상화 레이어 (PostgreSQL 구현체 포함)
├── storage/        # 저장소 추상화 레이어 (S3 구현체 포함)
├── security/       # 보안 (Argon2id 비밀번호 암호화)
├── job/            # 실행 단위 Job 인터페이스 및 구현체
├── job_queue/      # Job 큐 추상화
├── process/        # 멀티프로세스 기반 병렬 처리
├── thread/         # 멀티스레드 기반 병렬 처리
├── category/       # 계층적 컴포넌트 조직 (Composite 패턴)
├── configure/      # conf 기반 설정 관리 (Singleton)
├── delegate/       # 타입 안전한 콜백 패턴 (Action, Func)
├── meta_data/      # 데이터 파이프라인 메타데이터 구조
├── singleton/      # Singleton 기반 클래스
├── utils/          # 공통 유틸리티
└── define/         # 공통 Enum 및 상수
```

각 패키지의 설계 의도와 사용법은 해당 디렉토리의 `README.md`를 참고한다.

---

## 핵심 설계 원칙

### 1. 외부 의존은 인터페이스로 추상화
DB, Storage, Security 등 외부 시스템에 대한 의존은 반드시 인터페이스(`IDB`, `IStorage`, `IPasswordCrypto`)를 통해 접근한다.
구현체(PostgreSQL, S3, Argon2id)는 인터페이스를 구현하는 형태로 추가한다.

```
IDB (interface)
└── PostgresqlDB (구현체)  ← 교체 가능
```

### 2. 구현체 생성은 Factory로 분리
`new PostgresqlDB()` 대신 `PostgresqlDBFactory(info).create()` 형태로 생성한다.
접속 정보(host, port 등)는 `InfoFactory`로 별도 분리해 설정 소스(환경변수, INI, Secrets Manager)를 자유롭게 교체할 수 있다.

### 3. 앱 전역 상태는 Singleton으로 관리
`AppConfig`, `AppLogger(BaseConfLogger 상속)`, `AppCategory`는 Singleton이다.
인스턴스를 직접 생성(`MyConfig()`)하지 않고 반드시 `.instance()`로 접근한다.

### 4. 병렬 처리는 Template Method 패턴
`abProcess`, `abThread`를 상속하고 `action()` 메서드만 구현하면 된다.
생명주기(start, stop, 공유 큐 연결)는 부모 클래스가 관리한다.

---

## 새 구현체 추가 방법

| 추가하려는 것 | 구현해야 하는 인터페이스 | 위치 |
|---|---|---|
| 새 DB (MySQL 등) | `IDB`, `IDBClient`, `IDBFactory`, `IDBInfoFactory` | `db/mysql/` |
| 새 저장소 (GCS 등) | `IStorage`, `IStorageClient`, `IStorageFactory`, `IStorageInfoFactory` | `storage/gcs/` |
| 새 암호화 알고리즘 | `IPasswordCrypto`, `IPasswordCryptoHasher`, `IPasswordCryptoFactory`, `IPasswordCryptoInfoFactory` | `security/password/bcrypt/` |
| 새 Job | `IJob` (`execute()` 구현) | `job/` |

---

## python-library 개발 세팅

```
# 파이썬 패키지 동기화(옵션 postgres 추가)
$ uv sync --extra postgres
# 파이썬 패키지 동기화(옵션 postgres 없이)
$ uv sync
# pre-commit 실행
$ uv run pre-commit install

# windows
## ssh-agent 서비스 자동 시작 켜기 (관리자 PowerShell)
$ Get-Service ssh-agent | Set-Service -StartupType Automatic
$ Start-Service ssh-agent
$ ssh-add ~/.ssh/id_ed25519-company

# linux
## keychain 설치
$ sudo apt-get update
$ sudo apt-get install -y keychain

## ~/.bashrc 맨 아래에 추가
## ssh-agent 자동 관리 + 키 자동 로드
eval "$(keychain --eval --quiet ~/.ssh/id_ed25519-company)"

## 적용
$ source ~/.bashrc

## 확인
$ ssh-add -l
```

## 배포할때
```
# 포맷팅
$ uv run ruff format .
# 린팅 및 자동 수정
$ uv run ruff check . --fix
# 타입 체킹
$ uv run pyright

# pyproject.toml 파일 버전 수정
[project]
version = "x.x.x"

# 파이썬 라이브러리 빌드
$ uv build
$ {PROJECT_ROOT_PATH}/dist/python_library-{VERSION}-*.whl 파일 생성됨
```

## 개발하는 프로젝트에 import하는 법
```
# whl 파일을 직접 import
$ uv add ./lib/python_library-0.1.0-py3-none-any.whl
# github에서 직접 import
$ uv add git+ssh://git@personal-github/Sinminbeom/python-library.git@1.15.0
```

---

## 테스트 실행

```bash
# 전체 테스트
$ uv run pytest

# 커버리지 포함
$ uv run pytest --cov=python_library

# 특정 패키지만
$ uv run pytest tests/test_logger/
```

---

## 버전 관리 규칙

`pyproject.toml`의 `[project] version`을 **Semantic Versioning**(`MAJOR.MINOR.PATCH`)으로 관리한다.

| 변경 유형 | 올릴 버전 | 예시 |
|---|---|---|
| 하위 호환되지 않는 인터페이스 변경 | MAJOR | `IDB` 메서드 시그니처 변경 |
| 하위 호환되는 새 기능 추가 | MINOR | 새 패키지 또는 구현체 추가 |
| 버그 수정, 내부 개선 | PATCH | 기존 동작 유지하면서 수정 |

배포 후 git tag를 버전명으로 생성한다.
```bash
$ git tag 2.2.4
$ git push origin 2.2.4
```