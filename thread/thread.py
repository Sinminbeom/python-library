from abc import abstractmethod
from threading import Thread
from enum.enum import IENUM


class ThreadEvent:
    def __init__(self):
        self.vset = False

    def evt_set(self):
        self.vset = True
        return self.vset

    def evt_reset(self):
        self.vset = False
        return self.vset

    def evt_clear(self):
        self.vset = False

    def evt_is_set(self):
        return self.vset


class abThread(Thread):
    class E_THREAD_STATUS(IENUM):
        WAITING = "WAITING"
        RUNNING = "RUNNING"
        STOPING = "STOPING"

    def __init__(self) -> None:
        super().__init__()
        self.thread_status = abThread.E_THREAD_STATUS.WAITING
        self.event = ThreadEvent()

    def set_thread_status(self, _status):
        self.thread_status = _status

    def get_thread_status(self):
        return self.thread_status

    def stop(self):
        self.event.evt_set()
        self.set_thread_status(abThread.E_THREAD_STATUS.STOPING)

    def is_stop(self):
        return self.event.evt_is_set()

    def is_running(self):
        return not self.is_stop()

    def start(self):
        super().start()
        self.event.evt_clear()
        self.set_thread_status(abThread.E_THREAD_STATUS.RUNNING)

    def run(self):
        self.action()
        self.stop()

    @abstractmethod
    def action(self):
        print("abThread")
        pass
