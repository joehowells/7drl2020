import itertools
from typing import Tuple, Generator, Set

from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.processor import Processor


def iter_neighbors(x: int, y: int, map_: Map) -> Generator[Tuple[int, int], None, None]:
    neighbors = [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    ]

    for x_neighbor, y_neighbor in neighbors:
        if 0 <= x_neighbor < map_.w and 0 <= y_neighbor < map_.h:
            yield x_neighbor, y_neighbor


class DijkstraMapProcessor(Processor):
    def process(self):
        _, map_ = next(iter(self.world.get_component(Map)))
        _, (_, position) = next(iter(self.world.get_components(Player, Position)))

        old_front: Set[Tuple[int, int]]
        new_front: Set[Tuple[int, int]] = set()
        visited: Set[Tuple[int, int]] = set()

        for x, y in itertools.product(range(map_.w), range(map_.h)):
            map_.dijkstra[y][x] = -1

            if not map_.explored[y][x] and any(map_.explored[y][x] for x, y in iter_neighbors(x, y, map_)):
                new_front.add((x, y))

        for value in itertools.count():
            old_front = new_front.copy()
            new_front = set()
            visited.update(old_front)

            for x, y in old_front:
                map_.dijkstra[y][x] = value

                for x_neighbor, y_neighbor in iter_neighbors(x, y, map_):
                    if not map_.explored[y_neighbor][x_neighbor]:
                        continue

                    if not map_.walkable[y_neighbor][x_neighbor]:
                        continue

                    if (x_neighbor, y_neighbor) in visited:
                        continue

                    new_front.add((x_neighbor, y_neighbor))

            if not new_front:
                break
