from queue import Queue
from threading import Lock
from multiprocessing import Process, Event
from abc import ABC, abstractmethod
from typing import Optional, MutableMapping

from python_library.job.job import IJob
from python_library.utils.class_name_generator import ClassNameGenerator


class abProcess(ABC, Process):
    _name_gen = ClassNameGenerator()

    def __init__(self, name: str | None = None) -> None:
        name = self._name_gen(self, name)
        super().__init__(name=name)

        self._event = Event()

        self._shared_job_queue: Optional[Queue] = None
        self._shared_job_queue_lock: Optional[Lock] = None

        self._shared_queue: Optional[MutableMapping[str, Queue]] = None
        self._shared_queue_lock: Optional[MutableMapping[str, Lock]] = None

        pass

    ##########################################################################

    def set_shared_job_queue(
        self, shared_job_queue: Queue, shared_job_queue_lock: Lock
    ) -> None:
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

    def set_shared_queue(
        self,
        shared_queue: MutableMapping[str, Queue],
        shared_queue_lock: MutableMapping[str, Lock],
    ) -> None:
        self._shared_queue = shared_queue
        self._shared_queue_lock = shared_queue_lock

    def push_shared_queue(self, process_name: str, job: IJob) -> None:
        assert self._shared_queue_lock is not None

        with self._shared_queue_lock[process_name]:
            self._shared_queue[process_name].put(job)

    def pop_shared_queue(self, process_name: str) -> Optional[IJob]:
        assert self._shared_queue_lock is not None

        with self._shared_queue_lock[process_name]:
            if self._shared_queue[process_name].empty():
                return None

            return self._shared_queue[process_name].get()

    def size_shared_queue(self, process_name: str) -> int:
        assert self._shared_queue_lock is not None

        with self._shared_queue_lock[process_name]:
            return self._shared_queue[process_name].qsize()

    ##########################################################################

    def run(self) -> None:
        try:
            self.action()
        except Exception as e:
            raise e

    def start(self):
        self._event.clear()
        super().start()

    def is_stop(self) -> bool:
        return self._event.is_set()

    def is_running(self) -> bool:
        return self.is_alive() and not self.is_stop()

    @abstractmethod
    def action(self) -> None:
        print("abProcess action()")
        pass

    def stop(self):
        self._event.set()


class abProcessing(abProcess):
    def run(self) -> None:
        try:
            while not self.is_stop():
                self.action()
        except Exception as e:
            raise e

    @abstractmethod
    def action(self) -> None:
        # 작업
        pass
