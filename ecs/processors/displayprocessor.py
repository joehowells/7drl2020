import itertools
from textwrap import wrap
from typing import Tuple, Set

from bearlibterminal import terminal
from esper import Processor, World

# from constants import DijkstraMap
from ecs.components.display import Display
from ecs.components.gamestate import GameState
from ecs.components.inventory import Inventory
from ecs.components.item import Item
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.targeted import Targeted
from ecs.components.visible import Visible


def draw_borders() -> None:
    terminal.bkcolor(0xFF000000)
    terminal.color(0xFF666666)

    for y in range(21):
        terminal.put(33, y, 0x2551)

    for x in range(34, 84):
        terminal.put(x, 3, 0x2500)
        terminal.put(x, 6, 0x2500)

    for y in range(3):
        terminal.put(67, y, 0x2502)

    terminal.put(33, 3, 0x255F)
    terminal.put(33, 6, 0x255F)
    terminal.put(67, 3, 0x2534)


def draw_bar(x: int, y: int, value: int, color: int = 0xFFFFFFFF) -> None:
    terminal.color(color)
    terminal.printf(x, y, "=" * value)
    terminal.color(0xFFFFFFFF)


def filter_color(color: int, player: Player) -> int:
    factor = player.anger / 100

    r = color >> 16 & 255
    g = color >> 8 & 255
    b = color & 255

    r = min(int(r + factor*(g+b)), 255)
    g = int((1.0 - factor) * g)
    b = int((1.0 - factor) * b)

    return 0xFF000000 + (r << 16) + (g << 8) + b


class DisplayProcessor(Processor):
    def __init__(self):
        self.buffer = []

    def process(self):
        self.world: World

        _, state = next(iter(self.world.get_component(GameState)))

        if state is GameState.TITLE_SCREEN:
            self.draw_title_screen()

        if state is GameState.MAIN_GAME:
            self.draw_main_game()

    def get_targets(self) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]], Set[Tuple[int, int]]]:
        """Get coordinates of all targeted tiles."""
        self.world: World

        attack_targets = set()
        defend_targets = set()

        for _, player in self.world.get_component(Player):
            if player.attack_action.target:
                attack_targets.add(player.attack_action.target)

            if player.defend_action.target:
                defend_targets.add(player.defend_action.target)

        for entity, (position, _) in self.world.get_components(Position, Targeted):
            if self.world.has_component(entity, Monster):
                attack_targets.add((position.x, position.y))
            else:
                defend_targets.add((position.x, position.y))

        both_targets = attack_targets.intersection(defend_targets)
        attack_targets -= both_targets
        defend_targets -= both_targets

        return attack_targets, defend_targets, both_targets

    def draw_title_screen(self):
        self.buffer = []

        terminal.bkcolor(0xFF000000)
        terminal.color(0xFFFFFFFF)
        terminal.clear()
        terminal.printf(0, 0, "Title Screen")
        terminal.printf(0, 0, "Press [[Z+X]] to start ...")
        terminal.refresh()

    def draw_main_game(self):
        terminal.bkcolor(0xFF000000)
        terminal.color(0xFFFFFFFF)
        terminal.clear()

        draw_borders()

        self.draw_map()
        self.draw_entities()
        self.highlight_targets()
        self.draw_ui()
        self.draw_messages()

        terminal.bkcolor(0xFF000000)
        terminal.color(0xFFFFFFFF)
        for _, player in self.world.get_component(Player):
            terminal.printf(0, 0, f"Level: {player.level + 1}")
            break

        terminal.bkcolor(0xFF000000)
        terminal.color(0xFF666666)
        for x in range(0, 8):
            terminal.put(x, 1, 0x2500)

        terminal.put(8, 0, 0x2502)
        terminal.put(8, 1, 0x2518)

        terminal.refresh()

    def draw_map(self):
        _, (player, position) = next(iter(self.world.get_components(Player, Position)))
        x_offset = 16 - position.x
        y_offset = 10 - position.y

        _, game_map = next(iter(self.world.get_component(Map)))

        # key = DijkstraMap.PLAYER
        # max_dijkstra = max(max(value for value in row) for row in game_map.dijkstra[key])

        for xc, yc in itertools.product(range(33), range(21)):
            x = xc - x_offset
            y = yc - y_offset

            if not 0 <= x < game_map.w or not 0 <= y < game_map.h:
                continue

            if game_map.explored[y][x]:
                if game_map.visible[y][x]:
                    if game_map.walkable[y][x]:
                        bkcolor = 0xFF100800
                        color = 0xFF281400
                    else:
                        bkcolor = 0xFF301800
                        color = 0xFF582C00

                    bkcolor = filter_color(bkcolor, player)
                    color = filter_color(color, player)
                else:
                    bkcolor = 0xFF000000
                    color = 0xFF202020

                if game_map.walkable[y][x]:
                    code = 0x002E
                else:
                    code = 0x0023

                # if game_map.dijkstra[key][y][x] >= 0:
                #     distance = int(game_map.dijkstra[key][y][x] / max_dijkstra * 767)
                #     if 0 <= distance <= 255:
                #         color = terminal.color_from_argb(255, 255, 255 - distance, 0)
                #     elif 256 <= distance <= 511:
                #         color = terminal.color_from_argb(255, 255, 0, distance - 256)
                #     elif 512 <= distance <= 767:
                #         color = terminal.color_from_argb(255, 767 - distance, 0, 255)

                terminal.bkcolor(bkcolor)
                terminal.color(color)

                terminal.put(x + x_offset, y + y_offset, code)

    def draw_entities(self):
        _, (player, position) = next(iter(self.world.get_components(Player, Position)))

        # Set player offset relative to display
        x_offset = 16 - position.x
        y_offset = 10 - position.y

        # Set the bounding box for filtering out entities
        x_min = position.x - 16
        x_max = position.x + 16
        y_min = position.y - 10
        y_max = position.y + 10

        entity_pairs = self.world.get_components(Display, LastKnownPosition)

        if not entity_pairs:
            return

        entity_pairs.sort(key=lambda pair: pair[1][0].draw_order)

        for entity, (display, position) in entity_pairs:
            if not x_min <= position.x <= x_max or not y_min <= position.y <= y_max:
                continue

            if self.world.has_component(entity, Visible):
                bkcolor = 0xFF100800
                color = display.color

                bkcolor = filter_color(bkcolor, player)
                color = filter_color(color, player)
            else:
                bkcolor = 0xFF000000
                color = 0xFF666666

            terminal.bkcolor(bkcolor)
            terminal.color(color)

            terminal.put(
                position.x + x_offset,
                position.y + y_offset,
                display.code,
            )

    def highlight_targets(self):
        attack_targets, defend_targets, both_targets = self.get_targets()

        _, (_, position) = next(iter(self.world.get_components(Player, Position)))

        # Set player offset relative to display
        x_offset = 16 - position.x
        y_offset = 10 - position.y

        # Set the bounding box for filtering out entities
        x_min = position.x - 16
        x_max = position.x + 16
        y_min = position.y - 10
        y_max = position.y + 10

        terminal.color(0xFF000000)

        terminal.bkcolor(0xFFFF0000)
        for x, y in attack_targets:
            if x_min <= position.x <= x_max and y_min <= position.y <= y_max:
                x += x_offset
                y += y_offset
                terminal.put(x, y, terminal.pick(x, y))

        terminal.bkcolor(0xFF0000FF)
        for x, y in defend_targets:
            if x_min <= position.x <= x_max and y_min <= position.y <= y_max:
                x += x_offset
                y += y_offset
                terminal.put(x, y, terminal.pick(x, y))

        terminal.bkcolor(0xFFFF00FF)
        for x, y in both_targets:
            if x_min <= position.x <= x_max and y_min <= position.y <= y_max:
                x += x_offset
                y += y_offset
                terminal.put(x, y, terminal.pick(x, y))

    def draw_ui(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, player = next(iter(self.world.get_component(Player)))

        terminal.bkcolor(0xFF000000)
        terminal.color(0xFFFFFFFF)

        terminal.printf(34, 0, f"Health: {player.health:>3d}")
        terminal.printf(34, 1, f"Anger:  {player.anger:>3d}")
        terminal.printf(34, 2, f"Threat: {player.actual_threat:>3d}")

        draw_bar(46, 0, 20, 0xFF333333)
        draw_bar(46, 1, 20, 0xFF333333)
        draw_bar(46, 2, 20, 0xFF333333)

        draw_bar(46, 0, player.health * 2)
        draw_bar(46, 1, player.anger // 5, 0xFFFF0000)
        draw_bar(46, 2, player.visible_threat, 0xFFFFFF00)
        draw_bar(46, 2, player.actual_threat, 0xFFFF0000)

        terminal.color(0xFFFF0000)
        terminal.printf(34, 4, "z)")
        terminal.color(0xFF0000FF)
        terminal.printf(34, 5, "x)")
        terminal.color(0xFFFFFFFF)
        terminal.printf(37, 4, f"{player.attack_action.nice_name}")
        terminal.printf(37, 5, f"{player.defend_action.nice_name}")

        inventory = sum(1 for _ in self.world.get_components(Item, Inventory))
        inventory = min(max(inventory, 0), 99)

        terminal.printf(68, 0, f"Attack: {player.attack:>2d}")
        terminal.printf(68, 1, f"Defend: {player.defend:>2d}")
        terminal.printf(68, 2, f"Items:  {inventory:>2d}")

        if player.attack_bonus > 0:
            terminal.color(0xFFFF0000)
            terminal.printf(79, 0, f"(+{player.attack_bonus})")

        if player.defend_bonus > 0:
            terminal.color(0xFFFF0000)
            terminal.printf(79, 1, f"(+{player.defend_bonus})")

    def draw_messages(self):
        terminal.bkcolor(0xFF000000)
        terminal.color(0xFFFFFFFF)

        # Load new messages into a list
        messages = []
        for entity, message in self.world.get_component(Message):
            messages.append(message)
            self.world.delete_entity(entity)

        # Sort by priority
        messages.sort(key=lambda m: m.priority, reverse=True)

        for message in messages:
            for text in wrap(message.text, 50):
                self.buffer.append((text, message.color))

        self.buffer = self.buffer[-14:]

        for row, (message, color) in enumerate(self.buffer):
            terminal.color(color)
            terminal.printf(34, row + 7, message)
