from dataclasses import dataclass

from ecs.components.event import Event


@dataclass
class Player:
    action: Event = Event("wait", {"anger": -1})
    attack_action: Event = Event("wait", {"anger": -1})
    defend_action: Event = Event("wait", {"anger": -1})

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
