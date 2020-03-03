from bearlibterminal import terminal
from esper import Processor, World

from ecs.components.dead import Dead
from ecs.components.gamestate import GameState
from ecs.components.player import Player
from ecs.eventmixin import EventMixin


class InputProcessor(Processor, EventMixin):
    def process(self):
        self.world: World

        game_state_entity, game_state = next(iter(self.world.get_component(GameState)))

        if game_state is GameState.TITLE_SCREEN:
            self.process_title_screen(game_state_entity)

        if game_state is GameState.MAIN_GAME:
            self.process_main_game(game_state_entity)

    def process_title_screen(self, game_state_entity: int) -> None:
        self.world: World

        while True:
            event = terminal.read()

            while terminal.has_input():
                terminal.read()

            if event == terminal.TK_CLOSE:
                raise SystemExit

            if event == terminal.TK_Z or event == terminal.TK_X:
                self.world.add_component(game_state_entity, GameState.MAIN_GAME)
                return

    def process_main_game(self, game_state_entity: int) -> None:
        self.world: World

        while True:
            event = terminal.read()

            while terminal.has_input():
                terminal.read()

            if event == terminal.TK_CLOSE:
                raise SystemExit

            entity, player = next(iter(self.world.get_component(Player)))

            if self.world.has_component(entity, Dead):
                if event == terminal.TK_Z or event == terminal.TK_X:
                    self.world.add_component(game_state_entity, GameState.TITLE_SCREEN)
                    return

            else:
                if event == terminal.TK_Z:
                    player.action = player.attack_action
                    player.anger = min(max(player.anger + player.action.data.get("anger", 0), 0), 100)
                    return

                if event == terminal.TK_X:
                    _, player = next(iter(self.world.get_component(Player)))
                    player.action = player.defend_action
                    player.anger = min(max(player.anger + player.action.data.get("anger", 0), 0), 100)
                    return
