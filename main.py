from contextlib import contextmanager

from bearlibterminal import terminal

from ecs.components.display import Display
from ecs.components.map import Map
from ecs.components.position import Position
from ecs.world import World
from ecs.systems.displayprocessor import DisplayProcessor
from ecs.systems.inputprocessor import InputProcessor
from ecs.systems.movementprocessor import MovementProcessor


@contextmanager
def terminal_context():
    terminal.open()
    yield
    terminal.close()


class Main:
    def __init__(self):
        self.world = World()

        player = self.world.create_entity()
        self.world.add_component(player, Display(0x0040))
        self.world.add_component(player, Position(10, 10))

        map_ = self.world.create_entity()
        self.world.add_component(map_, Map())

        self.world.add_processor(DisplayProcessor())
        self.world.add_processor(MovementProcessor())
        self.world.add_processor(InputProcessor())

    def core_game_loop(self):
        while True:
            self.world.process()


if __name__ == "__main__":
    with terminal_context():
        Main().core_game_loop()
