from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

from action import Action


@dataclass
class Player:
    action: Action = Action()
    attack_action: Action = Action()
    defend_action: Action = Action()

    health: int = 10
    anger: int = 0
    visible_threat: int = 0
    actual_threat: int = 0

    base_attack: int = 1
    base_defend: int = 1
    attack_bonus: int = 0
    defend_bonus: int = 0
    attack_equip: int = 0
    defend_equip: int = 0
    attack: int = 1
    defend: int = 1
    number_of_attacks: int = 1

    level: int = 0

    kills: Counter = field(default_factory=Counter)
    killer: Optional[str] = None
