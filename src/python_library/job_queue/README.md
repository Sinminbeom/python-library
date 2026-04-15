# job_queue

`IJob` 인스턴스를 담는 큐 추상화 패키지.
`thread`, `process` 패키지의 공유 작업 큐로 사용된다.

## 클래스 구조

```
IJobQueue (ABC)             # 큐 인터페이스
└── JobQueue                # list 기반 기본 구현 (FIFO)
```

## IJobQueue 인터페이스

```python
class IJobQueue(ABC):
    def append(self, job: IJob) -> None: ...   # 뒤에 추가
    def pop(self) -> IJob | None: ...          # 앞에서 제거 (FIFO)
    def size(self) -> int: ...
    def clear(self) -> None: ...
    def is_empty(self) -> bool: ...
```

---

## 설계 의도

`thread`와 `process` 패키지에서 직접 `list`나 `Queue`를 쓰지 않고 인터페이스를 통해 의존한다.
`JobQueue` 구현을 우선순위 큐, 지연 큐 등으로 교체할 수 있다.

현재 `JobQueue`는 `list` 기반이며 FIFO로 동작한다 (`append`로 뒤에서 추가, `pop`으로 앞에서 제거).

---

## 스레드 안전성

`JobQueue` 자체는 스레드 안전하지 않다.
`MultiThreadManager`와 `abWorkerThread`에서 `Lock`을 함께 사용해 안전하게 접근한다.
직접 `JobQueue`를 사용할 때는 `Lock`을 별도로 관리해야 한다.

---

## 새 큐 구현 추가

```python
class PriorityJobQueue(IJobQueue):
    def __init__(self):
        import heapq
        self._queue = []

    def append(self, job: IJob) -> None:
        heapq.heappush(self._queue, (job.priority, job))

    def pop(self) -> IJob | None:
        if self.is_empty():
            return None
        return heapq.heappop(self._queue)[1]

    def size(self) -> int:
        return len(self._queue)

    def clear(self) -> None:
        self._queue.clear()

    def is_empty(self) -> bool:
        return len(self._queue) == 0
```
