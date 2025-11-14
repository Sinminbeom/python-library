from datetime import datetime


class StorageFile:
    def __init__(self, file_path: str, last_modified_time: datetime):
        self.file_path = file_path
        self.last_modified_time = last_modified_time
        self.is_dir: bool = self.get_is_dir()
        self.file_name: str = self.get_file_name()
        self.depth: int = self.get_depth()
        pass

    def get_file_path(self):
        return self.file_path

    def get_last_modified_time(self):
        return self.last_modified_time

    def get_is_dir(self):
        if self.file_path.endswith("/"):
            return True

        return False

    def get_file_name(self):
        if self.is_dir:
            return self.file_path.split("/")[-2]

        return self.file_path.split("/")[-1]

    def get_depth(self):
        parts: list[str] = [p for p in self.file_path.strip("/").split("/") if p]
        return len(parts)

    def __str__(self) -> str:
        return f"StorageFile(file_path={self.file_path}, last_modified_time={self.last_modified_time}, is_dir={self.is_dir}, file_name={self.file_name}, depth={self.depth})"
