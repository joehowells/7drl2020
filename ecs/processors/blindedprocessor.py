from esper import Processor, World

from ecs.components.blinded import Blinded
from ecs.components.message import Message
from ecs.components.monster import Monster


class BlindedProcessor(Processor):
    """Handles the Blinded monster status effect."""

    def process(self):
        self.world: World

        for entity, (monster, blinded) in self.world.get_components(Monster, Blinded):
            if blinded.turns_left <= 0:
                self.world.remove_component(entity, Blinded)
            else:
                blinded.turns_left -= 1
                self.world.create_entity(Message(
                    text=f"[color=#FF666666]The {monster.name} is blinded by smoke.[/color]",
                    priority=45,
                ))
