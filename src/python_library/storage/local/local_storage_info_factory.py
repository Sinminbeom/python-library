from python_library.storage.local.local_storage_client import LocalStorageClient
from python_library.storage.storage_client import IStorageClient
from python_library.storage.storage_info_factory import IStorageInfoFactory


class LocalStorageInfoFactory(IStorageInfoFactory):
    def __init__(self):
        super().__init__()

    def create_storage_client(self) -> IStorageClient:
        storage_client = LocalStorageClient()
        return storage_client
