from enum import Enum, auto

from esper import Processor

from constants import DijkstraMap
from ecs.components.event import Event
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.eventmixin import EventMixin
from functions import dijkstra_map, iter_neighbors


class AttackMode(Enum):
    ATTACK_MONSTER = auto()
    EXPLORE = auto()
    FIND_STAIRCASE = auto()


class AttackAIProcessor(Processor, EventMixin):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, (player, player_position) = next(iter(self.world.get_components(Player, Position)))

        neighbors = set(iter_neighbors(player_position.x, player_position.y, game_map))

        sources = set()
        adjacent_entities = []

        for entity, (position, _) in self.world.get_components(Position, Monster):
            if game_map.visible[position.y][position.x]:
                sources.add((position.x, position.y))

                if (position.x, position.y) in neighbors:
                    adjacent_entities.append(entity)

        if adjacent_entities:
            self.world.delete_entity(adjacent_entities[0])
            position = self.world.component_for_entity(adjacent_entities[0], Position)
            game_map.blocked[position.y][position.x] = False
            self.set_event(Event("attack", {}))
            player.attack_action = Event("attack", {})

        elif sources:
            game_map.dijkstra[DijkstraMap.MONSTER] = dijkstra_map(game_map, sources)
            player.attack_action = Event("move", {"dijkstra": DijkstraMap.MONSTER})

        elif not game_map.done_exploring:
            player.attack_action = Event("move", {"dijkstra": DijkstraMap.EXPLORE})

        else:
            player.attack_action = Event("move", {"dijkstra": DijkstraMap.STAIRS})
