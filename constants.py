from enum import auto, Enum


class DijkstraMap(Enum):
    EXPLORE = auto()
    PLAYER = auto()
    MONSTER = auto()
    STAIRS = auto()
