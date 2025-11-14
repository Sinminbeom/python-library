from abc import ABC, abstractmethod
from typing import TypeVar, Generic


class IDelegate(ABC):
    pass


T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
R = TypeVar("R")


class Action(IDelegate):
    @abstractmethod
    def invork(self):
        pass


class Action1(IDelegate, Generic[T1]):
    @abstractmethod
    def invork(self, t1: T1):
        pass


class Action2(IDelegate, Generic[T1, T2]):
    @abstractmethod
    def invork(self, t1: T1, t2: T2):
        pass


class Action3(IDelegate, Generic[T1, T2, T3]):
    @abstractmethod
    def invork(self, t1: T1, t2: T2, t3: T3):
        pass


class Action4(IDelegate, Generic[T1, T2, T3, T4]):
    @abstractmethod
    def invork(self, t1: T1, t2: T2, t3: T3, t4: T4):
        pass


class Action5(IDelegate, Generic[T1, T2, T3, T4, T5]):
    @abstractmethod
    def invork(self, t1: T1, t2: T2, t3: T3, t4: T4, t5: T5):
        pass


class Action6(IDelegate, Generic[T1, T2, T3, T4, T5, T6]):
    @abstractmethod
    def invork(self, t1: T1, t2: T2, t3: T3, t4: T4, t5: T5, t6: T6):
        pass


class Func(IDelegate, Generic[R]):
    @abstractmethod
    def invork(self) -> R:
        pass


class Func1(IDelegate, Generic[T1, R]):
    @abstractmethod
    def invork(self, t1: T1) -> R:
        pass


class Func2(IDelegate, Generic[T1, T2, R]):
    @abstractmethod
    def invork(self, t1: T1, t2: T2) -> R:
        pass


class Func3(IDelegate, Generic[T1, T2, T3, R]):
    @abstractmethod
    def invork(self, t1: T1, t2: T2, t3: T3) -> R:
        pass


class Func4(IDelegate, Generic[T1, T2, T3, T4, R]):
    @abstractmethod
    def invork(self, t1: T1, t2: T2, t3: T3, t4, T4) -> R:
        pass


class Func5(IDelegate, Generic[T1, T2, T3, T4, T5, R]):
    @abstractmethod
    def invork(self, t1: T1, t2: T2, t3: T3, t4, T4, t5: T5) -> R:
        pass


class Func6(IDelegate, Generic[T1, T2, T3, T4, T5, T6, R]):
    @abstractmethod
    def invork(self, t1: T1, t2: T2, t3: T3, t4, T4, t5: T5, t6: T6) -> R:
        pass
