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

                for entity, (monster, visible, position) in self.world.get_components(Monster, Visible, Position):
                    distance = game_map.dijkstra[DijkstraMap.PLAYER][position.y][position.x]
                    in_range = 1 <= distance <= len(monster.threat)

                    if in_range or not self.world.has_component(entity, Assassin):
                        threat = max(monster.threat)
                        threat = max(0, threat - player.defend)
                        player.visible_threat += threat

                    if in_range and not self.world.has_component(entity, Blinded):
                        threat = monster.threat[distance - 1]
                        threat = max(0, threat - player.defend)
                        player.actual_threat += threat

                player.visible_threat = min(max(player.visible_threat, 0), MAX_THREAT)
                player.actual_threat = min(max(player.actual_threat, 0), MAX_THREAT)
