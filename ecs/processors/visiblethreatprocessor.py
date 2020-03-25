from esper import Processor, World

from constants import DijkstraMap
from ecs.components.assassin import Assassin
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.visible import Visible


class VisibleThreatProcessor(Processor):
    def process(self):
        self.world: World

        for _, game_map in self.world.get_component(Map):
            for _, player in self.world.get_component(Player):
                for entity, (monster, _, position) in self.world.get_components(Monster, Visible, Position):
                    distance = game_map.dijkstra[DijkstraMap.PLAYER][position.y][position.x]
                    in_range = 1 <= distance <= len(monster.threat)

                    if in_range or not self.world.has_component(entity, Assassin):
                        visible_threat = max(monster.threat)
                        visible_threat = max(0, visible_threat - player.defend)
                    else:
                        visible_threat = 0

                    monster.visible_threat = visible_threat
