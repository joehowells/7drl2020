from bearlibterminal import terminal
from esper import Processor

from ecs.components.event import Event
from ecs.eventmixin import EventMixin


class InputProcessor(Processor, EventMixin):
    def process(self):
        event = terminal.read()

        while terminal.has_input():
            terminal.read()

        if event == terminal.TK_CLOSE:
            raise SystemExit

        if event == terminal.TK_Z:
            self.set_event(Event("attack_ai", {}))
            return
