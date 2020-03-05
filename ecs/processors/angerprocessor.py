from esper import Processor

from ecs.components.message import Message
from ecs.components.player import Player


class AngerProcessor(Processor):
    def __init__(self):
        self.old_tier = 0

    def process(self):
        _, player = next(iter(self.world.get_component(Player)))

        player.attack_bonus = 0
        player.defend_bonus = 0
        new_tier = 0

        if player.anger >= 20:
            new_tier = 1
            player.attack_bonus += 1

        if player.anger >= 40:
            new_tier = 2
            player.defend_bonus += 1

        if player.anger >= 60:
            new_tier = 3
            player.attack_bonus += 1

        if player.anger >= 80:
            new_tier = 4
            player.defend_bonus += 1

        if player.anger >= 95:
            new_tier = 5
            player.attack_bonus += 1
            player.defend_bonus += 1

        player.attack = player.base_attack + player.attack_equip + player.attack_bonus
        player.defend = player.base_defend + player.defend_equip + player.defend_bonus

        if new_tier > self.old_tier:
            self.world.create_entity(Message(
                text="Your anger makes you stronger!",
                color=0xFFFF0000,
            ))

        if new_tier < self.old_tier:
            self.world.create_entity(Message(
                text="You calm down.",
                color=0xFF0000FF,
            ))

        self.old_tier = new_tier
