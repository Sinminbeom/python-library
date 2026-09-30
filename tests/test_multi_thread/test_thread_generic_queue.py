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
    assert popped == "a"

    queue.clear()
    assert queue.is_empty() is True


def test_job_queue_pops_in_fifo_order():
    queue: JobQueue[int] = JobQueue()
    for item in range(5):
        queue.append(item)

    assert [queue.pop() for _ in range(5)] == [0, 1, 2, 3, 4]
    assert queue.pop() is None


def test_shared_queue_pops_in_fifo_order():
    thread = IntEchoThread()
    _wire(thread)

    for item in range(3):
        thread.push_shared_queue(thread.name, item)

    assert [thread.pop_shared_queue(thread.name) for _ in range(3)] == [0, 1, 2]


def test_shared_job_queue_generic_payload():
    thread = StrEchoThread()
    job_queue: JobQueue[str] = JobQueue()
    thread.set_shared_job_queue(job_queue, Lock())

    thread.push_shared_job_queue("envelope-job-1")
    assert thread.size_shared_job_queue() == 1

    popped = thread.pop_shared_job_queue()
    assert popped == "envelope-job-1"
    assert thread.size_shared_job_queue() == 0
