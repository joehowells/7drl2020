from random import choice, randint
from typing import List, Any

from ecs.components.display import Display
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.staircase import Staircase


def make_world() -> List[List[Any]]:
    dungeon_map = Map()
    entities = [[dungeon_map]]

    room = choice(dungeon_map.rooms)
    x = randint(room.x1, room.x2-1)
    y = randint(room.y1, room.y2-1)
    entities.append([
        Display(0x003E),
        Staircase(),
        Position(x, y),
    ])

    room = choice(dungeon_map.rooms)
    x = randint(room.x1, room.x2-1)
    y = randint(room.y1, room.y2-1)
    entities.append([
        Display(0x0040),
        Player(),
        Position(x, y),
    ])

    for _ in range(10):
        room = choice(dungeon_map.rooms)
        x = randint(room.x1, room.x2-1)
        y = randint(room.y1, room.y2-1)
        entities.append([
            Display(0x0026),
            Monster(),
            Position(x, y),
        ])

    return entities
