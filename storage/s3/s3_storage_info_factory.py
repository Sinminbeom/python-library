from storage.s3.s3_storage_client import S3StorageClient
from storage.storage_client import IStorageClient
from storage.storage_info_factory import IStorageInfoFactory


class S3StorageInfoFactory(IStorageInfoFactory):
    def __init__(self, access_key_id: str, secret_access_key: str, bucket_name: str):
        self._access_key_id: str = access_key_id
        self._secret_access_key: str = secret_access_key
        self._bucket_name: str = bucket_name

    def create_storage_client(self) -> IStorageClient:
        storage_client = S3StorageClient(
            self._access_key_id, self._secret_access_key, self._bucket_name
        )
        return storage_client
