from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Union


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
    anger: int = -1
    target: Union[int, Tuple[int, int], None] = None
    nice_name: str = "???"
