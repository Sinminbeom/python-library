from abc import ABC, abstractmethod
from typing import List

from python_library.db.db_row import IDBRow


class IDBClient(ABC):
    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def execute_query(self, sql: str, params: tuple | None = None) -> List[IDBRow]:
        raise NotImplementedError()

    @abstractmethod
    def execute_update(self, sql: str, params: tuple | None = None) -> None:
        raise NotImplementedError()

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError()
