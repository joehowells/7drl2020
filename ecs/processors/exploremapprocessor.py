import itertools
from dataclasses import dataclass
from typing import Optional, Set, Tuple

from esper import Processor, World

from constants import DijkstraMap
from ecs.components.map import Map
from ecs.eventmixin import EventMixin
from functions import dijkstra_map


@dataclass
class ExploreMapProcessor(Processor, EventMixin):
    sources: Optional[Set[Tuple[int, int]]] = None

    def process(self):
        self.world: World

        _, game_map = next(iter(self.world.get_component(Map)))

        sources: Set[Tuple[int, int]] = set()
        for x, y in itertools.product(range(game_map.w), range(game_map.h)):
            if not game_map.explored[y][x]:
                sources.add((x, y))

        if self.sources != sources:
            game_map.dijkstra[DijkstraMap.EXPLORE] = dijkstra_map(game_map, sources)
            self.sources = sources
