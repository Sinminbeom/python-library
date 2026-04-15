from abc import ABC, abstractmethod

from python_library.security.password.password_crypto_hasher import IPasswordCryptoHasher


class IPasswordCryptoInfoFactory(ABC):
    @abstractmethod
    def create_hasher(self) -> IPasswordCryptoHasher:
        raise NotImplementedError()
