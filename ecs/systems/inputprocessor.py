from bearlibterminal import terminal
from esper import Processor

from ecs.components.player import Player
from ecs.eventmixin import EventMixin


class InputProcessor(Processor, EventMixin):
    def process(self):
        event = terminal.read()

        while terminal.has_input():
            terminal.read()

        if event == terminal.TK_CLOSE:
            raise SystemExit

        _, player = next(iter(self.world.get_component(Player)))

        if event == terminal.TK_Z:
            player.action = player.attack_action

        if event == terminal.TK_X:
            player.action = player.defend_action
