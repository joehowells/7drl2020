from random import randint, choices

from esper import Processor

from ecs.components.dead import Dead
from ecs.components.message import Message
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.threatening import Threatening
from ecs.components.visible import Visible


class ThreatProcessor(Processor):
    def process(self):
        player_entity, player = next(iter(self.world.get_component(Player)))

        player.visible_threat = 0
        player.actual_threat = 0

        monsters = []
        weights = []

        for entity, (monster, visible) in self.world.get_components(Monster, Visible):
            threat = max(0, max(monster.threat) - player.defend)
            player.visible_threat += threat

        for entity, (monster, threatening) in self.world.get_components(Monster, Threatening):
            threat = max(0, threatening.threat - player.defend)
            player.actual_threat += threat

            monsters.append(monster)
            weights.append(threat)

        if randint(0, 99) < player.actual_threat:
            # Work out which monster hit us
            monster = choices(monsters, weights)[0]

            self.world.create_entity(Message(
                text=f"The {monster.name} hits!",
                color=0xFFFF0000,
            ))

            player.health -= 1

            if player.health <= 0:
                self.world.add_component(player_entity, Dead())
                self.world.create_entity(Message(
                    text=f"You die...",
                ))
