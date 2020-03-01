import random

random.seed(100)


class Map:
    def __init__(self):
        self.w = 100
        self.h = 100
        self.walkable = [[False for _ in range(100)] for _ in range(100)]
        self.visible = [[False for _ in range(100)] for _ in range(100)]
        self.transparent = [[False for _ in range(100)] for _ in range(100)]
        self.explored = [[False for _ in range(100)] for _ in range(100)]

        for y, row in enumerate(self.walkable):
            for x, _ in enumerate(row):
                if random.random() < 0.8:
                    self.walkable[y][x] = True
                    self.transparent[y][x] = True
