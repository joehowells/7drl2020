from contextlib import contextmanager

from bearlibterminal import terminal
from esper import World

from ecs.processors.angerprocessor import AngerProcessor
from ecs.processors.attackaiprocessor import AttackAIProcessor
from ecs.processors.autoexploreprocessor import AutoExploreProcessor
from ecs.processors.awakeprocessor import AwakeProcessor
from ecs.processors.combatsystem import CombatProcessor
from ecs.processors.defendaiprocessor import DefendAIProcessor
from ecs.processors.displayprocessor import DisplayProcessor
from ecs.processors.inputprocessor import InputProcessor
from ecs.processors.itemprocessor import ItemProcessor
from ecs.processors.monsterprocessor import MonsterProcessor
from ecs.processors.movementprocessor import MovementProcessor
from ecs.processors.stairprocessor import StairProcessor
from ecs.processors.threatprocessor import ThreatProcessor
from ecs.processors.trapprocessor import TrapProcessor
from ecs.processors.visibilityprocessor import VisibilityProcessor
from ecs.processors.visionprocessor import VisionProcessor
from factories.world import make_world


@contextmanager
def terminal_context():
    terminal.open()
    terminal.set("""
    font: UbuntuMono-R.ttf, size=12;
    window.size=67x21;
    """)
    yield
    terminal.close()


class Main:
    def __init__(self):
        self.world = World(timed=True)

        entities = make_world()

        for entity in entities:
            self.world.create_entity(*entity)

        self.world.add_processor(VisionProcessor())
        self.world.add_processor(VisibilityProcessor())
        self.world.add_processor(ItemProcessor())
        self.world.add_processor(AwakeProcessor())
        self.world.add_processor(MonsterProcessor())
        self.world.add_processor(ThreatProcessor())
        self.world.add_processor(AutoExploreProcessor())
        self.world.add_processor(TrapProcessor())
        self.world.add_processor(AttackAIProcessor())
        self.world.add_processor(DefendAIProcessor())
        self.world.add_processor(DisplayProcessor())
        self.world.add_processor(InputProcessor())
        self.world.add_processor(StairProcessor())
        self.world.add_processor(CombatProcessor())
        self.world.add_processor(MovementProcessor())
        self.world.add_processor(AngerProcessor())

    def core_game_loop(self):
        while True:
            self.world.process()

            if hasattr(self.world, "process_times"):
                print(self.world.process_times)


if __name__ == "__main__":
    with terminal_context():
        Main().core_game_loop()
