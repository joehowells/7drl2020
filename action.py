from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional


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
    target: Optional[Tuple[int, int]] = None
    nice_name: str = "???"
