from datetime import datetime


class StorageFile:
    def __init__(self, file_path: str, last_modified_time: datetime):
        self._file_path = file_path
        self._last_modified_time = last_modified_time
        self._is_dir: bool = self.is_dir()
        self._file_name: str = self.get_file_name()
        self._depth: int = self.get_depth()
        pass

    def get_file_path(self):
        return self._file_path

    def get_last_modified_time(self):
        return self._last_modified_time

    def is_dir(self):
        if self._file_path.endswith("/"):
            return True

        return False

    def get_file_name(self):
        if self.is_dir():
            return self._file_path.split("/")[-2]

        return self._file_path.split("/")[-1]

    def get_depth(self):
        parts: list[str] = [p for p in self._file_path.strip("/").split("/") if p]
        return len(parts)

    def __str__(self) -> str:
        return f"StorageFile(file_path={self._file_path}, last_modified_time={self._last_modified_time}, is_dir={self._is_dir}, file_name={self._file_name}, depth={self._depth})"
