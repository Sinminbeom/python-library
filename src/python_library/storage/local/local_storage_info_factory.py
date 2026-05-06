from python_library.storage.local.local_storage_client import LocalStorageClient
from python_library.storage.storage_client import IStorageClient
from python_library.storage.storage_info_factory import IStorageInfoFactory


class LocalStorageInfoFactory(IStorageInfoFactory):
    def __init__(self, root_dir: str):
        super().__init__()
        self._root_dir: str = root_dir

    def create_storage_client(self) -> IStorageClient:
        storage_client = LocalStorageClient(self._root_dir)
        return storage_client
