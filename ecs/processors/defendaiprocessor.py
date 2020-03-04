from esper import Processor, World

from action import Action, ActionType
from constants import DijkstraMap
from ecs.components.healingpotion import HealingPotion
from ecs.components.inventory import Inventory
from ecs.components.item import Item
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.targeted import Targeted
from ecs.components.teleportscroll import TeleportScroll
from ecs.components.visible import Visible
from ecs.processors.spatialprocessor import Coincident
from functions import move_dijkstra


class DefendAIProcessor(Processor):
    def process(self):
        self.world: World

        _, game_map = next(iter(self.world.get_component(Map)))
        _, (player, player_position) = next(iter(self.world.get_components(Player, Position)))

        if player.health < 10:
            for entity, (item, _, _) in self.world.get_components(Item, Inventory, HealingPotion):
                self.world.add_component(entity, Targeted())
                player.defend_action = Action(
                    action_type=ActionType.USE_ITEM,
                    anger=-10,
                    nice_name=f"Use {item.name}",
                )
                return

        for _ in self.world.get_components(Monster, Visible):
            target = move_dijkstra(game_map, player_position, DijkstraMap.MONSTER, reverse=True)

            if target:
                player.defend_action = Action(
                    action_type=ActionType.MOVE,
                    anger=-1,
                    target=target,
                    nice_name="Retreat",
                )
                return

            for entity, (item, _, _) in self.world.get_components(Item, Inventory, TeleportScroll):
                self.world.add_component(entity, Targeted())
                player.defend_action = Action(
                    action_type=ActionType.USE_ITEM,
                    anger=-10,
                    nice_name=f"Use {item.name}",
                )
                return

            player.defend_action = Action(
                action_type=ActionType.WAIT,
                anger=-1,
                nice_name="Wait",
            )
            return

        for _, (item, _) in self.world.get_components(Item, Coincident):
            player.defend_action = Action(
                action_type=ActionType.GET_ITEM,
                anger=-1,
                nice_name=f"Get {item.name}",
            )
            return

        target = move_dijkstra(game_map, player_position, DijkstraMap.ITEM)

        if target:
            player.defend_action = Action(
                action_type=ActionType.MOVE,
                anger=-1,
                target=target,
                nice_name="Find item",
            )
            return

        player.defend_action = Action(
            action_type=ActionType.WAIT,
            anger=-1,
            nice_name="Wait",
        )
