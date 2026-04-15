from threading import Lock
from typing import List, Dict, Optional
from abc import abstractmethod

from python_library.job_queue.job_queue import IJobQueue, JobQueue
from python_library.thread.thread import abThread
from python_library.thread.worker_thread import abWorkerThread


class MultiThreadManager(abWorkerThread):
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)

        self._threads: List[abThread] = list()

        self._shared_job_queue: IJobQueue = JobQueue()
        self._shared_job_queue_lock: Lock = Lock()

        self._shared_queue: Dict[str, IJobQueue] = dict()
        self._shared_queue_lock: Dict[str, Lock] = dict()

        self._allocate_shared_queue()

    def append(self, thread: abWorkerThread):
        thread.set_shared_job_queue(self._shared_job_queue, self._shared_job_queue_lock)
        thread.set_shared_queue(self._shared_queue, self._shared_queue_lock)

        self._threads.append(thread)

    def run(self) -> None:
        try:
            for thread in self._threads:
                thread.start()

            self.action()

            for thread in self._threads:
                thread.join()

        except Exception as e:
            raise e

    @abstractmethod
    def action(self) -> None:
        print("MultiThreadManager action()")
        pass

    def stop(self):
        for thread in self._threads:
            thread.stop()

        super().stop()
