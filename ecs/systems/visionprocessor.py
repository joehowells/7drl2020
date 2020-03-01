import itertools

from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.processor import Processor
from functions import line_iter


class VisionProcessor(Processor):
    def process(self):
        _, map_ = next(iter(self.world.get_component(Map)))

        for x, y in itertools.product(range(map_.w), range(map_.h)):
            map_.visible[y][x] = False

        _, (_, position) = next(iter(self.world.get_components(Player, Position)))
        map_.visible[position.y][position.x] = False

        for x, y in itertools.product(range(map_.w), range(map_.h)):
            for xi, yi in line_iter(position.x, position.y, x, y):
                map_.visible[yi][xi] = True
                map_.explored[yi][xi] = True
                if not map_.transparent[yi][xi]:
                    break
