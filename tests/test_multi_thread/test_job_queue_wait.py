import threading
import time
from typing import List, Optional

from python_library.job_queue.job_queue import JobQueue
from python_library.thread.multi_thread_manager import MultiThreadManager
from python_library.thread.queue_thread import QueueThread


def test_waiting_pop_wakes_on_append():
    queue: JobQueue[str] = JobQueue()
    result: List[Optional[str]] = []
    thread = threading.Thread(target=lambda: result.append(queue.pop(timeout=5)))
    thread.start()

    time.sleep(0.05)
    assert thread.is_alive()

    started = time.monotonic()
    queue.append("job")
    thread.join(timeout=1)

    assert not thread.is_alive()
    assert time.monotonic() - started < 1
    assert result == ["job"]


def test_pop_returns_none_after_timeout():
    queue: JobQueue[str] = JobQueue()

    started = time.monotonic()
    assert queue.pop(timeout=0.1) is None
    assert time.monotonic() - started >= 0.1


def test_pop_default_does_not_wait():
    queue: JobQueue[str] = JobQueue()

    started = time.monotonic()
    assert queue.pop() is None
    assert time.monotonic() - started < 0.05


class NamedWorker(QueueThread[str]):
    def action(self) -> None:
        pass


def test_same_name_threads_share_one_queue():
    manager: MultiThreadManager[str] = MultiThreadManager()
    worker1 = NamedWorker(name="worker")
    worker2 = NamedWorker(name="worker")

    manager.append(worker1)
    worker1.push_shared_queue("worker", "job")
    manager.append(worker2)

    assert worker2.pop_shared_queue("worker") == "job"


class WaitingWorker(QueueThread[str]):
    def action(self) -> None:
        while not self.is_stop():
            self.pop_shared_queue(self.name, timeout=0.1)


def test_manager_stop_ends_waiting_worker_within_timeout():
    manager: MultiThreadManager[str] = MultiThreadManager()
    worker = WaitingWorker()
    manager.append(worker)

    worker.start()
    time.sleep(0.05)
    assert worker.is_alive()

    manager.stop()
    worker.join(timeout=1)

    assert not worker.is_alive()
