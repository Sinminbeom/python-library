from abc import abstractmethod
from typing import List, Optional
from threading import Lock

from job.job import IJob


class IJobQueue:
    @abstractmethod
    def append(self, job: IJob) -> None:
        pass

    @abstractmethod
    def pop(self) -> Optional[IJob]:
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


class JobQueue(IJobQueue):
    def __init__(self) -> None:
        self._job_queue: List[IJob] = list()
        self._lock = Lock()

    def append(self, job: IJob) -> None:
        with self._lock:
            self._job_queue.append(job)

    def pop(self) -> Optional[IJob]:
        if self.is_empty():
            return None

        with self._lock:
            return self._job_queue.pop()

    def size(self) -> int:
        with self._lock:
            return len(self._job_queue)

    def clear(self) -> None:
        with self._lock:
            self._job_queue.clear()

    def is_empty(self) -> bool:
        with self._lock:
            return len(self._job_queue) == 0
