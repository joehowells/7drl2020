from dataclasses import dataclass

from ecs.components.event import Event


@dataclass
class Player:
    action: Event = None
    attack_action: Event = None
    defend_action: Event = None

    health: int = 0
    anger: int = 0
    visible_threat: int = 0
    actual_threat: int = 0
