from esper import Processor

from constants import DijkstraMap, AWAKE_DISTANCE
from action import ActionType
from ecs.components.awake import Awake
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.visible import Visible


class AwakeProcessor(Processor):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, player = next(iter(self.world.get_component(Player)))

        event = player.action

        if player.action.action_type is ActionType.ATTACK:
            for entity, (_, position) in self.world.get_components(Monster, Position):
                if self.world.has_component(entity, Awake):
                    if game_map.dijkstra[DijkstraMap.PLAYER][position.y][position.x] > AWAKE_DISTANCE:
                        self.world.remove_component(entity, Awake)
                else:
                    if self.world.has_component(entity, Visible):
                        self.world.add_component(entity, Awake())

                    if event and game_map.dijkstra[DijkstraMap.PLAYER][position.y][position.x] <= AWAKE_DISTANCE:
                        self.world.add_component(entity, Awake())
