# job

실행 단위 작업(Job)을 정의하는 패키지.
`IJob.execute()`를 구현하면 `process`, `thread` 패키지의 공유 큐에 넣어 병렬 실행할 수 있다.

## 클래스 구조

```
IJob (ABC)
  execute() -> None

Job             # 아무 동작 없는 기본 구현체 (테스트/스텁용)
```

---

## 사용법

### 커스텀 Job 정의

`IJob`을 상속하고 `execute()`에 로직을 구현한다.

```python
from python_library.job.job import IJob

class MyJob(IJob):
    def execute(self) -> None:
        print("MyJob execute!!!")
```

### process / thread 큐에 넣어 실행

`IJob`을 구현한 객체는 `push_shared_queue()`로 큐에 넣고,
워커에서 `pop` 후 `execute()`를 호출한다.

```python
# 워커 측
job = self.pop_shared_queue(self.name)
if job is not None:
    job.execute()

# 관리자 측
manager.push_shared_queue("WorkerThread1", MyJob())
```

자세한 사용법은 `process/README.md`, `thread/README.md` 참고.
