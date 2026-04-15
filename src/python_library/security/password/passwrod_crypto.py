from abc import abstractmethod, ABC

from python_library.security.password.password_crypto_hasher import IPasswordCryptoHasher


class IPasswordCrypto(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def verify(self, hash_value: str, password: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def set_hasher(self, hasher: IPasswordCryptoHasher) -> None:
        raise NotImplementedError()
