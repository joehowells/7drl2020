from esper import Processor, World

import script
from ecs.components.message import Message
from ecs.components.player import Player
from ecs.components.taunted import Taunted


class TauntedProcessor(Processor):
    """Handles the Taunted player status effect."""

    def process(self):
        self.world: World

        for entity, (player, taunted) in self.world.get_components(Player, Taunted):
            if taunted.turns_left <= 0:
                self.world.remove_component(entity, Taunted)
                self.world.create_entity(Message(
                    text=script.STATUS_RAGE_END,
                    priority=25,
                ))
            else:
                taunted.turns_left -= 1
                self.world.create_entity(Message(
                    text=script.STATUS_RAGE_CONTINUE,
                    priority=25,
                ))
