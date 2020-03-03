from bearlibterminal import terminal
from esper import Processor

from ecs.components.dead import Dead
from ecs.components.player import Player
from ecs.eventmixin import EventMixin


class InputProcessor(Processor, EventMixin):
    def process(self):
        while True:
            event = terminal.read()

            while terminal.has_input():
                terminal.read()

            if event == terminal.TK_CLOSE:
                raise SystemExit

            entity, player = next(iter(self.world.get_component(Player)))

            if not self.world.has_component(entity, Dead):
                if event == terminal.TK_Z:
                    player.action = player.attack_action
                    player.anger = min(max(player.anger + player.action.data.get("anger", 0), 0), 100)
                    return

                if event == terminal.TK_X:
                    _, player = next(iter(self.world.get_component(Player)))
                    player.action = player.defend_action
                    player.anger = min(max(player.anger + player.action.data.get("anger", 0), 0), 100)
                    return
