from abc import abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class IJobQueue(Generic[T]):
    @abstractmethod
    def append(self, item: T) -> None:
        pass

    @abstractmethod
    def pop(self) -> Optional[T]:
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
        self._job_queue: List[T] = list()

    def append(self, item: T) -> None:
        self._job_queue.append(item)

    def pop(self) -> Optional[T]:
        if self.is_empty():
            return None

        return self._job_queue.pop()

    def size(self) -> int:
        return len(self._job_queue)

    def clear(self) -> None:
        self._job_queue.clear()

    def is_empty(self) -> bool:
        return len(self._job_queue) == 0
