from esper import Processor

from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.position import Position
from ecs.components.visible import Visible


class VisibilityProcessor(Processor):
    """
    Determines whether entities are visible.
    """
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))

        for entity, position in self.world.get_component(Position):
            if game_map.visible[position.y][position.x]:
                self.world.add_component(entity, Visible())
                self.world.add_component(entity, LastKnownPosition(position.x, position.y))
            else:
                if self.world.has_component(entity, Visible):
                    self.world.remove_component(entity, Visible)
