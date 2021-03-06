from esper import Processor, World

from constants import DijkstraMap
from ecs.components.map import Map
from ecs.components.position import Position


class Coincident:
    pass


class Adjacent:
    pass


class SpatialProcessor(Processor):
    def process(self):
        self.world: World

        for _, game_map in self.world.get_component(Map):
            for entity, position in self.world.get_component(Position):
                distance = game_map.dijkstra[DijkstraMap.PLAYER][position.y][position.x]

                if distance == 0:
                    self.world.add_component(entity, Coincident())
                elif self.world.has_component(entity, Coincident):
                    self.world.remove_component(entity, Coincident)

                if distance == 1:
                    self.world.add_component(entity, Adjacent())
                elif self.world.has_component(entity, Adjacent):
                    self.world.remove_component(entity, Adjacent)
