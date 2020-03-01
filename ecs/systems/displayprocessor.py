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
        for y, row in enumerate(map_.walkable):
            for x, walkable in enumerate(row):
                if walkable:
                    terminal.put(x+x_offset, y+y_offset, chr(0x002e))
                else:
                    terminal.put(x+x_offset, y+y_offset, chr(0x0023))

        for _, (display, position) in self.world.get_components(Display, Position):
            terminal.put(position.x+x_offset, position.y+y_offset, chr(display.code))

        terminal.refresh()
