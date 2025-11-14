from abc import ABC, abstractmethod

from storage.storage_client import IStorageClient


class IStorageInfoFactory(ABC):
    @abstractmethod
    def create_storage_client(self) -> IStorageClient:
        pass
