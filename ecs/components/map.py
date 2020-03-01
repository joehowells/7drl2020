import random

random.seed(100)


class Map:
    def __init__(self):
        self.w = 100
        self.h = 100
        self.walkable = [[False for _ in range(self.w)] for _ in range(self.h)]
        self.visible = [[False for _ in range(self.w)] for _ in range(self.h)]
        self.transparent = [[False for _ in range(self.w)] for _ in range(self.h)]
        self.explored = [[False for _ in range(self.w)] for _ in range(self.h)]
        self.dijkstra = {
            "auto_explore": [[-1 for _ in range(self.w)] for _ in range(self.h)],
            "enemy": [[-1 for _ in range(self.w)] for _ in range(self.h)],
            "staircase": [[-1 for _ in range(self.w)] for _ in range(self.h)],
        }
        self.done_exploring = False

        for y, row in enumerate(self.walkable):
            for x, _ in enumerate(row):
                if random.random() < 0.8:
                    self.walkable[y][x] = True
                    self.transparent[y][x] = True
