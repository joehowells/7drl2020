import itertools

from bearlibterminal import terminal
from esper import Processor

from constants import DijkstraMap
from ecs.components.display import Display
from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position


class DisplayProcessor(Processor):
    def process(self):
        terminal.clear()

        _, (_, position) = next(iter(self.world.get_components(Player, Position)))
        x_offset = 16 - position.x
        y_offset = 10 - position.y

        _, game_map = next(iter(self.world.get_component(Map)))
        for xc, yc in itertools.product(range(33), range(21)):
            x = xc - x_offset
            y = yc - y_offset

            if not 0 <= x < game_map.w or not 0 <= y < game_map.h:
                continue

            if game_map.explored[y][x]:
                if game_map.visible[y][x]:
                    if game_map.walkable[y][x]:
                        color = 0x99999999
                    else:
                        color = 0xCCCCCCCC
                else:
                    color = 0x66666666

                if game_map.walkable[y][x]:
                    code = 0x0041 + game_map.dijkstra[DijkstraMap.EXPLORE][y][x]
                else:
                    code = 0x0023

                terminal.color(color)
                terminal.put(x + x_offset, y + y_offset, code)

        terminal.color(0xFFFFFFFF)

        for _, (display, position) in self.world.get_components(Display, Position):
            if game_map.visible[position.y][position.x]:
                terminal.put(position.x + x_offset, position.y + y_offset, chr(display.code))

        terminal.refresh()
