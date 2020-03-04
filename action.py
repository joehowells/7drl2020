from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple


class ActionType(Enum):
    ATTACK = auto()
    GET_ITEM = auto()
    MOVE = auto()
    USE_ITEM = auto()
    USE_STAIRS = auto()
    WAIT = auto()


@dataclass(frozen=True)
class Action:
    action_type: ActionType = ActionType.WAIT
    anger: int = 0
    target: Tuple[int, int] = (0, 0)
