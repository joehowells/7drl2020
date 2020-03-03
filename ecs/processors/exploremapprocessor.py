import itertools

from esper import Processor, World

from constants import DijkstraMap
from ecs.components.map import Map
from ecs.eventmixin import EventMixin
from functions import dijkstra_map, iter_neighbors


class ExploreMapProcessor(Processor, EventMixin):
    def process(self):
        self.world: World

        _, game_map = next(iter(self.world.get_component(Map)))

        sources = []
        for x, y in itertools.product(range(game_map.w), range(game_map.h)):
            if not game_map.explored[y][x]:
                sources.append((x, y))

        game_map.dijkstra[DijkstraMap.EXPLORE] = dijkstra_map(game_map, sources)
