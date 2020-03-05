from esper import Processor, World

from action import ActionType
from ecs.components.awake import Awake
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.trap import Trap
from ecs.components.visible import Visible
from factories.entities import get_monster_factory
from functions import get_blocked_tiles


class TrapProcessor(Processor):
    def process(self):
        self.world: World

        _, game_map = next(iter(self.world.get_component(Map)))
        _, player = next(iter(self.world.get_component(Player)))
        blocked = get_blocked_tiles(self.world)

        if player.action.action_type is ActionType.ATTACK:
            sprung_trap = False
            for entity, (trap, position, _) in self.world.get_components(Trap, Position, Visible):
                sprung_trap = True

                if (position.x, position.y) not in blocked:
                    factory = get_monster_factory(player.level)
                    components = factory(position.x, position.y)
                    components.extend([
                        Visible(),
                        Awake(),
                        LastKnownPosition(position.x, position.y),
                    ])
                    self.world.create_entity(*components)
                    self.world.delete_entity(entity)

            if sprung_trap:
                self.world.create_entity(Message(
                    text=f"Enemies appear from the stairs!",
                    color=0xFFFFFF00,
                ))
