from python_library.security.password.argon2id_crypto.argon2id_crypto_hasher import (
    Argon2idCryptoHasher,
)
from python_library.security.password.argon2id_crypto.argon2id_crypto_policy import (
    Argon2idCryptoPolicy,
)
from python_library.security.password.password_crypto_hasher import IPasswordCryptoHasher
from python_library.security.password.password_crypto_info_factory import (
    IPasswordCryptoInfoFactory,
)


class Argon2idCryptoInfoFactory(IPasswordCryptoInfoFactory):
    def __init__(self, policy: Argon2idCryptoPolicy):
        super().__init__()
        self._policy = policy

    def create_hasher(self) -> IPasswordCryptoHasher:
        return Argon2idCryptoHasher(self._policy)
