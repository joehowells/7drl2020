import itertools
from typing import Tuple, Set

from esper import Processor

from constants import DijkstraMap
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

        _, game_map = next(iter(self.world.get_component(Map)))
        _, (_, position) = next(iter(self.world.get_components(Player, Position)))

        sources: Set[Tuple[int, int]] = set()

        for x, y in itertools.product(range(game_map.w), range(game_map.h)):
            if game_map.explored[y][x]:
                continue

            if not game_map.walkable[y][x] and not any(game_map.walkable[y][x] for x, y in iter_neighbors(x, y, game_map)):
                continue

            if any(game_map.explored[y][x] for x, y in iter_neighbors(x, y, game_map)):
                sources.add((x, y))

        if sources:
            game_map.dijkstra[DijkstraMap.EXPLORE] = dijkstra_map(game_map, sources)
        else:
            game_map.done_exploring = True
