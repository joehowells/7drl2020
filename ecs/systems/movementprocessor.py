from ecs.components.map import Map
from ecs.components.position import Position
from ecs.processor import Processor
from ecs.systems.dijkstramapprocessor import iter_neighbors


class MovementProcessor(Processor):
    def process(self):
        pass

    def event_move(self, event):
        _, map_ = next(iter(self.world.get_component(Map)))

        for _, (position,) in self.world.get_components(Position):
            neighbors = [
                (x, y)
                for x, y, in iter_neighbors(position.x, position.y, map_)
                if map_.walkable[y][x] and map_.dijkstra[y][x] < map_.dijkstra[position.y][position.x]
            ]

            if not neighbors:
                return

            neighbors.sort(key=lambda xy: map_.dijkstra[xy[1]][xy[0]])
            x, y = neighbors[0]

            position.x = x
            position.y = y
