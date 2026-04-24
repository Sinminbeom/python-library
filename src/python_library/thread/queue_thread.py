from abc import abstractmethod
from typing import Optional, Dict
from threading import Lock

from python_library.job.job import IJob
from python_library.job_queue.job_queue import IJobQueue, JobQueue
from python_library.thread.thread import IThread, abThread


class IQueueThread(IThread):

    @abstractmethod
    def set_shared_job_queue(self, shared_job_queue: IJobQueue, shared_job_queue_lock: Lock) -> None: ...

    @abstractmethod
    def push_shared_job_queue(self, job: IJob) -> None: ...

    @abstractmethod
    def pop_shared_job_queue(self) -> IJob | None: ...

    @abstractmethod
    def size_shared_job_queue(self) -> int: ...

    @abstractmethod
    def set_shared_queue(self, shared_queue: Dict[str, IJobQueue], shared_queue_lock: Dict[str, Lock]) -> None: ...

    @abstractmethod
    def push_shared_queue(self, name: str, job: IJob) -> None: ...

    @abstractmethod
    def pop_shared_queue(self, name: str) -> Optional[IJob]: ...

    @abstractmethod
    def size_shared_queue(self, name: str) -> int: ...


class QueueThread(abThread, IQueueThread):
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self._shared_job_queue: Optional[IJobQueue] = None
        self._shared_job_queue_lock: Optional[Lock] = None
        self._shared_queue: Optional[Dict[str, IJobQueue]] = None
        self._shared_queue_lock: Optional[Dict[str, Lock]] = None

    def _allocate_shared_queue(self) -> None:
        self._shared_queue[self.name] = JobQueue()
        self._shared_queue_lock[self.name] = Lock()

    ##########################################################################

    def set_shared_job_queue(self, shared_job_queue: IJobQueue, shared_job_queue_lock: Lock) -> None:
        self._shared_job_queue = shared_job_queue
        self._shared_job_queue_lock = shared_job_queue_lock

    def push_shared_job_queue(self, job: IJob) -> None:
        with self._shared_job_queue_lock:
            self._shared_job_queue.append(job)

    def pop_shared_job_queue(self) -> IJob | None:
        with self._shared_job_queue_lock:
            if self._shared_job_queue.is_empty():
                return None
            return self._shared_job_queue.pop()

    def size_shared_job_queue(self) -> int:
        with self._shared_job_queue_lock:
            return self._shared_job_queue.size()

    ##########################################################################

    def set_shared_queue(self, shared_queue: Dict[str, IJobQueue], shared_queue_lock: Dict[str, Lock]) -> None:
        self._shared_queue = shared_queue
        self._shared_queue_lock = shared_queue_lock
        self._allocate_shared_queue()

    def push_shared_queue(self, name: str, job: IJob) -> None:
        assert self._shared_queue_lock is not None
        with self._shared_queue_lock[name]:
            self._shared_queue[name].append(job)

    def pop_shared_queue(self, name: str) -> Optional[IJob]:
        assert self._shared_queue_lock is not None
        with self._shared_queue_lock[name]:
            if self._shared_queue[name].is_empty():
                return None
            return self._shared_queue[name].pop()

    def size_shared_queue(self, name: str) -> int:
        assert self._shared_queue_lock is not None
        with self._shared_queue_lock[name]:
            return self._shared_queue[name].size()

    @abstractmethod
    def action(self) -> None:
        pass


class QueueThreading(QueueThread):
    def run(self) -> None:
        try:
            while not self.is_stop():
                self.action()
        except Exception as e:
            raise e

    @abstractmethod
    def action(self) -> None:
        pass
