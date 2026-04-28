# state

상태 머신(state machine) 4-layer 패키지. 어떤 클래스든 `StateComponent`를 보유시키면 상태 기반 동작을 적용할 수 있다.

## 클래스 구조

```
abState (ABC)              # 단일 state 추상 클래스 (lifecycle 메서드)
StateMap                   # state_id → abState 매핑 + StateManager 백레퍼런스
StateManager               # state 전환 (즉시 적용)
StateComponent             # 외부 컨테이너 (reservation 패턴)
```

소유 관계:

```
owner class
└── StateComponent
    └── StateManager
        └── StateMap
            └── abState 인스턴스들
```

---

## 핵심 개념

### Reservation 패턴

`StateComponent.change_state(id, dto)`는 즉시 전환하지 않고 **예약만** 한다.
다음 frame에서 `on_change_state()`가 호출될 때 비로소 실제 전환이 일어난다.
이렇게 분리하면 frame 내부에서 state를 바꿔도 현재 frame의 처리가 안전하게 끝난 뒤 적용된다.

### Lifecycle wrapper

`abState`는 두 가지 wrapper 메서드를 제공한다.

- `base_on_enter(state_param_dto)`: `_is_run_proc_once` 리셋 + `owner` cache + `state_param_dto` 저장 후 `on_enter()` 호출
- `base_on_proc_every_frame()`: `on_proc_once()`를 첫 frame에 한 번만 실행 후 매 frame마다 `on_proc_every_frame()` 호출

상속 클래스는 `on_enter` / `on_leave` / `on_proc_once` / `on_proc_every_frame` 4개의 abstract 메서드만 구현한다.

### state_param_dto

state 전환 시 다음 state로 전달되는 payload (`Optional[Any]`).
새 state는 `self.state_param_dto`로 접근한다.

### owner 타입 narrowing

`abState.owner`의 base 타입은 `Any`. concrete state class에서 attribute annotation으로 narrow하면 IDE/pyright의 자동완성·타입체크 효과를 받을 수 있다.

```python
class GameState(abState):
    owner: Game        # ← annotation override로 narrow
    ...
```

---

## 사용법

### 1. state 정의

`abState`를 상속하고 lifecycle 메서드를 구현한다.

```python
from enum import IntEnum
from python_library.state import abState, StateMap


class E_GAME_STATE(IntEnum):
    IDLE = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3


class IdleState(abState):
    owner: Game

    def on_enter(self):
        print(f"[IDLE] enter, dto={self.state_param_dto}")

    def on_leave(self):
        print("[IDLE] leave")

    def on_proc_once(self):
        print("[IDLE] first frame")

    def on_proc_every_frame(self):
        pass


class PlayingState(abState):
    owner: Game

    def on_enter(self):
        score = self.state_param_dto.get("score", 0) if self.state_param_dto else 0
        print(f"[PLAYING] start with score={score}")

    def on_leave(self): pass
    def on_proc_once(self): pass
    def on_proc_every_frame(self):
        if self.owner.is_game_over():
            self.owner.state_component.change_state(E_GAME_STATE.GAME_OVER)
```

### 2. owner class에 StateComponent 부착

```python
from python_library.state import StateComponent


class Game:
    def __init__(self):
        state_map = StateMap({})
        state_map._state_map = {
            E_GAME_STATE.IDLE: IdleState(state_map, E_GAME_STATE.IDLE),
            E_GAME_STATE.PLAYING: PlayingState(state_map, E_GAME_STATE.PLAYING),
        }

        self.state_component = StateComponent(
            owner=self,
            state_map=state_map,
            init_state_id=E_GAME_STATE.IDLE,
        )

    def is_game_over(self) -> bool:
        return False

    def tick(self):
        self.state_component.on_change_state()
        self.state_component.on_proc_every_frame()
```

### 3. state 전환

```python
game = Game()
game.tick()

game.state_component.change_state(
    E_GAME_STATE.PLAYING,
    state_param_dto={"score": 0, "level": 1},
)

game.tick()  # 예약 적용 → IdleState.on_leave → PlayingState.base_on_enter → on_proc_once + on_proc_every_frame
```

---

## API 요약

### `abState`

| 메서드 | 설명 |
|---|---|
| `base_on_enter(state_param_dto)` | 진입 wrapper — abstract `on_enter()` 호출 |
| `base_on_proc_every_frame()` | 매 frame wrapper — 첫 frame `on_proc_once()` + 매 frame `on_proc_every_frame()` |
| `on_enter()` (abstract) | state 진입 시 1회 호출 |
| `on_leave()` (abstract) | state 떠날 때 1회 호출 |
| `on_proc_once()` (abstract) | state 진입 후 첫 frame 1회 호출 |
| `on_proc_every_frame()` (abstract) | state 활성 동안 매 frame 호출 |
| `owner` | base_on_enter 시 자동 cache되는 owner 참조 (`Any`, concrete에서 narrow 권장) |
| `state_param_dto` | base_on_enter 시 저장된 payload |

### `StateComponent`

| 메서드 | 설명 |
|---|---|
| `change_state(state_id, state_param_dto=None)` | 다음 frame에 적용할 전환을 예약만 |
| `on_change_state()` | 예약된 전환을 실제 적용 (frame 시작 시 호출 권장) |
| `on_proc_once()` | 현재 state의 `on_proc_once` 위임 |
| `on_proc_every_frame()` | 현재 state의 `base_on_proc_every_frame` 위임 |
| `get_owner()` | owner 반환 |
| `get_state_manager()` | 내부 StateManager 반환 |

### `StateManager`

| 메서드 | 설명 |
|---|---|
| `change_state(state_id, dto)` | 즉시 전환 (현재 `on_leave` → 다음 `base_on_enter`) |
| `get_current_state()` | 현재 state 인스턴스 |
| `get_current_state_id()` | 현재 state_id (Enum) |

---

## frame loop 구성 예시

```python
while running:
    game.state_component.on_change_state()
    game.state_component.on_proc_every_frame()
    time.sleep(1 / 60)
```

`change_state`는 어느 시점에 호출해도 안전 — 항상 다음 frame 시작 시점에 적용된다.
