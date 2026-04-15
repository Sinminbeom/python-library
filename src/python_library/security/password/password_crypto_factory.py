from abc import ABC, abstractmethod

from python_library.security.password.passwrod_crypto import IPasswordCrypto


class IPasswordCryptoFactory(ABC):
    @abstractmethod
    def create_password_crypto(self) -> IPasswordCrypto:
        raise NotImplementedError()
