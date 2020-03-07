from enum import auto, Enum


class DijkstraMap(Enum):
    EXPLORE = auto()
    PLAYER = auto()
    MONSTER = auto()
    ITEM = auto()
    STAIRS = auto()


ROOM_SIZE: int = 9
GRAPH_MIN_DEPTH: int = 2
GRAPH_MAX_DEPTH: int = 4
AWAKE_DISTANCE: int = 12
MAX_LEVEL: int = 5

MAX_HEALTH: int = 10
MAX_RAGE: int = 100
MAX_THREAT: int = 20

RAGE_TIER_1: int = 20
RAGE_TIER_2: int = 40
RAGE_TIER_3: int = 60
RAGE_TIER_4: int = 80
RAGE_TIER_5: int = 90

FOV_RADIUS: int = 8

MAX_WEAPON: int = 6
MAX_ARMOUR: int = 6
