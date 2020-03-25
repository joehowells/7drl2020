from esper import Processor, World

from constants import MAX_THREAT
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player


class PlayerThreatProcessor(Processor):
    def process(self):
        self.world: World

        for _, game_map in self.world.get_component(Map):
            for player_entity, player in self.world.get_component(Player):
                player.visible_threat = 0
                player.actual_threat = 0

                for entity, monster in self.world.get_component(Monster):
                    player.visible_threat += monster.visible_threat
                    player.actual_threat += monster.actual_threat

                player.visible_threat = min(max(player.visible_threat, 0), MAX_THREAT)
                player.actual_threat = min(max(player.actual_threat, 0), MAX_THREAT)
