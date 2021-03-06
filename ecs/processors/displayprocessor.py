import itertools
from typing import Tuple, Set

from bearlibterminal import terminal
from esper import Processor, World

from constants import MAX_RAGE, MAX_HEALTH, MAX_THREAT
from ecs.components.assassin import Assassin
from ecs.components.attacktarget import AttackTarget
from ecs.components.blinded import Blinded
from ecs.components.defendtarget import DefendTarget
from ecs.components.display import Display
from ecs.components.firescroll import FireScroll
from ecs.components.gamestate import GameState
from ecs.components.healingpotion import HealingPotion
from ecs.components.inventory import Inventory
from ecs.components.item import Item
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.smokebomb import SmokeBomb
from ecs.components.taunted import Taunted
from ecs.components.teleportscroll import TeleportScroll
from ecs.components.visible import Visible
from ecs.processors.spatialprocessor import Adjacent


def draw_borders() -> None:
    terminal.bkcolor(0xFF000000)
    terminal.color(0xFF666666)

    for y in range(21):
        terminal.put(33, y, 0x2551)

    for x in range(34, 84):
        terminal.put(x, 3, 0x2500)
        terminal.put(x, 6, 0x2500)

    for y in range(6):
        terminal.put(67, y, 0x2502)

    terminal.put(33, 3, 0x255F)
    terminal.put(33, 6, 0x255F)
    terminal.put(67, 3, 0x253C)
    terminal.put(67, 6, 0x2534)


def draw_bar(x: int, y: int, value: int, max_value: int, color: int = 0xFFFFFFFF) -> None:
    terminal.color(color)
    terminal.printf(x, y, "=" * int(20 * value / max_value))
    terminal.color(0xFFFFFFFF)


def filter_color(color: int, player: Player) -> int:
    factor = player.rage / MAX_RAGE

    r = color >> 16 & 255
    g = color >> 8 & 255
    b = color & 255

    r = min(int(r + factor * (g + b)), 255)
    g = int((1.0 - factor) * g)
    b = int((1.0 - factor) * b)

    return 0xFF000000 + (r << 16) + (g << 8) + b


class DisplayProcessor(Processor):
    def __init__(self):
        self.buffer = []
        self.old_rage = 0

    def process(self):
        self.world: World

        for _, state in self.world.get_component(GameState):
            if state is GameState.TITLE_SCREEN:
                self.draw_title_screen()

            if state is GameState.MAIN_GAME:
                self.draw_main_game()

            if state is GameState.GAME_OVER:
                self.draw_game_over()

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

        for entity, (position, _) in self.world.get_components(Position, AttackTarget):
            attack_targets.add((position.x, position.y))

        for entity, (position, _) in self.world.get_components(Position, DefendTarget):
            defend_targets.add((position.x, position.y))

        for _ in self.world.get_components(Player, Taunted):
            defend_targets = set()

        both_targets = attack_targets.intersection(defend_targets)
        attack_targets -= both_targets
        defend_targets -= both_targets

        return attack_targets, defend_targets, both_targets

    def draw_title_screen(self):
        # Clear the message buffer on first draw to get rid of messages from previous game
        self.buffer = []
        self.old_rage = 0

        terminal.clear()

        terminal.bkcolor(0xFF000000)
        terminal.color(0xFFFFFFFF)
        with open("data/title_screen.txt") as file:
            terminal.puts(
                x=5,
                y=0,
                s=file.read(),
                width=74,
                height=21,
                align=terminal.TK_ALIGN_CENTER | terminal.TK_ALIGN_MIDDLE,
            )

        terminal.refresh()

    def draw_game_over(self):
        terminal.clear()

        terminal.bkcolor(0xFF000000)
        terminal.color(0xFFFFFFFF)

        buffer = [
        ]

        for _, player in self.world.get_component(Player):
            if player.killer:
                buffer.extend([
                    "[color=#FFFF0000]Defeat[/color]",
                    "",
                    "",
                    f"You were killed by {player.killer} on level {player.level + 1} of the dungeon.",
                ])
            else:
                buffer.extend([
                    "[color=#FFFF0000]Victory![/color]",
                    "",
                    "",
                    (
                        "[color=#FF999999]With the milita defeated, you can finally put your feet up and read your"
                        " newspaper. But you lost it somewhere in the dungeon...[/color]"
                    ),
                ])

            buffer.append("")

            if not player.kills:
                buffer.append("You didn[U+2019]t kill anyone.")
            else:
                buffer.extend([
                    f"You killed {sum(player.kills.values())} enemies:",
                    "",
                ])

                # Generate kill strings from Counter
                items = sorted(player.kills.items())

                kills = []
                for i, (key, value) in enumerate(items):
                    plural = "s" if value > 1 else ""
                    kills.append(f"{value} {key}{plural}")

                if len(kills) % 2:
                    kills.append("")

                for one, two in zip(kills[::2], kills[1::2]):
                    buffer.append(f"{one.ljust(24)}  {two.ljust(24)}")

        buffer.extend([
            "",
            "",
            "Press [color=#FFFF0000](z)[/color] and [color=#FF0000FF](x)[/color] to return.",
        ])

        terminal.puts(
            x=8,
            y=1,
            s="\n".join(buffer),
            width=68,
            height=19,
            align=terminal.TK_ALIGN_CENTER,
        )

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

        terminal.refresh()

    def draw_map(self):
        for _, (player, position) in self.world.get_components(Player, Position):
            x_offset = 16 - position.x
            y_offset = 10 - position.y

            for _, game_map in self.world.get_component(Map):
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

                        code = game_map.glyphs.get((x, y), code)

                        terminal.bkcolor(bkcolor)
                        terminal.color(color)

                        terminal.put(x + x_offset, y + y_offset, code)

    def draw_entities(self):
        for _, (player, player_position) in self.world.get_components(Player, Position):
            # Set player offset relative to display
            x_offset = 16 - player_position.x
            y_offset = 10 - player_position.y

            # Set the bounding box for filtering out entities
            x_min = player_position.x - 16
            x_max = player_position.x + 16
            y_min = player_position.y - 10
            y_max = player_position.y + 10

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

                if self.world.has_component(entity, Blinded):
                    bkcolor = 0xFFFFFFFF
                    color = 0xFF000000

                    bkcolor = filter_color(bkcolor, player)
                    color = filter_color(color, player)

                terminal.bkcolor(bkcolor)
                terminal.color(color)

                # Render assassins as underscores until they are in range
                if self.world.has_component(entity, Assassin) and not self.world.has_component(entity, Adjacent):
                    code = 0x005F
                else:
                    code = display.code

                terminal.put(
                    position.x + x_offset,
                    position.y + y_offset,
                    code,
                )

    def highlight_targets(self):
        attack_targets, defend_targets, both_targets = self.get_targets()

        for _, (_, position) in self.world.get_components(Player, Position):
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
        for _, game_map in self.world.get_component(Map):
            for player_entity, player in self.world.get_component(Player):
                terminal.bkcolor(0xFF000000)
                terminal.color(0xFFFFFFFF)

                terminal.printf(34, 0, f"Health: {player.health:>3d}")
                terminal.printf(34, 1, f"Rage:   {player.rage:>3d}")
                terminal.printf(34, 2, f"Threat: {player.actual_threat:>3d}")

                draw_bar(46, 0, 1, 1, 0xFF333333)
                draw_bar(46, 1, 1, 1, 0xFF333333)
                draw_bar(46, 2, 1, 1, 0xFF333333)

                if player.health <= 4:
                    color = 0xFFFF0000
                elif player.health <= 8:
                    color = 0xFFFFFF00
                else:
                    color = 0xFF00FF00

                draw_bar(46, 0, player.health, MAX_HEALTH, color)
                draw_bar(46, 1, self.old_rage, MAX_RAGE, 0xFF0000FF)
                draw_bar(46, 1, player.rage, MAX_RAGE, 0xFFFF0000)
                draw_bar(46, 2, player.visible_threat, MAX_THREAT, 0xFFFFFF00)
                draw_bar(46, 2, player.actual_threat, MAX_THREAT, 0xFFFF0000)

                self.old_rage = player.rage

                terminal.color(0xFFFF0000)
                terminal.printf(34, 4, "z)")

                if self.world.has_component(player_entity, Taunted):
                    terminal.color(0xFFFF0000)
                else:
                    terminal.color(0xFF0000FF)

                terminal.printf(34, 5, "x)")
                terminal.color(0xFFFFFFFF)
                terminal.printf(37, 4, f"{player.attack_action.nice_name}")
                terminal.printf(37, 5, f"{player.defend_action.nice_name}")

                terminal.printf(68, 0, f"Attack: {player.attack:>2d}")
                terminal.printf(68, 1, f"Armour: {player.defend:>2d}")
                terminal.printf(68, 2, f"Level:  {player.level + 1:>2d}")

                inventory = sum(1 for _ in self.world.get_components(Item, Inventory, HealingPotion))
                inventory = min(max(inventory, 0), 9)
                terminal.printf(68, 4, f"[color=#FFFF0066]![/color]: {inventory}")

                inventory = sum(1 for _ in self.world.get_components(Item, Inventory, SmokeBomb))
                inventory = min(max(inventory, 0), 9)
                terminal.printf(68, 5, f"[color=#FF00FF66]![/color]: {inventory}")

                inventory = sum(1 for _ in self.world.get_components(Item, Inventory, TeleportScroll))
                inventory = min(max(inventory, 0), 9)
                terminal.printf(73, 4, f"[color=#FF6600FF]?[/color]: {inventory}")

                inventory = sum(1 for _ in self.world.get_components(Item, Inventory, FireScroll))
                inventory = min(max(inventory, 0), 9)
                terminal.printf(73, 5, f"[color=#FFFF6600]?[/color]: {inventory}")

                terminal.printf(78, 4, f"[color=#FF999999])[/color]: {player.attack_equip}")
                terminal.printf(78, 5, f"[color=#FF999999][[[/color]: {player.defend_equip}")

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

        prefix = "[color=#FF666666]>[/color] "
        for index, message in enumerate(messages):
            self.buffer.append(prefix + message.text)
            prefix = "  "

        self.buffer = self.buffer[-14:]
        s = "\n".join(self.buffer)
        w, h = terminal.measure(s, 50, 14)

        if h < 14:
            align = terminal.TK_ALIGN_TOP
        else:
            align = terminal.TK_ALIGN_BOTTOM

        terminal.puts(x=34, y=7, s=s, width=50, height=14, align=align)
