from __future__ import annotations

from enum import Enum
from typing import Any, Optional, TYPE_CHECKING

from python_library.state.state import abState
from python_library.state.state_map import StateMap

if TYPE_CHECKING:
    from python_library.state.state_component import StateComponent


class StateManager:
    def __init__(
        self,
        state_map: StateMap,
        parent_state_component: StateComponent,
    ) -> None:
        self._parent_state_component: StateComponent = parent_state_component
        self._current_state_id: Optional[Enum] = None
        self._state_map: StateMap = state_map
        state_map.set_state_manager(self)

    def get_parent_state_component(self) -> StateComponent:
        return self._parent_state_component

    def get_state(self, state_id: Enum) -> abState:
        return self._state_map.get_state(state_id)

    def change_state(self, state_id: Enum, state_param_dto: Optional[Any] = None) -> abState:
        if self._current_state_id is not None:
            self.get_state(self._current_state_id).on_leave()

        self._current_state_id = state_id
        next_state = self.get_state(state_id)
        next_state.base_on_enter(state_param_dto)
        return next_state

    def get_current_state(self) -> Optional[abState]:
        if self._current_state_id is None:
            return None
        return self._state_map.get_state(self._current_state_id)

    def get_current_state_id(self) -> Optional[Enum]:
        return self._current_state_id
