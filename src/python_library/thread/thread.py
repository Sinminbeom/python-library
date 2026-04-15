from abc import ABC, abstractmethod
from threading import Thread, Event
from typing import Optional

from python_library.utils.class_name_generator import ClassNameGenerator


class abThread(ABC, Thread):
    _name_gen = ClassNameGenerator()

    def __init__(self, name: Optional[str] = None) -> None:
        name = self._name_gen(self, name)
        super().__init__(name=name)

        self.event = Event()

    def stop(self):
        self.event.set()

    def is_stop(self):
        return self.event.is_set()

    def is_running(self):
        return self.is_alive() and not self.is_stop()

    def start(self) -> None:
        self.event.clear()
        super().start()

    # 기본 run 구조
    def run(self) -> None:
        try:
            self.action()
        except Exception as e:
            raise e

    @abstractmethod
    def action(self) -> None:
        print("abThread")
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
