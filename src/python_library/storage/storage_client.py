from abc import ABC, abstractmethod
from typing import List

from python_library.storage.storage_file import StorageFile
from python_library.storage.upload_options import UploadOptions


class IStorageClient(ABC):
    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def upload(
        self, src_path: str, dst_path: str, options: UploadOptions | None = None
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def download(self, src_path: str, dst_path: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_file_list(self, path: str) -> List[StorageFile]:
        raise NotImplementedError()

    @abstractmethod
    def is_exists(self, path: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def read(self, path: str) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def write(
        self, path: str, data: bytes, options: UploadOptions | None = None
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def copy(self, src_path: str, dst_path: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def to_url(self, path: str) -> str:
        raise NotImplementedError()
