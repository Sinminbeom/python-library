from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from python_library.state.state_component import StateComponent
    from python_library.state.state_manager import StateManager
    from python_library.state.state_map import StateMap


class abState(ABC):
    """
    Tetris C# abState 동등 클래스.

    Lifecycle:
      base_on_enter(state_param_dto)
        -> _is_run_proc_once 리셋
        -> parents_process cache
        -> state_param_dto 저장
        -> on_enter()

      base_on_proc_every_frame()
        -> on_proc_once() 1회
        -> on_proc_every_frame() 매 frame
    """

    def __init__(self, state_map: StateMap, state_id: Enum) -> None:
        self.state_map: StateMap = state_map
        self.state_id: Enum = state_id
        self._is_run_proc_once: bool = False
        self.parents_process: Any = None
        self.state_param_dto: Optional[Any] = None

    def get_state_manager(self) -> Optional[StateManager]:
        if self.state_map is None:
            return None
        return self.state_map.get_state_manager()

    def get_state_component(self) -> Optional[StateComponent]:
        mgr = self.get_state_manager()
        if mgr is None:
            return None
        return mgr.get_parent_state_component()

    def get_parents_process(self) -> Any:
        component = self.get_state_component()
        if component is None:
            return None
        return component.get_parent_process()

    def _set_parent_process(self) -> None:
        self.parents_process = self.get_parents_process()

    def base_on_enter(self, state_param_dto: Optional[Any] = None) -> None:
        self._is_run_proc_once = False
        self.state_param_dto = state_param_dto
        self._set_parent_process()
        self.on_enter()

    def base_on_proc_every_frame(self) -> None:
        if not self._is_run_proc_once:
            self.on_proc_once()
            self._is_run_proc_once = True

        self.on_proc_every_frame()

    @abstractmethod
    def on_enter(self) -> None: ...

    @abstractmethod
    def on_leave(self) -> None: ...

    @abstractmethod
    def on_proc_once(self) -> None: ...

    @abstractmethod
    def on_proc_every_frame(self) -> None: ...
