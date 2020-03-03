from esper import Processor, World

from ecs.components.inventory import Inventory
from ecs.components.item import Item
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.message import Message
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.processors.spatialprocessor import Coincident


class GetItemProcessor(Processor):
    def process(self):
        self.world: World

        _, player = next(iter(self.world.get_component(Player)))

        event = player.action

        if event and event.name == "pickup":
            for entity, (item, _) in self.world.get_components(Item, Coincident):
                if self.world.has_component(entity, Position):
                    self.world.remove_component(entity, Position)
                if self.world.has_component(entity, LastKnownPosition):
                    self.world.remove_component(entity, LastKnownPosition)

                self.world.add_component(entity, Inventory())

                self.world.create_entity(Message(
                    text=f"You pick up the {item.name}."
                ))
