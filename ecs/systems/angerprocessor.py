from esper import Processor

from ecs.components.player import Player


class AngerProcessor(Processor):
    def process(self):
        _, player = next(iter(self.world.get_component(Player)))

        player.attack_bonus = 0
        player.defend_bonus = 0

        if player.anger >= 20:
            player.attack_bonus += 1

        if player.anger >= 40:
            player.defend_bonus += 1

        if player.anger >= 60:
            player.attack_bonus += 1

        if player.anger >= 80:
            player.defend_bonus += 1

        if player.anger >= 100:
            player.attack_bonus += 2
            player.defend_bonus += 2

        player.attack = player.base_attack + player.attack_bonus
        player.defend = player.base_defend + player.defend_bonus
