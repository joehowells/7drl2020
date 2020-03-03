from dataclasses import dataclass
from typing import Optional, Set, Tuple

from esper import Processor, World

from constants import DijkstraMap
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.monster import Monster
from functions import dijkstra_map


@dataclass
class MonsterMapProcessor(Processor):
    sources: Optional[Set[Tuple[int, int]]] = None

    def process(self):
        self.world: World

        _, game_map = next(iter(self.world.get_component(Map)))

        sources: Set[Tuple[int, int]] = set()
        for _, (position, monster) in self.world.get_components(LastKnownPosition, Monster):
            sources.add((position.x, position.y))

        if self.sources != sources:
            game_map.dijkstra[DijkstraMap.MONSTER] = dijkstra_map(game_map, sources)
            self.sources = sources
