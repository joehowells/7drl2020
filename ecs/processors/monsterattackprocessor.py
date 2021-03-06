from random import choices, randint

from esper import Processor, World

import script
from ecs.components.dead import Dead
from ecs.components.message import Message
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.threatening import Threatening


class MonsterAttackProcessor(Processor):
    def process(self):
        self.world: World

        for entity, player in self.world.get_component(Player):
            monsters = []
            weights = []

            for _, (monster, threatening) in self.world.get_components(Monster, Threatening):
                threat = max(0, threatening.threat - player.defend)
                monsters.append(monster)
                weights.append(threat)

            if not monsters or not weights:
                return

            monster = choices(monsters, weights)[0]

            if randint(0, 19) < sum(weights):
                self.world.create_entity(Message(
                    text=script.MONSTER_HIT.format(name=monster.name),
                    priority=40,
                ))

                player.health -= 1

                if player.health <= 0:
                    player.killer = f"{monster.article} {monster.name}"
                    self.world.add_component(entity, Dead())
                    self.world.create_entity(Message(
                        text=script.MONSTER_KILL,
                        priority=-100,
                    ))
                    self.world.create_entity(Message(
                        text=script.GAME_OVER,
                        priority=-200,
                    ))

            else:
                self.world.create_entity(Message(
                    text=script.MONSTER_MISS.format(name=monster.name),
                    priority=40,
                ))
