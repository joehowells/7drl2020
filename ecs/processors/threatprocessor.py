from esper import Processor

from constants import DijkstraMap
from ecs.components.assassin import Assassin
from ecs.components.blinded import Blinded
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.visible import Visible


class ThreatProcessor(Processor):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        player_entity, player = next(iter(self.world.get_component(Player)))

        player.visible_threat = 0
        player.actual_threat = 0

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

        player.visible_threat = min(max(player.visible_threat, 0), 20)
        player.actual_threat = min(max(player.actual_threat, 0), 20)
