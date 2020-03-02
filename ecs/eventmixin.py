from typing import Optional

import esper

from ecs.components.event import Event


class EventMixin:
    world: esper.World

    def set_event(self, event: Event) -> None:
        entity = self.world.create_entity()
        self.world.add_component(entity, event)

    def get_event(self, name: str) -> Optional[Event]:
        for entity, event in self.world.get_component(Event):
            if event.name == name:
                self.world.delete_entity(entity)
                return event
