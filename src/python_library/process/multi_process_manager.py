from multiprocessing import Manager
from queue import Queue
from typing import Generic, List, MutableMapping, Optional, TypeVar

from python_library.process.queue_process import IQueueProcess, get_or_none
from python_library.thread.thread import abThread

T = TypeVar("T")


class MultiProcessManager(abThread, Generic[T]):
    def __init__(self) -> None:
        super().__init__()
        self._manager = Manager()

        self._process_list: List[IQueueProcess[T]] = list()

        self._shared_job_queue: Queue = self._manager.Queue()
        self._shared_queue: MutableMapping[str, Queue] = self._manager.dict()

        self._allocate_shared_queue(self.name)

    def append(self, process: IQueueProcess[T]) -> None:
        process.set_shared_job_queue(self._shared_job_queue)
        process.set_shared_queue(self._shared_queue)

        self._allocate_shared_queue(process.name)

        self._process_list.append(process)

    def _allocate_shared_queue(self, process_name: str) -> None:
        if process_name not in self._shared_queue:
            self._shared_queue[process_name] = self._manager.Queue()

    ##########################################################################

    def push_shared_job_queue(self, item: T) -> None:
        self._shared_job_queue.put(item)

    def pop_shared_job_queue(self, timeout: float = 0) -> Optional[T]:
        return get_or_none(self._shared_job_queue, timeout)

    def size_shared_job_queue(self) -> int:
        return self._shared_job_queue.qsize()

    ##########################################################################

    def push_shared_queue(self, process_name: str, item: T) -> None:
        self._shared_queue[process_name].put(item)

    def pop_shared_queue(self, process_name: str, timeout: float = 0) -> Optional[T]:
        return get_or_none(self._shared_queue[process_name], timeout)

    def size_shared_queue(self, process_name: str) -> int:
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
            self.on_exception(e)

    def action(self) -> None:
        pass

    def stop(self):
        for process in self._process_list:
            process.stop()

        super().stop()
