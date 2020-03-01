from contextlib import contextmanager

from bearlibterminal import terminal

from ecs.components.display import Display
from ecs.components.map import Map
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.components.staircase import Staircase
from ecs.systems.autoexploreprocessor import AutoExploreProcessor
from ecs.systems.displayprocessor import DisplayProcessor
from ecs.systems.findstaircaseprocessor import FindStaircaseProcessor
from ecs.systems.inputprocessor import InputProcessor
from ecs.systems.movementprocessor import MovementProcessor
from ecs.systems.visionprocessor import VisionProcessor
from ecs.world import World


@contextmanager
def terminal_context():
    terminal.open()
    yield
    terminal.close()


class Main:
    def __init__(self):
        self.world = World(timed=True)

        player = self.world.create_entity()
        self.world.add_component(player, Display(0x0040))
        self.world.add_component(player, Player())
        self.world.add_component(player, Position(10, 10))

        player = self.world.create_entity()
        self.world.add_component(player, Display(0x003E))
        self.world.add_component(player, Staircase())
        self.world.add_component(player, Position(92, 12))

        map_ = self.world.create_entity()
        self.world.add_component(map_, Map())

        self.world.add_processor(MovementProcessor())
        self.world.add_processor(VisionProcessor())
        self.world.add_processor(AutoExploreProcessor())
        self.world.add_processor(FindStaircaseProcessor())
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
