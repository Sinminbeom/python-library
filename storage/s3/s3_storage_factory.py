from storage.s3.s3_storage import S3Storage
from storage.storage import IStorage
from storage.storage_factory import IStorageFactory
from storage.storage_info_factory import IStorageInfoFactory


class S3StorageFactory(IStorageFactory):
    def __init__(self, storage_info_factory: IStorageInfoFactory):
        self._storage_info_factory: IStorageInfoFactory = storage_info_factory

    def create_storage(self) -> IStorage:
        storage = S3Storage()
        storage.set_storage_client(self._storage_info_factory.create_storage_client())
        return storage
