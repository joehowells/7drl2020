from esper import Processor

from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position


class CombatProcessor(Processor):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, (position, player) = next(iter(self.world.get_components(Position, Player)))

        event = player.action

        if not event:
            return

        if event.name == "attack":
            entity = event.data["target"]
            position = self.world.component_for_entity(entity, Position)
            self.world.delete_entity(entity)
            game_map.blocked[position.y][position.x] = False
