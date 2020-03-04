from enum import Enum, auto

from esper import Processor

from action import Action, ActionType
from constants import DijkstraMap
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.stairs import Stairs
from ecs.components.targeted import Targeted
from ecs.processors.spatialprocessor import Adjacent, Coincident
from functions import move_dijkstra


class AttackMode(Enum):
    ATTACK_MONSTER = auto()
    EXPLORE = auto()
    FIND_STAIRCASE = auto()


class AttackAIProcessor(Processor):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, (player, player_position) = next(iter(self.world.get_components(Player, Position)))

        strong_entities = []
        weak_entities = []

        for entity, (position, monster, _) in self.world.get_components(Position, Monster, Adjacent):
            if player.attack <= monster.defend:
                strong_entities.append(entity)
            else:
                weak_entities.append((-monster.threat[0], monster.health, entity, monster))

        # Attack something we can actually damage
        if weak_entities:
            weak_entities.sort()
            _, _, entity, monster = weak_entities[0]
            self.world.add_component(entity, Targeted())
            player.attack_action = Action(
                action_type=ActionType.ATTACK,
                anger=+2,
                nice_name=f"Attack {monster.name}",
            )
            return

        # Attack a strong enemy to build meter
        if strong_entities:
            target = strong_entities[0]
            self.world.add_component(target, Targeted())
            player.attack_action = Action(
                action_type=ActionType.ATTACK,
                anger=+2,
                nice_name=f"Attack {monster.name}",
            )
            return

        target = move_dijkstra(game_map, player_position, DijkstraMap.MONSTER)

        if target:
            player.attack_action = Action(
                action_type=ActionType.MOVE,
                anger=+1,
                target=target,
                nice_name="Charge",
            )
            return

        target = move_dijkstra(game_map, player_position, DijkstraMap.EXPLORE)

        if target:
            player.attack_action = Action(
                action_type=ActionType.MOVE,
                anger=-1,
                target=target,
                nice_name="Explore",
            )
            return

        for entity, (position, _, _) in self.world.get_components(Position, Stairs, Coincident):
            player.attack_action = Action(
                action_type=ActionType.USE_STAIRS,
                anger=-1,
                target=target,
                nice_name="Use stairs",
            )
            return

        target = move_dijkstra(game_map, player_position, DijkstraMap.STAIRS)

        if target:
            player.attack_action = Action(
                action_type=ActionType.MOVE,
                anger=-1,
                target=target,
                nice_name="Find stairs",
            )
            return

        player.attack_action = Action(
            action_type=ActionType.WAIT,
            anger=-1,
            nice_name="Wait",
        )
