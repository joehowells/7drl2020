from enum import Enum, auto

from esper import Processor

from constants import DijkstraMap
from ecs.components.event import Event
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.stair import Stair
from ecs.components.targeted import Targeted
from ecs.eventmixin import EventMixin
from ecs.processors.spatialprocessor import Adjacent, Coincident
from functions import move_dijkstra


class AttackMode(Enum):
    ATTACK_MONSTER = auto()
    EXPLORE = auto()
    FIND_STAIRCASE = auto()


class AttackAIProcessor(Processor, EventMixin):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, (player, player_position) = next(iter(self.world.get_components(Player, Position)))

        strong_entities = []
        weak_entities = []

        for entity, (position, monster, _) in self.world.get_components(Position, Monster, Adjacent):
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

        target = move_dijkstra(game_map, player_position, DijkstraMap.MONSTER)

        if target:
            player.attack_action = Event("move", {"target": target, "anger": 1})
            return

        target = move_dijkstra(game_map, player_position, DijkstraMap.EXPLORE)

        if target:
            player.attack_action = Event("move", {"target": target, "anger": -1})
            return

        for entity, (position, _, _) in self.world.get_components(Position, Stair, Coincident):
            player.attack_action = Event("stairs", {})
            return

        target = move_dijkstra(game_map, player_position, DijkstraMap.STAIRS)

        if target:
            player.attack_action = Event("move", {"target": target, "anger": -1})
            return

        player.attack_action = Event("wait", {"anger": -1})
