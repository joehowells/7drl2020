from dataclasses import dataclass


@dataclass
class Message:
    text: str
    color: int = 0xFFFFFFFF
    priority: int = 0
