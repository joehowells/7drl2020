from esper import Processor

from constants import DijkstraMap
from ecs.components.awake import Awake
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.position import Position
from ecs.components.threatening import Threatening
from functions import move_dijkstra


class MonsterProcessor(Processor):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))

        for entity, (monster, position, _) in self.world.get_components(Monster, Position, Awake):
            distance = game_map.dijkstra[DijkstraMap.PLAYER][position.y][position.x]
            if distance == monster.target_distance:
                self.world.add_component(entity, Threatening())
            else:
                if self.world.has_component(entity, Threatening):
                    self.world.add_component(entity, Threatening)
                move_dijkstra(game_map, position, DijkstraMap.PLAYER)
