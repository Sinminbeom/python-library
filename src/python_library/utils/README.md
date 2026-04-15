# utils

공통 유틸리티를 담는 패키지.

## ClassNameGenerator

클래스 이름 기반으로 자동 순번 이름을 생성하는 유틸리티.
`abProcess`, `abThread`에서 이름이 지정되지 않은 인스턴스에 자동 이름을 부여할 때 사용한다.

### 동작 방식

- 클래스별로 독립적인 카운터를 유지한다.
- 이름이 제공되면 그대로 사용하고, `None`이면 `클래스명 + 순번`을 반환한다.

```python
gen = ClassNameGenerator()

gen(my_process_instance, None)  # → "MyProcess1"
gen(my_process_instance, None)  # → "MyProcess2"
gen(other_process, None)        # → "OtherProcess1"
gen(my_thread, "custom-name")   # → "custom-name"
```

### 이름이 큐 키로 사용됨

`process`와 `thread` 패키지에서 이름 지정 큐(`shared_queue`)의 키가 이 이름이다.
`push_shared_queue("MyProcess1", job)` 형태로 사용하므로,
자동 생성된 이름이 몇 번인지 인지하고 사용해야 한다.

### 사용 예시 (abProcess 내부)

```python
class abProcess(ABC, Process):
    _name_gen = ClassNameGenerator()

    def __init__(self, name: str | None = None) -> None:
        name = self._name_gen(self, name)  # None이면 자동 생성
        super().__init__(name=name)
```

---

## 새 유틸리티 추가

공통적으로 사용되는 순수 함수 또는 유틸리티 클래스를 이 패키지에 추가한다.
특정 도메인(db, storage 등)에 종속된 로직은 해당 패키지에 두는 것이 맞다.
