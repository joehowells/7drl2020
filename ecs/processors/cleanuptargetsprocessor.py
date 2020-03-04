from esper import Processor, World

from ecs.components.targeted import Targeted


class CleanupTargetsProcessor(Processor):
    def process(self):
        self.world: World

        for entity, _ in self.world.get_component(Targeted):
            self.world.remove_component(entity, Targeted)
