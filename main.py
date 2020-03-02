from contextlib import contextmanager

from bearlibterminal import terminal
from esper import World

from ecs.systems.attackaiprocessor import AttackAIProcessor
from ecs.systems.autoexploreprocessor import AutoExploreProcessor
from ecs.systems.defendaiprocessor import DefendAIProcessor
from ecs.systems.displayprocessor import DisplayProcessor
from ecs.systems.inputprocessor import InputProcessor
from ecs.systems.movementprocessor import MovementProcessor
from ecs.systems.visionprocessor import VisionProcessor
from factories.world import make_world


@contextmanager
def terminal_context():
    terminal.open()
    terminal.set("""
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

        self.world.add_processor(MovementProcessor())
        self.world.add_processor(VisionProcessor())
        self.world.add_processor(AutoExploreProcessor())
        self.world.add_processor(AttackAIProcessor())
        self.world.add_processor(DefendAIProcessor())
        self.world.add_processor(DisplayProcessor())
        self.world.add_processor(InputProcessor())

    def core_game_loop(self):
        while True:
            self.world.process()

            if hasattr(self.world, "process_times"):
                print(self.world.process_times)


if __name__ == "__main__":
    with terminal_context():
        Main().core_game_loop()
