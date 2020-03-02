from enum import auto, Enum


class DijkstraMap(Enum):
    EXPLORE = auto()
    PLAYER = auto()
    MONSTER = auto()
    STAIRS = auto()


ROOM_SIZE: int = 9
GRAPH_MIN_DEPTH: int = 4
GRAPH_MAX_DEPTH: int = 8
