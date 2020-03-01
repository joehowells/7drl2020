import itertools
from typing import Generator, Tuple, Collection, Set, List

from ecs.components.map import Map
from ecs.components.position import Position


def line_iter(xo: int, yo: int, xd: int, yd: int) -> Generator[Tuple[int, int], None, None]:
    x_step = 1 if xd >= xo else -1
    y_step = 1 if yd >= yo else -1

    x_range = range(xo + x_step, xd + x_step, x_step)
    y_range = range(yo + y_step, yd + y_step, y_step)

    if xo == xd and yo == yd:
        return

    if xo == xd:
        for yi in y_range:
            yield xo, yi

        return

    if yo == yd:
        for xi in x_range:
            yield xi, yo

        return

    if abs(xd - xo) == abs(yd - yo):
        for xi, yi in zip(x_range, y_range):
            yield xi, yi

        return

    if abs(xd - xo) > abs(yd - yo):
        for xi in x_range:
            yi = int(round(yo + (yd - yo) * (xi - xo) / (xd - xo)))
            yield xi, yi

        return

    if abs(xd - xo) < abs(yd - yo):
        for yi in y_range:
            xi = int(round(xo + (xd - xo) * (yi - yo) / (yd - yo)))
            yield xi, yi

        return


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


def dijkstra_map(map_: Map, sources: Collection[Tuple[int, int]]) -> List[List[int]]:
    output = [[-1 for _ in range(map_.w)] for _ in range(map_.h)]

    for x, y in sources:
        output[y][x] = 0

    old_front: Set[Tuple[int, int]]
    new_front: Set[Tuple[int, int]] = set(sources)
    visited: Set[Tuple[int, int]] = set()

    for value in itertools.count():
        old_front = new_front.copy()
        new_front = set()
        visited.update(old_front)

        for x, y in old_front:
            output[y][x] = value

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

    return output


def move_dijkstra(map_: Map, position: Position, key: str) -> None:
    neighbors = [
        (x, y)
        for x, y, in iter_neighbors(position.x, position.y, map_)
        if map_.walkable[y][x] and map_.dijkstra[key][y][x] < map_.dijkstra[key][position.y][position.x]
    ]

    if not neighbors:
        return

    neighbors.sort(key=lambda xy: map_.dijkstra[key][xy[1]][xy[0]])
    x, y = neighbors[0]

    position.x = x
    position.y = y