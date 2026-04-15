from abc import ABC, abstractmethod

from python_library.storage.storage import IStorage


class IStorageFactory(ABC):
    @abstractmethod
    def create_storage(self) -> IStorage:
        raise NotImplementedError()
