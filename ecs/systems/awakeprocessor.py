from esper import Processor

from constants import DijkstraMap
from ecs.components.awake import Awake
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.position import Position
from ecs.components.visible import Visible
from ecs.eventmixin import EventMixin


class AwakeProcessor(Processor, EventMixin):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        event = self.get_event("attack")

        for entity, (_, position) in self.world.get_components(Monster, Position):
            if self.world.has_component(entity, Awake):
                if game_map.dijkstra[DijkstraMap.PLAYER][position.y][position.x] < 0:
                    self.world.remove_component(entity, Awake)
            else:
                if self.world.has_component(entity, Visible):
                    self.world.add_component(entity, Awake())

                if event and game_map.dijkstra[DijkstraMap.PLAYER][position.y][position.x] > 0:
                    self.world.add_component(entity, Awake())
