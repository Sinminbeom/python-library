from __future__ import annotations

from enum import Enum
from typing import Dict, Optional, TYPE_CHECKING

from python_library.state.state import abState

if TYPE_CHECKING:
    from python_library.state.state_manager import StateManager


class StateMap:
    """state_id → abState 매핑 + StateManager 백레퍼런스 보유."""

    def __init__(self, state_map: Dict[Enum, abState]) -> None:
        self._state_map: Dict[Enum, abState] = state_map
        self._state_manager: Optional[StateManager] = None

    def get_state(self, state_id: Enum) -> abState:
        return self._state_map[state_id]

    def set_state_manager(self, state_manager: StateManager) -> None:
        self._state_manager = state_manager

    def get_state_manager(self) -> Optional[StateManager]:
        return self._state_manager
