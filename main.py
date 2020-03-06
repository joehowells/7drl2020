from contextlib import contextmanager

from bearlibterminal import terminal
from esper import World

from ecs.components.gamestate import GameState
from ecs.processors.displayprocessor import DisplayProcessor
from ecs.processors.gamestateprocessor import GameStateProcessor
from ecs.processors.inputprocessor import InputProcessor


@contextmanager
def terminal_context():
    terminal.open()
    terminal.set("""
    window.title='Two Button Berserker';
    font: data/UbuntuMono-R.ttf, size=12;
    window.size=84x21;
    input.filter=[keyboard+];
    """)
    yield
    terminal.close()


class Main:
    def __init__(self):
        self.world = World()

        self.world.add_processor(DisplayProcessor(), priority=30)
        self.world.add_processor(InputProcessor(), priority=20)
        self.world.add_processor(GameStateProcessor(), priority=100)

        self.world.create_entity(GameState.TITLE_SCREEN)

    def core_game_loop(self):
        while True:
            self.world.process()


if __name__ == "__main__":
    with terminal_context():
        Main().core_game_loop()
