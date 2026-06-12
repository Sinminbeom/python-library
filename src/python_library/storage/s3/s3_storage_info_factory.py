from typing import Optional

from python_library.storage.s3.s3_storage_client import S3StorageClient
from python_library.storage.storage_client import IStorageClient
from python_library.storage.storage_info_factory import IStorageInfoFactory


class S3StorageInfoFactory(IStorageInfoFactory):
    def __init__(
        self,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        session_token: Optional[str] = None,
    ) -> None:
        super().__init__()
        self._access_key = access_key
        self._secret_key = secret_key
        self._session_token = session_token

    def create_storage_client(self) -> IStorageClient:
        return S3StorageClient(
            access_key=self._access_key,
            secret_key=self._secret_key,
            session_token=self._session_token,
        )
