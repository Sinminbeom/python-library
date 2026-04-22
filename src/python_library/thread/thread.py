from abc import ABC, abstractmethod
from threading import Thread, Event, Lock
from typing import Optional, Dict

from python_library.job.job import IJob
from python_library.job_queue.job_queue import IJobQueue
from python_library.utils.class_name_generator import ClassNameGenerator


class IThread(ABC):

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def action(self) -> None: ...

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def join(self) -> None: ...

    @abstractmethod
    def is_stop(self) -> bool: ...

    @abstractmethod
    def is_running(self) -> bool: ...


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


class abThread(Thread, IThread):
    _name_gen = ClassNameGenerator()

    def __init__(self, name: Optional[str] = None) -> None:
        name = self._name_gen(self, name)
        super().__init__(name=name)
        self.event = Event()

    def start(self) -> None:
        self.event.clear()
        super().start()

    def stop(self) -> None:
        self.event.set()

    def is_stop(self) -> bool:
        return self.event.is_set()

    def is_running(self) -> bool:
        return self.is_alive() and not self.is_stop()

    def run(self) -> None:
        try:
            self.action()
        except Exception as e:
            raise e

    @abstractmethod
    def action(self) -> None:
        pass


class abThreading(abThread):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        try:
            while not self.is_stop():
                self.action()
        except Exception as e:
            raise e
