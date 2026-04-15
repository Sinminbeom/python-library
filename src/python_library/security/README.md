# security

보안 관련 기능을 담는 패키지. 현재 비밀번호 암호화 기능만 포함한다.

## 하위 패키지

```
security/
└── password/
    ├── password_crypto.py              # IPasswordCrypto 인터페이스
    ├── password_crypto_hasher.py       # IPasswordCryptoHasher 인터페이스
    ├── password_crypto_factory.py      # IPasswordCryptoFactory 인터페이스
    ├── password_crypto_info_factory.py # IPasswordCryptoInfoFactory 인터페이스
    └── argon2id_crypto/
        ├── argon2id_crypto.py          # Argon2id 구현체
        ├── argon2id_crypto_hasher.py   # argon2-cffi 기반 해셔
        ├── argon2id_crypto_policy.py   # 해싱 파라미터 정책
        ├── argon2id_crypto_factory.py  # 팩토리 구현체
        └── argon2id_crypto_info_factory.py
```

---

## 사용법

```python
from python_library.security.password.argon2id_crypto.argon2id_crypto_factory import Argon2idCryptoFactory
from python_library.security.password.argon2id_crypto.argon2id_crypto_info_factory import Argon2idCryptoInfoFactory
from python_library.security.password.argon2id_crypto.argon2id_crypto_policy import Argon2idCryptoPolicy

factory = Argon2idCryptoFactory(Argon2idCryptoInfoFactory(Argon2idCryptoPolicy()))
crypto = factory.create_password_crypto()

hashed = crypto.hash("mypassword")
is_valid = crypto.verify(hashed, "mypassword")  # True
```

`Argon2idCryptoPolicy()`는 기본 파라미터(OWASP 권장값)를 사용한다.
환경(개발/운영)에 따라 파라미터를 다르게 주입할 수 있다.

```python
policy = Argon2idCryptoPolicy(time_cost=3, memory_cost=65536, parallelism=4)
```

---

## 추상 팩토리 패턴

두 Factory 인터페이스가 협력해 암호화 객체를 완성한다.

```
IPasswordCryptoFactory ──────────── IPasswordCryptoInfoFactory
  create_password_crypto()             create_hasher()
        │                                    │
        ▼                                    ▼
  Argon2idCrypto  ◄── set_hasher ── Argon2idCryptoHasher
```

- `IPasswordCryptoInfoFactory.create_hasher()` → `Argon2idCryptoPolicy`(파라미터 정책)를 받아 해셔를 만든다.
- `IPasswordCryptoFactory.create_password_crypto()` → 암호화 객체를 만들고, 위 해셔를 `set_hasher()`로 주입한다.
- 호출 측은 `IPasswordCryptoFactory` 하나만 알면 되고, 해싱 파라미터 소스(기본값, 환경별 정책 등)는 `IPasswordCryptoInfoFactory` 구현체 교체로 처리한다.

```python
# Argon2idCryptoFactory 내부 동작
def create_password_crypto(self) -> IPasswordCrypto:
    password_crypto = Argon2idCrypto()
    password_crypto.set_hasher(self._password_crypto_info_factory.create_hasher())
    return password_crypto
```

---

## 설계 의도

### 왜 Argon2id인가

Argon2id는 OWASP에서 권장하는 최신 패스워드 해싱 알고리즘이다.
MD5, SHA-256, bcrypt보다 브루트포스 공격에 강하며 메모리 하드(memory-hard) 특성을 가진다.

### 인터페이스 계층

```
IPasswordCrypto
  hash(password: str) -> str
  verify(hash_value: str, password: str) -> bool

IPasswordCryptoHasher         # 실제 해싱 로직 (argon2-cffi 래핑)
IPasswordCryptoInfoFactory    # 파라미터(정책) 정보 팩토리
IPasswordCryptoFactory        # 구현체 생성 팩토리
```

`IPasswordCrypto`만 알면 구체 구현에 의존하지 않는다.
알고리즘 교체 시 `IPasswordCrypto`를 구현하는 새 클래스만 추가하면 된다.

---

## 새 암호화 알고리즘 추가 방법

1. `security/password/` 하위에 새 디렉토리를 만든다 (예: `bcrypt/`).
2. `IPasswordCrypto`, `IPasswordCryptoHasher`, `IPasswordCryptoInfoFactory`, `IPasswordCryptoFactory`를 구현한다.
3. Argon2id 구현체(`argon2id_crypto/`)를 참고해 동일한 파일 구조로 작성한다.
