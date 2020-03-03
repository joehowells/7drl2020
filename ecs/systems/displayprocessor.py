import itertools
from textwrap import wrap

from bearlibterminal import terminal
from esper import Processor

from constants import DijkstraMap
from ecs.components.display import Display
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.visible import Visible


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
    terminal.printf(x, y, "=" * value)
    terminal.color(0xFFFFFFFF)


class DisplayProcessor(Processor):
    def __init__(self):
        self.buffer = []

    def process(self):
        terminal.clear()

        terminal.color(0xFF666666)

        draw_borders()

        self.draw_map()
        self.draw_entities()
        self.draw_ui()
        self.draw_messages()

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

                distance = min(game_map.dijkstra[DijkstraMap.EXPLORE][y][x], 63)
                if 0 <= distance <= 15:
                    color = terminal.color_from_argb(255, 255, 0x11 * distance, 0)
                elif 16 <= distance <= 31:
                    color = terminal.color_from_argb(255, 255 - 0x11 * (distance - 16), 255, 0)
                elif 32 <= distance <= 47:
                    color = terminal.color_from_argb(255, 0, 255, 0x11 * (distance - 32))
                elif 48 <= distance <= 63:
                    color = terminal.color_from_argb(255, 0, 255 - 0x11 * (distance - 48), 255)

                terminal.color(color)
                terminal.put(x + x_offset, y + y_offset, code)

    def draw_entities(self):
        _, (_, position) = next(iter(self.world.get_components(Player, Position)))

        # Set player offset relative to display
        x_offset = 16 - position.x
        y_offset = 10 - position.y

        # Set the bounding box for filtering out entities
        x_min = position.x - 16
        x_max = position.x + 16
        y_min = position.y - 10
        y_max = position.y + 10

        for entity, (display, position) in self.world.get_components(Display, Position):
            if not x_min <= position.x <= x_max or not y_min <= position.y <= y_max:
                continue

            if self.world.has_component(entity, Visible):
                terminal.color(0xFFFFFFFF)
                terminal.put(
                    position.x + x_offset,
                    position.y + y_offset,
                    display.code,
                )
            else:
                for old_position in self.world.try_component(entity, LastKnownPosition):
                    terminal.color(0xFF666666)
                    terminal.put(
                        old_position.x + x_offset,
                        old_position.y + y_offset,
                        display.code,
                    )
                    break

    def draw_ui(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, player = next(iter(self.world.get_component(Player)))

        terminal.color(0xFFFFFFFF)

        terminal.printf(34, 0, f"Health: {player.health:>3d}")
        terminal.printf(34, 1, f"Anger:  {player.anger:>3d}")
        terminal.printf(34, 2, f"Threat: {player.actual_threat:>3d}")

        draw_bar(46, 0, 20, 0xFF333333)
        draw_bar(46, 1, 20, 0xFF333333)
        draw_bar(46, 2, 20, 0xFF333333)

        draw_bar(46, 0, player.health * 2)
        draw_bar(46, 1, player.anger // 5, 0xFFFF0000)
        draw_bar(46, 2, player.visible_threat // 5, 0xFFFFFF00)
        draw_bar(46, 2, player.actual_threat // 5, 0xFFFF0000)

        terminal.printf(34, 4, f"[[Z]] {player.attack_action.name}")
        terminal.printf(34, 5, f"[[X]] {player.defend_action.name}")

        terminal.printf(51, 4, f"Attack: {player.attack}")
        terminal.printf(51, 5, f"Defend: {player.defend}")

        if player.attack_bonus > 0:
            terminal.color(0xFFFF0000)
            terminal.printf(61, 4, f"(+{player.attack_bonus})")

        if player.defend_bonus > 0:
            terminal.color(0xFFFF0000)
            terminal.printf(61, 5, f"(+{player.defend_bonus})")

    def draw_messages(self):
        for entity, message in self.world.get_component(Message):
            self.world.delete_entity(entity)

            for text in wrap(message.text, 31):
                self.buffer.append((text, message.color))

        self.buffer = self.buffer[-14:]

        for row, (message, color) in enumerate(self.buffer):
            terminal.color(color)
            terminal.printf(34, row + 7, message)
