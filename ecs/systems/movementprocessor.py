from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.processor import Processor
from functions import iter_neighbors


def move_dijkstra(map_: Map, position: Position, key: str) -> bool:
    neighbors = [
        (x, y)
        for x, y, in iter_neighbors(position.x, position.y, map_)
        if map_.walkable[y][x] and map_.dijkstra[key][y][x] < map_.dijkstra[key][position.y][position.x]
    ]

    if not neighbors:
        return False

    neighbors.sort(key=lambda xy: map_.dijkstra[key][xy[1]][xy[0]])
    x, y = neighbors[0]

    position.x = x
    position.y = y

    return True


class MovementProcessor(Processor):
    def process(self):
        pass

    def event_move(self, event):
        _, map_ = next(iter(self.world.get_component(Map)))
        _, (position, _) = next(iter(self.world.get_components(Position, Player)))

        success = move_dijkstra(map_, position, "auto_explore")
        if not success:
            move_dijkstra(map_, position, "staircase")
