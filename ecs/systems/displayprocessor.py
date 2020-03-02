import itertools

from bearlibterminal import terminal
from esper import Processor

from ecs.components.display import Display
from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position


def draw_borders() -> None:
    for y in range(21):
        terminal.put(33, y, 0x2551)

    for x in range(34, 50):
        terminal.put(x, 3, 0x2500)
        terminal.put(x, 6, 0x2500)

    for x in range(51, 67):
        terminal.put(x, 3, 0x2500)
        terminal.put(x, 6, 0x2500)

    for y in range(4, 6):
        terminal.put(50, y, 0x2502)

    terminal.put(33, 3, 0x255F)
    terminal.put(33, 6, 0x255F)
    terminal.put(50, 3, 0x252C)
    terminal.put(50, 6, 0x2534)


def draw_bar(x: int, y: int, value: int, color: int = 0xFFFFFFFF) -> None:
    terminal.color(color)
    terminal.printf(x, y, "="*value)
    terminal.color(0xFFFFFFFF)


class DisplayProcessor(Processor):
    def process(self):
        terminal.clear()

        terminal.color(0xFF666666)

        draw_borders()

        self.draw_map()

        _, player = next(iter(self.world.get_component(Player)))

        terminal.printf(34, 0, f"Health: {player.health:>3d}")
        terminal.printf(34, 1, f"Anger:  {player.anger:>3d}")
        terminal.printf(34, 2, f"Threat: {player.actual_threat:>3d}")

        draw_bar(46, 0, 20, 0xFF333333)
        draw_bar(46, 1, 20, 0xFF333333)
        draw_bar(46, 2, 20, 0xFF333333)

        draw_bar(46, 0, player.health)
        draw_bar(46, 1, player.anger // 5, 0xFFFF0000)
        draw_bar(46, 2, player.visible_threat // 5, 0xFFFFFF00)
        draw_bar(46, 2, player.actual_threat // 5, 0xFFFF0000)

        terminal.printf(34, 4, f"[[X]] {player.attack_action.name}")
        terminal.printf(34, 5, f"[[Z]] {player.defend_action.name}")

        terminal.refresh()

    def draw_map(self):
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
                    code = 0x002E
                else:
                    code = 0x0023

                terminal.color(color)
                terminal.put(x + x_offset, y + y_offset, code)

        terminal.color(0xFFFFFFFF)

        for _, (display, position) in self.world.get_components(Display, Position):
            if game_map.visible[position.y][position.x]:
                terminal.put(position.x + x_offset, position.y + y_offset, chr(display.code))
