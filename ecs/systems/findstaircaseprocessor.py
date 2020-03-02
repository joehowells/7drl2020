from esper import Processor

from constants import DijkstraMap
from ecs.components.map import Map
from ecs.components.position import Position
from ecs.components.staircase import Staircase
from functions import dijkstra_map


class FindStaircaseProcessor(Processor):
    def process(self):
        _, map_ = next(iter(self.world.get_component(Map)))
        _, (_, position) = next(iter(self.world.get_components(Staircase, Position)))

        map_.dijkstra[DijkstraMap.STAIRS] = dijkstra_map(map_, [(position.x, position.y)])
