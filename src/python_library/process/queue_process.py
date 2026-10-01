from abc import abstractmethod
from queue import Empty, Queue
from typing import Generic, MutableMapping, Optional, TypeVar

from python_library.process.process import IProcess, abProcess

T = TypeVar("T")


def get_or_none(queue: Queue[T], timeout: float) -> Optional[T]:
    try:
        return queue.get(timeout=timeout)
    except Empty:
        return None


class IQueueProcess(IProcess, Generic[T]):
    @abstractmethod
    def set_shared_job_queue(self, shared_job_queue: Queue) -> None: ...

    @abstractmethod
    def push_shared_job_queue(self, item: T) -> None: ...

    @abstractmethod
    def pop_shared_job_queue(self, timeout: float = 0) -> Optional[T]: ...

    @abstractmethod
    def size_shared_job_queue(self) -> int: ...

    @abstractmethod
    def set_shared_queue(self, shared_queue: MutableMapping[str, Queue]) -> None: ...

    @abstractmethod
    def push_shared_queue(self, process_name: str, item: T) -> None: ...

    @abstractmethod
    def pop_shared_queue(
        self, process_name: str, timeout: float = 0
    ) -> Optional[T]: ...

    @abstractmethod
    def size_shared_queue(self, process_name: str) -> int: ...


class QueueProcess(abProcess, IQueueProcess[T], Generic[T]):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name=name)
        self._shared_job_queue: Optional[Queue] = None
        self._shared_queue: Optional[MutableMapping[str, Queue]] = None

    ##########################################################################

    def set_shared_job_queue(self, shared_job_queue: Queue) -> None:
        self._shared_job_queue = shared_job_queue

    def push_shared_job_queue(self, item: T) -> None:
        self._shared_job_queue.put(item)

    def pop_shared_job_queue(self, timeout: float = 0) -> Optional[T]:
        assert self._shared_job_queue is not None
        return get_or_none(self._shared_job_queue, timeout)

    def size_shared_job_queue(self) -> int:
        return self._shared_job_queue.qsize()

    ##########################################################################

    def set_shared_queue(self, shared_queue: MutableMapping[str, Queue]) -> None:
        self._shared_queue = shared_queue

    def push_shared_queue(self, process_name: str, item: T) -> None:
        self._shared_queue[process_name].put(item)

    def pop_shared_queue(self, process_name: str, timeout: float = 0) -> Optional[T]:
        return get_or_none(self._shared_queue[process_name], timeout)

    def size_shared_queue(self, process_name: str) -> int:
        return self._shared_queue[process_name].qsize()


class QueueProcessing(QueueProcess[T], Generic[T]):
    def run(self) -> None:
        while not self.is_stop():
            try:
                self.action()
            except Exception as e:
                self.on_exception(e)

    @abstractmethod
    def action(self) -> None:
        pass
