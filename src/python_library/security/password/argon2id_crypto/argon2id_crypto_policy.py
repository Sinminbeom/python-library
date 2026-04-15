from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Argon2idCryptoPolicy:
    time_cost: int = 3
    memory_cost_kib: int = 65536
    parallelism: int = 1
    pass
