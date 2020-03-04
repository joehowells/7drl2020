from random import shuffle, randint, choice
from typing import List, Any, Optional, Callable

from ecs.components.map import Map
from ecs.components.player import Player
from factories.entities import (
    make_soldier, make_defender, make_officer, make_assassin, make_archer, make_trap, make_healing_potion, make_player,
    make_stairs,
    make_elite_soldier, make_elite_defender, make_elite_officer, make_elite_assassin, make_elite_archer,
    make_teleport_scroll, make_blink_scroll)
from factories.map import Room


def get_factory(level: int = 0) -> Callable[[int, int], List[Any]]:
    if level <= 0:
        return choice([
            make_soldier,
            make_soldier,
            make_soldier,
            make_soldier,
            make_defender,
            make_officer,
            make_assassin,
            make_archer,
        ])

    if level <= 1:
        return choice([
            make_soldier,
            make_soldier,
            make_elite_soldier,
            make_elite_soldier,
            make_defender,
            make_officer,
            make_assassin,
            make_archer,
        ])

    if level <= 2:
        return choice([
            make_soldier,
            make_soldier,
            make_elite_soldier,
            make_elite_soldier,
            make_defender,
            make_officer,
            make_assassin,
            make_archer,
            make_elite_defender,
            make_elite_officer,
        ])

    if level <= 2:
        return choice([
            make_soldier,
            make_soldier,
            make_elite_soldier,
            make_elite_soldier,
            make_defender,
            make_officer,
            make_assassin,
            make_archer,
            make_elite_defender,
            make_elite_officer,
            make_elite_assassin,
            make_elite_archer,
        ])

    return choice([
        make_elite_soldier,
        make_elite_soldier,
        make_elite_soldier,
        make_elite_soldier,
        make_elite_defender,
        make_elite_officer,
        make_elite_defender,
        make_elite_officer,
    ])


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
        factory = get_factory(level)
        entity = factory(x, y)
        entities.append(entity)


def make_trap_room(game_map: Map, entities: List[List[Any]], room: Room, level: int = 0) -> None:
    cells = [(x, y) for x, y, in room.cells if game_map.walkable[y][x]]
    shuffle(cells)

    for _ in range(randint(2, 8)):
        if not cells:
            break

        x, y = cells.pop()
        factory = get_factory(level)
        entity = make_trap(x, y, factory)
        entities.append(entity)

    for _ in range(randint(1, 2)):
        if not cells:
            break

        x, y = cells.pop()
        factory = get_factory(level)
        entity = factory(x, y)
        entities.append(entity)


def make_item_room(game_map: Map, entities: List[List[Any]], room: Room, level: int = 0) -> None:
    cells = [(x, y) for x, y, in room.cells if game_map.walkable[y][x]]
    shuffle(cells)

    for _ in range(randint(1, 2)):
        if not cells:
            break

        x, y = cells.pop()
        factories = [
            make_healing_potion,
            make_healing_potion,
            make_healing_potion,
            make_blink_scroll,
            make_blink_scroll,
            make_teleport_scroll,
        ]
        factory = choice(factories)
        entity = factory(x, y)
        entities.append(entity)

    for _ in range(randint(2, 4)):
        if not cells:
            break

        x, y = cells.pop()
        factory = get_factory(level)
        entity = factory(x, y)
        entities.append(entity)
