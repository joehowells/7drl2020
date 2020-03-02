import random

from constants import DijkstraMap
from factories.map import make_map

random.seed(100)


class Map:
    def __init__(self):
        self.walkable, self.rooms = make_map()
        self.w = len(self.walkable[0])
        self.h = len(self.walkable)
        self.visible = [[False for _ in range(self.w)] for _ in range(self.h)]
        self.transparent = [[False for _ in range(self.w)] for _ in range(self.h)]
        self.explored = [[False for _ in range(self.w)] for _ in range(self.h)]
        self.blocked = [[False for _ in range(self.w)] for _ in range(self.h)]

        self.dijkstra = {
            key: [[-1 for _ in range(self.w)] for _ in range(self.h)]
            for key in DijkstraMap
        }

        self.done_exploring = False

        for y, row in enumerate(self.walkable):
            for x, _ in enumerate(row):
                self.transparent[y][x] = self.walkable[y][x]
