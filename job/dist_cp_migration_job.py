import time

from job.job import IJob
from log.logger import Logger
from storage.storage import IStorage


class DistCpMigrationJob(IJob):
    def __init__(
        self, src_storage: IStorage, src_path: str, dst_bucket_name: str, dst_path: str
    ):
        super().__init__()
        self.src_storage = src_storage
        self.src_path = src_path
        self.dst_bucket_name = dst_bucket_name
        self.dst_path = dst_path

    def execute(self) -> None:
        text = f"start DistCpMigrationJob src_path = {self.src_path}, dst_path = {self.dst_path}"
        Logger.instance().logger.info(text)

        start = time.time()

        self.src_storage.copy("", self.src_path, self.dst_bucket_name, self.dst_path)

        end = time.time()

        text = f"end DistCpMigrationJob elapsed time = {end - start:.2f} : src_path = {self.src_path}, dst_bucket_name = {self.dst_bucket_name}, dst_path = {self.dst_path}"
        Logger.instance().logger.info(text)
