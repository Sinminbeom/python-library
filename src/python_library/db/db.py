from abc import abstractmethod, ABC
from typing import List

from python_library.db.db_client import IDBClient
from python_library.db.db_row import IDBRow


class IDB(ABC):
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

    @abstractmethod
    def set_db_client(self, db_client: IDBClient) -> None:
        raise NotImplementedError()
