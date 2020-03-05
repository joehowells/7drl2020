from esper import Processor, World

from ecs.components.attacktarget import AttackTarget
from ecs.components.defendtarget import DefendTarget


class CleanupTargetsProcessor(Processor):
    def process(self):
        self.world: World

        for entity, _ in self.world.get_component(AttackTarget):
            self.world.remove_component(entity, AttackTarget)

        for entity, _ in self.world.get_component(DefendTarget):
            self.world.remove_component(entity, DefendTarget)
