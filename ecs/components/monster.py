from dataclasses import dataclass


@dataclass
class Monster:
    target_distance: int = 1
    threat: int = 1
