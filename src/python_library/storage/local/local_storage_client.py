import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from python_library.storage.storage_file import StorageFile
from python_library.storage.storage_client import IStorageClient
from python_library.storage.upload_options import UploadOptions


class LocalStorageClient(IStorageClient):
    SERVICE_NAME = "local"
    SCHEME = "file://"

    def __init__(self):
        pass

    def connect(self) -> None:
        return

    def disconnect(self) -> None:
        return

    def upload(
        self, src_path: str, dst_path: str, options: UploadOptions | None = None
    ) -> None:
        # local 구현에서는 options(metadata/tagging/multipart 등)는 의미가 없어 무시
        del options

        dst = self._resolve(dst_path)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_path, dst)

    def download(self, src_path: str, dst_path: str) -> None:
        src = self._resolve(src_path)
        dst_parent = Path(dst_path).parent
        if str(dst_parent):
            dst_parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst_path)

    def get_file_list(self, path: str) -> List[StorageFile]:
        files: List[StorageFile] = list()

        prefix = self._resolve(path)

        # S3 list_objects_v2는 prefix가 디렉터리/파일 모두 매칭하므로 동일하게 처리
        if prefix.is_file():
            files.append(self._to_storage_file(prefix))
            return files

        if not prefix.exists():
            return files

        for root, _dirs, names in os.walk(prefix):
            root_path = Path(root)
            for name in names:
                files.append(self._to_storage_file(root_path / name))

        return files

    def read(self, path: str) -> bytes:
        return self._resolve(path).read_bytes()

    def write(
        self, path: str, data: bytes, options: UploadOptions | None = None
    ) -> None:
        del options

        abs_path = self._resolve(path)
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        abs_path.write_bytes(data)

    def is_exists(self, path: str) -> bool:
        return self._resolve(path).exists()

    def copy(self, src_path: str, dst_path: str) -> None:
        src = self._resolve(src_path)
        dst = self._resolve(dst_path)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)

    def to_url(self, path: str) -> str:
        """
        절대 fs 경로를 file:// scheme url로 변환.
        - "/abs/path" -> "file:///abs/path"
        - 이미 "file://..."면 그대로 반환
        """
        if not path:
            raise ValueError("path is empty")

        if path.startswith(self.SCHEME):
            return path

        if not path.startswith("/"):
            raise ValueError(f"Invalid path (must start with '/'): {path}")

        return f"{self.SCHEME}{path}"

    def _resolve(self, path: str) -> Path:
        if not path.startswith("/"):
            raise ValueError(f"Invalid path (must start with '/'): {path}")
        return Path(path)

    def _to_storage_file(self, abs_path: Path) -> StorageFile:
        std_path = abs_path.as_posix()
        mtime = datetime.fromtimestamp(abs_path.stat().st_mtime, tz=timezone.utc)
        return StorageFile(std_path, mtime)
