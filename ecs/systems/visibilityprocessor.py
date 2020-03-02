from esper import Processor

from ecs.components.map import Map
from ecs.components.position import Position
from ecs.components.visible import Visible
from ecs.eventmixin import EventMixin


class VisibilityProcessor(Processor, EventMixin):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))

        for entity, position in self.world.get_component(Position):
            if game_map.visible[position.y][position.x]:
                self.world.add_component(entity, Visible())