from esper import Processor

from constants import DijkstraMap, AWAKE_DISTANCE
from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.eventmixin import EventMixin
from functions import dijkstra_map, move


class MovementProcessor(Processor, EventMixin):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, (position, player) = next(iter(self.world.get_components(Position, Player)))

        event = player.action

        if not event:
            return

        if event.name == "move":
            if event.data["target"]:
                move(game_map, position, event.data["target"])

                game_map.dijkstra[DijkstraMap.PLAYER] = dijkstra_map(
                    game_map=game_map,
                    sources=[(position.x, position.y)],
                    check_explored=False,
                    max_value=AWAKE_DISTANCE,
                )
