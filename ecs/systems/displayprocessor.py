import itertools

from bearlibterminal import terminal

from ecs.components.display import Display
from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.processor import Processor


class DisplayProcessor(Processor):
    def process(self):
        terminal.clear()

        _, (_, position) = next(iter(self.world.get_components(Player, Position)))
        x_offset = 10 - position.x
        y_offset = 10 - position.y

        _, map_ = next(iter(self.world.get_component(Map)))
        for x, y in itertools.product(range(map_.w), range(map_.h)):
            if map_.explored[y][x]:
                if map_.visible[y][x]:
                    if map_.walkable[y][x]:
                        color = 0x99999999
                    else:
                        color = 0xCCCCCCCC
                else:
                    color = 0x66666666

                if 0 <= map_.dijkstra[y][x] < 26:
                    code = 0x0040 + map_.dijkstra[y][x]
                else:
                    if map_.walkable[y][x]:
                        code = 0x002E
                    else:
                        code = 0x0023

                terminal.color(color)
                terminal.put(x + x_offset, y + y_offset, code)

        for _, (display, position) in self.world.get_components(Display, Position):
            terminal.color("white")
            terminal.put(position.x + x_offset, position.y + y_offset, chr(display.code))

        terminal.refresh()
