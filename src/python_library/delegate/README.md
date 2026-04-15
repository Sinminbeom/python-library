# delegate

C# 스타일의 타입 안전한 콜백/델리게이트 패턴을 제공하는 패키지.
`Action`(반환값 없음)과 `Func`(반환값 있음) 두 계열로 나뉜다.

## 클래스 구조

```
IDelegate (ABC)
├── Action                  # () -> None
├── Action1[T1]             # (T1) -> None
├── Action2[T1, T2]         # (T1, T2) -> None
├── Action3[T1, T2, T3]
├── Action4[T1, T2, T3, T4]
├── Action5[T1, T2, T3, T4, T5]
├── Action6[T1, T2, T3, T4, T5, T6]
├── Func[R]                 # () -> R
├── Func1[T1, R]            # (T1) -> R
├── Func2[T1, T2, R]
├── Func3[T1, T2, T3, R]
├── Func4[T1, T2, T3, T4, R]
├── Func5[T1, T2, T3, T4, T5, R]
└── Func6[T1, T2, T3, T4, T5, T6, R]
```

---

## 사용법

### Action (반환값 없음)

```python
from python_library.delegate.delegate import Action1

class OnDataReceived(Action1[bytes]):
    def invoke(self, data: bytes) -> None:
        process(data)

def register_callback(handler: Action1[bytes]) -> None:
    ...

register_callback(OnDataReceived())
```

### Func (반환값 있음)

```python
from python_library.delegate.delegate import Func1

class ParseData(Func1[str, dict]):
    def invoke(self, raw: str) -> dict:
        return json.loads(raw)
```

---

## 설계 의도

Python의 `Callable` 타입 힌트는 파라미터 타입을 구체적으로 표현하기 어렵다.
`Action`/`Func` 계열은 Generic을 통해 파라미터 수와 타입을 명시적으로 표현한다.
콜백을 주입받는 곳에서 타입 힌트를 명확하게 할 수 있고, Pyright가 타입 오류를 잡아준다.

---

## 주의사항

파라미터가 7개 이상인 경우는 현재 지원하지 않는다.
그 경우 dataclass나 dict로 파라미터를 묶어서 `Action1[MyParams]`처럼 사용하는 것을 권장한다.
