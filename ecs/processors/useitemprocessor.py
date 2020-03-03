from esper import Processor, World

from ecs.components.item import Item
from ecs.components.message import Message
from ecs.components.player import Player


class UseItemProcessor(Processor):
    def process(self):
        self.world: World

        _, player = next(iter(self.world.get_component(Player)))

        event = player.action

        if not event:
            return

        if event.name == "use":
            player.health = min(player.health + 5, 10)
            self.world.delete_entity(event.data["item"])
            item = self.world.component_for_entity(event.data["item"], Item)
            self.world.create_entity(Message(
                text=f"You use the {item.name}.",
                color=0xFF00FFFF,
            ))
