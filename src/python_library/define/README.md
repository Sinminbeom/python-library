# define

상수와 열거형 기반 타입을 정의하는 패키지.

## IENUM

모든 커스텀 Enum의 기반 클래스.
`str`과 `Enum`을 동시에 상속해 문자열처럼 비교하고 직렬화할 수 있다.

```python
class IENUM(str, Enum):
    ...
```

### 사용 예시

```python
from python_library.define.enum import IENUM

class E_CHECKSUM_ALGORITHM(IENUM):
    SHA256 = "SHA256"

algo = E_CHECKSUM_ALGORITHM.SHA256
algo == "SHA256"           # True (str 비교 가능)
json.dumps({"alg": algo})  # '{"alg": "SHA256"}' (직렬화 가능)
```

---

## 컨벤션

- Enum 클래스 이름은 `E_` 접두사로 시작한다 (예: `E_CHECKSUM_ALGORITHM`, `E_CATE`).
- 도메인별 Enum은 해당 패키지에 직접 정의해도 된다 (`storage/upload_options.py`의 `E_CHECKSUM_ALGORITHM` 참고).
- 여러 패키지에서 공유하는 상수/Enum만 이 패키지에 정의한다.
- `category` 패키지처럼 중첩 Enum이 필요한 경우 `IENUM`을 중첩 클래스로 사용할 수 있다.

```python
class E_CATE(IENUM):
    DOWNLOAD = "DOWNLOAD"

    class E_DOWNLOAD(IENUM):
        VIDEO = "VIDEO"

        class E_VIDEO(IENUM):
            MP4 = "MP4"
            E_MP4 = (MP4, lambda: print("MP4"))  # (NAME, LAMBDA) 쌍
```
