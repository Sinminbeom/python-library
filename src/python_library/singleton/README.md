# singleton

Singleton 패턴을 제공하는 패키지.
`python_library` 내의 `AppConfig`, `BaseConfLogger`, `AppCategory` 등이 이를 상속한다.

## 클래스 구조

```
Singleton
  instance(*args, **kwargs) -> Self
```

---

## 사용법

`Singleton`을 상속하고, 반드시 `.instance()`로 접근한다.

```python
from python_library.singleton.singleton import Singleton

class MyConfig(Singleton):
    def __init__(self):
        self.value = 42

config1 = MyConfig.instance()
config2 = MyConfig.instance()
assert config1 is config2  # True — 동일 인스턴스
```

---

## 설계 의도

클래스 변수 `__instance`를 각 서브클래스별로 독립적으로 유지한다.
최초 `instance()` 호출 시 인스턴스를 생성하고 이후에는 동일 인스턴스를 반환한다.

```python
class Singleton:
    __instance = None

    @classmethod
    def instance(cls, *args, **kargs):
        if cls.__instance is None:
            cls.__instance = cls(*args, **kargs)
        return cls.__instance
```

---

## 주의: 직접 생성 금지

`MyConfig()` 처럼 직접 생성하면 Singleton을 우회한다.
반드시 `MyConfig.instance()`로만 접근한다.

---

## 주의: 테스트에서 리셋

테스트 간 Singleton 상태를 초기화하려면 `__instance`를 직접 `None`으로 설정한다.

```python
AppLogger._Singleton__instance = None
AppLogger.set_config("./tests/logging_json.conf", "python-library")
```
