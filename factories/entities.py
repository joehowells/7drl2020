from typing import List, Any, Optional, Callable

from ecs.components.display import Display
from ecs.components.item import Item
from ecs.components.monster import Monster
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
        Display(0x005F),
        Monster(
            name="assassin",
            threat=[4],
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


def make_elite_soldier(x: int, y: int) -> List[Any]:
    return [
        Display(0x0053),
        Monster(
            name="elite soldier",
            threat=[4],
            defend=2,
            health=2,
        ),
        Position(x, y),
    ]


def make_elite_defender(x: int, y: int) -> List[Any]:
    return [
        Display(0x0044),
        Monster(
            name="elite defender",
            threat=[4],
            defend=3,
            health=3,
        ),
        Position(x, y),
    ]


def make_elite_officer(x: int, y: int) -> List[Any]:
    return [
        Display(0x004F),
        Monster(
            name="elite officer",
            threat=[6],
            defend=2,
            health=3,
        ),
        Position(x, y),
    ]


def make_elite_assassin(x: int, y: int) -> List[Any]:
    return [
        Display(0x005F),
        Monster(
            name="elite assassin",
            threat=[8],
            defend=2,
            health=2,
        ),
        Position(x, y),
    ]


def make_elite_archer(x: int, y: int) -> List[Any]:
    return [
        Display(0x0041),
        Monster(
            name="elite archer",
            threat=[2, 6],
            defend=2,
            health=2,
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


def make_trap(x: int, y: int, factory: Callable[[int, int], List[Any]]) -> List[Any]:
    return [
        Display(0x005E, draw_order=-2),
        Trap(factory),
        Position(x, y),
    ]
