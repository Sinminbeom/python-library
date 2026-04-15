from python_library.security.password.argon2id_crypto.argon2id_crypto_factory import (
    Argon2idCryptoFactory,
)
from python_library.security.password.argon2id_crypto.argon2id_crypto_info_factory import (
    Argon2idCryptoInfoFactory,
)
from python_library.security.password.argon2id_crypto.argon2id_crypto_policy import (
    Argon2idCryptoPolicy,
)


def test_argon2id():
    factory = Argon2idCryptoFactory(Argon2idCryptoInfoFactory(Argon2idCryptoPolicy()))
    crypto = factory.create_password_crypto()
    crypto_hash = crypto.hash("mypassword")
    print(crypto_hash)
    verify = crypto.verify(crypto_hash, "mypassword")
    assert verify is True
