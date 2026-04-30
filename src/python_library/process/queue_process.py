from queue import Queue
from threading import Lock
from abc import abstractmethod
from typing import Generic, MutableMapping, Optional, TypeVar

from python_library.job.job import IJob
from python_library.process.process import IProcess, abProcess

T = TypeVar("T")


class IQueueProcess(IProcess, Generic[T]):

    @abstractmethod
    def set_shared_job_queue(self, shared_job_queue: Queue, shared_job_queue_lock: Lock) -> None: ...

    @abstractmethod
    def push_shared_job_queue(self, job: IJob) -> None: ...

    @abstractmethod
    def pop_shared_job_queue(self) -> IJob | None: ...

    @abstractmethod
    def size_shared_job_queue(self) -> int: ...

    @abstractmethod
    def set_shared_queue(self, shared_queue: MutableMapping[str, Queue], shared_queue_lock: MutableMapping[str, Lock]) -> None: ...

    @abstractmethod
    def push_shared_queue(self, process_name: str, item: T) -> None: ...

    @abstractmethod
    def pop_shared_queue(self, process_name: str) -> Optional[T]: ...

    @abstractmethod
    def size_shared_queue(self, process_name: str) -> int: ...


class QueueProcess(abProcess, IQueueProcess[T], Generic[T]):

    def __init__(self, name: str | None = None) -> None:
        super().__init__(name=name)
        self._shared_job_queue: Optional[Queue] = None
        self._shared_job_queue_lock: Optional[Lock] = None
        self._shared_queue: Optional[MutableMapping[str, Queue]] = None
        self._shared_queue_lock: Optional[MutableMapping[str, Lock]] = None

    ##########################################################################

    def set_shared_job_queue(self, shared_job_queue: Queue, shared_job_queue_lock: Lock) -> None:
        self._shared_job_queue = shared_job_queue
        self._shared_job_queue_lock = shared_job_queue_lock

    def push_shared_job_queue(self, job: IJob) -> None:
        with self._shared_job_queue_lock:
            self._shared_job_queue.put(job)

    def pop_shared_job_queue(self) -> IJob | None:
        with self._shared_job_queue_lock:
            if self._shared_job_queue.empty():
                return None
            return self._shared_job_queue.get()

    def size_shared_job_queue(self) -> int:
        with self._shared_job_queue_lock:
            return self._shared_job_queue.qsize()

    ##########################################################################

    def set_shared_queue(self, shared_queue: MutableMapping[str, Queue], shared_queue_lock: MutableMapping[str, Lock]) -> None:
        self._shared_queue = shared_queue
        self._shared_queue_lock = shared_queue_lock

    def push_shared_queue(self, process_name: str, item: T) -> None:
        assert self._shared_queue_lock is not None
        with self._shared_queue_lock[process_name]:
            self._shared_queue[process_name].put(item)

    def pop_shared_queue(self, process_name: str) -> Optional[T]:
        assert self._shared_queue_lock is not None
        with self._shared_queue_lock[process_name]:
            if self._shared_queue[process_name].empty():
                return None
            return self._shared_queue[process_name].get()

    def size_shared_queue(self, process_name: str) -> int:
        assert self._shared_queue_lock is not None
        with self._shared_queue_lock[process_name]:
            return self._shared_queue[process_name].qsize()


class QueueProcessing(QueueProcess[T], Generic[T]):
    def run(self) -> None:
        try:
            while not self.is_stop():
                self.action()
        except Exception as e:
            raise e

    @abstractmethod
    def action(self) -> None:
        pass
