from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.event import Event
from ecs.processor import Processor
from functions import move_dijkstra


class MovementProcessor(Processor):
    def process(self):
        pass

    def event_move(self, event: Event):
        _, map_ = next(iter(self.world.get_component(Map)))
        _, (position, _) = next(iter(self.world.get_components(Position, Player)))

        move_dijkstra(map_, position, event.data["dijkstra"])
