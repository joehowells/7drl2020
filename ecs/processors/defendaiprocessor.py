from esper import Processor, World

from constants import DijkstraMap
from action import Action, ActionType
from ecs.components.inventory import Inventory
from ecs.components.item import Item
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.targeted import Targeted
from ecs.components.visible import Visible
from ecs.processors.spatialprocessor import Coincident
from functions import move_dijkstra


class DefendAIProcessor(Processor):
    def process(self):
        self.world: World

        _, game_map = next(iter(self.world.get_component(Map)))
        _, (player, player_position) = next(iter(self.world.get_components(Player, Position)))

        for _ in self.world.get_components(Monster, Visible):
            entity_pairs = self.world.get_components(Item, Inventory)

            if entity_pairs:
                entity = entity_pairs[0][0]
                self.world.add_component(entity, Targeted())
                player.defend_action = Action(ActionType.USE_ITEM, -10)
                return

            target = move_dijkstra(game_map, player_position, DijkstraMap.MONSTER, reverse=True)

            if target:
                player.defend_action = Action(ActionType.MOVE, -1, target)
                return

            player.defend_action = Action(ActionType.WAIT, -1)
            return

        for _ in self.world.get_components(Item, Coincident):
            player.defend_action = Action(ActionType.GET_ITEM, -1)
            return

        for _ in self.world.get_components(Item, LastKnownPosition):
            target = move_dijkstra(game_map, player_position, DijkstraMap.ITEM)

            if target:
                player.defend_action = Action(ActionType.MOVE, -1, target)
                return
            else:
                break

        player.defend_action = Action(ActionType.WAIT, -1)
        return
