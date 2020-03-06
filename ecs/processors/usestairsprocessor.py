from typing import List, Collection, Any

from esper import Processor, World

import script
from action import ActionType
from constants import MAX_LEVEL
from ecs.components.dead import Dead
from ecs.components.gamestate import GameState
from ecs.components.inventory import Inventory
from ecs.components.item import Item
from ecs.components.message import Message
from ecs.components.player import Player
from factories.world import make_world


class UseStairsProcessor(Processor):
    def process(self):
        self.world: World

        for player_entity, player in self.world.get_component(Player):
            if player.action.action_type is ActionType.USE_STAIRS:
                if player.level >= MAX_LEVEL:
                    self.world.add_component(player_entity, Dead())
                    self.world.create_entity(Message(text=script.GAME_COMPLETE, priority=-100))
                    self.world.create_entity(Message(text=script.GAME_OVER, priority=-200))
                else:
                    player.level += 1
                    entities: List[Collection[Any]] = make_world(player=player, level=player.level)

                    for entity, _ in self.world.get_component(GameState):
                        entities.append(self.world.components_for_entity(entity))

                    for entity, _ in self.world.get_components(Item, Inventory):
                        entities.append(self.world.components_for_entity(entity))

                    self.world.clear_database()
                    for entity in entities:
                        self.world.create_entity(*entity)

                    self.world.create_entity(Message(text=script.USE_STAIRS, priority=100))
