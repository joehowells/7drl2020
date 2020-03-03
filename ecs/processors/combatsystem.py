from esper import Processor

from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.monster import Monster
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
            monster = self.world.component_for_entity(entity, Monster)

            if player.attack > monster.defend:
                monster.health -= 1
                if monster.health <= 0:
                    position = self.world.component_for_entity(entity, Position)
                    self.world.delete_entity(entity)
                    game_map.blocked[position.y][position.x] = False

                    self.world.create_entity(Message(f"You kill the {monster.name}!", 0xFF00FFFF))
                else:
                    self.world.create_entity(Message(f"You hit the {monster.name}."))
            else:
                self.world.create_entity(Message(
                    text=f"The {monster.name} blocks. ({player.attack}/{monster.defend}).",
                    color=0xFF666666,
                ))