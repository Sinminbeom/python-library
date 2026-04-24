from multiprocessing import Process, Event
from abc import ABC, abstractmethod

from python_library.utils.class_name_generator import ClassNameGenerator


class IProcess(ABC):

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
    def close(self) -> None: ...

    @abstractmethod
    def is_stop(self) -> bool: ...

    @abstractmethod
    def is_running(self) -> bool: ...


class abProcess(Process, IProcess):
    _name_gen = ClassNameGenerator()

    def __init__(self, name: str | None = None) -> None:
        name = self._name_gen(self, name)
        super().__init__(name=name)
        self._event = Event()

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

    def stop(self):
        self._event.set()

    @abstractmethod
    def action(self) -> None:
        pass


class abProcessing(abProcess):
    def run(self) -> None:
        try:
            while not self.is_stop():
                self.action()
        except Exception as e:
            raise e

    @abstractmethod
    def action(self) -> None:
        pass
