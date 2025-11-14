from abc import ABC, abstractmethod
from typing import List

from storage.storage_file import StorageFile


class IStorageClient(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def upload(self, src_path: str, dst_path: str) -> None:
        pass

    @abstractmethod
    def download(self, src_path: str, dst_path: str) -> None:
        pass

    @abstractmethod
    def get_file_list(self, path: str) -> List[StorageFile]:
        pass

    @abstractmethod
    def is_exists(self, path: str) -> bool:
        pass

    @abstractmethod
    def read(self, path: str) -> str:
        pass

    @abstractmethod
    def copy(
        self, src_root_path: str, src_path: str, dst_root_path: str, dst_path: str
    ) -> None:
        pass
