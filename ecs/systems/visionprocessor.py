import itertools

from esper import Processor

from ecs.components.event import Event
from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.eventmixin import EventMixin
from functions import line_iter


class VisionProcessor(Processor, EventMixin):
    def process(self):
        _, map_ = next(iter(self.world.get_component(Map)))

        for x, y in itertools.product(range(map_.w), range(map_.h)):
            map_.visible[y][x] = False

        _, (_, position) = next(iter(self.world.get_components(Player, Position)))

        x_min = max(position.x - 8, 0)
        x_max = min(position.x + 9, map_.w)
        y_min = max(position.y - 8, 0)
        y_max = min(position.y + 9, map_.h)

        map_.visible[position.y][position.x] = True
        map_.explored[position.y][position.x] = True
        new_tiles_explored = False

        for x, y in itertools.product(range(x_min, x_max), range(y_min, y_max)):
            for xi, yi in line_iter(position.x, position.y, x, y):
                map_.visible[yi][xi] = True

                if not map_.explored[yi][xi]:
                    map_.explored[yi][xi] = True
                    new_tiles_explored = True

                if not map_.transparent[yi][xi]:
                    break

        if new_tiles_explored:
            self.set_event(Event("new_tiles_explored", {}))
