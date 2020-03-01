from enum import Enum, auto

from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.event import Event
from ecs.processor import Processor
from functions import dijkstra_map, iter_neighbors


class AttackMode(Enum):
    ATTACK_MONSTER = auto()
    EXPLORE = auto()
    FIND_STAIRCASE = auto()


class AttackAIProcessor(Processor):
    def process(self):
        pass

    def event_attack_ai(self, event):
        _, map_ = next(iter(self.world.get_component(Map)))
        _, (_, player_position) = next(iter(self.world.get_components(Player, Position)))

        neighbors = set(iter_neighbors(player_position.x, player_position.y, map_))

        sources = set()
        adjacent_entities = []

        for entity, (position, _) in self.world.get_components(Position, Monster):
            if map_.visible[position.y][position.x]:
                sources.add((position.x, position.y))

                if (position.x, position.y) in neighbors:
                    adjacent_entities.append(entity)

        if adjacent_entities:
            self.world.delete_entity(adjacent_entities[0])
            return

        if sources:
            map_.dijkstra["enemy"] = dijkstra_map(map_, sources)
            self.event(Event("move", {"dijkstra": "enemy"}))
            return

        self.event(Event("move", {"dijkstra": "auto_explore"}))
