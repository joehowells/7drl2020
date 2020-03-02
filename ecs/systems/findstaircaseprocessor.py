from esper import Processor

from constants import DijkstraMap
from ecs.components.map import Map
from ecs.components.position import Position
from ecs.components.staircase import Staircase
from functions import dijkstra_map


class FindStaircaseProcessor(Processor):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, (_, position) = next(iter(self.world.get_components(Staircase, Position)))

        game_map.dijkstra[DijkstraMap.STAIRS] = dijkstra_map(game_map, [(position.x, position.y)])
