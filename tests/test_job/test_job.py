from python_library.job.cloud_normalization_job import CloudNormalizationJob
from python_library.job.local_normalization_job import LocalNormalizationJob
from python_library.storage.s3.s3_storage_factory import S3StorageFactory
from python_library.storage.s3.s3_storage_info_factory import S3StorageInfoFactory

ACCESS_KEY_ID = "access-key-id"
SECRET_ACCESS_KEY = "your-secret-access-key"


def test_local_normalization_job():
    root_path = "/python_library-dl-raw-dev"
    instrument_type = "LCMS"
    production_datetime = "20251112T031301Z"

    src_path = f"{root_path}/{instrument_type}/{production_datetime}/meta.json"
    dst_path = (
        f"{root_path}/{instrument_type}/{production_datetime}/parquet/output3.parquet"
    )

    storage_factory = S3StorageFactory(S3StorageInfoFactory())
    storage = storage_factory.create_storage()
    storage.connect()

    normalization_job = LocalNormalizationJob(storage, src_path, storage, dst_path)
    normalization_job.execute()

    storage.disconnect()
    pass


def test_cloud_normalization_job():
    instrument_type = "LCMS"
    production_datetime = "20251112T031301Z"

    cloud_normalization_job = CloudNormalizationJob(
        instrument_type,
        production_datetime,
        access_key_id=ACCESS_KEY_ID,
        secret_access_key=SECRET_ACCESS_KEY,
    )
    cloud_normalization_job.execute()
    pass
