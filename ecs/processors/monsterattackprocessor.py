from random import choices, randint

from esper import Processor, World

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
                    text=f"[color=#FFFFFF00]The {monster.name} hits![/color]",
                    priority=40,
                ))

                player.health -= 1

                if player.health <= 0:
                    player.killer = f"{monster.article} {monster.name}"
                    self.world.add_component(entity, Dead())
                    self.world.create_entity(Message(
                        text=f"You die...",
                        priority=-100,
                    ))
                    self.world.create_entity(Message(
                        text=f"Press [color=#FFFF0000](z)[/color] and [color=#FF0000FF](x)[/color] to continue...",
                        priority=-200,
                    ))

            else:
                self.world.create_entity(Message(
                    text=f"[color=#FF666666]The {monster.name} misses you.[/color]",
                    priority=40,
                ))
