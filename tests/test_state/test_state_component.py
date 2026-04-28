from enum import IntEnum

from python_library.state import abState, StateComponent, StateMap


class E_TEST(IntEnum):
    A = 0
    B = 1


class _State(abState):
    log: list = []

    def on_enter(self):
        _State.log.append((self.state_id, "on_enter", self.state_param_dto))

    def on_leave(self):
        _State.log.append((self.state_id, "on_leave"))

    def on_proc_once(self):
        _State.log.append((self.state_id, "on_proc_once"))

    def on_proc_every_frame(self):
        _State.log.append((self.state_id, "on_proc_every_frame"))


def _build_component(init_state_id=None):
    _State.log = []
    sm = StateMap({})
    sm._state_map = {
        E_TEST.A: _State(sm, E_TEST.A),
        E_TEST.B: _State(sm, E_TEST.B),
    }
    return StateComponent(owner="owner_obj", state_map=sm, init_state_id=init_state_id)


def test_init_state_id_triggers_change_state_immediately():
    component = _build_component(init_state_id=E_TEST.A)

    assert component.get_state_manager().get_current_state_id() == E_TEST.A
    assert _State.log == [(E_TEST.A, "on_enter", None)]


def test_change_state_only_reserves_does_not_apply():
    component = _build_component(init_state_id=E_TEST.A)
    _State.log = []

    component.change_state(E_TEST.B, state_param_dto={"data": 1})

    assert component.get_state_manager().get_current_state_id() == E_TEST.A
    assert _State.log == []


def test_on_change_state_applies_reservation():
    component = _build_component(init_state_id=E_TEST.A)
    _State.log = []

    component.change_state(E_TEST.B, state_param_dto={"data": 1})
    component.on_change_state()

    assert component.get_state_manager().get_current_state_id() == E_TEST.B
    assert _State.log == [
        (E_TEST.A, "on_leave"),
        (E_TEST.B, "on_enter", {"data": 1}),
    ]


def test_on_change_state_without_reservation_is_noop():
    component = _build_component(init_state_id=E_TEST.A)
    _State.log = []

    component.on_change_state()

    assert component.get_state_manager().get_current_state_id() == E_TEST.A
    assert _State.log == []


def test_reservation_consumed_after_apply():
    component = _build_component(init_state_id=E_TEST.A)

    component.change_state(E_TEST.B)
    component.on_change_state()
    _State.log = []

    component.on_change_state()

    assert _State.log == []


def test_on_proc_every_frame_runs_proc_once_then_every_frame():
    component = _build_component(init_state_id=E_TEST.A)
    _State.log = []

    component.on_proc_every_frame()
    component.on_proc_every_frame()

    assert _State.log == [
        (E_TEST.A, "on_proc_once"),
        (E_TEST.A, "on_proc_every_frame"),
        (E_TEST.A, "on_proc_every_frame"),
    ]


def test_state_param_dto_propagated_to_new_state_on_enter():
    component = _build_component(init_state_id=E_TEST.A)

    payload = {"x": 42}
    component.change_state(E_TEST.B, state_param_dto=payload)
    component.on_change_state()

    state_b = component.get_state_manager().get_state(E_TEST.B)
    assert state_b.state_param_dto == payload


def test_owner_cached_in_state_after_enter():
    component = _build_component(init_state_id=E_TEST.A)

    state_a = component.get_state_manager().get_state(E_TEST.A)
    assert state_a.owner == "owner_obj"


def test_get_owner_returns_owner():
    component = _build_component()
    assert component.get_owner() == "owner_obj"
