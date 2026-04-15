from typing import Callable, Generic, Self, TypeVar, ParamSpec
from python_library.category.category_component import ICategoryComponent

P = ParamSpec("P")
R = TypeVar("R")


class CategoryAction(ICategoryComponent, Generic[P, R]):
    def __init__(self, action: Callable[P, R]) -> None:
        super().__init__()
        self.action: Callable[P, R] = action

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.action(*args, **kwargs)

    def invoke(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.action(*args, **kwargs)

    def get(self, name: str) -> ICategoryComponent:
        raise KeyError(f"CategoryAction has no children: cannot get '{name}'")

    def get_all_actions(self) -> list[Self]:
        return [self]
