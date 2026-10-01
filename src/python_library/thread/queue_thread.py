from abc import abstractmethod
from typing import Dict, Generic, Optional, TypeVar

from python_library.job_queue.job_queue import IJobQueue, JobQueue
from python_library.thread.thread import IThread, abThread

T = TypeVar("T")


class IQueueThread(IThread, Generic[T]):
    @abstractmethod
    def set_shared_job_queue(self, shared_job_queue: IJobQueue[T]) -> None: ...

    @abstractmethod
    def push_shared_job_queue(self, item: T) -> None: ...

    @abstractmethod
    def pop_shared_job_queue(self, timeout: float = 0) -> Optional[T]: ...

    @abstractmethod
    def size_shared_job_queue(self) -> int: ...

    @abstractmethod
    def set_shared_queue(self, shared_queue: Dict[str, IJobQueue[T]]) -> None: ...

    @abstractmethod
    def push_shared_queue(self, name: str, item: T) -> None: ...

    @abstractmethod
    def pop_shared_queue(self, name: str, timeout: float = 0) -> Optional[T]: ...

    @abstractmethod
    def size_shared_queue(self, name: str) -> int: ...


class QueueThread(abThread, IQueueThread[T], Generic[T]):
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self._shared_job_queue: Optional[IJobQueue[T]] = None
        self._shared_queue: Optional[Dict[str, IJobQueue[T]]] = None

    def _allocate_shared_queue(self) -> None:
        self._shared_queue.setdefault(self.name, JobQueue[T]())

    ##########################################################################

    def set_shared_job_queue(self, shared_job_queue: IJobQueue[T]) -> None:
        self._shared_job_queue = shared_job_queue

    def push_shared_job_queue(self, item: T) -> None:
        self._shared_job_queue.append(item)

    def pop_shared_job_queue(self, timeout: float = 0) -> Optional[T]:
        return self._shared_job_queue.pop(timeout)

    def size_shared_job_queue(self) -> int:
        return self._shared_job_queue.size()

    ##########################################################################

    def set_shared_queue(self, shared_queue: Dict[str, IJobQueue[T]]) -> None:
        self._shared_queue = shared_queue
        self._allocate_shared_queue()

    def push_shared_queue(self, name: str, item: T) -> None:
        self._shared_queue[name].append(item)

    def pop_shared_queue(self, name: str, timeout: float = 0) -> Optional[T]:
        return self._shared_queue[name].pop(timeout)

    def size_shared_queue(self, name: str) -> int:
        return self._shared_queue[name].size()

    @abstractmethod
    def action(self) -> None:
        pass


class QueueThreading(QueueThread[T], Generic[T]):
    def run(self) -> None:
        while not self.is_stop():
            try:
                self.action()
            except Exception as e:
                self.on_exception(e)

    @abstractmethod
    def action(self) -> None:
        pass
