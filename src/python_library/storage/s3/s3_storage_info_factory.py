from python_library.storage.s3.s3_storage_client import S3StorageClient
from python_library.storage.storage_client import IStorageClient
from python_library.storage.storage_info_factory import IStorageInfoFactory


class S3StorageInfoFactory(IStorageInfoFactory):
    def __init__(self):
        super().__init__()

    def create_storage_client(self) -> IStorageClient:
        storage_client = S3StorageClient()
        return storage_client
