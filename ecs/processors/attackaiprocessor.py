from enum import Enum, auto

from esper import Processor

from action import Action, ActionType
from constants import DijkstraMap
from ecs.components.attacktarget import AttackTarget
from ecs.components.boss import Boss
from ecs.components.map import Map
from ecs.components.monster import Monster
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.stairs import Stairs
from ecs.processors.spatialprocessor import Adjacent, Coincident
from functions import move_dijkstra


class AttackMode(Enum):
    ATTACK_MONSTER = auto()
    EXPLORE = auto()
    FIND_STAIRCASE = auto()


class AttackAIProcessor(Processor):
    def process(self):
        for _, game_map in self.world.get_component(Map):
            for _, (player, player_position) in self.world.get_components(Player, Position):
                entities = []
                for entity, (monster, _) in self.world.get_components(Monster, Adjacent):
                    entities.append((monster.threat, entity, monster))

                if entities:
                    entities.sort(reverse=True)

                    name = None
                    for _, entity, monster in entities[:player.number_of_attacks]:
                        self.world.add_component(entity, AttackTarget())
                        if name is None:
                            name = monster.name
                        else:
                            name = "multiple enemies"

                    player.attack_action = Action(
                        action_type=ActionType.ATTACK,
                        rage=+2,
                        nice_name=f"Attack {name}",
                    )
                    return

                target = move_dijkstra(self.world, game_map, player_position, DijkstraMap.MONSTER)

                if target:
                    player.attack_action = Action(
                        action_type=ActionType.MOVE,
                        rage=+1,
                        target=target,
                        nice_name="Charge",
                    )
                    return

                for _, (_, monster) in self.world.get_components(Boss, Monster):
                    target = move_dijkstra(self.world, game_map, player_position, DijkstraMap.EXPLORE)

                    if target:
                        player.attack_action = Action(
                            action_type=ActionType.MOVE,
                            rage=-1,
                            target=target,
                            nice_name=f"Find {monster.name}",
                        )
                        return

                for entity, (position, _, _) in self.world.get_components(Position, Stairs, Coincident):
                    player.attack_action = Action(
                        action_type=ActionType.USE_STAIRS,
                        rage=-1,
                        target=target,
                        nice_name="Use stairs",
                    )
                    return

                target = move_dijkstra(self.world, game_map, player_position, DijkstraMap.STAIRS)

                if target:
                    player.attack_action = Action(
                        action_type=ActionType.MOVE,
                        rage=-1,
                        target=target,
                        nice_name="Find stairs",
                    )
                    return

                target = move_dijkstra(self.world, game_map, player_position, DijkstraMap.EXPLORE)

                if target:
                    player.attack_action = Action(
                        action_type=ActionType.MOVE,
                        rage=-1,
                        target=target,
                        nice_name="Explore",
                    )
                    return

                player.attack_action = Action(
                    action_type=ActionType.WAIT,
                    rage=-1,
                    nice_name="Wait",
                )
