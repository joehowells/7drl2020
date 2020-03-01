from bearlibterminal import terminal

from ecs.event import Event
from ecs.processor import Processor


class InputProcessor(Processor):
    def process(self):
        event = terminal.read()

        if event == terminal.TK_CLOSE:
            raise SystemExit

        if event == terminal.TK_Z:
            self.event(Event("attack_ai", {}))
            return
