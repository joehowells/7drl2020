from dataclasses import dataclass


@dataclass
class Display:
    code: int
    draw_order: int = 0
    color: int = 0xFFFFFFFF
