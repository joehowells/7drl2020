from enum import auto, Enum


class GameState(Enum):
    TITLE_SCREEN = auto()
    MAIN_GAME = auto()
    GAME_OVER = auto()
