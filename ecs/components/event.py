from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class Event:
    name: str
    data: Mapping[str, Any]
