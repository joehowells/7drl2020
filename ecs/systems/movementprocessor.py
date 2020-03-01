from ecs.components.map import Map
from ecs.components.position import Position
from ecs.processor import Processor


class MovementProcessor(Processor):
    def process(self):
        pass

    def event_move(self, event):
        _, map_ = next(iter(self.world.get_component(Map)))

        for _, (position,) in self.world.get_components(Position):
            x = position.x + event.data["dx"]
            y = position.y + event.data["dy"]

            if not 0 <= x < map_.w:
                continue

            if not 0 <= y < map_.h:
                continue

            if not map_.walkable[y][x]:
                continue

            position.x = x
            position.y = y
