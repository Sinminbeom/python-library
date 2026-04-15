from abc import abstractmethod
from typing import List, Optional

from python_library.job.job import IJob


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

    def append(self, job: IJob) -> None:
        self._job_queue.append(job)

    def pop(self) -> Optional[IJob]:
        if self.is_empty():
            return None

        return self._job_queue.pop()

    def size(self) -> int:
        return len(self._job_queue)

    def clear(self) -> None:
        self._job_queue.clear()

    def is_empty(self) -> bool:
        return len(self._job_queue) == 0
