from random import randint, choices

from esper import Processor

from constants import DijkstraMap
from ecs.components.assassin import Assassin
from ecs.components.blinded import Blinded
from ecs.components.dead import Dead
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.threatening import Threatening
from ecs.components.visible import Visible


class ThreatProcessor(Processor):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        player_entity, player = next(iter(self.world.get_component(Player)))

        player.visible_threat = 0
        player.actual_threat = 0

        monsters = []
        weights = []

        for entity, (monster, visible, position) in self.world.get_components(Monster, Visible, Position):
            if self.world.has_component(entity, Blinded):
                continue

            if not self.world.has_component(entity, Assassin):
                threat = max(0, max(monster.threat) - player.defend)
                player.visible_threat += threat

            distance = game_map.dijkstra[DijkstraMap.PLAYER][position.y][position.x]
            if 1 <= distance <= len(monster.threat):
                threat = monster.threat[distance - 1]
                threat = max(0, threat - player.defend)
                player.actual_threat += threat

            for threatening in self.world.try_component(entity, Threatening):
                threat = max(0, threatening.threat - player.defend)
                monsters.append(monster)
                weights.append(threat)

        player.visible_threat = min(max(player.visible_threat, 0), 20)
        player.actual_threat = min(max(player.actual_threat, 0), 20)

        if not monsters or not weights:
            return

        monster = choices(monsters, weights)[0]

        if randint(0, 19) < player.actual_threat:
            self.world.create_entity(Message(
                text=f"[color=#FFFFFF00]The {monster.name} hits![/color]",
            ))

            player.health -= 1

            if player.health <= 0:
                player.killer = f"{monster.article} {monster.name}"
                self.world.add_component(player_entity, Dead())
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
            ))
