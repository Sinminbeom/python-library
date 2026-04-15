from __future__ import annotations

from abc import abstractmethod
from typing import List, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from python_library.category.category_action import CategoryAction


class ICategoryComponent:
    @abstractmethod
    def get(self, name: str) -> ICategoryComponent:
        raise NotImplementedError

    @abstractmethod
    def invoke(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_all_actions(self) -> List[CategoryAction]:
        raise NotImplementedError

    def __getitem__(self, name: str) -> ICategoryComponent:
        return self.get(name)

    def __contains__(self, name: object) -> bool:
        # 기본 구현은 group이 아니면 False
        return False

    # 선택: 모든 컴포넌트를 ()로 호출 가능하게 기본 제공
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.invoke(*args, **kwargs)
