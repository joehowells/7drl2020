from random import choice
from typing import List, Any, Optional, Callable

from ecs.components.blinkscroll import BlinkScroll
from ecs.components.display import Display
from ecs.components.healingpotion import HealingPotion
from ecs.components.item import Item
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.stairs import Stairs
from ecs.components.teleportscroll import TeleportScroll
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
        Display(
            code=0x0073,
            color=0xFFFF6600,
        ),
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
        Display(
            code=0x0064,
            color=0xFF66FF00,
        ),
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
        Display(
            code=0x006F,
            color=0xFF6600FF,
        ),
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
        Display(
            code=0x005F,
            color=0xFF666666,
        ),
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
        Display(
            code=0x0061,
            color=0xFF0066FF,
        ),
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
        Display(
            code=0x0053,
            color=0xFFFF6600,
        ),
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
        Display(
            code=0x0044,
            color=0xFF00FF00,
        ),
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
        Display(
            code=0x004F,
            color=0xFF9900FF,
        ),
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
        Display(
            code=0x005F,
            color=0xFF666666,
        ),
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
        Display(
            code=0x0041,
            color=0xFF00FF99,
        ),
        Monster(
            name="elite archer",
            threat=[2, 6],
            defend=2,
            health=2,
        ),
        Position(x, y),
    ]


def make_healing_potion(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x0021,
            color=0xFFFF0066,
            draw_order=-1,
        ),
        Item(
            name="healing potion",
        ),
        HealingPotion(),
        Position(x, y),
    ]


def make_blink_scroll(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x003F,
            color=0xFFCC66FF,
            draw_order=-1,
        ),
        Item(
            name="blink scroll",
        ),
        BlinkScroll(),
        Position(x, y),
    ]


def make_teleport_scroll(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x003F,
            color=0xFF6600FF,
            draw_order=-1,
        ),
        Item(
            name="teleport scroll",
        ),
        TeleportScroll(),
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


def get_monster_factory(level: int = 0) -> Callable[[int, int], List[Any]]:
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


def get_item_factory() -> Callable[[int, int], List[Any]]:
    return choice([
        make_healing_potion,
        make_healing_potion,
        make_healing_potion,
        make_blink_scroll,
        make_blink_scroll,
        make_teleport_scroll,
    ])
