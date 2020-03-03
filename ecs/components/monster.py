from dataclasses import dataclass


@dataclass
class Monster:
    name: str = "monster"
    target_distance: int = 1
    threat: int = 5
    health: int = 2
    defend: int = 1
