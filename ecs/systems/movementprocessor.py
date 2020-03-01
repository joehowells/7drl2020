from ecs.components.position import Position
from ecs.processor import Processor


class MovementProcessor(Processor):
    def process(self):
        pass

    def event_move(self, event):
        for _, (position,) in self.world.get_components(Position):
            position.x += event.data["dx"]
            position.y += event.data["dy"]
