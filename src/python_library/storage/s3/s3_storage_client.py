import boto3
from typing import List, Tuple, Optional, Any
import urllib.parse

from boto3.s3.transfer import TransferConfig
from botocore.client import BaseClient
from botocore.config import Config
from botocore.exceptions import ClientError

from python_library.storage.storage_file import StorageFile
from python_library.storage.storage_client import IStorageClient
from python_library.storage.upload_options import UploadOptions, E_CHECKSUM_ALGORITHM


class S3StorageClient(IStorageClient):
    SERVICE_NAME = "s3"
    SCHEME = "s3://"

    def __init__(self):
        self._client: Optional[BaseClient] = None

    def connect(self) -> None:
        try:
            config = Config(
                retries={"max_attempts": 20, "mode": "standard"},
                connect_timeout=60,
                read_timeout=600,
                max_pool_connections=50,
                tcp_keepalive=True,
            )

            self._client = boto3.client(
                service_name=S3StorageClient.SERVICE_NAME,
                config=config,
            )
        except Exception as e:
            raise e
        pass

    def disconnect(self) -> None:
        if self._client is None:
            return

        self._client.close()
        self._client = None
        pass

    def upload(
        self, src_path: str, dst_path: str, options: UploadOptions | None = None
    ) -> None:
        try:
            # 옵션 방어: None이면 기본 옵션 적용
            opts = options or UploadOptions()

            dst_bucket, dst_key = self._parse_s3_path(dst_path)

            transfer_config = TransferConfig(
                multipart_threshold=opts.multipart_threshold,
                multipart_chunksize=opts.multipart_chunk_size,
                max_concurrency=opts.max_concurrency,
                use_threads=True,
            )

            extra_args = self._build_s3_args(opts)

            if extra_args:
                self._client.upload_file(
                    src_path,
                    dst_bucket,
                    dst_key,
                    ExtraArgs=extra_args,
                    Config=transfer_config,
                )
            else:
                self._client.upload_file(
                    src_path,
                    dst_bucket,
                    dst_key,
                    Config=transfer_config,
                )

        except Exception as e:
            raise e
        pass

    def download(self, src_path: str, dst_path: str) -> None:
        try:
            src_bucket, src_key = self._parse_s3_path(src_path)

            self._client.download_file(src_bucket, src_key, dst_path)

        except Exception as e:
            raise e
        pass

    def get_file_list(self, path: str) -> List[StorageFile]:
        files: List[StorageFile] = list()

        try:
            bucket, key = self._parse_s3_path(path)

            paginator = self._client.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=bucket, Prefix=key):
                for obj in page["Contents"]:
                    files.append(
                        StorageFile(f"/{bucket}/{obj['Key']}", obj["LastModified"])
                    )

            return files

        except Exception as e:
            raise e

    def read(self, path: str) -> bytes:
        try:
            bucket, key = self._parse_s3_path(path)

            response = self._client.get_object(Bucket=bucket, Key=key)

            data = response["Body"].read()

            return data

        except Exception as e:
            raise e

    def write(
        self, path: str, data: bytes, options: UploadOptions | None = None
    ) -> None:
        try:
            bucket, key = self._parse_s3_path(path)

            put_args = self._build_s3_args(options)

            self._client.put_object(Bucket=bucket, Key=key, Body=data, **put_args)

        except Exception as e:
            raise e

    def is_exists(self, path: str) -> bool:
        try:
            bucket, key = self._parse_s3_path(path)

            self._client.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                raise

    def copy(self, src_path: str, dst_path: str) -> None:
        try:
            src_bucket, src_key = self._parse_s3_path(src_path)
            dst_bucket, dst_key = self._parse_s3_path(dst_path)

            src_source = {"Bucket": src_bucket, "Key": src_key}
            self._client.copy_object(
                CopySource=src_source, Bucket=dst_bucket, Key=dst_key
            )

        except Exception as e:
            raise e

    def to_url(self, path: str) -> str:
        """
        내부 표준 path (/bucket/key)를 scheme 붙인 url로 변환.
        - "/bucket/key" -> "s3://bucket/key"
        - 이미 "s3://..."면 그대로 반환
        """
        if not path:
            raise ValueError("path is empty")

        scheme = getattr(self, "SCHEME", None)
        if not scheme:
            raise ValueError(f"{self.__class__.__name__}.SCHEME is not set")

        if path.startswith(scheme):
            return path

        if not path.startswith("/"):
            raise ValueError(f"Invalid path (must start with '/'): {path}")

        trimmed = path.lstrip("/")  # "bucket/key..."
        return f"{scheme}{trimmed}"

    def _parse_s3_path(self, path: str) -> Tuple[str, str]:
        """
        /bucket/key 형태의 path에서 bucket, key를 분리.
        예:
            /bucket/data/file.txt → bucket='bucket', key='data/file.txt'
        """

        if not path.startswith("/"):
            raise ValueError(f"Invalid path (must start with '/'): {path}")

        # 앞의 슬래시 제거 → 'bucket/key/...'
        trimmed = path.lstrip("/")

        # 첫 '/' 기준으로 bucket, key 분리
        parts = trimmed.split("/", 1)

        if len(parts) == 1:
            # key가 없는 경우 (버킷만 입력)
            bucket = parts[0]
            key = ""
        else:
            bucket, key = parts[0], parts[1]

        return bucket, key

    def _build_s3_args(self, options: UploadOptions | None) -> dict[str, Any]:
        """
        Build arguments that are compatible with both:
          - client.upload_file(..., ExtraArgs=...)
          - client.put_object(**args)
        """
        if options is None:
            return {}

        # options가 있지만 실질 값이 없으면 빈 dict 반환
        if (
            (not options.metadata)
            and (not options.tagging)
            and (not options.checksum_algorithm)
        ):
            return {}

        metadata: dict[str, str] = dict(options.metadata or {})
        tagging: dict[str, str] = dict(options.tagging or {})

        checksum_algorithm = options.checksum_algorithm or E_CHECKSUM_ALGORITHM.SHA256

        args: dict[str, Any] = {}

        if checksum_algorithm:
            args["ChecksumAlgorithm"] = checksum_algorithm

        if metadata:
            args["Metadata"] = metadata

        if tagging:
            args["Tagging"] = urllib.parse.urlencode(tagging)

        return args
