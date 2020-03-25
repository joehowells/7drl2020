from esper import Processor, World

from action import Action, ActionType
from constants import DijkstraMap
from ecs.components.boss import Boss
from ecs.components.defendtarget import DefendTarget
from ecs.components.firescroll import FireScroll
from ecs.components.healingpotion import HealingPotion
from ecs.components.inventory import Inventory
from ecs.components.item import Item
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.smokebomb import SmokeBomb
from ecs.components.taunted import Taunted
from ecs.components.teleportscroll import TeleportScroll
from ecs.components.visible import Visible
from ecs.processors.spatialprocessor import Coincident
from functions import move_dijkstra, color_item_name


class DefendAIProcessor(Processor):
    def process(self):
        self.world: World

        for _, game_map in self.world.get_component(Map):
            for player_entity, (player, player_position) in self.world.get_components(Player, Position):
                if self.world.has_component(player_entity, Taunted):
                    player.defend_action = player.attack_action
                    return

                if player.health < 9:
                    for entity, (item, _, _) in self.world.get_components(Item, Inventory, HealingPotion):
                        self.world.add_component(entity, DefendTarget())
                        player.defend_action = Action(
                            action_type=ActionType.USE_ITEM,
                            rage=-20,
                            nice_name=f"Use {color_item_name(self.world, entity)}",
                        )
                        return

                for _ in self.world.get_components(Monster, Visible):
                    target = move_dijkstra(self.world, game_map, player_position, DijkstraMap.MONSTER, reverse=True)

                    if target:
                        player.defend_action = Action(
                            action_type=ActionType.MOVE,
                            rage=-1,
                            target=target,
                            nice_name="Retreat",
                        )
                        return

                    for entity, (item, _, _) in self.world.get_components(Item, Inventory, FireScroll):
                        candidates = []
                        for monster_entity, (monster, _) in self.world.get_components(Monster, Visible):
                            if self.world.has_component(monster_entity, Boss):
                                continue

                            if monster.max_threat <= 0:
                                continue

                            candidates.append((monster.cur_threat, monster.max_threat, monster_entity, monster))

                        if candidates:
                            candidates.sort(reverse=True)
                            _, _, monster_entity, monster = candidates[0]
                            self.world.add_component(monster_entity, DefendTarget())
                            self.world.add_component(entity, DefendTarget())
                            player.defend_action = Action(
                                action_type=ActionType.USE_ITEM,
                                rage=-20,
                                nice_name=f"Use {color_item_name(self.world, entity)}",
                            )
                            return

                    if player.actual_threat > 0:
                        for entity, (item, _, _) in self.world.get_components(Item, Inventory, SmokeBomb):
                            self.world.add_component(entity, DefendTarget())
                            player.defend_action = Action(
                                action_type=ActionType.USE_ITEM,
                                rage=-20,
                                nice_name=f"Use {color_item_name(self.world, entity)}",
                            )
                            return

                        for entity, (item, _, _) in self.world.get_components(Item, Inventory, TeleportScroll):
                            self.world.add_component(entity, DefendTarget())
                            player.defend_action = Action(
                                action_type=ActionType.USE_ITEM,
                                rage=-20,
                                nice_name=f"Use {color_item_name(self.world, entity)}",
                            )
                            return

                    player.defend_action = Action(
                        action_type=ActionType.WAIT,
                        rage=-1,
                        nice_name="Wait",
                    )
                    return

                for entity, (item, _) in self.world.get_components(Item, Coincident):
                    player.defend_action = Action(
                        action_type=ActionType.GET_ITEM,
                        rage=-1,
                        nice_name=f"Get {color_item_name(self.world, entity)}",
                    )
                    return

                target = move_dijkstra(self.world, game_map, player_position, DijkstraMap.ITEM)

                if target:
                    player.defend_action = Action(
                        action_type=ActionType.MOVE,
                        rage=-1,
                        target=target,
                        nice_name="Gather items",
                    )
                    return

                target = move_dijkstra(self.world, game_map, player_position, DijkstraMap.EXPLORE)

                if target:
                    player.defend_action = Action(
                        action_type=ActionType.MOVE,
                        rage=-1,
                        target=target,
                        nice_name="Explore",
                    )
                    return

                player.defend_action = Action(
                    action_type=ActionType.WAIT,
                    rage=-1,
                    nice_name="Wait",
                )
