from esper import Processor, World

from ecs.components.awake import Awake
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.position import Position
from ecs.components.trap import Trap
from ecs.components.visible import Visible
from ecs.eventmixin import EventMixin
from factories.world import make_officer


class TrapProcessor(Processor, EventMixin):
    def process(self):
        self.world: World

        _, game_map = next(iter(self.world.get_component(Map)))
        event = self.get_event("attack")

        if not event:
            return

        sprung_trap = False
        for entity, (trap, position, _) in self.world.get_components(Trap, Position, Visible):
            sprung_trap = True

            if not game_map.blocked[position.y][position.x]:
                components = make_officer(position.x, position.y)
                components.extend([
                    Visible(),
                    Awake(),
                    LastKnownPosition(position.x, position.y),
                ])
                self.world.create_entity(*components)
                self.world.delete_entity(entity)

        if sprung_trap:
            self.world.create_entity(Message(
                text=f"Enemies appear from the stairs!",
                color=0xFFFFFF00,
            ))