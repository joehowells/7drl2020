from dataclasses import dataclass

from ecs.components.event import Event


@dataclass
class Player:
    action: Event = None
    attack_action: Event = None
    defend_action: Event = None

    health: int = 1
    anger: int = 0
    visible_threat: int = 0
    actual_threat: int = 0

    base_attack: int = 1
    base_defend: int = 1
    attack_bonus: int = 0
    defend_bonus: int = 0
    attack: int = 1
    defend: int = 1
