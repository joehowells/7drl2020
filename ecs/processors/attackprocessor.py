from esper import Processor, World

from action import ActionType
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.attacktarget import AttackTarget


class AttackProcessor(Processor):
    def process(self):
        self.world: World

        _, game_map = next(iter(self.world.get_component(Map)))
        _, (position, player) = next(iter(self.world.get_components(Position, Player)))

        if player.action.action_type is ActionType.ATTACK:
            for entity, (monster, _) in self.world.get_components(Monster, AttackTarget):
                self.world.remove_component(entity, AttackTarget)

                if player.attack > monster.defend:
                    monster.health -= 1
                    if monster.health <= 0:
                        self.world.delete_entity(entity)
                        self.world.create_entity(Message(f"You kill the {monster.name}!", 0xFF00FFFF))
                        player.kills[monster.name] += 1
                    else:
                        self.world.create_entity(Message(f"You hit the {monster.name}."))
                else:
                    self.world.create_entity(Message(
                        text=f"You miss the {monster.name}.",
                        color=0xFF666666,
                    ))
