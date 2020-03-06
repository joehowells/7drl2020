from itertools import product

from esper import Processor

from constants import FOV_RADIUS
from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from functions import line_iter


class FOVProcessor(Processor):
    def process(self):
        for _, game_map in self.world.get_component(Map):
            generator = product(
                range(game_map.w),
                range(game_map.h),
            )
            for x, y in generator:
                game_map.visible[y][x] = False

            for _, (_, position) in self.world.get_components(Player, Position):
                x_min = max(position.x - FOV_RADIUS, 0)
                x_max = min(position.x + FOV_RADIUS + 1, game_map.w)
                y_min = max(position.y - FOV_RADIUS, 0)
                y_max = min(position.y + FOV_RADIUS + 1, game_map.h)

                game_map.visible[position.y][position.x] = True
                game_map.explored[position.y][position.x] = True

                generator = product(
                    range(x_min, x_max),
                    range(y_min, y_max),
                )
                for x, y in generator:
                    for xi, yi in line_iter(position.x, position.y, x, y):
                        game_map.visible[yi][xi] = True
                        game_map.explored[yi][xi] = True

                        if not game_map.transparent[yi][xi]:
                            break
