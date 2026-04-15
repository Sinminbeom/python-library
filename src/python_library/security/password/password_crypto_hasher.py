from abc import ABC, abstractmethod


class IPasswordCryptoHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def verify(self, hash_value: str, password: str) -> bool:
        raise NotImplementedError()
