from dataclasses import dataclass
from typing import Optional, Set, Tuple

from esper import Processor, World

from constants import DijkstraMap
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.stairs import Stairs
from functions import dijkstra_map


@dataclass
class StairMapProcessor(Processor):
    sources: Optional[Set[Tuple[int, int]]] = None

    def process(self):
        self.world: World

        for _, game_map in self.world.get_component(Map):
            sources: Set[Tuple[int, int]] = set()
            for _, (position, _) in self.world.get_components(LastKnownPosition, Stairs):
                sources.add((position.x, position.y))

            if self.sources != sources:
                game_map.dijkstra[DijkstraMap.STAIRS] = dijkstra_map(game_map, sources, check_explored=False)
                self.sources = sources
