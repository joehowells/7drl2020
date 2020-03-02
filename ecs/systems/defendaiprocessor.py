from esper import Processor

from constants import DijkstraMap
from ecs.components.event import Event
from ecs.components.player import Player


class DefendAIProcessor(Processor):
    def process(self):
        _, player, = next(iter(self.world.get_component(Player)))
        player.defend_action = Event("move", {"dijkstra": DijkstraMap.STAIRS, "anger": -2})
