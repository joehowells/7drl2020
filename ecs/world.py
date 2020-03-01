import esper

from ecs.event import Event


class World(esper.World):
    def event(self, event: Event) -> None:
        for processor in self._processors:
            method = getattr(processor, f"event_{event.name}", None)

            if method:
                method(event)
