from typing import List

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from storage.storage_file import StorageFile
from storage.storage_client import IStorageClient


class S3StorageClient(IStorageClient):
    SERVICE_NAME = "s3"

    def __init__(self, access_key_id: str, secret_access_key: str, bucket_name: str):
        self._access_key_id: str = access_key_id
        self._secret_access_key: str = secret_access_key
        self._bucket_name: str = bucket_name

        self._client: BaseClient | None = None

    def connect(self) -> None:
        self._client = boto3.client(
            service_name=S3StorageClient.SERVICE_NAME,
            aws_access_key_id=self._access_key_id,
            aws_secret_access_key=self._secret_access_key,
        )
        pass

    def disconnect(self) -> None:
        if self._client is None:
            return

        self._client.close()
        self._client = None
        pass

    def upload(self, src_path: str, dst_path: str) -> None:
        if self._client is None:
            raise RuntimeError("Connection failed")

        try:
            self._client.upload_file(src_path, self._bucket_name, dst_path)
        except Exception as e:
            # TODO: log
            raise e
        pass

    def download(self, src_path: str, dst_path: str) -> None:
        if self._client is None:
            raise RuntimeError("Connection failed")

        try:
            self._client.download_file(self._bucket_name, src_path, dst_path)
        except Exception as e:
            # TODO: log
            raise e
        pass

    def get_file_list(self, path: str) -> List[StorageFile]:
        if self._client is None:
            raise RuntimeError("Connection failed")

        files: List[StorageFile] = list()

        try:
            paginator = self._client.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=self._bucket_name, Prefix=path):
                for obj in page["Contents"]:
                    files.append(StorageFile(obj["Key"], obj["LastModified"]))

            return files

        except Exception as e:
            raise e

    def read(self, path: str) -> str:
        if self._client is None:
            raise RuntimeError("Connection failed")

        try:
            response = self._client.get_object(Bucket=self._bucket_name, Key=path)

            content: str = response["Body"].read().decode("utf-8")

            return content

        except Exception as e:
            raise e

    def is_exists(self, path: str) -> bool:
        if self._client is None:
            raise RuntimeError("Connection failed")

        try:
            self._client.head_object(Bucket=self._bucket_name, Key=path)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                raise

    def copy(
        self, src_root_path: str, src_path: str, dst_root_path: str, dst_path: str
    ) -> None:
        if self._client is None:
            raise RuntimeError("Connection failed")

        try:
            src_source = {"Bucket": self._bucket_name, "Key": src_path}
            self._client.copy_object(
                CopySource=src_source, Bucket=dst_root_path, Key=dst_path
            )

        except Exception as e:
            raise e
