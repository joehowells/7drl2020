from esper import Processor, World

from constants import DijkstraMap, MAX_THREAT
from ecs.components.assassin import Assassin
from ecs.components.blinded import Blinded
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.visible import Visible


class ThreatProcessor(Processor):
    def process(self):
        self.world: World

        for _, game_map in self.world.get_component(Map):
            for player_entity, player in self.world.get_component(Player):
                player.visible_threat = 0
                player.actual_threat = 0

                for entity, (monster, _, position) in self.world.get_components(Monster, Visible, Position):
                    distance = game_map.dijkstra[DijkstraMap.PLAYER][position.y][position.x]
                    in_range = 1 <= distance <= len(monster.threat)

                    if in_range or not self.world.has_component(entity, Assassin):
                        visible_threat = max(monster.threat)
                        visible_threat = max(0, visible_threat - player.defend)
                    else:
                        visible_threat = 0

                    if in_range and not self.world.has_component(entity, Blinded):
                        actual_threat = monster.threat[distance - 1]
                        actual_threat = max(0, actual_threat - player.defend)
                    else:
                        actual_threat = 0

                    monster.visible_threat = visible_threat
                    monster.actual_threat = actual_threat

                    player.visible_threat += visible_threat
                    player.actual_threat += actual_threat

                player.visible_threat = min(max(player.visible_threat, 0), MAX_THREAT)
                player.actual_threat = min(max(player.actual_threat, 0), MAX_THREAT)
