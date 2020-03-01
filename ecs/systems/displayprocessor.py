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
                color = 0xCCCCCCCC if map_.visible[y][x] else 0x66666666
                code = 0x002E if map_.walkable[y][x] else 0x0023
                terminal.color(color)
                terminal.put(x + x_offset, y + y_offset, code)

        for _, (display, position) in self.world.get_components(Display, Position):
            terminal.color("white")
            terminal.put(position.x + x_offset, position.y + y_offset, chr(display.code))

        terminal.refresh()
