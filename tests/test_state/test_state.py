from enum import IntEnum

from python_library.state import abState, StateMap


class E_TEST(IntEnum):
    A = 0
    B = 1


class _TrackingState(abState):
    def __init__(self, state_map, state_id):
        super().__init__(state_map, state_id)
        self.calls = []

    def on_enter(self):
        self.calls.append(("on_enter", self.state_param_dto))

    def on_leave(self):
        self.calls.append(("on_leave",))

    def on_proc_once(self):
        self.calls.append(("on_proc_once",))

    def on_proc_every_frame(self):
        self.calls.append(("on_proc_every_frame",))


def _build_state_map():
    sm = StateMap({})
    sm._state_map = {E_TEST.A: _TrackingState(sm, E_TEST.A)}
    return sm


def test_base_on_enter_resets_proc_once_flag_and_caches_parent():
    sm = _build_state_map()
    state = sm.get_state(E_TEST.A)
    state._is_run_proc_once = True

    state.base_on_enter(state_param_dto={"x": 1})

    assert state._is_run_proc_once is False
    assert state.state_param_dto == {"x": 1}
    assert state.calls == [("on_enter", {"x": 1})]


def test_base_on_enter_default_dto_is_none():
    sm = _build_state_map()
    state = sm.get_state(E_TEST.A)

    state.base_on_enter()

    assert state.state_param_dto is None
    assert state.calls == [("on_enter", None)]


def test_base_on_proc_every_frame_runs_on_proc_once_only_once():
    sm = _build_state_map()
    state = sm.get_state(E_TEST.A)

    state.base_on_proc_every_frame()
    state.base_on_proc_every_frame()
    state.base_on_proc_every_frame()

    assert state.calls == [
        ("on_proc_once",),
        ("on_proc_every_frame",),
        ("on_proc_every_frame",),
        ("on_proc_every_frame",),
    ]


def test_base_on_enter_then_base_on_proc_every_frame_full_lifecycle():
    sm = _build_state_map()
    state = sm.get_state(E_TEST.A)

    state.base_on_enter()
    state.base_on_proc_every_frame()
    state.base_on_proc_every_frame()

    assert state.calls == [
        ("on_enter", None),
        ("on_proc_once",),
        ("on_proc_every_frame",),
        ("on_proc_every_frame",),
    ]


def test_re_enter_resets_proc_once():
    sm = _build_state_map()
    state = sm.get_state(E_TEST.A)

    state.base_on_enter()
    state.base_on_proc_every_frame()

    state.base_on_enter()
    state.base_on_proc_every_frame()

    assert state.calls == [
        ("on_enter", None),
        ("on_proc_once",),
        ("on_proc_every_frame",),
        ("on_enter", None),
        ("on_proc_once",),
        ("on_proc_every_frame",),
    ]
