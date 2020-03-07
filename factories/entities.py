from typing import List, Any, Optional, Callable

from ecs.components.display import Display
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.stairs import Stairs
from ecs.components.trap import Trap


def make_player(x: int, y: int, player: Optional[Player] = None) -> List[Any]:
    if player is None:
        player = Player()

    return [
        Display(0x0040),
        player,
        Position(x, y),
    ]


def make_stairs(x: int, y: int) -> List[Any]:
    return [
        Display(0x003E, draw_order=-2),
        Stairs(),
        Position(x, y),
    ]


def make_trap(x: int, y: int, factory: Callable[[int, int], List[Any]]) -> List[Any]:
    return [
        Display(
            code=0x005E,
            color=0xFF999999,
            draw_order=-2,
        ),
        Trap(factory),
        Position(x, y),
    ]


