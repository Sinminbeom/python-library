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

    def __init__(self, root_dir: str):
        if not root_dir:
            raise ValueError("root_dir is empty")

        self._root_dir: Path = Path(root_dir).resolve()

    def connect(self) -> None:
        self._root_dir.mkdir(parents=True, exist_ok=True)

    def disconnect(self) -> None:
        return

    def upload(
        self, src_path: str, dst_path: str, options: UploadOptions | None = None
    ) -> None:
        # local 구현에서는 options(metadata/tagging/multipart 등)는 의미가 없어 무시
        del options

        dst_abs = self._resolve(dst_path)
        dst_abs.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_path, dst_abs)

    def download(self, src_path: str, dst_path: str) -> None:
        src_abs = self._resolve(src_path)
        dst_parent = Path(dst_path).parent
        if str(dst_parent):
            dst_parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_abs, dst_path)

    def get_file_list(self, path: str) -> List[StorageFile]:
        files: List[StorageFile] = list()

        prefix_abs = self._resolve(path)

        # S3 list_objects_v2는 prefix가 디렉터리/파일 모두 매칭하므로 동일하게 처리
        if prefix_abs.is_file():
            files.append(self._to_storage_file(prefix_abs))
            return files

        if not prefix_abs.exists():
            return files

        for root, _dirs, names in os.walk(prefix_abs):
            root_path = Path(root)
            for name in names:
                files.append(self._to_storage_file(root_path / name))

        return files

    def read(self, path: str) -> bytes:
        abs_path = self._resolve(path)
        return abs_path.read_bytes()

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
        src_abs = self._resolve(src_path)
        dst_abs = self._resolve(dst_path)
        dst_abs.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_abs, dst_abs)

    def to_url(self, path: str) -> str:
        """
        내부 표준 path (/root/key)를 file:// scheme url로 변환.
        - "/root/key" -> "file://{abs root_dir}/root/key"
        - 이미 "file://..."면 그대로 반환
        """
        if not path:
            raise ValueError("path is empty")

        if path.startswith(self.SCHEME):
            return path

        abs_path = self._resolve(path)
        return f"{self.SCHEME}{abs_path.as_posix()}"

    def _resolve(self, path: str) -> Path:
        """
        /root/key 형태의 path를 root_dir 하위 절대 경로로 변환.
        예 (root_dir=/data):
            /myroot/foo/bar.txt → /data/myroot/foo/bar.txt
        """
        if not path.startswith("/"):
            raise ValueError(f"Invalid path (must start with '/'): {path}")

        rel = path.lstrip("/")
        return self._root_dir / rel

    def _to_storage_file(self, abs_path: Path) -> StorageFile:
        rel = abs_path.relative_to(self._root_dir).as_posix()
        std_path = f"/{rel}"
        mtime = datetime.fromtimestamp(abs_path.stat().st_mtime, tz=timezone.utc)
        return StorageFile(std_path, mtime)
