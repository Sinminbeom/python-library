import time
import os
from job.job import IJob
from log.logger import Logger
from storage.storage import IStorage


class LocalStagingMigrationJob(IJob):
    def __init__(
        self,
        src_storage: IStorage,
        src_path: str,
        local_path: str,
        dst_storage: IStorage,
        dst_path: str,
    ):
        super().__init__()
        self.src_storage = src_storage
        self.src_path = src_path
        self.local_path = local_path
        self.dst_storage = dst_storage
        self.dst_path = dst_path

    def execute(self) -> None:
        start = time.time()

        text = f"start LocalStagingMigrationJob : src_path = {self.src_path}, local_path = {self.local_path}, dst_path = {self.dst_path}"
        Logger.instance().logger.info(text)

        dir_path = os.path.dirname(self.local_path)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # src storage 다운로드
        self.src_storage.download(self.src_path, self.local_path)

        # dst storage 업로드
        self.dst_storage.upload(self.local_path, self.dst_path)

        # local file 삭제
        if os.path.isfile(self.local_path):
            os.remove(self.local_path)

        end = time.time()

        text = f"end LocalStagingMigrationJob elapsed time = {end - start:.2f} : src_path = {self.src_path}, local_path = {self.local_path}, dst_path = {self.dst_path}"
        Logger.instance().logger.info(text)
