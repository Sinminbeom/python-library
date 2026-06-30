# process

멀티프로세스 기반 병렬 작업을 위한 패키지.

## 클래스 구조

```
multiprocessing.Process
└── abProcess (ABC)             # 프로세스 기본 추상 클래스
    └── abProcessing (ABC)      # 반복 실행 프로세스 (stop 신호까지 루프)

MultiProcessManager             # 여러 프로세스를 묶어서 관리 (abThread 상속)
```

---

## 사용법

### 1. 프로세스 정의

`abProcess`를 상속하고 `action()`만 구현한다.

```python
from python_library.process.process import abProcess

class MyProcess(abProcess):
    def action(self) -> None:
        while True:
            time.sleep(1)

            job = self.pop_shared_queue(self.name)  # 이름 지정 큐에서 꺼내기
            if job is None:
                continue

            print(f"pid: {os.getpid()}")
            job.execute()
```

### 2. 매니저 정의

`MultiProcessManager`를 상속하고 `action()`을 구현한다.
매니저 자체도 스레드로 동작하며, 하위 프로세스를 시작하고 관리한다.

```python
from python_library.process.multi_process_manager import MultiProcessManager

class MyManager(MultiProcessManager):
    def action(self) -> None:
        while True:
            time.sleep(1)

            job = self.pop_shared_queue(self.name)
            if job is None:
                continue

            job.execute()
```

### 3. 조립 및 실행

```python
process1 = MyProcess()
process2 = MyProcess()

manager = MyManager()
manager.append(process1)
manager.append(process2)

# 이름 지정 큐: 특정 프로세스에만 전달
manager.push_shared_queue("MyProcess1", MyJob())
manager.push_shared_queue("MyProcess2", MyJob())
manager.push_shared_queue("MyManager1", MyJob())  # 매니저 자신의 큐

manager.start()

while True:
    time.sleep(2)
```

---

## 설계 의도

### Template Method 패턴

`action()`만 오버라이드하면 프로세스를 만들 수 있다.
생명주기(start, stop, is_running)는 `abProcess`가 모두 관리한다.

### abProcess vs abProcessing

| | abProcess | abProcessing |
|---|---|---|
| `action()` 실행 | **한 번** 실행 후 종료 | `is_stop()`이 True가 될 때까지 **반복** |
| 용도 | 단발성 작업 | 폴링 루프, 상주 워커 |

### 공유 큐 두 가지

| 큐 | 메서드 | 설명 |
|---|---|---|
| 공용 큐 | `push_shared_job_queue(job)` | 모든 프로세스가 경쟁적으로 소비 |
| 이름 지정 큐 | `push_shared_queue("이름", job)` | 특정 프로세스에만 전달 |

`MultiProcessManager`가 `multiprocessing.Manager()`로 큐와 Lock을 생성해 각 프로세스에 주입한다.
프로세스 간 메모리가 분리되므로 반드시 `multiprocessing.Queue`를 사용한다.

### 이름 자동 생성

`ClassNameGenerator`를 통해 이름을 지정하지 않으면 `MyProcess1`, `MyProcess2`처럼 클래스별로 순번이 붙는다.
`push_shared_queue("MyProcess1", job)` 형태로 이름을 키로 사용하므로 정확한 이름 확인이 중요하다.

### Event 기반 정지

`stop()` 호출 시 내부 `multiprocessing.Event`를 set한다.
`is_stop()`, `is_running()`으로 외부에서 상태를 확인할 수 있다.

### 예외 처리 (on_exception)

`action()` 예외는 `run()`이 잡아 `on_exception(e)`를 호출한다. **기본은 예외를 다시
던진다(fail-loud)** — 단발형(`abProcess`)은 종료, 루프형(`abProcessing`/`QueueProcessing`)은
루프가 끝난다. resilient 워커가 필요하면 `on_exception`을 오버라이드해 예외를 삼긴다.

```python
class MyProcess(abProcess):
    def on_exception(self, e: Exception) -> None:
        logger.error("process %s failed, continuing: %s", self.name, e)  # 삼키고 계속
```

> 주의: `on_exception`은 **자식 프로세스 안에서** 실행된다. 메모리가 분리되므로
> 부모 프로세스의 상태를 직접 바꿀 수 없다. 부모가 실패를 인지해야 한다면
> `multiprocessing.Queue`(공유 큐)에 실패 정보를 push하는 식으로 전달한다.
