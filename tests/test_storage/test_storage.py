from python_library.storage.s3.s3_storage_factory import S3StorageFactory
from python_library.storage.s3.s3_storage_info_factory import S3StorageInfoFactory
from python_library.storage.upload_options import UploadOptions


def test_upload():
    src_path = "C:\\Users\\shinminbeom\\fefefe.txt"
    dst_path = "/oncx-dl-raw-dev/test/fefefe.txt"

    storage_factory = S3StorageFactory(S3StorageInfoFactory())
    storage = storage_factory.create_storage()
    storage.connect()
    storage.upload(src_path, dst_path)
    pass


def test_upload_metadata():
    src_path = "C:\\Users\\shinminbeom\\fefefe.txt"
    dst_path = "/oncx-dl-raw-dev/test/fefefe.txt"

    options = UploadOptions(metadata={"test": "test1"}, tagging={"test": "test2"})

    storage_factory = S3StorageFactory(S3StorageInfoFactory())
    storage = storage_factory.create_storage()
    storage.connect()
    storage.upload(src_path, dst_path, options)
    print(storage.to_url(dst_path))
    pass


def test_write():
    dst_path = "/oncx-dl-raw-dev/test/write_test.txt"

    options = UploadOptions(metadata={"test": "test1"}, tagging={"test": "test2"})

    storage_factory = S3StorageFactory(S3StorageInfoFactory())
    storage = storage_factory.create_storage()
    storage.connect()
    storage.write(dst_path, b"hello world", options)
    print(storage.to_url(dst_path))
    pass


def test_download():
    src_path = "/oncx-dl-raw-dev/test/fefefe.txt"
    dst_path = "C:\\Users\\shinminbeom\\fefefe.txt"

    storage_factory = S3StorageFactory(S3StorageInfoFactory())
    storage = storage_factory.create_storage()
    storage.connect()
    storage.download(src_path, dst_path)
    pass


def test_get_file_list():
    path = "/oncx-dl-raw-dev"

    storage_factory = S3StorageFactory(S3StorageInfoFactory())
    storage = storage_factory.create_storage()
    storage.connect()
    file_list = storage.get_file_list(path)
    print()

    for file in file_list:
        print(file)


def test_read():
    path = "/oncx-dl-raw-dev/test/meta.json"

    storage_factory = S3StorageFactory(S3StorageInfoFactory())
    storage = storage_factory.create_storage()
    storage.connect()
    data = storage.read(path)
    print(data.decode("utf-8"))


def test_copy():
    src_path = "/oncx-dl-raw-dev/test/test.txt"
    dst_path = "/oncx-dl-raw-dev/test/ttt/test.txt"

    storage_factory = S3StorageFactory(S3StorageInfoFactory())
    storage = storage_factory.create_storage()
    storage.connect()
    storage.copy(src_path, dst_path)


def test_is_exists():
    path = "/khulab-miracurenas01/Proteomics/astral_data/TEST_PROJECT/meta.json"

    storage_factory = S3StorageFactory(S3StorageInfoFactory())
    storage = storage_factory.create_storage()
    storage.connect()
    is_exists = storage.is_exists(path)
    print(is_exists)
