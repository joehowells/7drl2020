from contextlib import contextmanager

from bearlibterminal import terminal
from esper import World

from ecs.components.gamestate import GameState
from ecs.processors.displayprocessor import DisplayProcessor
from ecs.processors.gamestateprocessor import GameStateProcessor
from ecs.processors.inputprocessor import InputProcessor
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

        self.world.add_processor(DisplayProcessor(), priority=-100)
        self.world.add_processor(InputProcessor(), priority=-200)
        self.world.add_processor(GameStateProcessor(), priority=-300)

        self.world.create_entity(GameState.TITLE_SCREEN)

    def core_game_loop(self):
        while True:
            self.world.process()

            if hasattr(self.world, "process_times"):
                print(self.world.process_times)


if __name__ == "__main__":
    with terminal_context():
        Main().core_game_loop()
