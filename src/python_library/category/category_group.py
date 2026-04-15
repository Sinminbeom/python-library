from typing import Dict, List, KeysView, ValuesView, ItemsView, Iterator, Any

from python_library.category.category_action import CategoryAction
from python_library.category.category_component import ICategoryComponent


class CategoryGroup(ICategoryComponent):
    def __init__(self) -> None:
        super().__init__()
        self._children: Dict[str, ICategoryComponent] = dict()

    def push(self, name: str, component: ICategoryComponent) -> None:
        self._children[name] = component

    def get(self, name: str) -> ICategoryComponent:
        return self._children[name]

    def invoke(self, *args: Any, **kwargs: Any) -> None:
        for action in self.get_all_actions():
            action.invoke(*args, **kwargs)

    def get_all_actions(self) -> List[CategoryAction]:
        result: list[CategoryAction] = []
        for child in self._children.values():
            result.extend(child.get_all_actions())
        return result

    # --- 여기부터 dict-like 편의 기능 추가 ---
    def __contains__(self, name: object) -> bool:
        return name in self._children

    def __getitem__(self, name: str) -> ICategoryComponent:
        return self._children[name]

    def __setitem__(self, name: str, component: ICategoryComponent) -> None:
        self._children[name] = component

    def __iter__(self) -> Iterator[str]:
        # dict처럼 iterate하면 key가 나옴
        return iter(self._children)

    def __len__(self) -> int:
        return len(self._children)

    def keys(self) -> KeysView[str]:
        return self._children.keys()

    def values(self) -> ValuesView[ICategoryComponent]:
        return self._children.values()

    def items(self) -> ItemsView[str, ICategoryComponent]:
        return self._children.items()

    # 필요하면 children 원본 dict 반환 (읽기용으로만 쓰는 걸 추천)
    def to_dict(self) -> Dict[str, ICategoryComponent]:
        return dict(self._children)

    def __repr__(self) -> str:
        def convert(value):
            if isinstance(value, CategoryGroup):
                return {k: convert(v) for k, v in value._children.items()}
            else:
                return value

        return repr({k: convert(v) for k, v in self._children.items()})
