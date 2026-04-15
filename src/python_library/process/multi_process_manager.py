from multiprocessing import Manager
from threading import Lock
from queue import Queue
from typing import List, Optional, MutableMapping

from python_library.job.job import IJob
from python_library.process.process import abProcess
from python_library.thread.thread import abThread


class MultiProcessManager(abThread):
    def __init__(self) -> None:
        super().__init__()
        self._manager = Manager()

        self._process_list: List[abProcess] = list()

        self._shared_job_queue: Queue = self._manager.Queue()
        self._shared_job_queue_lock: Lock = self._manager.Lock()

        self._shared_queue: MutableMapping[str, Queue] = self._manager.dict()
        self._shared_queue_lock: MutableMapping[str, Lock] = self._manager.dict()

        self._allocate_shared_queue(self.name)

        pass

    def append(self, process: abProcess) -> None:
        process.set_shared_job_queue(
            self._shared_job_queue, self._shared_job_queue_lock
        )
        process.set_shared_queue(self._shared_queue, self._shared_queue_lock)

        self._allocate_shared_queue(process.name)

        self._process_list.append(process)
        pass

    def _allocate_shared_queue(self, process_name: str) -> None:
        if process_name not in self._shared_queue:
            self._shared_queue[process_name] = self._manager.Queue()
            self._shared_queue_lock[process_name] = self._manager.Lock()

    ##########################################################################

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

    def push_shared_queue(self, process_name: str, job: IJob) -> None:
        with self._shared_queue_lock[process_name]:
            self._shared_queue[process_name].put(job)

    def pop_shared_queue(self, process_name: str) -> Optional[IJob]:
        with self._shared_queue_lock[process_name]:
            if self._shared_queue[process_name].empty():
                return None

            return self._shared_queue[process_name].get()

    def size_shared_queue(self, process_name: str) -> int:
        with self._shared_queue_lock[process_name]:
            return self._shared_queue[process_name].qsize()

    ##########################################################################

    def run(self) -> None:
        try:
            for process in self._process_list:
                process.start()

            self.action()

            for process in self._process_list:
                process.join()

        except Exception as e:
            raise e

    def action(self) -> None:
        print("MultiProcessManager action()")
        pass

    def stop(self):
        for process in self._process_list:
            process.close()

        super().stop()
