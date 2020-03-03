import itertools

from esper import Processor

from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.eventmixin import EventMixin
from functions import line_iter


class VisionProcessor(Processor, EventMixin):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))

        for x, y in itertools.product(range(game_map.w), range(game_map.h)):
            game_map.visible[y][x] = False

        _, (_, position) = next(iter(self.world.get_components(Player, Position)))

        x_min = max(position.x - 8, 0)
        x_max = min(position.x + 9, game_map.w)
        y_min = max(position.y - 8, 0)
        y_max = min(position.y + 9, game_map.h)

        game_map.visible[position.y][position.x] = True
        game_map.explored[position.y][position.x] = True

        for x, y in itertools.product(range(x_min, x_max), range(y_min, y_max)):
            for xi, yi in line_iter(position.x, position.y, x, y):
                game_map.visible[yi][xi] = True

                if not game_map.explored[yi][xi]:
                    game_map.explored[yi][xi] = True

                if not game_map.transparent[yi][xi]:
                    break
