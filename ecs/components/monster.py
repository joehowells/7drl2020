from dataclasses import dataclass, field
from typing import List


@dataclass
class Monster:
    name: str = "monster"
    article: str = "a"
    threat: List[int] = field(default_factory=lambda: [1])
    health: int = 1
    defend: int = 1
    thunder_immune: bool = False
