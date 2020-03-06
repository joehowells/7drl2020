from random import randint

from esper import Processor, World

from action import ActionType
from ecs.components.blinded import Blinded
from ecs.components.defendtarget import DefendTarget
from ecs.components.healingpotion import HealingPotion
from ecs.components.item import Item
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.smokebomb import SmokeBomb
from ecs.components.teleportscroll import TeleportScroll
from ecs.components.thunderscroll import ThunderScroll
from ecs.components.visible import Visible
from functions import move, get_blocked_tiles, color_item_name


class UseItemProcessor(Processor):
    def process(self):
        self.world: World

        player_entity, player = next(iter(self.world.get_component(Player)))
        blocked = get_blocked_tiles(self.world)

        if player.action.action_type is ActionType.USE_ITEM:
            for entity, (item, _) in self.world.get_components(Item, DefendTarget):
                self.world.create_entity(Message(
                    text=f"You use the {color_item_name(self.world, entity)}.",
                ))

                if self.world.has_component(entity, HealingPotion):
                    player.health = min(player.health + 2, 10)

                if self.world.has_component(entity, SmokeBomb):
                    for monster_entity, _ in self.world.get_components(Monster, Visible):
                        self.world.add_component(monster_entity, Blinded())

                if self.world.has_component(entity, ThunderScroll):
                    for monster_entity, (monster, _) in self.world.get_components(Monster, DefendTarget):
                        self.world.delete_entity(monster_entity, immediate=True)
                        self.world.create_entity(Message(
                            text=f"[color=#FF00FFFF]You incinerate the {monster.name}![/color]",
                        ))
                        player.kills[monster.name] += 1

                if self.world.has_component(entity, TeleportScroll):
                    _, game_map = next(iter(self.world.get_component(Map)))

                    for _ in range(1000):
                        x = randint(0, game_map.w - 1)
                        y = randint(0, game_map.h - 1)

                        if not game_map.walkable[y][x] or (x, y) in blocked:
                            continue

                        for position in self.world.try_component(player_entity, Position):
                            move(position, (x, y))
                            break

                        break

                    else:
                        self.world.create_entity(Message(
                            text=f"Your mind is elsewhere.",
                        ))

                self.world.delete_entity(entity, immediate=True)
