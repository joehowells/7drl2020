from dataclasses import dataclass
from typing import Optional, Tuple, Set

from esper import Processor, World

from constants import DijkstraMap, AWAKE_DISTANCE
from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from functions import dijkstra_map


@dataclass
class PlayerMapProcessor(Processor):
    sources: Optional[Set[Tuple[int, int]]] = None

    def process(self):
        self.world: World

        for _, game_map in self.world.get_component(Map):
            for _, (position, _) in self.world.get_components(Position, Player):
                sources = {(position.x, position.y)}

                if self.sources != sources:
                    game_map.dijkstra[DijkstraMap.PLAYER] = dijkstra_map(
                        game_map=game_map,
                        sources=sources,
                        check_explored=False,
                        max_value=AWAKE_DISTANCE,
                    )
                    self.sources = sources
