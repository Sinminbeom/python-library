from typing import List

from job.job import IJob
from job_queue.job_queue import JobQueue, IJobQueue
from thread.thread import abThread
from thread.work_thread import WorkThread


class MultiThreadManager(abThread):
    def __init__(self, thread_count: int) -> None:
        super().__init__()

        self._thread_count = thread_count
        self._threads: List[abThread] = list()

        self._job_queue: IJobQueue = JobQueue()

        self.init()

    def init(self) -> None:
        for cnt in range(self._thread_count):
            self._threads.append(WorkThread(self._job_queue))

    def append(self, job: IJob) -> None:
        self._job_queue.append(job)

    def start(self) -> None:
        for thread in self._threads:
            thread.start()

        for thread in self._threads:
            thread.join()
