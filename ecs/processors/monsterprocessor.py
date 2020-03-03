from esper import Processor

from constants import DijkstraMap
from ecs.components.awake import Awake
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.position import Position
from ecs.components.threatening import Threatening
from functions import move_dijkstra, move


class MonsterProcessor(Processor):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))

        for entity, (monster, position, _) in self.world.get_components(Monster, Position, Awake):
            distance = game_map.dijkstra[DijkstraMap.PLAYER][position.y][position.x]
            if distance <= len(monster.threat):
                self.world.add_component(entity, Threatening(threat=monster.threat[distance-1]))
            else:
                if self.world.has_component(entity, Threatening):
                    self.world.remove_component(entity, Threatening)

                if distance > len(monster.threat):
                    target = move_dijkstra(game_map, position, DijkstraMap.PLAYER)
                else:
                    target = move_dijkstra(game_map, position, DijkstraMap.PLAYER, reverse=True)

                if target:
                    move(game_map, position, target)