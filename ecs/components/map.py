from itertools import product
from random import choice

from constants import DijkstraMap
from factories.map import make_map


class Map:
    def __init__(self):
        self.walkable, self.rooms = make_map()
        self.w = len(self.walkable[0])
        self.h = len(self.walkable)
        self.visible = [[False for _ in range(self.w)] for _ in range(self.h)]
        self.transparent = [[False for _ in range(self.w)] for _ in range(self.h)]
        self.explored = [[False for _ in range(self.w)] for _ in range(self.h)]

        self.dijkstra = {
            key: [[-1 for _ in range(self.w)] for _ in range(self.h)]
            for key in DijkstraMap
        }

        self.done_exploring = False

        self.floor_glyphs = {}
        for x, y in product(range(self.w), range(self.h)):
            self.transparent[y][x] = self.walkable[y][x]

            if self.walkable[y][x]:
                self.floor_glyphs[(x, y)] = choice([0x0027, 0x002C, 0x002E, 0x0060])
