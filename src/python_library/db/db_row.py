from abc import abstractmethod, ABC
from datetime import datetime
from typing import Dict, Any, Type, TypeVar, cast, Callable
from uuid import UUID

T = TypeVar("T")


class IDBRow(ABC):
    @abstractmethod
    def push(self, key: str, value: Any) -> None: ...

    @abstractmethod
    def get(self, key: str) -> Any: ...

    @abstractmethod
    def size(self) -> int: ...

    @abstractmethod
    def get_as(self, key: str, typ: Type[T]) -> T: ...

    @abstractmethod
    def get_as_or_none(self, key: str, typ: Type[T]) -> T | None: ...


class DBRow(IDBRow):
    def __init__(self):
        self._row: Dict[str, Any] = dict()
        pass

    def push(self, key: str, value: Any) -> None:
        self._row[key] = value

    def get(self, key: str) -> Any:
        return self._row[key]

    def size(self) -> int:
        return len(self._row)

    def get_as(self, key: str, typ: Type[T]) -> T:
        v = self._row.get(key)
        if v is None:
            raise KeyError(key)

        if typ is UUID:
            return cast(T, v if isinstance(v, UUID) else UUID(str(v)))

        if typ is datetime:
            return cast(
                T, v if isinstance(v, datetime) else datetime.fromisoformat(str(v))
            )

        if isinstance(v, typ):
            return v

        try:
            ctor = cast(Callable[[Any], T], typ)
            return ctor(v)
        except Exception as e:
            raise TypeError(f"Cannot cast key={key} value={v!r} to {typ}") from e

    def get_as_or_none(self, key: str, typ: Type[T]) -> T | None:
        v = self._row.get(key)
        if v is None:
            return None
        return self.get_as(key, typ)

    def __repr__(self):
        return f"DBRow({self._row})"
