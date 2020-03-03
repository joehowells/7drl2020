from enum import Enum, auto

from esper import Processor

from constants import DijkstraMap
from ecs.components.event import Event
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.staircase import Staircase
from ecs.components.targeted import Targeted
from ecs.eventmixin import EventMixin
from functions import dijkstra_map, iter_neighbors, move_dijkstra


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
        strong_entities = []
        weak_entities = []

        for entity, (position, monster) in self.world.get_components(Position, Monster):
            if game_map.visible[position.y][position.x]:
                sources.add((position.x, position.y))

                if (position.x, position.y) in neighbors:
                    if player.attack <= monster.defend:
                        strong_entities.append(entity)
                    else:
                        weak_entities.append((-monster.threat[0], monster.health, entity))

        # Attack something we can actually damage
        if weak_entities:
            weak_entities.sort()
            target = weak_entities[0][-1]
            self.world.add_component(target, Targeted())
            player.attack_action = Event("attack", {"target": target, "anger": 2})
            return

        # Attack a strong enemy to build meter
        if strong_entities:
            target = strong_entities[0]
            self.world.add_component(target, Targeted())
            player.attack_action = Event("attack", {"target": target, "anger": 2})
            return

        elif sources:
            game_map.dijkstra[DijkstraMap.MONSTER] = dijkstra_map(game_map, sources)
            target = move_dijkstra(game_map, player_position, DijkstraMap.MONSTER)

            if target:
                player.attack_action = Event("move", {"target": target, "anger": 1})
                return

        elif not game_map.done_exploring:
            target = move_dijkstra(game_map, player_position, DijkstraMap.EXPLORE)

            if target:
                player.attack_action = Event("move", {"target": target, "anger": -1})
                return

        else:
            for entity, (position, _) in self.world.get_components(Position, Staircase):
                if position.x == player_position.x and position.y == player_position.y:
                    player.attack_action = Event("stairs", {})
                    break
            else:
                target = move_dijkstra(game_map, player_position, DijkstraMap.STAIRS)

                if target:
                    player.attack_action = Event("move", {"target": target, "anger": -1})
                    return
