import time
from threading import Lock
from typing import Dict

from python_library.job_queue.job_queue import IJobQueue, JobQueue
from python_library.thread.queue_thread import QueueThread


class StrEchoThread(QueueThread[str]):
    def action(self) -> None:
        for _ in range(50):
            item = self.pop_shared_queue(self.name)
            if item is None:
                time.sleep(0.01)
                continue
            assert isinstance(item, str)
            return


class IntEchoThread(QueueThread[int]):
    def action(self) -> None:
        for _ in range(50):
            item = self.pop_shared_queue(self.name)
            if item is None:
                time.sleep(0.01)
                continue
            assert isinstance(item, int)
            return


def _wire(thread: QueueThread) -> None:
    shared_queue: Dict[str, IJobQueue] = dict()
    shared_queue_lock: Dict[str, Lock] = dict()
    thread.set_shared_queue(shared_queue, shared_queue_lock)


def test_str_payload_round_trip():
    thread = StrEchoThread()
    _wire(thread)

    thread.push_shared_queue(thread.name, "envelope-1")
    assert thread.size_shared_queue(thread.name) == 1

    popped = thread.pop_shared_queue(thread.name)
    assert popped == "envelope-1"
    assert thread.size_shared_queue(thread.name) == 0


def test_int_payload_round_trip():
    thread = IntEchoThread()
    _wire(thread)

    thread.push_shared_queue(thread.name, 42)
    popped = thread.pop_shared_queue(thread.name)
    assert popped == 42


def test_pop_returns_none_when_empty():
    thread = StrEchoThread()
    _wire(thread)

    assert thread.pop_shared_queue(thread.name) is None


def test_job_queue_generic_str():
    queue: JobQueue[str] = JobQueue()
    queue.append("a")
    queue.append("b")

    assert queue.size() == 2
    assert queue.is_empty() is False

    popped = queue.pop()
    assert popped == "b"  # list.pop() is LIFO

    queue.clear()
    assert queue.is_empty() is True
