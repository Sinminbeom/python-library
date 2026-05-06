from pathlib import Path

import pytest

from python_library.storage.local.local_storage_factory import LocalStorageFactory
from python_library.storage.local.local_storage_info_factory import (
    LocalStorageInfoFactory,
)


@pytest.fixture
def storage(tmp_path: Path):
    factory = LocalStorageFactory(LocalStorageInfoFactory(str(tmp_path)))
    s = factory.create_storage()
    s.connect()
    yield s
    s.disconnect()


def test_connect_creates_root_dir(tmp_path: Path):
    root = tmp_path / "new_root"
    factory = LocalStorageFactory(LocalStorageInfoFactory(str(root)))
    s = factory.create_storage()
    s.connect()
    assert root.is_dir()


def test_write_and_read(storage):
    storage.write("/myroot/hello.txt", b"hello world")
    assert storage.read("/myroot/hello.txt") == b"hello world"


def test_write_creates_parent_dirs(storage, tmp_path: Path):
    storage.write("/myroot/sub/nested/file.bin", b"\x00\x01\x02")
    assert (tmp_path / "myroot" / "sub" / "nested" / "file.bin").is_file()


def test_is_exists(storage):
    assert storage.is_exists("/myroot/missing.txt") is False
    storage.write("/myroot/found.txt", b"x")
    assert storage.is_exists("/myroot/found.txt") is True


def test_upload(storage, tmp_path: Path):
    src = tmp_path / "src.txt"
    src.write_bytes(b"upload-data")
    storage.upload(str(src), "/myroot/dst.txt")
    assert storage.read("/myroot/dst.txt") == b"upload-data"


def test_download(storage, tmp_path: Path):
    storage.write("/myroot/remote.txt", b"download-data")
    dst = tmp_path / "out" / "local.txt"
    storage.download("/myroot/remote.txt", str(dst))
    assert dst.read_bytes() == b"download-data"


def test_copy(storage):
    storage.write("/myroot/a.txt", b"copy-me")
    storage.copy("/myroot/a.txt", "/myroot/sub/b.txt")
    assert storage.read("/myroot/sub/b.txt") == b"copy-me"
    # 원본은 유지
    assert storage.is_exists("/myroot/a.txt") is True


def test_get_file_list(storage):
    storage.write("/myroot/a.txt", b"1")
    storage.write("/myroot/sub/b.txt", b"2")
    storage.write("/myroot/sub/c.txt", b"3")

    files = storage.get_file_list("/myroot")
    paths = sorted(f.get_file_path() for f in files)
    assert paths == ["/myroot/a.txt", "/myroot/sub/b.txt", "/myroot/sub/c.txt"]


def test_get_file_list_with_prefix(storage):
    storage.write("/myroot/sub/b.txt", b"2")
    storage.write("/myroot/other/x.txt", b"3")

    files = storage.get_file_list("/myroot/sub")
    paths = [f.get_file_path() for f in files]
    assert paths == ["/myroot/sub/b.txt"]


def test_get_file_list_missing_returns_empty(storage):
    assert storage.get_file_list("/myroot/no_such_dir") == []


def test_to_url(storage, tmp_path: Path):
    url = storage.to_url("/myroot/file.txt")
    expected = f"file://{tmp_path.resolve().as_posix()}/myroot/file.txt"
    assert url == expected


def test_to_url_passthrough(storage):
    already = "file:///already/abs.txt"
    assert storage.to_url(already) == already


def test_invalid_path_rejected(storage):
    with pytest.raises(ValueError):
        storage.read("no-leading-slash.txt")


def test_empty_root_dir_rejected():
    with pytest.raises(ValueError):
        LocalStorageInfoFactory("").create_storage_client()
