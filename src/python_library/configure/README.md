# configure

conf 형식의 설정 파일을 로드하고 제공하는 패키지.

## 클래스 구조

```
Singleton
└── AppConfig               # 애플리케이션 설정 관리자

ConfigUtils                 # configparser 래핑 유틸리티
```

---

## 설정 파일 형식

`configparser` 표준 라이브러리를 사용해 conf 파일을 파싱한다.
섹션명이 `title1`(카테고리), 키가 `title2`(설정 키)에 해당한다.

```conf
[COMMON]
ProjectName = python-library
ThreadCount = 20
LocalDownloadPath = /
VolumesPlaceHolder = data1 | data2 | data3

[S3]
SrcBucketName = my-bucket
SrcRootPath = Proteomics/astral_data/
```

### 리스트 값 지원

`|` 구분자로 여러 값을 나열하면 자동으로 `list`로 파싱된다.
단일 값은 `str`로 반환된다.

```
VolumesPlaceHolder = data1 | data2 | data3
→ ["data1", "data2", "data3"]

ProjectName = python-library
→ "python-library"
```

---

## 사용법

### 초기화

`instance()` 호출 전 반드시 `set_config()`로 경로를 지정해야 한다.

```python
from python_library.configure.app_config import AppConfig

AppConfig.set_config("./config/application.conf")
```

### 값 조회

```python
# 특정 값 조회
project_name = AppConfig.instance().get_config("COMMON", "ProjectName")  # "python-library"

# 섹션 전체 조회
s3_config = AppConfig.instance().get_config("S3")  # {"srcbucketname": "my-bucket", ...}

# 전체 설정 조회
all_config = AppConfig.instance().get_config()
```

### COMMON 섹션

`COMMON` 섹션의 값은 어느 `title1`으로 조회해도 항상 함께 포함된다.
공통 설정(프로젝트명, 스레드 수 등)을 넣는 용도로 사용한다.

---

## 설계 의도

- `Singleton`을 상속하므로 앱 전체에서 설정 인스턴스가 하나만 존재한다.
- `set_config(config_path)`는 경로를 변경하고 설정을 다시 로드하므로, 테스트 등에서 설정 파일을 교체할 수 있다.
- `instance()` 호출 전에 `set_config()`가 반드시 선행되어야 한다.
