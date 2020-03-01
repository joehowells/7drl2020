import itertools
from typing import Tuple, Set

from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.processor import Processor
from functions import dijkstra_map, iter_neighbors


class AutoExploreProcessor(Processor):
    def process(self):
        _, map_ = next(iter(self.world.get_component(Map)))
        _, (_, position) = next(iter(self.world.get_components(Player, Position)))

        sources: Set[Tuple[int, int]] = set()

        for x, y in itertools.product(range(map_.w), range(map_.h)):
            if not map_.explored[y][x] and any(map_.explored[y][x] for x, y in iter_neighbors(x, y, map_)):
                sources.add((x, y))

        map_.dijkstra["auto_explore"] = dijkstra_map(map_, sources)
