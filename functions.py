from collections import deque
from typing import Generator, Tuple, Collection, List, Optional, Set

from esper import World

from constants import DijkstraMap
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
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


def iter_neighbors(x: int, y: int, game_map: Map) -> Generator[Tuple[int, int], None, None]:
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
        if 0 <= x_neighbor < game_map.w and 0 <= y_neighbor < game_map.h:
            yield x_neighbor, y_neighbor


def dijkstra_map(game_map: Map, sources: Collection[Tuple[int, int]], check_explored=True, max_value: int = None) -> \
        List[List[int]]:
    output = [[-1 for _ in range(game_map.w)] for _ in range(game_map.h)]
    queue = deque()

    for x, y in sources:
        queue.append((x, y))
        output[y][x] = 0

    while queue:
        x, y = queue.popleft()
        value = output[y][x]

        if max_value and value >= max_value:
            continue

        for x_neighbor, y_neighbor in iter_neighbors(x, y, game_map):
            if check_explored and not game_map.explored[y_neighbor][x_neighbor]:
                continue

            if not game_map.walkable[y_neighbor][x_neighbor]:
                continue

            if output[y_neighbor][x_neighbor] > -1:
                continue

            queue.append((x_neighbor, y_neighbor))
            output[y_neighbor][x_neighbor] = value + 1

    return output


def move_dijkstra(world: World, game_map: Map, position: Position, key: DijkstraMap, reverse: bool = False,
                  strict: bool = True) -> Optional[Tuple[int, int]]:
    old_dijkstra = game_map.dijkstra[key][position.y][position.x]

    blocked = get_blocked_tiles(world)

    neighbors = []
    for x, y, in iter_neighbors(position.x, position.y, game_map):
        if not game_map.walkable[y][x]:
            continue

        if (x, y) in blocked:
            continue

        new_dijkstra = game_map.dijkstra[key][y][x]

        if new_dijkstra < 0:
            return

        if strict:
            if new_dijkstra == old_dijkstra:
                continue

        if reverse:
            if new_dijkstra < old_dijkstra:
                continue
        else:
            if new_dijkstra > old_dijkstra:
                continue

        if reverse:
            new_dijkstra = -new_dijkstra

        break_ties = abs(x - position.x) and abs(y - position.y)
        neighbors.append((new_dijkstra, break_ties, x, y))

    if not neighbors:
        return

    neighbors.sort()
    _, _, x, y = neighbors[0]

    return x, y


def move(position: Position, target: Tuple[int, int]) -> None:
    x, y = target
    position.x = x
    position.y = y


def get_blocked_tiles(world: World) -> Set[Tuple[int, int]]:
    blocked = set()
    blocked.update(
        (position.x, position.y)
        for _, (position, _) in world.get_components(Position, Player)
    )
    blocked.update(
        (position.x, position.y)
        for _, (position, _) in world.get_components(Position, Monster)
    )
    return blocked
