from abc import ABC, abstractmethod

from python_library.db.db_client import IDBClient


class IDBInfoFactory(ABC):
    @abstractmethod
    def create_db_client(self) -> IDBClient:
        raise NotImplementedError()
