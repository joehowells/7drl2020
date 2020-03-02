import itertools
from typing import Tuple, Set

from esper import Processor

from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.eventmixin import EventMixin
from functions import dijkstra_map, iter_neighbors


class AutoExploreProcessor(Processor, EventMixin):
    def process(self):
        event = self.get_event("new_tiles_explored")

        if not event:
            return

        _, map_ = next(iter(self.world.get_component(Map)))
        _, (_, position) = next(iter(self.world.get_components(Player, Position)))

        sources: Set[Tuple[int, int]] = set()

        for x, y in itertools.product(range(map_.w), range(map_.h)):
            if map_.explored[y][x]:
                continue

            if not map_.walkable[y][x] and not any(map_.walkable[y][x] for x, y in iter_neighbors(x, y, map_)):
                continue

            if any(map_.explored[y][x] for x, y in iter_neighbors(x, y, map_)):
                sources.add((x, y))

        if sources:
            map_.dijkstra["auto_explore"] = dijkstra_map(map_, sources)
        else:
            map_.done_exploring = True
