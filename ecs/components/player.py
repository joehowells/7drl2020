from dataclasses import dataclass

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
    attack: int = 1
    defend: int = 1

    # TODO: Find a better place to put this
    level: int = 0
