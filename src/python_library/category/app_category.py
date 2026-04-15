from typing import Dict, Callable
from abc import abstractmethod

from python_library.category.category_component import ICategoryComponent
from python_library.singleton.singleton import Singleton


class AppCategory(Singleton):
    def __init__(self) -> None:
        super().__init__()

        self.cate_queue: Dict[str, ICategoryComponent] = dict()
        self.cate_reg_queue: Dict[str, Callable[[], None]] = dict()

        self.register_category()

    @abstractmethod
    def register_category(self) -> None:
        raise NotImplementedError

    def get_cate_callback(self, category: str) -> Callable[[], None]:
        return self.cate_reg_queue[category]
