from random import randint

from esper import Processor, World

from action import ActionType
from ecs.components.blinded import Blinded
from ecs.components.blinkscroll import BlinkScroll
from ecs.components.healingpotion import HealingPotion
from ecs.components.item import Item
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.smokebomb import SmokeBomb
from ecs.components.targeted import Targeted
from ecs.components.teleportscroll import TeleportScroll
from ecs.components.visible import Visible
from functions import move, get_blocked_tiles


class UseItemProcessor(Processor):
    def process(self):
        self.world: World

        player_entity, player = next(iter(self.world.get_component(Player)))
        blocked = get_blocked_tiles(self.world)

        if player.action.action_type is ActionType.USE_ITEM:
            for entity, (item, _) in self.world.get_components(Item, Targeted):
                self.world.create_entity(Message(
                    text=f"You use the {item.name}.",
                    color=0xFF00FFFF,
                ))

                if self.world.has_component(entity, HealingPotion):
                    player.health = min(player.health + 2, 10)

                if self.world.has_component(entity, SmokeBomb):
                    for monster_entity, _ in self.world.get_components(Monster, Visible):
                        self.world.add_component(monster_entity, Blinded())

                if self.world.has_component(entity, BlinkScroll):
                    _, game_map = next(iter(self.world.get_component(Map)))

                    for _ in range(1000):
                        x = randint(0, game_map.w - 1)
                        y = randint(0, game_map.h - 1)

                        if not game_map.walkable[y][x] or (x, y) in blocked or not game_map.visible[y][x]:
                            continue

                        for position in self.world.try_component(player_entity, Position):
                            move(position, (x, y))
                            break

                        break

                    else:
                        self.world.create_entity(Message(
                            text=f"Your mind is elsewhere.",
                            color=0xFFFFFFFF,
                        ))

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
                            color=0xFFFFFFFF,
                        ))

                self.world.delete_entity(entity, immediate=True)
