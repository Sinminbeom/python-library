from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from python_library.state.state_lists import StateLists
from python_library.state.state_manager import StateManager


class StateComponents:
    """
    process가 보유하는 state machine 컨테이너.

    Reservation 패턴:
      - change_state(state_id, dto): 다음 frame에 적용할 전환을 예약만
      - on_change_state(): 예약된 전환을 실제 적용 (frame 안전성)
      - on_proc_every_frame(): 현재 state의 base_on_proc_every_frame 위임
    """

    def __init__(
        self,
        parent_process: Any,
        state_lists: StateLists,
        init_state_id: Optional[Enum] = None,
    ) -> None:
        self._parent_process: Any = parent_process
        self._state_manager: StateManager = StateManager(state_lists, self)
        self._reserve_state_id: Optional[Enum] = None
        self._reserve_state_param_dto: Optional[Any] = None

        if init_state_id is not None:
            self._state_manager.change_state(init_state_id)

    def get_parent_process(self) -> Any:
        return self._parent_process

    def get_state_manager(self) -> StateManager:
        return self._state_manager

    def change_state(self, state_id: Enum, state_param_dto: Optional[Any] = None) -> None:
        """다음 on_change_state() 호출 시 적용될 전환을 예약."""
        self._reserve_state_id = state_id
        self._reserve_state_param_dto = state_param_dto

    def on_change_state(self) -> None:
        """예약된 state 전환을 실제 적용."""
        if self._reserve_state_id is None:
            return

        self._state_manager.change_state(self._reserve_state_id, self._reserve_state_param_dto)
        self._reserve_state_id = None
        self._reserve_state_param_dto = None

    def on_proc_once(self) -> None:
        current = self._state_manager.get_current_state()
        if current is not None:
            current.on_proc_once()

    def on_proc_every_frame(self) -> None:
        current = self._state_manager.get_current_state()
        if current is not None:
            current.base_on_proc_every_frame()
