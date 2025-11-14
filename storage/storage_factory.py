from abc import ABC, abstractmethod

from storage.storage import IStorage


class IStorageFactory(ABC):
    @abstractmethod
    def create_storage(self) -> IStorage:
        pass
