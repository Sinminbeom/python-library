from pathlib import Path

import pytest

from python_library.storage.local.local_storage_factory import LocalStorageFactory
from python_library.storage.local.local_storage_info_factory import (
    LocalStorageInfoFactory,
)


@pytest.fixture
def storage(tmp_path: Path):
    factory = LocalStorageFactory(LocalStorageInfoFactory())
    s = factory.create_storage()
    s.connect()
    yield s
    s.disconnect()


@pytest.fixture
def base(tmp_path: Path) -> str:
    return tmp_path.as_posix()


def test_write_and_read(storage, base):
    p = f"{base}/myroot/hello.txt"
    storage.write(p, b"hello world")
    assert storage.read(p) == b"hello world"


def test_write_creates_parent_dirs(storage, base, tmp_path: Path):
    p = f"{base}/myroot/sub/nested/file.bin"
    storage.write(p, b"\x00\x01\x02")
    assert (tmp_path / "myroot" / "sub" / "nested" / "file.bin").is_file()


def test_is_exists(storage, base):
    assert storage.is_exists(f"{base}/myroot/missing.txt") is False
    storage.write(f"{base}/myroot/found.txt", b"x")
    assert storage.is_exists(f"{base}/myroot/found.txt") is True


def test_upload(storage, base, tmp_path: Path):
    src = tmp_path / "src.txt"
    src.write_bytes(b"upload-data")
    storage.upload(str(src), f"{base}/myroot/dst.txt")
    assert storage.read(f"{base}/myroot/dst.txt") == b"upload-data"


def test_download(storage, base, tmp_path: Path):
    storage.write(f"{base}/myroot/remote.txt", b"download-data")
    dst = tmp_path / "out" / "local.txt"
    storage.download(f"{base}/myroot/remote.txt", str(dst))
    assert dst.read_bytes() == b"download-data"


def test_copy(storage, base):
    storage.write(f"{base}/myroot/a.txt", b"copy-me")
    storage.copy(f"{base}/myroot/a.txt", f"{base}/myroot/sub/b.txt")
    assert storage.read(f"{base}/myroot/sub/b.txt") == b"copy-me"
    assert storage.is_exists(f"{base}/myroot/a.txt") is True


def test_get_file_list(storage, base):
    storage.write(f"{base}/myroot/a.txt", b"1")
    storage.write(f"{base}/myroot/sub/b.txt", b"2")
    storage.write(f"{base}/myroot/sub/c.txt", b"3")

    files = storage.get_file_list(f"{base}/myroot")
    paths = sorted(f.get_file_path() for f in files)
    assert paths == [
        f"{base}/myroot/a.txt",
        f"{base}/myroot/sub/b.txt",
        f"{base}/myroot/sub/c.txt",
    ]


def test_get_file_list_with_prefix(storage, base):
    storage.write(f"{base}/myroot/sub/b.txt", b"2")
    storage.write(f"{base}/myroot/other/x.txt", b"3")

    files = storage.get_file_list(f"{base}/myroot/sub")
    paths = [f.get_file_path() for f in files]
    assert paths == [f"{base}/myroot/sub/b.txt"]


def test_get_file_list_missing_returns_empty(storage, base):
    assert storage.get_file_list(f"{base}/myroot/no_such_dir") == []


def test_to_url(storage, base):
    p = f"{base}/myroot/file.txt"
    assert storage.to_url(p) == f"file://{p}"


def test_to_url_passthrough(storage):
    already = "file:///already/abs.txt"
    assert storage.to_url(already) == already


def test_invalid_path_rejected(storage):
    with pytest.raises(ValueError):
        storage.read("no-leading-slash.txt")
