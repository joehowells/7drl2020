from bearlibterminal import terminal

from ecs.components.display import Display
from ecs.components.position import Position
from ecs.processor import Processor


class DisplayProcessor(Processor):
    def process(self):
        terminal.clear()

        for _, (display, position) in self.world.get_components(Display, Position):
            terminal.put(position.x, position.y, chr(display.code))

        terminal.refresh()
