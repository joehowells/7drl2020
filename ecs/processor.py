from abc import ABC

import esper

from ecs.event import Event


class Processor(ABC, esper.Processor):
    def event(self, event: Event) -> None:
        self.world.event(event)
