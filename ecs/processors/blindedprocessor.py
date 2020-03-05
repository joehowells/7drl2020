from esper import Processor, World

from ecs.components.blinded import Blinded


class BlindedProcessor(Processor):
    """Handles the blinded status effect."""

    def process(self):
        self.world: World

        for entity, blinded in self.world.get_component(Blinded):
            blinded.turns_left -= 1

            if blinded.turns_left <= 0:
                self.world.remove_component(entity, Blinded)
