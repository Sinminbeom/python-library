from typing import List, Optional

from storage.storage_file import StorageFile
from storage.storage import IStorage
from storage.storage_client import IStorageClient


class S3Storage(IStorage):
    def __init__(self) -> None:
        self._storage_client: Optional[IStorageClient] = None

    def connect(self) -> None:
        if self._storage_client is None:
            raise RuntimeError("The storage client has not been initialized")
        self._storage_client.connect()
        pass

    def disconnect(self) -> None:
        if self._storage_client is None:
            raise RuntimeError("The storage client has not been initialized")
        self._storage_client.disconnect()
        pass

    def upload(self, src_path: str, dst_path: str) -> None:
        if self._storage_client is None:
            raise RuntimeError("The storage client has not been initialized")
        self._storage_client.upload(src_path, dst_path)
        pass

    def download(self, src_path: str, dst_path: str) -> None:
        if self._storage_client is None:
            raise RuntimeError("The storage client has not been initialized")
        self._storage_client.download(src_path, dst_path)
        pass

    def get_file_list(self, path: str) -> List[StorageFile]:
        if self._storage_client is None:
            raise RuntimeError("The storage client has not been initialized")
        return self._storage_client.get_file_list(path)

    def is_exists(self, path: str) -> bool:
        if self._storage_client is None:
            raise RuntimeError("The storage client has not been initialized")
        return self._storage_client.is_exists(path)

    def read(self, path: str) -> str:
        if self._storage_client is None:
            raise RuntimeError("The storage client has not been initialized")
        return self._storage_client.read(path)

    def copy(
        self, src_root_path: str, src_path: str, dst_root_path: str, dst_path: str
    ) -> None:
        if self._storage_client is None:
            raise RuntimeError("The storage client has not been initialized")
        self._storage_client.copy(src_root_path, src_path, dst_root_path, dst_path)
        pass

    def set_storage_client(self, storage_client: IStorageClient) -> None:
        self._storage_client = storage_client
        pass
