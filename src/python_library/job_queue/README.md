# job_queue

`IJob` 인스턴스를 담는 큐 추상화 패키지.
`thread`, `process` 패키지의 공유 작업 큐로 사용된다.

## 클래스 구조

```
IJobQueue (ABC)             # 큐 인터페이스
└── JobQueue                # deque 기반 기본 구현 (FIFO)
```

## IJobQueue 인터페이스

```python
class IJobQueue(ABC):
    def append(self, job: IJob) -> None: ...   # 뒤에 추가
    def pop(self, timeout: float = 0) -> IJob | None: ...  # 앞에서 제거 (FIFO)
    def size(self) -> int: ...
    def clear(self) -> None: ...
    def is_empty(self) -> bool: ...
```

---

## 설계 의도

`thread`와 `process` 패키지에서 직접 `list`나 `Queue`를 쓰지 않고 인터페이스를 통해 의존한다.
`JobQueue` 구현을 우선순위 큐, 지연 큐 등으로 교체할 수 있다.

현재 `JobQueue`는 `collections.deque` 기반이며 FIFO로 동작한다 (`append`로 뒤에서 추가, `pop`으로 앞에서 제거).

---

## 스레드 안전성

`JobQueue`는 내부 `Lock` + `Condition`으로 스스로 스레드 안전하다. 외부에서 락을 관리할 필요가 없다.

`pop(timeout)`으로 잡이 들어오기를 기다릴 수 있다(busy polling 불필요).

| `timeout` | 동작 |
|---|---|
| `0` (기본값) | 기다리지 않고 바로 반환 |
| 양수 | 최대 그 시간(초)만큼 기다린 뒤, 잡이 없으면 `None` |

무한 대기는 지원하지 않는다. 소비 스레드는 `while not self.is_stop()` 루프에서 유한 `timeout`으로 기다리며,
`stop()` 후 최대 `timeout` 안에 루프를 빠져나온다.

---

## 새 큐 구현 추가

```python
class PriorityJobQueue(IJobQueue):
    def __init__(self):
        import heapq
        self._queue = []

    def append(self, job: IJob) -> None:
        heapq.heappush(self._queue, (job.priority, job))

    def pop(self, timeout: float = 0) -> IJob | None:
        # 대기·스레드 안전성이 필요하면 JobQueue처럼 Condition으로 구현한다
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
