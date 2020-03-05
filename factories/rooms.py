from random import shuffle, randint
from typing import List, Any, Optional

from ecs.components.map import Map
from ecs.components.player import Player
from factories.entities import make_trap, make_player, make_stairs, get_monster_factory, get_item_factory
from factories.map import Room


def make_player_room(game_map: Map, entities: List[List[Any]], room: Room, player: Optional[Player] = None) -> None:
    cells = [(x, y) for x, y, in room.cells if game_map.walkable[y][x]]
    shuffle(cells)

    x, y = cells.pop()
    entities.append(make_player(x, y, player))


def make_stairs_room(game_map: Map, entities: List[List[Any]], room: Room) -> None:
    cells = [(x, y) for x, y, in room.cells if game_map.walkable[y][x]]
    shuffle(cells)

    x, y = cells.pop()
    entities.append(make_stairs(x, y))


def make_enemy_room(game_map: Map, entities: List[List[Any]], room: Room, level: int = 0) -> None:
    cells = [(x, y) for x, y, in room.cells if game_map.walkable[y][x]]
    shuffle(cells)

    for _ in range(randint(2, 8)):
        if not cells:
            break

        x, y = cells.pop()
        factory = get_monster_factory(level)
        entity = factory(x, y)
        entities.append(entity)


def make_trap_room(game_map: Map, entities: List[List[Any]], room: Room, level: int = 0) -> None:
    cells = [(x, y) for x, y, in room.cells if game_map.walkable[y][x]]
    shuffle(cells)

    for _ in range(randint(2, 8)):
        if not cells:
            break

        x, y = cells.pop()
        factory = get_monster_factory(level)
        entity = make_trap(x, y, factory)
        entities.append(entity)

    for _ in range(randint(1, 2)):
        if not cells:
            break

        x, y = cells.pop()
        factory = get_monster_factory(level)
        entity = factory(x, y)
        entities.append(entity)


def make_item_room(game_map: Map, entities: List[List[Any]], room: Room, level: int = 0) -> None:
    cells = [(x, y) for x, y, in room.cells if game_map.walkable[y][x]]
    shuffle(cells)

    for _ in range(randint(1, 2)):
        if not cells:
            break

        x, y = cells.pop()
        factory = get_item_factory()
        entity = factory(x, y)
        entities.append(entity)

    for _ in range(randint(2, 4)):
        if not cells:
            break

        x, y = cells.pop()
        factory = get_monster_factory(level)
        entity = factory(x, y)
        entities.append(entity)
