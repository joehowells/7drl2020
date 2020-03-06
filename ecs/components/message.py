from dataclasses import dataclass


@dataclass
class Message:
    text: str
    priority: int = 0
