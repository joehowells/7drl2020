from esper import Processor

from ecs.components.message import Message
from ecs.components.player import Player
from factories.world import make_world


class StairProcessor(Processor):
    def process(self):
        entity, player = next(iter(self.world.get_component(Player)))
        event = player.action

        if event and event.name == "stairs":
            self.world.clear_database()

            entities = make_world()
            for entity in entities:
                self.world.create_entity(*entity)

            self.world.create_entity(Message("You go downstairs."))
