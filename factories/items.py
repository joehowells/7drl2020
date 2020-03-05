from random import choice
from typing import List, Any, Callable

from ecs.components.display import Display
from ecs.components.healingpotion import HealingPotion
from ecs.components.item import Item
from ecs.components.position import Position
from ecs.components.smokebomb import SmokeBomb
from ecs.components.teleportscroll import TeleportScroll
from ecs.components.thunderscroll import ThunderScroll


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


def make_smoke_bomb(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x0021,
            color=0xFF00FF66,
            draw_order=-1,
        ),
        Item(
            name="smoke bomb",
        ),
        SmokeBomb(),
        Position(x, y),
    ]


def make_thunder_scroll(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x003F,
            color=0xFFFF6600,
            draw_order=-1,
        ),
        Item(
            name="scroll of thunder",
        ),
        ThunderScroll(),
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
            name="scroll of teleport",
        ),
        TeleportScroll(),
        Position(x, y),
    ]


def get_item_factory() -> Callable[[int, int], List[Any]]:
    return choice([
        make_healing_potion,
        make_healing_potion,
        make_healing_potion,
        make_thunder_scroll,
        make_teleport_scroll,
        make_smoke_bomb,
    ])
