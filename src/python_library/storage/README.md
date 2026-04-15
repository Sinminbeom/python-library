# storage

파일 저장소 접근을 추상화하는 패키지.
현재 AWS S3 구현체가 포함되어 있으며, 다른 저장소(GCS, Azure Blob 등)를 추가할 때도 동일한 인터페이스를 따른다.

## 클래스 구조

```
IStorage (ABC)                  # 저장소 인터페이스
└── S3Storage                   # boto3 기반 S3 구현체

IStorageClient (ABC)            # 저장소 클라이언트 인터페이스
└── S3StorageClient             # boto3 S3 클라이언트 래퍼

IStorageFactory (ABC)           # 저장소 인스턴스 팩토리
└── S3StorageFactory

IStorageInfoFactory (ABC)       # 저장소 접속 정보 팩토리
└── S3StorageInfoFactory

StorageFile (dataclass)         # 파일 메타데이터 (경로, 수정시간, 깊이 등)
UploadOptions (frozen dataclass)# 업로드 옵션
```

---

## 경로 형식

S3 경로는 `/버킷명/키경로` 형식을 사용한다.

```
/oncx-dl-raw-dev/test/fefefe.txt
 ↑ 버킷명          ↑ 키 경로
```

---

## 사용법

### 연결

```python
from python_library.storage.s3.s3_storage_factory import S3StorageFactory
from python_library.storage.s3.s3_storage_info_factory import S3StorageInfoFactory

storage = S3StorageFactory(S3StorageInfoFactory()).create_storage()
storage.connect()
```

`S3StorageInfoFactory()`는 AWS 기본 자격증명 체인(환경변수, ~/.aws/credentials 등)을 사용한다.

### 업로드

```python
from python_library.storage.upload_options import UploadOptions

# 기본 업로드
storage.upload("/local/fefefe.txt", "/oncx-dl-raw-dev/test/fefefe.txt")

# 메타데이터 + 태그 포함
options = UploadOptions(metadata={"source": "sensor-A"}, tagging={"env": "dev"})
storage.upload("/local/fefefe.txt", "/oncx-dl-raw-dev/test/fefefe.txt", options)

# URL 조회
print(storage.to_url("/oncx-dl-raw-dev/test/fefefe.txt"))
```

### 다운로드

```python
storage.download("/oncx-dl-raw-dev/test/fefefe.txt", "/local/fefefe.txt")
```

### 바이트 읽기/쓰기

```python
# 읽기
data: bytes = storage.read("/oncx-dl-raw-dev/test/meta.json")
print(data.decode("utf-8"))

# 쓰기
options = UploadOptions(metadata={"test": "test1"}, tagging={"test": "test2"})
storage.write("/oncx-dl-raw-dev/test/write_test.txt", b"hello world", options)
```

### 파일 목록 조회

```python
files: list[StorageFile] = storage.get_file_list("/oncx-dl-raw-dev")
for file in files:
    print(file)
```

### 복사 / 존재 확인

```python
storage.copy("/oncx-dl-raw-dev/test/test.txt", "/oncx-dl-raw-dev/test/ttt/test.txt")

is_exists: bool = storage.is_exists("/oncx-dl-raw-dev/test/meta.json")
```

---

## UploadOptions

```python
@dataclass(frozen=True)
class UploadOptions:
    max_concurrency: int = 1             # 병렬 업로드 스레드 수
    multipart_threshold: int = 8 * MB   # 멀티파트 전환 기준 크기
    multipart_chunk_size: int = 8 * MB  # 멀티파트 청크 크기
    checksum_algorithm: str = "SHA256"  # 체크섬 알고리즘
    metadata: dict[str, str] = {}       # 오브젝트 메타데이터
    tagging: dict[str, str] = {}        # 오브젝트 태그
```

`frozen=True`로 불변 객체이므로 생성 후 수정할 수 없다.

---

## 추상 팩토리 패턴

두 Factory 인터페이스가 협력해 저장소 객체를 완성한다.

```
IStorageFactory ──────────── IStorageInfoFactory
  create_storage()             create_storage_client()
        │                              │
        ▼                              ▼
  S3Storage  ◄── set_storage_client ── S3StorageClient
```

- `IStorageInfoFactory.create_storage_client()` → 자격증명 정보로 클라이언트를 만든다.
- `IStorageFactory.create_storage()` → 저장소 객체를 만들고, 위 클라이언트를 `set_storage_client()`로 주입한다.
- 호출 측은 `IStorageFactory` 하나만 알면 되고, 자격증명 소스(환경변수, ~/.aws/credentials, IAM Role 등)는 `IStorageInfoFactory` 구현체 교체로 처리한다.

```python
# S3StorageFactory 내부 동작
def create_storage(self) -> IStorage:
    storage = S3Storage()
    storage.set_storage_client(self._storage_info_factory.create_storage_client())
    return storage
```

---

## 설계 의도

직접 `S3Storage()`를 생성하지 않고 Factory를 통해 생성한다.
접속 정보를 `IStorageInfoFactory`로 분리해 설정 소스를 교체할 수 있다.
`IStorage` 인터페이스에만 의존하면 S3 → GCS 등으로 구현체를 교체해도 호출 측 코드가 변경되지 않는다.

---

## 새 저장소 추가 방법

1. `storage/` 하위에 새 디렉토리를 만든다 (예: `gcs/`).
2. `IStorage`, `IStorageClient`, `IStorageFactory`, `IStorageInfoFactory`를 구현한다.
3. S3 구현체(`storage/s3/`)를 참고해 동일한 파일 구조로 작성한다.
