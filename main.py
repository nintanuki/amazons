"""Main executable module for the Amazons game."""

from __future__ import annotations

import pygame

from amazons import settings
from amazons.ai import RandomAI
from amazons.game_state import GameState, Move
from amazons.input_handler import InputHandler
from amazons.renderer import Renderer


class GameManager:
    """Coordinates game flow while delegating specialized responsibilities.

    Args:
        None

    Returns:
        None
    """

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Amazons")

        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        self.renderer = Renderer(self.screen)
        self.input_handler = InputHandler()
        self.ai_player = RandomAI()

        self.human_player = settings.WHITE
        self.computer_player = settings.BLACK

        self.selected_amazon: tuple[int, int] | None = None
        self.selected_destination: tuple[int, int] | None = None

    def _handle_selection(self, board_position: tuple[int, int]) -> None:
        """Handle staged human move selection (amazon, destination, arrow).

        Args:
            board_position: Position selected by the human player.

        Returns:
            None
        """

        if self.game_state.current_player != self.human_player:
            return

        token = self.game_state.piece_at(board_position)

        if self.selected_amazon is None:
            if token == settings.WHITE_AMAZON:
                self.selected_amazon = board_position
            return

        if self.selected_destination is None:
            trial_move = Move(self.selected_amazon, board_position, board_position)
            if self.game_state._path_is_clear(trial_move.from_pos, trial_move.to_pos):
                self.selected_destination = board_position
            elif token == settings.WHITE_AMAZON:
                self.selected_amazon = board_position
            return

        final_move = Move(self.selected_amazon, self.selected_destination, board_position)
        move_applied = self.game_state.apply_move(final_move)
        self.selected_amazon = None
        self.selected_destination = None

        if not move_applied and token == settings.WHITE_AMAZON:
            self.selected_amazon = board_position

    def _process_human_turn(self) -> bool:
        """Consume inputs during human turn.

        Args:
            None

        Returns:
            False if game loop should end, otherwise True.
        """

        for action in self.input_handler.poll_actions():
            if action.action_type == InputHandler.ACTION_QUIT:
                return False
            if action.action_type == InputHandler.ACTION_SELECT and action.board_position:
                self._handle_selection(action.board_position)
        return True

    def _process_ai_turn(self) -> None:
        """Apply one AI move when it is the AI player's turn.

        Args:
            None

        Returns:
            None
        """

        if self.game_state.current_player != self.computer_player:
            return

        pygame.time.delay(settings.AI_TURN_DELAY_MS)
        ai_move = self.ai_player.choose_move(self.game_state, self.computer_player)
        if ai_move is not None:
            self.game_state.apply_move(ai_move)

    def run(self) -> None:
        """Run the main game loop.

        Args:
            None

        Returns:
            None
        """

        running = True
        while running:
            winner = self.game_state.winner()
            if winner is None:
                if self.game_state.current_player == self.human_player:
                    running = self._process_human_turn()
                else:
                    self._process_ai_turn()
            else:
                for action in self.input_handler.poll_actions():
                    if action.action_type == InputHandler.ACTION_QUIT:
                        running = False

            self.renderer.draw(
                self.game_state,
                self.input_handler.cursor_position,
                self.selected_amazon,
                self.selected_destination,
            )
            pygame.display.flip()
            self.clock.tick(settings.FPS)

        pygame.quit()


if __name__ == "__main__":
    manager = GameManager()
    manager.run()
