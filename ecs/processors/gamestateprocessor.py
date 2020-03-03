from dataclasses import dataclass

from esper import Processor, World

from ecs.components.gamestate import GameState
from ecs.processors.angerprocessor import AngerProcessor
from ecs.processors.attackaiprocessor import AttackAIProcessor
from ecs.processors.awakeprocessor import AwakeProcessor
from ecs.processors.combatsystem import CombatProcessor
from ecs.processors.defendaiprocessor import DefendAIProcessor
from ecs.processors.exploremapprocessor import ExploreMapProcessor
from ecs.processors.itemmapprocessor import ItemMapProcessor
from ecs.processors.getitemprocessor import GetItemProcessor
from ecs.processors.monstermapprocessor import MonsterMapProcessor
from ecs.processors.monsterprocessor import MonsterProcessor
from ecs.processors.movementprocessor import MovementProcessor
from ecs.processors.playermapprocessor import PlayerMapProcessor
from ecs.processors.spatialprocessor import SpatialProcessor
from ecs.processors.stairmapprocessor import StairMapProcessor
from ecs.processors.stairprocessor import StairProcessor
from ecs.processors.threatprocessor import ThreatProcessor
from ecs.processors.trapprocessor import TrapProcessor
from ecs.processors.useitemprocessor import UseItemProcessor
from ecs.processors.visibilityprocessor import VisibilityProcessor
from ecs.processors.visionprocessor import VisionProcessor
from factories.world import make_world


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

        self.world.add_processor(StairProcessor())
        self.world.add_processor(UseItemProcessor())
        self.world.add_processor(CombatProcessor())
        self.world.add_processor(GetItemProcessor())
        self.world.add_processor(MovementProcessor())

        self.world.add_processor(AngerProcessor())
        self.world.add_processor(PlayerMapProcessor())

        self.world.add_processor(MonsterProcessor())
        self.world.add_processor(ThreatProcessor())
        self.world.add_processor(TrapProcessor())

        self.world.add_processor(VisionProcessor())
        self.world.add_processor(VisibilityProcessor())
        self.world.add_processor(AwakeProcessor())

        # Update player Dijkstra maps
        self.world.add_processor(ExploreMapProcessor())
        self.world.add_processor(ItemMapProcessor())
        self.world.add_processor(MonsterMapProcessor())
        self.world.add_processor(StairMapProcessor())

        self.world.add_processor(SpatialProcessor())

        # Decide which options to give the player
        self.world.add_processor(AttackAIProcessor())
        self.world.add_processor(DefendAIProcessor())

        entities = make_world()

        for entity in entities:
            self.world.create_entity(*entity)

    # noinspection PyTypeChecker
    def end_game(self):
        self.world: World

        self.world.remove_processor(StairProcessor)
        self.world.remove_processor(UseItemProcessor)
        self.world.remove_processor(CombatProcessor)
        self.world.remove_processor(GetItemProcessor)
        self.world.remove_processor(MovementProcessor)

        self.world.remove_processor(AngerProcessor)
        self.world.remove_processor(PlayerMapProcessor)

        self.world.remove_processor(MonsterProcessor)
        self.world.remove_processor(ThreatProcessor)
        self.world.remove_processor(TrapProcessor)

        self.world.remove_processor(VisionProcessor)
        self.world.remove_processor(VisibilityProcessor)
        self.world.remove_processor(AwakeProcessor)

        # Update player Dijkstra maps
        self.world.remove_processor(ExploreMapProcessor)
        self.world.remove_processor(ItemMapProcessor)
        self.world.remove_processor(MonsterMapProcessor)
        self.world.remove_processor(StairMapProcessor)

        self.world.remove_processor(SpatialProcessor)

        # Decide which options to give the player
        self.world.remove_processor(AttackAIProcessor)
        self.world.remove_processor(DefendAIProcessor)
