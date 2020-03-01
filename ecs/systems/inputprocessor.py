from bearlibterminal import terminal

from ecs.event import Event
from ecs.processor import Processor


class InputProcessor(Processor):
    def process(self):
        event = terminal.read()
        self.event(Event("key_pressed", {"key": event}))

        if event == terminal.TK_CLOSE:
            raise SystemExit

        if event == terminal.TK_LEFT:
            self.event(Event("move", {"dx": -1, "dy": 0}))
            return

        if event == terminal.TK_RIGHT:
            self.event(Event("move", {"dx": 1, "dy": 0}))
            return

        if event == terminal.TK_UP:
            self.event(Event("move", {"dx": 0, "dy": -1}))
            return

        if event == terminal.TK_DOWN:
            self.event(Event("move", {"dx": 0, "dy": 1}))
            return
