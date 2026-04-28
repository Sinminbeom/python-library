from enum import IntEnum

from python_library.state import abState, StateLists, StateComponents


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


def _build_components(init_state_id=None):
    _State.log = []
    sl = StateLists({})
    sl._state_list = {
        E_TEST.A: _State(sl, E_TEST.A),
        E_TEST.B: _State(sl, E_TEST.B),
    }
    return StateComponents(parent_process="parent_obj", state_lists=sl, init_state_id=init_state_id)


def test_init_state_id_triggers_change_state_immediately():
    components = _build_components(init_state_id=E_TEST.A)

    assert components.get_state_manager().get_current_state_id() == E_TEST.A
    assert _State.log == [(E_TEST.A, "on_enter", None)]


def test_change_state_only_reserves_does_not_apply():
    components = _build_components(init_state_id=E_TEST.A)
    _State.log = []

    components.change_state(E_TEST.B, state_param_dto={"data": 1})

    assert components.get_state_manager().get_current_state_id() == E_TEST.A
    assert _State.log == []


def test_on_change_state_applies_reservation():
    components = _build_components(init_state_id=E_TEST.A)
    _State.log = []

    components.change_state(E_TEST.B, state_param_dto={"data": 1})
    components.on_change_state()

    assert components.get_state_manager().get_current_state_id() == E_TEST.B
    assert _State.log == [
        (E_TEST.A, "on_leave"),
        (E_TEST.B, "on_enter", {"data": 1}),
    ]


def test_on_change_state_without_reservation_is_noop():
    components = _build_components(init_state_id=E_TEST.A)
    _State.log = []

    components.on_change_state()

    assert components.get_state_manager().get_current_state_id() == E_TEST.A
    assert _State.log == []


def test_reservation_consumed_after_apply():
    components = _build_components(init_state_id=E_TEST.A)

    components.change_state(E_TEST.B)
    components.on_change_state()
    _State.log = []

    components.on_change_state()

    assert _State.log == []


def test_on_proc_every_frame_runs_proc_once_then_every_frame():
    components = _build_components(init_state_id=E_TEST.A)
    _State.log = []

    components.on_proc_every_frame()
    components.on_proc_every_frame()

    assert _State.log == [
        (E_TEST.A, "on_proc_once"),
        (E_TEST.A, "on_proc_every_frame"),
        (E_TEST.A, "on_proc_every_frame"),
    ]


def test_state_param_dto_propagated_to_new_state_on_enter():
    components = _build_components(init_state_id=E_TEST.A)

    payload = {"x": 42}
    components.change_state(E_TEST.B, state_param_dto=payload)
    components.on_change_state()

    state_b = components.get_state_manager().get_state(E_TEST.B)
    assert state_b.state_param_dto == payload


def test_parent_process_cached_in_state_after_enter():
    components = _build_components(init_state_id=E_TEST.A)

    state_a = components.get_state_manager().get_state(E_TEST.A)
    assert state_a.parents_process == "parent_obj"


def test_get_parent_process_returns_owner():
    components = _build_components()
    assert components.get_parent_process() == "parent_obj"
