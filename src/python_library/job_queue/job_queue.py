from abc import abstractmethod
from collections import deque
from threading import Condition, Lock
from typing import Deque, Generic, Optional, TypeVar

T = TypeVar("T")


class IJobQueue(Generic[T]):
    @abstractmethod
    def append(self, item: T) -> None:
        pass

    @abstractmethod
    def pop(self, timeout: float = 0) -> Optional[T]:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass


class JobQueue(IJobQueue[T], Generic[T]):
    def __init__(self) -> None:
        self._job_queue: Deque[T] = deque()
        self._lock = Lock()
        self._not_empty = Condition(self._lock)

    def append(self, item: T) -> None:
        with self._not_empty:
            self._job_queue.append(item)
            self._not_empty.notify()

    def pop(self, timeout: float = 0) -> Optional[T]:
        with self._not_empty:
            if not self._not_empty.wait_for(lambda: len(self._job_queue) > 0, timeout):
                return None
            return self._job_queue.popleft()

    def size(self) -> int:
        with self._lock:
            return len(self._job_queue)

    def clear(self) -> None:
        with self._lock:
            self._job_queue.clear()

    def is_empty(self) -> bool:
        with self._lock:
            return len(self._job_queue) == 0
