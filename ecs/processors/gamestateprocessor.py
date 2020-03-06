from dataclasses import dataclass
from typing import List, Type

from esper import Processor, World

from ecs.components.gamestate import GameState
from ecs.processors.angerprocessor import AngerProcessor
from ecs.processors.attackaiprocessor import AttackAIProcessor
from ecs.processors.playerattackprocessor import PlayerAttackProcessor
from ecs.processors.awakeprocessor import AwakeProcessor
from ecs.processors.blindedprocessor import BlindedProcessor
from ecs.processors.cleanuptargetsprocessor import CleanupTargetsProcessor
from ecs.processors.defendaiprocessor import DefendAIProcessor
from ecs.processors.exploremapprocessor import ExploreMapProcessor
from ecs.processors.getitemprocessor import GetItemProcessor
from ecs.processors.itemmapprocessor import ItemMapProcessor
from ecs.processors.monsterattackprocessor import MonsterAttackProcessor
from ecs.processors.monstermapprocessor import MonsterMapProcessor
from ecs.processors.monsterprocessor import MonsterProcessor
from ecs.processors.moveprocessor import MoveProcessor
from ecs.processors.playermapprocessor import PlayerMapProcessor
from ecs.processors.spatialprocessor import SpatialProcessor
from ecs.processors.stairmapprocessor import StairMapProcessor
from ecs.processors.tauntedprocessor import TauntedProcessor
from ecs.processors.threatprocessor import ThreatProcessor
from ecs.processors.trapprocessor import TrapProcessor
from ecs.processors.useitemprocessor import UseItemProcessor
from ecs.processors.usestairsprocessor import UseStairsProcessor
from ecs.processors.visibilityprocessor import VisibilityProcessor
from ecs.processors.fovprocessor import FOVProcessor
from factories.world import make_world

# Processors that run before user input
HI_PROCESSORS: List[Type[Processor]] = [
    BlindedProcessor,
    MonsterProcessor,
    MonsterAttackProcessor,
    TrapProcessor,

    FOVProcessor,
    VisibilityProcessor,
    AwakeProcessor,

    # Update player Dijkstra maps
    ExploreMapProcessor,
    ItemMapProcessor,
    MonsterMapProcessor,
    StairMapProcessor,

    SpatialProcessor,
    ThreatProcessor,
    TauntedProcessor,

    # Decide which options to give the player
    AttackAIProcessor,
    DefendAIProcessor,
]

# Processors that run after user input
LO_PROCESSORS: List[Type[Processor]] = [
    # Player actions
    UseStairsProcessor,
    UseItemProcessor,
    PlayerAttackProcessor,
    GetItemProcessor,
    MoveProcessor,

    # Update anger and combat bonuses
    AngerProcessor,

    # Update monster Dijkstra map
    PlayerMapProcessor,

    # Remove target components from all entities
    CleanupTargetsProcessor,
]


@dataclass
class GameStateProcessor(Processor):
    old_state: GameState = GameState.TITLE_SCREEN

    def process(self):
        self.world: World

        entity, state = next(iter(self.world.get_component(GameState)))

        if state is GameState.MAIN_GAME and self.old_state != GameState.MAIN_GAME:
            self.new_game()

        if state is GameState.TITLE_SCREEN and self.old_state != GameState.TITLE_SCREEN:
            self.world.clear_database()
            self.world.create_entity(state)
            self.end_game()

        self.old_state = state

    def new_game(self):
        self.world: World

        for processor in HI_PROCESSORS:
            self.world.add_processor(processor(), priority=40)

        for processor in LO_PROCESSORS:
            self.world.add_processor(processor(), priority=10)

        entities = make_world()

        for entity in entities:
            self.world.create_entity(*entity)

    # noinspection PyTypeChecker
    def end_game(self):
        self.world: World

        for processor in HI_PROCESSORS:
            self.world.remove_processor(processor)

        for processor in LO_PROCESSORS:
            self.world.remove_processor(processor)
