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
