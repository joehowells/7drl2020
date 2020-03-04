from random import choice, shuffle
from typing import List, Any, Optional

from ecs.components.map import Map
from ecs.components.player import Player
from factories.rooms import make_enemy_room, make_trap_room, make_item_room, make_player_room, make_stairs_room

ROOM_FACTORIES = [
    make_enemy_room,
    make_enemy_room,
    make_item_room,
    make_item_room,
    make_trap_room,
]


def make_world(player: Optional[Player] = None) -> List[List[Any]]:
    game_map = Map()
    entities = [[game_map]]

    big_rooms = [room for room in game_map.rooms if room.w >= 4 and room.h >= 4]
    shuffle(big_rooms)

    make_player_room(game_map, entities, big_rooms.pop(), player)
    make_stairs_room(game_map, entities, big_rooms.pop())

    while big_rooms:
        factory = choice(ROOM_FACTORIES)
        factory(game_map, entities, big_rooms.pop())

    return entities
