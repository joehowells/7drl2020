from esper import Processor

from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from functions import move


class MovementProcessor(Processor):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, (position, player) = next(iter(self.world.get_components(Position, Player)))

        event = player.action

        if not event:
            return

        if event.name == "move":
            if event.data["target"]:
                move(game_map, position, event.data["target"])
