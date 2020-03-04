from dataclasses import dataclass

from action import Action


@dataclass
class Player:
    action: Action = Action("wait", {"anger": -1})
    attack_action: Action = Action("wait", {"anger": -1})
    defend_action: Action = Action("wait", {"anger": -1})

    health: int = 10
    anger: int = 0
    visible_threat: int = 0
    actual_threat: int = 0

    base_attack: int = 1
    base_defend: int = 1
    attack_bonus: int = 0
    defend_bonus: int = 0
    attack: int = 1
    defend: int = 1
