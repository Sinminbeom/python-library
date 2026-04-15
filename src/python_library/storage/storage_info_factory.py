from abc import ABC, abstractmethod

from python_library.storage.storage import IStorageClient


class IStorageInfoFactory(ABC):
    @abstractmethod
    def create_storage_client(self) -> IStorageClient:
        raise NotImplementedError()
