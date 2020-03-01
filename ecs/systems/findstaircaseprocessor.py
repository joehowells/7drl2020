from ecs.components.map import Map
from ecs.components.position import Position
from ecs.components.staircase import Staircase
from ecs.processor import Processor
from functions import dijkstra_map


class FindStaircaseProcessor(Processor):
    def process(self):
        _, map_ = next(iter(self.world.get_component(Map)))
        _, (_, position) = next(iter(self.world.get_components(Staircase, Position)))

        map_.dijkstra["staircase"] = dijkstra_map(map_, [(position.x, position.y)])
