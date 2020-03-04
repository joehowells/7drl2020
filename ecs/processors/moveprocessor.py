from esper import Processor

from action import ActionType
from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from functions import move


class MoveProcessor(Processor):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, (position, player) = next(iter(self.world.get_components(Position, Player)))

        if player.action.action_type is ActionType.MOVE and player.action.target:
            move(position, player.action.target)
