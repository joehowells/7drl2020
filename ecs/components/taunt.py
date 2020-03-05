from dataclasses import dataclass


class CanTaunt:
    pass


@dataclass
class Taunted:
    turns_left: int = 3
