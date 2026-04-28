from enum import IntEnum

from python_library.state import abState, StateComponent, StateMap


class E_TEST(IntEnum):
    A = 0
    B = 1
    C = 2


class _RecordingState(abState):
    log: list = []

    def on_enter(self):
        _RecordingState.log.append((self.state_id, "on_enter", self.state_param_dto))

    def on_leave(self):
        _RecordingState.log.append((self.state_id, "on_leave"))

    def on_proc_once(self): pass
    def on_proc_every_frame(self): pass


def _build():
    _RecordingState.log = []
    sm = StateMap({})
    sm._state_map = {
        E_TEST.A: _RecordingState(sm, E_TEST.A),
        E_TEST.B: _RecordingState(sm, E_TEST.B),
        E_TEST.C: _RecordingState(sm, E_TEST.C),
    }
    component = StateComponent(owner="parent", state_map=sm)
    return component.get_state_manager()


def test_change_state_immediate_calls_on_leave_then_base_on_enter():
    mgr = _build()
    mgr.change_state(E_TEST.A)
    _RecordingState.log = []

    mgr.change_state(E_TEST.B, state_param_dto={"k": "v"})

    assert _RecordingState.log == [
        (E_TEST.A, "on_leave"),
        (E_TEST.B, "on_enter", {"k": "v"}),
    ]


def test_first_change_state_no_on_leave():
    mgr = _build()

    mgr.change_state(E_TEST.A)

    assert _RecordingState.log == [(E_TEST.A, "on_enter", None)]


def test_get_current_state_id_tracks_change_state():
    mgr = _build()
    assert mgr.get_current_state_id() is None

    mgr.change_state(E_TEST.A)
    assert mgr.get_current_state_id() == E_TEST.A

    mgr.change_state(E_TEST.B)
    assert mgr.get_current_state_id() == E_TEST.B


def test_get_current_state_returns_instance():
    mgr = _build()
    mgr.change_state(E_TEST.C)

    current = mgr.get_current_state()
    assert current is mgr.get_state(E_TEST.C)


def test_state_manager_has_back_reference_from_state_map():
    mgr = _build()
    state = mgr.get_state(E_TEST.A)
    assert state.state_map.get_state_manager() is mgr
