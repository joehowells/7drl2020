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
AWAKE_DISTANCE = 12
MAX_LEVEL = 5

MAX_ANGER: int = 100

ANGER_TIER_1: int = 20
ANGER_TIER_2: int = 40
ANGER_TIER_3: int = 60
ANGER_TIER_4: int = 80
ANGER_TIER_5: int = 95

FOV_RADIUS: int = 8
