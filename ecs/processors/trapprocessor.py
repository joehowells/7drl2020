from esper import Processor, World

import script
from action import ActionType
from ecs.components.awake import Awake
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.trap import Trap
from ecs.components.visible import Visible
from factories.monsters import get_monster_factory
from functions import get_blocked_tiles


class TrapProcessor(Processor):
    def process(self):
        self.world: World

        for _, game_map in self.world.get_component(Map):
            for _, player in self.world.get_component(Player):
                blocked = get_blocked_tiles(self.world)

                if player.action.action_type is ActionType.ATTACK:
                    trap_activated = False
                    for entity, (trap, position, _) in self.world.get_components(Trap, Position, Visible):
                        if (position.x, position.y) not in blocked:
                            trap_activated = True
                            factory = get_monster_factory(player.level)
                            components = factory(position.x, position.y)
                            components.extend([
                                Visible(),
                                Awake(),
                                LastKnownPosition(position.x, position.y),
                            ])
                            self.world.create_entity(*components)
                            self.world.delete_entity(entity)

                    if trap_activated:
                        self.world.create_entity(Message(
                            text=script.TRAP,
                            priority=30,
                        ))
