from dataclasses import dataclass
from typing import Callable, List, Any


@dataclass
class Trap:
    factory: Callable[[int, int], List[Any]]
