# thread

멀티스레드 기반 병렬 작업을 위한 패키지.
`process` 패키지와 거의 동일한 설계를 따르되, `threading.Thread` 기반이다.

## 클래스 구조

```
threading.Thread
└── abThread (ABC)              # 스레드 기본 추상 클래스
    ├── abThreading (ABC)       # 반복 실행 스레드 (stop 신호까지 루프)
    └── QueueThread (ABC)       # 공유 큐를 사용하는 작업 스레드
        ├── QueueThreading      # 반복 실행 + 공유 큐
        └── MultiThreadManager  # 여러 QueueThread를 묶어서 관리
```

---

## 사용법

### 1. 단순 스레드 (abThread)

`abThread`를 상속하고 `action()`만 구현한다.
`action()`은 **한 번** 실행된다.

```python
from python_library.thread.thread import abThread

class MyThread(abThread):
    def action(self) -> None:
        print("MyThread!")

thread = MyThread()
thread.start()
```

### 2. 큐 기반 스레드 (QueueThread)

공유 큐에서 Job을 꺼내 처리하는 패턴.

```python
from python_library.thread.queue_thread import QueueThread

class MyWorkerThread(QueueThread):
    def action(self) -> None:
        while True:
            time.sleep(1)

            print(f"{self.name} || is_running = {self.is_running()}")

            job = self.pop_shared_queue(self.name)  # 이름 지정 큐
            if job is None:
                continue

            job.execute()
```

### 3. 매니저 (MultiThreadManager)

워커 스레드를 묶어 관리한다. `action()`에서 매니저 자신의 큐를 소비하거나 다른 로직을 수행한다.

```python
from python_library.thread.multi_thread_manager import MultiThreadManager

class MyManager(MultiThreadManager):
    def action(self) -> None:
        while True:
            time.sleep(1)

            job = self.pop_shared_queue(self.name)
            if job is None:
                continue

            job.execute()
```

### 4. 조립 및 실행

```python
manager = MyManager()

thread1 = MyWorkerThread()
thread2 = MyWorkerThread()
thread3 = MyWorkerThread()
thread4 = MyWorkerThread()

manager.append(thread1)
manager.append(thread2)
manager.append(thread3)
manager.append(thread4)

# 이름 지정 큐: 특정 스레드에만 전달
manager.push_shared_queue("MyWorkerThread1", MyJob())
manager.push_shared_queue("MyWorkerThread2", MyJob())
manager.push_shared_queue("MyWorkerThread3", MyJob())
manager.push_shared_queue("MyWorkerThread4", MyJob())

# 매니저 자신의 큐
manager.push_shared_queue("MyManager1", MyJob())

manager.start()

while True:
    time.sleep(5)
```

---

## 설계 의도

### process 패키지와의 차이

스레드는 **같은 메모리를 공유**하므로 일반 `threading.Lock`과 `JobQueue(list 기반)`를 사용한다.
프로세스는 메모리가 분리되므로 `multiprocessing.Queue`와 `multiprocessing.Lock`을 사용한다.

### 공유 큐 두 가지

| 큐 | 메서드 | 설명 |
|---|---|---|
| 공용 큐 | `push_shared_job_queue(job)` | 모든 스레드가 경쟁적으로 소비 |
| 이름 지정 큐 | `push_shared_queue("이름", job)` | 특정 스레드에만 전달 |

### MultiThreadManager

`QueueThread`를 상속하므로 그 자체도 스레드로 동작한다.
`start()` 호출 시 하위 스레드들을 모두 시작하고, `action()`을 실행한 후 `join()`으로 완료를 기다린다.

### stop 전파

`manager.stop()` 호출 시 관리 중인 모든 하위 스레드에도 `stop()`이 전파된다.

### 예외 처리 (on_exception)

`action()`에서 예외가 발생하면 `run()`이 이를 잡아 `on_exception(e)`를 호출한다.
**기본 구현은 예외를 다시 던진다(fail-loud)** — 표준 `threading.Thread`와 동일하게
단발형은 종료되고, 루프형(`abThreading`/`QueueThreading`)은 루프가 끝난다(fail-fast).
라이브러리가 실패를 조용히 삼키지 않도록 한 의도적 기본값이다.

"한 job이 실패해도 계속 도는" resilient 워커가 필요하면 `on_exception`을 오버라이드해
예외를 삼킨다(다시 던지지 않는다).

```python
class MyWorker(QueueThreading):
    def on_exception(self, e: Exception) -> None:
        logger.error("job failed, continuing: %s", e)  # 삼키고 계속
```

스레드 예외는 `start()`/`join()` 호출 측으로 전파되지 않으므로(기본값은
`threading.excepthook`으로 traceback 출력 후 종료), 호출 측이 실패를 인지해야 한다면
`on_exception`에서 별도로 신호를 전달해야 한다.

### 이름 자동 생성

`ClassNameGenerator`를 통해 이름을 지정하지 않으면 `MyWorkerThread1`, `MyWorkerThread2`처럼 클래스별로 순번이 붙는다.
`push_shared_queue("MyWorkerThread1", job)` 형태로 이름을 키로 사용하므로 정확한 이름 확인이 중요하다.
