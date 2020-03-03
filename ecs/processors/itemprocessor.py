from esper import Processor

from ecs.components.inventory import Inventory
from ecs.components.item import Item
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.player import Player
from ecs.components.position import Position


class ItemProcessor(Processor):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, player = next(iter(self.world.get_component(Player)))

        event = player.action

        if event and event.name == "pickup":
            self.world.remove_component(event.data["item"], Position)
            self.world.remove_component(event.data["item"], LastKnownPosition)
            self.world.add_component(event.data["item"], Inventory())
            item = self.world.component_for_entity(event.data["item"], Item)
            self.world.create_entity(Message(f"You pick up the {item.name}."))
