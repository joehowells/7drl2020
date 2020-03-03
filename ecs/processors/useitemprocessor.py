from esper import Processor, World

from ecs.components.item import Item
from ecs.components.message import Message
from ecs.components.player import Player
from ecs.components.targeted import Targeted


class UseItemProcessor(Processor):
    def process(self):
        self.world: World

        _, player = next(iter(self.world.get_component(Player)))

        event = player.action

        if event and event.name == "use":
            for entity, (item, _) in self.world.get_components(Item, Targeted):
                player.health = min(player.health + 5, 10)
                self.world.delete_entity(entity)

                self.world.create_entity(Message(
                    text=f"You use the {item.name}.",
                    color=0xFF00FFFF,
                ))
