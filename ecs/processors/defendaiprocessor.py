from esper import Processor, World

from action import Action, ActionType
from constants import DijkstraMap
from ecs.components.boss import Boss
from ecs.components.defendtarget import DefendTarget
from ecs.components.healingpotion import HealingPotion
from ecs.components.inventory import Inventory
from ecs.components.item import Item
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.smokebomb import SmokeBomb
from ecs.components.taunt import Taunted
from ecs.components.teleportscroll import TeleportScroll
from ecs.components.thunderscroll import ThunderScroll
from ecs.components.visible import Visible
from ecs.processors.spatialprocessor import Coincident
from functions import move_dijkstra, color_item_name


class DefendAIProcessor(Processor):
    def process(self):
        self.world: World

        _, game_map = next(iter(self.world.get_component(Map)))
        player_entity, (player, player_position) = next(iter(self.world.get_components(Player, Position)))

        for taunted in self.world.try_component(player_entity, Taunted):
            if taunted.turns_left <= 0:
                player.anger = min(max(player.anger - 10, 0), 100)
                self.world.remove_component(player_entity, Taunted)
                self.world.create_entity(Message(
                    text="You snap out of your rage.",
                    priority=25,
                ))
            else:
                taunted.turns_left -= 1
                player.anger = min(max(player.anger + 5, 0), 100)
                player.defend_action = player.attack_action
                self.world.create_entity(Message(
                    text="[color=#FFFFFF00]Your rage clouds your judgement![/color]",
                    priority=25,
                ))
                return

        if player.health < 9:
            for entity, (item, _, _) in self.world.get_components(Item, Inventory, HealingPotion):
                self.world.add_component(entity, DefendTarget())
                player.defend_action = Action(
                    action_type=ActionType.USE_ITEM,
                    anger=-20,
                    nice_name=f"Use {color_item_name(self.world, entity)}",
                )
                return

        for _ in self.world.get_components(Monster, Visible):
            target = move_dijkstra(self.world, game_map, player_position, DijkstraMap.MONSTER, reverse=True)

            if target:
                player.defend_action = Action(
                    action_type=ActionType.MOVE,
                    anger=-1,
                    target=target,
                    nice_name="Retreat",
                )
                return

            for entity, (item, _, _) in self.world.get_components(Item, Inventory, SmokeBomb):
                self.world.add_component(entity, DefendTarget())
                player.defend_action = Action(
                    action_type=ActionType.USE_ITEM,
                    anger=-20,
                    nice_name=f"Use {color_item_name(self.world, entity)}",
                )
                return

            for entity, (item, _, _) in self.world.get_components(Item, Inventory, ThunderScroll):
                candidates = []
                for monster_entity, (monster, _) in self.world.get_components(Monster, Visible):
                    if not self.world.has_component(monster_entity, Boss):
                        candidates.append((max(monster.threat), monster_entity, monster))

                if candidates:
                    candidates.sort(reverse=True)
                    _, monster_entity, monster = candidates[0]
                    self.world.add_component(monster_entity, DefendTarget())
                    self.world.add_component(entity, DefendTarget())
                    player.defend_action = Action(
                        action_type=ActionType.USE_ITEM,
                        anger=-20,
                        nice_name=f"Use {color_item_name(self.world, entity)}",
                    )
                    return

            for entity, (item, _, _) in self.world.get_components(Item, Inventory, TeleportScroll):
                self.world.add_component(entity, DefendTarget())
                player.defend_action = Action(
                    action_type=ActionType.USE_ITEM,
                    anger=-20,
                    nice_name=f"Use {color_item_name(self.world, entity)}",
                )
                return

            player.defend_action = Action(
                action_type=ActionType.WAIT,
                anger=-1,
                nice_name="Wait",
            )
            return

        for entity, (item, _) in self.world.get_components(Item, Coincident):
            player.defend_action = Action(
                action_type=ActionType.GET_ITEM,
                anger=-1,
                nice_name=f"Get {color_item_name(self.world, entity)}",
            )
            return

        target = move_dijkstra(self.world, game_map, player_position, DijkstraMap.ITEM)

        if target:
            player.defend_action = Action(
                action_type=ActionType.MOVE,
                anger=-1,
                target=target,
                nice_name="Gather items",
            )
            return

        target = move_dijkstra(self.world, game_map, player_position, DijkstraMap.EXPLORE)

        if target:
            player.defend_action = Action(
                action_type=ActionType.MOVE,
                anger=-1,
                target=target,
                nice_name="Explore",
            )
            return

        player.defend_action = Action(
            action_type=ActionType.WAIT,
            anger=-1,
            nice_name="Wait",
        )
