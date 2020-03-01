import itertools
from typing import Generator, Tuple, Collection, Set

from ecs.components.map import Map


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


def dijkstra_map(map_: Map, sources: Collection[Tuple[int, int]]) -> None:
    for x, y in itertools.product(range(map_.w), range(map_.h)):
        map_.dijkstra[y][x] = -1

    for x, y in sources:
        map_.dijkstra[y][x] = 0

    old_front: Set[Tuple[int, int]]
    new_front: Set[Tuple[int, int]] = set(sources)
    visited: Set[Tuple[int, int]] = set()

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
