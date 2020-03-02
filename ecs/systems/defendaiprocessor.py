from esper import Processor

from constants import DijkstraMap
from ecs.components.event import Event
from ecs.components.item import Item
from ecs.components.player import Player
from ecs.components.position import Position


class DefendAIProcessor(Processor):
    def process(self):
        _, (player, player_position) = next(iter(self.world.get_components(Player, Position)))

        for entity, (position, _) in self.world.get_components(Position, Item):
            if position.x == player_position.x and position.y == player_position.y:
                player.defend_action = Event("pickup", {"item": entity, "anger": -1})
                break
        else:
            player.defend_action = Event("move", {"dijkstra": DijkstraMap.ITEM, "anger": -1})
