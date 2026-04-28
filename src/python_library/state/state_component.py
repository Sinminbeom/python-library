from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from python_library.state.state_manager import StateManager
from python_library.state.state_map import StateMap


class StateComponent:
    def __init__(
        self,
        owner: Any,
        state_map: StateMap,
        init_state_id: Optional[Enum] = None,
    ) -> None:
        self._owner: Any = owner
        self._state_manager: StateManager = StateManager(state_map, self)
        self._reserve_state_id: Optional[Enum] = None
        self._reserve_state_param_dto: Optional[Any] = None

        if init_state_id is not None:
            self._state_manager.change_state(init_state_id)

    def get_owner(self) -> Any:
        return self._owner

    def get_state_manager(self) -> StateManager:
        return self._state_manager

    def change_state(self, state_id: Enum, state_param_dto: Optional[Any] = None) -> None:
        self._reserve_state_id = state_id
        self._reserve_state_param_dto = state_param_dto

    def on_change_state(self) -> None:
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
