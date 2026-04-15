# thread

멀티스레드 기반 병렬 작업을 위한 패키지.
`process` 패키지와 거의 동일한 설계를 따르되, `threading.Thread` 기반이다.

## 클래스 구조

```
threading.Thread
└── abThread (ABC)              # 스레드 기본 추상 클래스
    ├── abThreading (ABC)       # 반복 실행 스레드 (stop 신호까지 루프)
    └── abWorkerThread (ABC)    # 공유 큐를 사용하는 작업 스레드
        └── MultiThreadManager  # 여러 Worker Thread를 묶어서 관리
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

### 2. 워커 스레드 (abWorkerThread)

공유 큐에서 Job을 꺼내 처리하는 패턴.

```python
from python_library.thread.worker_thread import abWorkerThread

class MyWorkerThread(abWorkerThread):
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

`abWorkerThread`를 상속하므로 그 자체도 스레드로 동작한다.
`start()` 호출 시 하위 스레드들을 모두 시작하고, `action()`을 실행한 후 `join()`으로 완료를 기다린다.

### stop 전파

`manager.stop()` 호출 시 관리 중인 모든 하위 스레드에도 `stop()`이 전파된다.

### 이름 자동 생성

`ClassNameGenerator`를 통해 이름을 지정하지 않으면 `MyWorkerThread1`, `MyWorkerThread2`처럼 클래스별로 순번이 붙는다.
`push_shared_queue("MyWorkerThread1", job)` 형태로 이름을 키로 사용하므로 정확한 이름 확인이 중요하다.
