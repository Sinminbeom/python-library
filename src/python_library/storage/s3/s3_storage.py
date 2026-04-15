from typing import List, Optional

from python_library.storage.storage_file import StorageFile
from python_library.storage.storage import IStorage
from python_library.storage.storage_client import IStorageClient
from python_library.storage.upload_options import UploadOptions


class S3Storage(IStorage):
    def __init__(self) -> None:
        self._storage_client: Optional[IStorageClient] = None

    def connect(self) -> None:
        self._storage_client.connect()

    def disconnect(self) -> None:
        self._storage_client.disconnect()

    def upload(
        self, src_path: str, dst_path: str, options: UploadOptions | None = None
    ) -> None:
        self._storage_client.upload(src_path, dst_path, options=options)

    def download(self, src_path: str, dst_path: str) -> None:
        self._storage_client.download(src_path, dst_path)

    def get_file_list(self, path: str) -> List[StorageFile]:
        return self._storage_client.get_file_list(path)

    def is_exists(self, path: str) -> bool:
        return self._storage_client.is_exists(path)

    def read(self, path: str) -> bytes:
        return self._storage_client.read(path)

    def write(
        self, path: str, data: bytes, options: UploadOptions | None = None
    ) -> None:
        self._storage_client.write(path, data, options)

    def copy(self, src_path: str, dst_path: str) -> None:
        self._storage_client.copy(src_path, dst_path)

    def to_url(self, path: str) -> str:
        return self._storage_client.to_url(path)

    def set_storage_client(self, storage_client: IStorageClient) -> None:
        self._storage_client = storage_client
