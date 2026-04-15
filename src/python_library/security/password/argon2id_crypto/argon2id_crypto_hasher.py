from argon2 import PasswordHasher as _Argon2Hasher
from argon2 import Type

from python_library.security.password.argon2id_crypto.argon2id_crypto_policy import (
    Argon2idCryptoPolicy,
)
from python_library.security.password.password_crypto_hasher import IPasswordCryptoHasher


class Argon2idCryptoHasher(IPasswordCryptoHasher):
    def __init__(self, policy: Argon2idCryptoPolicy):
        super().__init__()
        self._hasher = _Argon2Hasher(
            time_cost=policy.time_cost,
            memory_cost=policy.memory_cost_kib,
            parallelism=policy.parallelism,
            type=Type.ID,
        )

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, hash_value: str, password: str) -> bool:
        try:
            return self._hasher.verify(hash_value, password)
        except Exception:
            return False
