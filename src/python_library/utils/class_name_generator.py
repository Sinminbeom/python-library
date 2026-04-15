from typing import Dict


class ClassNameGenerator:
    def __init__(self):
        self._seq_map: Dict[str, int] = dict()  # 클래스별 시퀀스 저장

    def __call__(self, owner: object, name: str | None = None) -> str:
        if name is not None:
            return name

        prefix = owner.__class__.__name__

        # prefix별로 독립적인 seq 생성
        if prefix not in self._seq_map:
            self._seq_map[prefix] = 0

        self._seq_map[prefix] += 1

        return f"{prefix}{self._seq_map[prefix]}"
