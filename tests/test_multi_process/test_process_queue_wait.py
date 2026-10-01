import threading
import time
from typing import List, Optional

from python_library.process.multi_process_manager import MultiProcessManager
from python_library.process.queue_process import QueueProcess, QueueProcessing


class IdleProcess(QueueProcess[str]):
    def action(self) -> None:
        pass


def test_pop_returns_none_after_timeout():
    manager: MultiProcessManager[str] = MultiProcessManager()
    process = IdleProcess()
    manager.append(process)

    started = time.monotonic()
    assert process.pop_shared_queue(process.name, timeout=0.1) is None
    assert time.monotonic() - started >= 0.1


def test_waiting_pop_receives_pushed_item():
    manager: MultiProcessManager[str] = MultiProcessManager()
    process = IdleProcess()
    manager.append(process)

    result: List[Optional[str]] = []
    waiter = threading.Thread(
        target=lambda: result.append(process.pop_shared_job_queue(timeout=5))
    )
    waiter.start()
    time.sleep(0.05)
    assert waiter.is_alive()

    started = time.monotonic()
    manager.push_shared_job_queue("job")
    waiter.join(timeout=1)

    assert not waiter.is_alive()
    assert time.monotonic() - started < 1
    assert result == ["job"]


class WaitingProcess(QueueProcessing[str]):
    def action(self) -> None:
        self.pop_shared_queue(self.name, timeout=0.1)


def test_manager_stop_ends_waiting_process_within_timeout():
    manager: MultiProcessManager[str] = MultiProcessManager()
    process = WaitingProcess()
    manager.append(process)

    process.start()
    time.sleep(0.2)
    assert process.is_alive()

    manager.stop()
    process.join(timeout=5)

    assert not process.is_alive()
