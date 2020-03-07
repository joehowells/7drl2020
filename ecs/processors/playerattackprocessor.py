from random import randint

from esper import Processor, World

import script
from action import ActionType
from ecs.components.attacktarget import AttackTarget
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position


class PlayerAttackProcessor(Processor):
    def process(self):
        self.world: World

        for _, game_map in self.world.get_component(Map):
            for _, (position, player) in self.world.get_components(Position, Player):
                if player.action.action_type is ActionType.ATTACK:
                    for entity, (monster, _) in self.world.get_components(Monster, AttackTarget):
                        self.world.remove_component(entity, AttackTarget)

                        if randint(0, monster.defend) < player.attack:
                            self.world.create_entity(Message(
                                text=script.PLAYER_HIT.format(name=monster.name),
                                priority=50,
                            ))

                            monster.health -= 1

                            if monster.health <= 0:
                                player.kills[monster.name] += 1
                                self.world.delete_entity(entity, immediate=True)
                                self.world.create_entity(Message(
                                    text=script.PLAYER_KILL.format(name=monster.name),
                                    priority=50,
                                ))

                        else:
                            self.world.create_entity(Message(
                                text=script.PLAYER_MISS.format(name=monster.name),
                                priority=50,
                            ))
