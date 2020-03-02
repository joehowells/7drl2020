from random import randint

from esper import Processor

from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.threatening import Threatening
from ecs.components.visible import Visible


class ThreatProcessor(Processor):
    def process(self):
        _, player = next(iter(self.world.get_component(Player)))

        player.visible_threat = 0
        player.actual_threat = 0

        for entity, (monster, visible) in self.world.get_components(Monster, Visible):
            player.visible_threat += monster.threat

            if self.world.has_component(entity, Threatening):
                player.actual_threat += monster.threat

        if randint(0, 99) < player.actual_threat:
            player.health += 1
