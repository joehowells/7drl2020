from esper import Processor, World

from action import ActionType
from ecs.components.gamestate import GameState
from ecs.components.inventory import Inventory
from ecs.components.item import Item
from ecs.components.message import Message
from ecs.components.player import Player
from factories.world import make_world


class UseStairsProcessor(Processor):
    def process(self):
        self.world: World

        entity, player = next(iter(self.world.get_component(Player)))

        if player.action.action_type is ActionType.USE_STAIRS:
            entities = make_world(player=player)

            for entity, _ in self.world.get_component(GameState):
                # noinspection PyTypeChecker
                entities.append(self.world.components_for_entity(entity))

            for entity, _ in self.world.get_components(Item, Inventory):
                # noinspection PyTypeChecker
                entities.append(self.world.components_for_entity(entity))

            self.world.clear_database()
            for entity in entities:
                self.world.create_entity(*entity)

            self.world.create_entity(Message("You go downstairs."))
