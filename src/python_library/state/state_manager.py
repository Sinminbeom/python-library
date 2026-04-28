from __future__ import annotations

from enum import Enum
from typing import Any, Optional, TYPE_CHECKING

from python_library.state.state import abState
from python_library.state.state_lists import StateLists

if TYPE_CHECKING:
    from python_library.state.state_components import StateComponents


class StateManager:
    """현재 state 관리 + 즉시 전환 (OnLeave → BaseOnEnter)."""

    def __init__(
        self,
        state_lists: StateLists,
        parents_state_components: StateComponents,
    ) -> None:
        self._parents_state_components: StateComponents = parents_state_components
        self._current_state_id: Optional[Enum] = None
        self._state_lists: StateLists = state_lists
        state_lists.set_state_manager(self)

    def get_parents_state_components(self) -> StateComponents:
        return self._parents_state_components

    def get_state(self, state_id: Enum) -> abState:
        return self._state_lists.get_state(state_id)

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
        return self._state_lists.get_state(self._current_state_id)

    def get_current_state_id(self) -> Optional[Enum]:
        return self._current_state_id
