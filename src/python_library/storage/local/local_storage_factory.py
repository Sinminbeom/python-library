from python_library.storage.local.local_storage import LocalStorage
from python_library.storage.storage import IStorage
from python_library.storage.storage_factory import IStorageFactory
from python_library.storage.storage_info_factory import IStorageInfoFactory


class LocalStorageFactory(IStorageFactory):
    def __init__(self, storage_info_factory: IStorageInfoFactory):
        self._storage_info_factory: IStorageInfoFactory = storage_info_factory

    def create_storage(self) -> IStorage:
        storage = LocalStorage()
        storage.set_storage_client(self._storage_info_factory.create_storage_client())
        return storage
