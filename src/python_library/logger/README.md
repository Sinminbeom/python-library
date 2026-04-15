# logger

애플리케이션 전반에서 사용하는 구조화 로깅 패키지.

## 클래스 구조

```
Singleton
└── BaseConfLogger          # INI 설정 파일 기반 로거 (추상)
    └── AppLogger           # 일반 애플리케이션 로그

JobLogger                   # 구조화 JSON 로그 (배치 잡 전용, 독립적)
AccessLogger                # 접근 로그

JsonFormatter               # logging.Formatter 구현체 (JSON 직렬화)
JobStatus (Enum)            # STARTED | DONE | FAILED | SKIPPED
```

---

## AppLogger

INI 설정 파일 기반의 Singleton 로거.

### 초기화

`instance()` 호출 전 반드시 `set_config()`로 설정 경로와 로거 이름을 지정해야 한다.
두 번 이상 `set_config()`를 호출하면 설정이 갱신된다.

```python
from python_library.logger.app_logger import AppLogger

AppLogger.set_config("./config/logging.conf", "python-library")

AppLogger.instance().info("서버 시작")
AppLogger.instance().error("예외 발생", exc_info=True)
```

### logging.conf 포맷

Python 표준 `logging.config.fileConfig` 형식의 INI 파일을 사용한다.

```ini
[loggers]
keys=root,python-library

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_python-library]
level=DEBUG
handlers=consoleHandler
qualname=python-library
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s %(name)s %(levelname)s %(message)s
```

### JSON 포맷터 사용

`JsonFormatter`를 핸들러 포매터로 지정하면 JSON으로 출력된다.

출력 예시:
```json
{"timestamp": "2025-01-01T00:00:00", "level": "INFO", "logger": "python-library", "message": "conf 기반 JSON 포맷 테스트", "thread_id": 12345}
```

---

## JobLogger

배치 잡 추적을 위한 구조화 JSON 로거. Singleton이 아니며 잡마다 인스턴스를 생성한다.

### 초기화

```python
from python_library.logger.job_logger import JobLogger, JobStatus

# job_run_id는 선택 — 지정하면 모든 로그에 자동 포함
logger = JobLogger(service="etl-pipeline", job_run_id="jr_001")
```

### 로그 작성

`step`, `status`, `**extra` 키워드로 컨텍스트를 추가한다.
값이 `None`인 필드는 JSON 출력에서 생략된다.

```python
logger.info("데이터 로드 완료", step="extract", status=JobStatus.DONE, row_count=1000)
logger.error("파일 없음", step="read", status=JobStatus.FAILED, file_path="/tmp/x.json")
logger.info("시작")  # step, status 생략 가능
```

출력 예시:
```json
{"timestamp": "...", "level": "INFO", "logger": "etl-pipeline", "message": "데이터 로드 완료", "job_run_id": "jr_001", "step": "extract", "status": "DONE", "row_count": 1000, "thread_id": 12345}
```

### JobStatus

```python
class JobStatus(str, Enum):
    STARTED = "STARTED"
    DONE    = "DONE"
    FAILED  = "FAILED"
    SKIPPED = "SKIPPED"
```

### 주의: 예약 키 충돌

`JsonFormatter.RESERVED_KEYS`에 해당하는 키(`timestamp`, `level`, `logger`, `message`, `thread_id`)를
`**extra`에 넣으면 `ValueError`가 발생한다.

---

## AppLogger vs JobLogger 비교

| | AppLogger | JobLogger |
|---|---|---|
| 설정 방식 | INI 파일 (`set_config`) | 코드에서 직접 생성 |
| 포맷 | INI에 정의된 포맷 (plain / JSON 선택 가능) | 항상 JSON |
| 용도 | 서비스 전반 로그 | 배치 잡 추적 로그 |
| Singleton | O | X (잡마다 인스턴스) |
| 컨텍스트 추가 | X | O (`step`, `status`, `**extra`) |

---

## 새 로거 추가

- INI 기반 로거: `BaseConfLogger`를 상속하고 필요한 메서드를 추가한다.
- INI가 아닌 로거: `JobLogger` 방식(직접 핸들러 구성)을 참고한다.
