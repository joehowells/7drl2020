from esper import Processor

from constants import DijkstraMap
from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.eventmixin import EventMixin
from functions import move_dijkstra, dijkstra_map


class MovementProcessor(Processor, EventMixin):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, (position, player) = next(iter(self.world.get_components(Position, Player)))

        event = player.action
        print(event)

        if not event:
            return

        if event.name == "move":
            move_dijkstra(game_map, position, event.data["dijkstra"])
            game_map.dijkstra[DijkstraMap.PLAYER] = dijkstra_map(game_map, [(position.x, position.y)], check_explored=False, max_value=16)
