# category

Composite 패턴 기반의 계층적 액션 트리를 구성하고 실행하는 패키지.

서비스에서 처리해야 하는 작업을 **트리 형태로 등록**해두고,
경로를 타고 들어가 특정 액션만 실행하거나, 그룹 전체를 한 번에 실행할 수 있다.

---

## 구성 요소

| 클래스 | 역할 |
|---|---|
| `ICategoryComponent` | `CategoryGroup`과 `CategoryAction` 공통 인터페이스 |
| `CategoryGroup` | 하위 컴포넌트를 담는 컨테이너 (dict-like 인터페이스 제공) |
| `CategoryAction` | 실행 가능한 말단 액션 (callable wrapping) |
| `AppCategory` | 서비스별 카테고리 트리의 Singleton 루트 — 상속해서 사용 |

---

## 클래스 구조

```
ICategoryComponent (ABC)
├── CategoryGroup       # 자식을 담는 노드 (중간 노드)
└── CategoryAction      # 실제 실행 단위 (리프 노드)

Singleton
└── AppCategory (ABC)   # 트리 전체를 관리하는 Singleton 루트
```

---

## 트리 구조 예시

```
AppCategory (Singleton)
└── cate_queue
    ├── "DOWNLOAD" → CategoryGroup
    │   ├── "DOCUMENT" → CategoryGroup
    │   │   ├── "WORD"  → CategoryAction(lambda)
    │   │   ├── "PDF"   → CategoryAction(lambda)
    │   │   └── ...
    │   ├── "IMAGE" → CategoryGroup
    │   └── "VIDEO" → CategoryGroup
    │       ├── "MP4" → CategoryAction(lambda)
    │       └── "AVI" → CategoryAction(lambda)
    └── "UPLOAD" → CategoryGroup
        └── ...
```

---

## 사용법

### 1. Enum 정의

액션 이름(NAME)과 실행 함수(LAMBDA)를 한 쌍으로 묶어 중첩 Enum으로 관리한다.
`E_CATE_META_ELE.NAME`(인덱스 0)으로 이름, `E_CATE_META_ELE.LAMBDA`(인덱스 1)로 함수를 꺼낸다.

```python
from python_library.define.enum import IENUM

class E_CATE_META_ELE(IENUM):
    NAME = 0      # 튜플의 첫 번째 요소: 액션 이름 (str)
    LAMBDA = 1    # 튜플의 두 번째 요소: 실행 함수 (Callable)

class E_CATE(IENUM):
    DOWNLOAD = "DOWNLOAD"
    UPLOAD = "UPLOAD"

    class E_DOWNLOAD(IENUM):
        VIDEO = "VIDEO"

        class E_VIDEO(IENUM):
            MP4 = "MP4"
            E_MP4 = (MP4, lambda: print("MP4 download"))  # (NAME, LAMBDA) 쌍
            AVI = "AVI"
            E_AVI = (AVI, lambda: print("AVI download"))
```

- `E_VIDEO.MP4` → `"MP4"` (이름 문자열, push/get 키로 사용)
- `E_VIDEO.E_MP4[E_CATE_META_ELE.NAME]` → `"MP4"`
- `E_VIDEO.E_MP4[E_CATE_META_ELE.LAMBDA]` → `lambda: print("MP4 download")`

### 2. AppCategory 상속 및 트리 등록

`AppCategory`를 상속하고 `register_category()`에서 `cate_reg_queue`에 등록 함수를 매핑한다.
실제 트리 구성은 별도 메서드(`register_download` 등)로 분리한다.

```python
from python_library.category.app_category import AppCategory
from python_library.category.category_action import CategoryAction
from python_library.category.category_group import CategoryGroup

class MyCategory(AppCategory):
    def register_category(self) -> None:
        # 지연 초기화: 실제 트리는 get_cate_callback()() 호출 시 구성됨
        self.cate_reg_queue[E_CATE.DOWNLOAD] = lambda: self.register_download()
        self.cate_reg_queue[E_CATE.UPLOAD] = lambda: self.register_upload()

    def register_download(self) -> None:
        download = CategoryGroup()
        video = CategoryGroup()

        video.push(
            E_CATE.E_DOWNLOAD.E_VIDEO.E_MP4[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_DOWNLOAD.E_VIDEO.E_MP4[E_CATE_META_ELE.LAMBDA]),
        )
        video.push(
            E_CATE.E_DOWNLOAD.E_VIDEO.E_AVI[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_DOWNLOAD.E_VIDEO.E_AVI[E_CATE_META_ELE.LAMBDA]),
        )

        download.push(E_CATE.E_DOWNLOAD.VIDEO, video)
        self.cate_queue[E_CATE.DOWNLOAD] = download
```

### 3. 카테고리 초기화

`get_cate_callback(key)()`를 호출해 트리를 `cate_queue`에 채운다.

```python
MyCategory.instance().get_cate_callback(E_CATE.DOWNLOAD)()
MyCategory.instance().get_cate_callback(E_CATE.UPLOAD)()
```

### 4. 특정 액션 실행

`.get()` 또는 `[]`로 경로를 타고 들어가 `invoke()`로 실행한다.

```python
cate = MyCategory.instance()

# .get() 체이닝
cate.cate_queue[E_CATE.DOWNLOAD] \
    .get(E_CATE.E_DOWNLOAD.VIDEO) \
    .get(E_CATE.E_DOWNLOAD.E_VIDEO.MP4) \
    .invoke()

# [] 인덱싱 (동일 동작)
cate.cate_queue[E_CATE.DOWNLOAD][E_CATE.E_DOWNLOAD.VIDEO][E_CATE.E_DOWNLOAD.E_VIDEO.MP4].invoke()
```

### 5. 그룹 전체 일괄 실행

`CategoryGroup.invoke()`는 하위 모든 `CategoryAction`을 재귀적으로 실행한다.

```python
# VIDEO 그룹의 MP4, AVI, MOV 모두 실행
cate.cate_queue[E_CATE.DOWNLOAD].get(E_CATE.E_DOWNLOAD.VIDEO).invoke()

# DOWNLOAD 전체(DOCUMENT + IMAGE + VIDEO) 실행
cate.cate_queue[E_CATE.DOWNLOAD].invoke()
```

### 6. 액션 목록 조회

```python
download_group = MyCategory.instance().cate_queue[E_CATE.DOWNLOAD]

all_actions = download_group.get_all_actions()  # List[CategoryAction]

video_group = download_group.get(E_CATE.E_DOWNLOAD.VIDEO)
video_actions = video_group.get_all_actions()
```

---

## 설계 의도

### Composite 패턴
`CategoryGroup`과 `CategoryAction`이 동일한 `ICategoryComponent`를 구현하므로,
트리의 어느 노드에서든 `get()`, `invoke()`, `get_all_actions()`를 동일하게 호출할 수 있다.
호출 측은 대상이 그룹인지 액션인지 신경 쓰지 않아도 된다.

### Enum 기반 키 관리
액션 이름을 문자열 리터럴 대신 중첩 Enum으로 관리한다.
`push("MP4", ...)` 대신 `push(E_CATE.E_DOWNLOAD.E_VIDEO.MP4, ...)`로 작성해 오타를 방지한다.
`(NAME, LAMBDA)` 쌍 Enum은 이름과 함수를 한 곳에서 관리해 분산을 막는다.

### 지연 초기화
`register_category()`에서 트리 구성 함수를 `cate_reg_queue`에 등록만 해두고,
실제 트리는 `get_cate_callback(key)()` 호출 시점에 구성된다.
앱 시작 시 모든 트리를 한 번에 초기화하지 않아도 된다.

### Singleton
`AppCategory`는 `Singleton`을 상속한다.
반드시 `.instance()`로 접근하고, 직접 생성(`MyCategory()`)하지 않는다.
