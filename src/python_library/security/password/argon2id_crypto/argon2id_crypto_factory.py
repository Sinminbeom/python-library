from python_library.security.password.argon2id_crypto.argon2id_crypto import Argon2idCrypto
from python_library.security.password.password_crypto_factory import IPasswordCryptoFactory
from python_library.security.password.password_crypto_info_factory import (
    IPasswordCryptoInfoFactory,
)
from python_library.security.password.passwrod_crypto import IPasswordCrypto


class Argon2idCryptoFactory(IPasswordCryptoFactory):
    def __init__(self, password_crypto_info_factory: IPasswordCryptoInfoFactory):
        super().__init__()
        self._password_crypto_info_factory = password_crypto_info_factory

    def create_password_crypto(self) -> IPasswordCrypto:
        password_crypto = Argon2idCrypto()
        password_crypto.set_hasher(self._password_crypto_info_factory.create_hasher())

        return password_crypto
