from bearlibterminal import terminal
from esper import Processor, World

from ecs.components.dead import Dead
from ecs.components.gamestate import GameState
from ecs.components.player import Player


class InputProcessor(Processor):
    def __init__(self):
        self.z_keydown = False
        self.x_keydown = False

    def check_both_keys(self, event: int) -> bool:
        if event == terminal.TK_Z:
            if self.x_keydown:
                self.z_keydown = False
                self.x_keydown = False
                return True
            else:
                self.z_keydown = True
                return False

        if event == terminal.TK_Z | terminal.TK_KEY_RELEASED:
            self.z_keydown = False
            return False

        if event == terminal.TK_X:
            if self.z_keydown:
                self.z_keydown = False
                self.x_keydown = False
                return True
            else:
                self.x_keydown = True
                return False

        if event == terminal.TK_X | terminal.TK_KEY_RELEASED:
            self.x_keydown = False
            return False

    def process(self):
        self.world: World

        game_state_entity, game_state = next(iter(self.world.get_component(GameState)))

        if game_state is GameState.TITLE_SCREEN:
            self.process_title_screen(game_state_entity)

        if game_state is GameState.MAIN_GAME:
            self.process_main_game(game_state_entity)

        if game_state is GameState.GAME_OVER:
            self.process_game_over(game_state_entity)

    def process_title_screen(self, game_state_entity: int) -> None:
        self.world: World

        while True:
            event = terminal.read()

            if event == terminal.TK_CLOSE:
                raise SystemExit

            check = self.check_both_keys(event)

            if check:
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
                check = self.check_both_keys(event)

                if check:
                    self.world.add_component(game_state_entity, GameState.GAME_OVER)
                    return

            else:
                if event == terminal.TK_Z:
                    player.action = player.attack_action
                    player.anger = min(max(player.anger + player.action.anger, 0), 100)
                    return

                if event == terminal.TK_X:
                    _, player = next(iter(self.world.get_component(Player)))
                    player.action = player.defend_action
                    player.anger = min(max(player.anger + player.action.anger, 0), 100)
                    return

    def process_game_over(self, game_state_entity: int) -> None:
        self.world: World

        while True:
            event = terminal.read()

            if event == terminal.TK_CLOSE:
                raise SystemExit

            check = self.check_both_keys(event)

            if check:
                self.world.add_component(game_state_entity, GameState.TITLE_SCREEN)
                return
