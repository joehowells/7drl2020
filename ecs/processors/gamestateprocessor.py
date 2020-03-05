from dataclasses import dataclass
from typing import List, Type

from esper import Processor, World

from ecs.components.gamestate import GameState
from ecs.processors.angerprocessor import AngerProcessor
from ecs.processors.attackaiprocessor import AttackAIProcessor
from ecs.processors.attackprocessor import AttackProcessor
from ecs.processors.awakeprocessor import AwakeProcessor
from ecs.processors.blindedprocessor import BlindedProcessor
from ecs.processors.cleanuptargetsprocessor import CleanupTargetsProcessor
from ecs.processors.defendaiprocessor import DefendAIProcessor
from ecs.processors.exploremapprocessor import ExploreMapProcessor
from ecs.processors.getitemprocessor import GetItemProcessor
from ecs.processors.itemmapprocessor import ItemMapProcessor
from ecs.processors.monstermapprocessor import MonsterMapProcessor
from ecs.processors.monsterprocessor import MonsterProcessor
from ecs.processors.moveprocessor import MoveProcessor
from ecs.processors.playermapprocessor import PlayerMapProcessor
from ecs.processors.spatialprocessor import SpatialProcessor
from ecs.processors.stairmapprocessor import StairMapProcessor
from ecs.processors.threatprocessor import ThreatProcessor
from ecs.processors.trapprocessor import TrapProcessor
from ecs.processors.useitemprocessor import UseItemProcessor
from ecs.processors.usestairsprocessor import UseStairsProcessor
from ecs.processors.visibilityprocessor import VisibilityProcessor
from ecs.processors.visionprocessor import VisionProcessor
from factories.world import make_world

PROCESSORS: List[Type[Processor]] = [
    UseStairsProcessor,
    UseItemProcessor,
    AttackProcessor,
    GetItemProcessor,
    MoveProcessor,

    AngerProcessor,
    PlayerMapProcessor,

    BlindedProcessor,
    MonsterProcessor,
    ThreatProcessor,
    TrapProcessor,

    VisionProcessor,
    VisibilityProcessor,
    AwakeProcessor,

    # Update player Dijkstra maps
    ExploreMapProcessor,
    ItemMapProcessor,
    MonsterMapProcessor,
    StairMapProcessor,

    SpatialProcessor,

    # Decide which options to give the player
    CleanupTargetsProcessor,
    AttackAIProcessor,
    DefendAIProcessor,
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

        for processor in PROCESSORS:
            self.world.add_processor(processor())

        entities = make_world()

        for entity in entities:
            self.world.create_entity(*entity)

    def end_game(self):
        self.world: World

        for processor in PROCESSORS:
            # noinspection PyTypeChecker
            self.world.remove_processor(processor)
