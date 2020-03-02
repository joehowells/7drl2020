from random import choice, randint
from typing import List, Any

from constants import DijkstraMap, AWAKE_DISTANCE
from ecs.components.display import Display
from ecs.components.item import Item
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.staircase import Staircase
from functions import dijkstra_map


def make_world() -> List[List[Any]]:
    game_map = Map()
    entities = [[game_map]]

    room = choice(game_map.rooms)
    x = randint(room.x1, room.x2 - 1)
    y = randint(room.y1, room.y2 - 1)
    entities.append([
        Display(0x003E),
        Staircase(),
        Position(x, y),
    ])

    game_map.dijkstra[DijkstraMap.STAIRS] = dijkstra_map(game_map, [(x, y)], check_explored=False)

    room = choice(game_map.rooms)
    x = randint(room.x1, room.x2 - 1)
    y = randint(room.y1, room.y2 - 1)
    entities.append([
        Display(0x0040),
        Player(),
        Position(x, y),
    ])
    game_map.blocked[y][x] = True

    game_map.dijkstra[DijkstraMap.PLAYER] = dijkstra_map(game_map, [(x, y)], check_explored=False, max_value=AWAKE_DISTANCE)

    for room in game_map.rooms:
        if min(room.w, room.h) < 4:
            continue

        for _ in range(randint(2, 8)):
            x = randint(room.x1, room.x2 - 1)
            y = randint(room.y1, room.y2 - 1)
            if not game_map.blocked[y][x]:
                if randint(1, 2) == 1:
                    entities.append([
                        Display(0x0026),
                        Monster(),
                        Position(x, y),
                    ])
                    game_map.blocked[y][x] = True
                else:
                    entities.append([
                        Display(0x0041),
                        Item(),
                        # Monster(target_distance=2, threat=10),
                        Position(x, y),
                    ])

    return entities
