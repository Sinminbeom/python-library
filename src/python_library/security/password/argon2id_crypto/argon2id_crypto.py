from python_library.security.password.password_crypto_hasher import IPasswordCryptoHasher
from python_library.security.password.passwrod_crypto import IPasswordCrypto


class Argon2idCrypto(IPasswordCrypto):
    def __init__(self):
        super().__init__()
        self._hasher: IPasswordCryptoHasher | None = None

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, hash_value: str, password: str) -> bool:
        return self._hasher.verify(hash_value, password)

    def set_hasher(self, hasher: IPasswordCryptoHasher) -> None:
        self._hasher = hasher
        pass
