import time
from multiprocessing import Manager

from python_library.process.queue_process import QueueProcess


class StrEchoProcess(QueueProcess[str]):
    def action(self) -> None:
        for _ in range(50):
            item = self.pop_shared_queue(self.name)
            if item is None:
                time.sleep(0.01)
                continue
            assert isinstance(item, str)
            return


class IntEchoProcess(QueueProcess[int]):
    def action(self) -> None:
        for _ in range(50):
            item = self.pop_shared_queue(self.name)
            if item is None:
                time.sleep(0.01)
                continue
            assert isinstance(item, int)
            return


def _wire(process: QueueProcess) -> None:
    manager = Manager()
    shared_queue = manager.dict()
    shared_queue_lock = manager.dict()
    shared_queue[process.name] = manager.Queue()
    shared_queue_lock[process.name] = manager.Lock()
    process.set_shared_queue(shared_queue, shared_queue_lock)


def test_str_payload_round_trip():
    process = StrEchoProcess()
    _wire(process)

    process.push_shared_queue(process.name, "envelope-1")
    assert process.size_shared_queue(process.name) == 1

    popped = process.pop_shared_queue(process.name)
    assert popped == "envelope-1"
    assert process.size_shared_queue(process.name) == 0


def test_int_payload_round_trip():
    process = IntEchoProcess()
    _wire(process)

    process.push_shared_queue(process.name, 42)
    popped = process.pop_shared_queue(process.name)
    assert popped == 42


def test_pop_returns_none_when_empty():
    process = StrEchoProcess()
    _wire(process)

    assert process.pop_shared_queue(process.name) is None
