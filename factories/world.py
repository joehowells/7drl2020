from random import choice, randint, shuffle
from typing import List, Any, Optional

from ecs.components.display import Display
from ecs.components.item import Item
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.stair import Stair
from ecs.components.trap import Trap
from factories.map import Room


def make_soldier(x: int, y: int) -> List[Any]:
    return [
        Display(0x0073),
        Monster(
            name="soldier",
            threat=[2],
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
            threat=[2],
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
            threat=[3],
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
            threat=[3],
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
            threat=[2, 3],
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

    if player is None:
        player = Player()

    big_rooms = [
        room for room in game_map.rooms
        if room.w >= 4 and room.h >= 4
    ]

    shuffle(big_rooms)

    # Start room
    room = big_rooms.pop()

    cells = [(x, y) for x, y, in room.cells if game_map.walkable[y][x]]
    shuffle(cells)
    x, y = cells.pop()

    entities.append([
        Display(0x0040),
        player,
        Position(x, y),
    ])
    game_map.blocked[y][x] = True

    # Exit room
    room = big_rooms.pop()

    cells = [(x, y) for x, y, in room.cells if game_map.walkable[y][x]]
    shuffle(cells)
    x, y = cells.pop()

    entities.append([
        Display(0x003E, draw_order=-2),
        Stair(),
        Position(x, y),
    ])

    # Populate the rest of the rooms
    while big_rooms:
        room = big_rooms.pop()

        factories = [
            make_enemy_room,
            make_enemy_room,
            make_item_room,
            make_item_room,
            make_trap_room,
        ]
        factory = choice(factories)
        factory(game_map, entities, room)

    return entities


def make_enemy_room(game_map: Map, entities: List[List[Any]], room: Room) -> None:
    cells = [(x, y) for x, y, in room.cells if game_map.walkable[y][x]]
    shuffle(cells)

    for _ in range(randint(2, 8)):
        if not cells:
            break

        x, y = cells.pop()

        if not game_map.blocked[y][x]:
            factories = [
                make_soldier,
                make_soldier,
                make_soldier,
                make_defender,
                make_officer,
                make_assassin,
                make_archer,
            ]
            factory = choice(factories)
            entity = factory(x, y)
            entities.append(entity)
            game_map.blocked[y][x] = True


def make_trap_room(game_map: Map, entities: List[List[Any]], room: Room) -> None:
    cells = [(x, y) for x, y, in room.cells if game_map.walkable[y][x]]
    shuffle(cells)

    for _ in range(randint(2, 8)):
        if not cells:
            break

        x, y = cells.pop()

        if not game_map.blocked[y][x]:
            entity = make_trap(x, y)
            entities.append(entity)

    for _ in range(randint(1, 2)):
        if not cells:
            break

        x, y = cells.pop()

        if not game_map.blocked[y][x]:
            factories = [
                make_soldier,
            ]
            factory = choice(factories)
            entity = factory(x, y)
            entities.append(entity)
            game_map.blocked[y][x] = True


def make_item_room(game_map: Map, entities: List[List[Any]], room: Room) -> None:
    cells = [(x, y) for x, y, in room.cells if game_map.walkable[y][x]]
    shuffle(cells)

    for _ in range(randint(1, 2)):
        if not cells:
            break

        x, y = cells.pop()

        if not game_map.blocked[y][x]:
            factories = [
                make_potion,
            ]
            factory = choice(factories)
            entity = factory(x, y)
            entities.append(entity)

    for _ in range(randint(2, 4)):
        if not cells:
            break

        x, y = cells.pop()

        if not game_map.blocked[y][x]:
            factories = [
                make_soldier,
            ]
            factory = choice(factories)
            entity = factory(x, y)
            entities.append(entity)
            game_map.blocked[y][x] = True
