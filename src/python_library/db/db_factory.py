from abc import ABC, abstractmethod

from python_library.db.db import IDB


class IDBFactory(ABC):
    @abstractmethod
    def create_db(self) -> IDB:
        raise NotImplementedError()
