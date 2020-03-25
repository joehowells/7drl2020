from esper import Processor, World

from constants import DijkstraMap
from ecs.components.blinded import Blinded
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.visible import Visible


class ActualThreatProcessor(Processor):
    def process(self):
        self.world: World

        for _, game_map in self.world.get_component(Map):
            for player_entity, player in self.world.get_component(Player):
                for entity, (monster, _, position) in self.world.get_components(Monster, Visible, Position):
                    distance = game_map.dijkstra[DijkstraMap.PLAYER][position.y][position.x]
                    in_range = 1 <= distance <= len(monster.threat)

                    if in_range and not self.world.has_component(entity, Blinded):
                        actual_threat = monster.threat[distance - 1]
                        actual_threat = max(0, actual_threat - player.defend)
                    else:
                        actual_threat = 0

                    monster.actual_threat = actual_threat
