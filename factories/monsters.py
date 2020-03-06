from random import choice
from typing import List, Any, Callable

from ecs.components.assassin import Assassin
from ecs.components.boss import Boss
from ecs.components.display import Display
from ecs.components.monster import Monster
from ecs.components.position import Position
from ecs.components.taunt import CanTaunt


def make_soldier(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x0073,
            color=0xFFFFFFFF,
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
            color=0xFF00FF00,
        ),
        Monster(
            name="defender",
            threat=[2],
            defend=4,
            health=1,
        ),
        Position(x, y),
    ]


def make_officer(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x0034,
            color=0xFFFFFF00,
        ),
        Monster(
            name="junior officer",
            threat=[3],
            defend=4,
            health=2,
            article="a",
        ),
        Position(x, y),
    ]


def make_assassin(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x0063,
            color=0xFF666666,
        ),
        Monster(
            name="assassin",
            threat=[5],
            defend=1,
            health=1,
            article="an",
        ),
        Assassin(),
        Position(x, y),
    ]


def make_archer(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x0061,
            color=0xFF00FFFF,
        ),
        Monster(
            name="archer",
            threat=[2, 5],
            defend=1,
            health=1,
            article="an",
        ),
        Position(x, y),
    ]


def make_elite_soldier(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x0053,
            color=0xFFFFFFFF,
        ),
        Monster(
            name="elite soldier",
            threat=[4],
            defend=2,
            health=2,
            article="an",
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
            defend=4,
            health=2,
            article="an",
        ),
        Position(x, y),
    ]


def make_elite_officer(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x0033,
            color=0xFFFFFF00,
        ),
        Monster(
            name="senior officer",
            threat=[5],
            defend=4,
            health=3,
            article="a",
        ),
        Position(x, y),
    ]


def make_elite_assassin(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x0043,
            color=0xFF666666,
        ),
        Monster(
            name="elite assassin",
            threat=[7],
            defend=2,
            health=2,
            article="an",
        ),
        Assassin(),
        Position(x, y),
    ]


def make_elite_archer(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x0041,
            color=0xFF00FFFF,
        ),
        Monster(
            name="elite archer",
            threat=[2, 7],
            defend=2,
            health=2,
            article="an",
        ),
        Position(x, y),
    ]


def make_mid_boss(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x0032,
            color=0xFFFFFFFF,
        ),
        Monster(
            name="militia commander",
            threat=[7, 3],
            defend=4,
            health=4,
            article="the",
        ),
        Position(x, y),
        Boss(),
        CanTaunt(),
    ]


def make_end_boss(x: int, y: int) -> List[Any]:
    return [
        Display(
            code=0x0031,
            color=0xFFFFFFFF,
        ),
        Monster(
            name="militia captain",
            threat=[9, 5],
            defend=5,
            health=5,
            article="the",
        ),
        Position(x, y),
        Boss(),
        CanTaunt(),
    ]


def get_monster_factory(level: int = 0) -> Callable[[int, int], List[Any]]:
    if level <= 0:
        return choice([
            make_soldier,
            make_soldier,
            make_soldier,
            make_soldier,
            make_soldier,
            make_soldier,
            make_defender,
            make_officer,
            make_assassin,
            make_archer,
        ])

    if level <= 2:
        return choice([
            make_soldier,
            make_soldier,
            make_soldier,
            make_soldier,
            make_elite_soldier,
            make_elite_soldier,
            make_defender,
            make_officer,
            make_assassin,
            make_archer,
        ])

    if level <= 3:
        return choice([
            make_soldier,
            make_soldier,
            make_soldier,
            make_soldier,
            make_elite_soldier,
            make_elite_soldier,
            make_elite_soldier,
            make_elite_soldier,
            make_elite_soldier,
            make_elite_soldier,
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

    if level <= 4:
        return choice([
            make_soldier,
            make_soldier,
            make_elite_soldier,
            make_elite_soldier,
            make_elite_soldier,
            make_elite_soldier,
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
        make_elite_soldier,
        make_elite_soldier,
        make_elite_defender,
        make_elite_officer,
        make_elite_defender,
        make_elite_officer,
    ])
