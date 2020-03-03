from random import choice, randint
from typing import List, Any, Optional

from ecs.components.display import Display
from ecs.components.item import Item
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.stair import Stair
from ecs.components.trap import Trap


def make_soldier(x: int, y: int) -> List[Any]:
    return [
        Display(0x0073),
        Monster(
            name="soldier",
            threat=[3],
            defend=1,
            health=1,
        ),
        Position(x, y),
    ]


def make_defender(x: int, y: int) -> List[Any]:
    return [
        Display(0x0064),
        Monster(
            name="defender",
            threat=[3],
            defend=2,
            health=2,
        ),
        Position(x, y),
    ]


def make_officer(x: int, y: int) -> List[Any]:
    return [
        Display(0x006F),
        Monster(
            name="officer",
            threat=[5],
            defend=1,
            health=2,
        ),
        Position(x, y),
    ]


def make_assassin(x: int, y: int) -> List[Any]:
    return [
        Display(0x0020),
        Monster(
            name="assassin",
            threat=[5],
            defend=1,
            health=1,
        ),
        Position(x, y),
    ]


def make_archer(x: int, y: int) -> List[Any]:
    return [
        Display(0x0061),
        Monster(
            name="archer",
            threat=[2, 5],
            defend=1,
            health=1,
        ),
        Position(x, y),
    ]


def make_potion(x: int, y: int) -> List[Any]:
    return [
        Display(0x0021, draw_order=-1),
        Item(
            name="potion",
        ),
        Position(x, y),
    ]


def make_trap(x: int, y: int) -> List[Any]:
    return [
        Display(0x005E, draw_order=-2),
        Trap(),
        Position(x, y),
    ]


def make_world(player: Optional[Player] = None) -> List[List[Any]]:
    game_map = Map()
    entities = [[game_map]]

    room = choice(game_map.rooms)
    x = randint(room.x1, room.x2 - 1)
    y = randint(room.y1, room.y2 - 1)
    entities.append([
        Display(0x003E, draw_order=-2),
        Stair(),
        Position(x, y),
    ])

    if player is None:
        player = Player()

    room = choice(game_map.rooms)
    x = randint(room.x1, room.x2 - 1)
    y = randint(room.y1, room.y2 - 1)
    entities.append([
        Display(0x0040),
        player,
        Position(x, y),
    ])
    game_map.blocked[y][x] = True

    for room in game_map.rooms:
        if min(room.w, room.h) < 4:
            continue

        if randint(1, 4) == 1:
            for _ in range(randint(2, 8)):
                x = randint(room.x1, room.x2 - 1)
                y = randint(room.y1, room.y2 - 1)

                if not game_map.blocked[y][x]:
                    entity = make_trap(x, y)
                    entities.append(entity)

            x = randint(room.x1, room.x2 - 1)
            y = randint(room.y1, room.y2 - 1)
            entity = make_soldier(x, y)
            entities.append(entity)
            game_map.blocked[y][x] = True
        else:
            for _ in range(randint(4, 16)):
                x = randint(room.x1, room.x2 - 1)
                y = randint(room.y1, room.y2 - 1)

                if not game_map.blocked[y][x]:
                    factories = [
                        make_soldier,
                        make_defender,
                        make_officer,
                        make_assassin,
                        make_archer,
                        make_potion,
                    ]
                    factory = choice(factories)
                    entity = factory(x, y)
                    entities.append(entity)
                    if Monster in entity:
                        game_map.blocked[y][x] = True

    return entities
