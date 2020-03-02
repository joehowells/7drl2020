from dataclasses import dataclass

from ecs.components.event import Event


@dataclass
class Player:
    action: Event = None
    attack_action: Event = None
    defend_action: Event = None
