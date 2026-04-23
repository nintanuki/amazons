"""Unit tests for Amazons game state rules."""

from __future__ import annotations

import unittest

from amazons import settings
from amazons.game_state import GameState, Move


class GameStateTests(unittest.TestCase):
    """Validates core move rules and endgame detection."""

    def test_initial_setup_places_default_amazons(self) -> None:
        """Default board should include expected initial amazons.

        Args:
            None

        Returns:
            None
        """

        state = GameState()
        for position in settings.DEFAULT_WHITE_POSITIONS:
            self.assertEqual(state.piece_at(position), settings.WHITE_AMAZON)
        for position in settings.DEFAULT_BLACK_POSITIONS:
            self.assertEqual(state.piece_at(position), settings.BLACK_AMAZON)

    def test_apply_valid_move_places_arrow_and_switches_turn(self) -> None:
        """A valid move should move the amazon, place arrow, and toggle turn.

        Args:
            None

        Returns:
            None
        """

        state = GameState(board_size=4, white_positions=((0, 0),), black_positions=((3, 3),))
        move = Move((0, 0), (0, 2), (1, 2))

        self.assertTrue(state.apply_move(move))
        self.assertEqual(state.piece_at((0, 0)), settings.EMPTY)
        self.assertEqual(state.piece_at((0, 2)), settings.WHITE_AMAZON)
        self.assertEqual(state.piece_at((1, 2)), settings.ARROW)
        self.assertEqual(state.current_player, settings.BLACK)

    def test_rejects_blocked_path_move(self) -> None:
        """Move should fail if another piece blocks queen path.

        Args:
            None

        Returns:
            None
        """

        state = GameState(board_size=4, white_positions=((0, 0), (0, 1)), black_positions=((3, 3),))
        move = Move((0, 0), (0, 3), (1, 3))
        self.assertFalse(state.apply_move(move))

    def test_detects_winner_when_current_player_has_no_moves(self) -> None:
        """Winner should be opponent if current player cannot move.

        Args:
            None

        Returns:
            None
        """

        state = GameState(board_size=3, white_positions=((1, 1),), black_positions=((0, 0),))
        for row, col in ((0, 1), (1, 0), (1, 2), (2, 1), (0, 2), (2, 0), (2, 2)):
            state.board[row][col] = settings.ARROW

        self.assertEqual(state.winner(), settings.BLACK)


if __name__ == "__main__":
    unittest.main()
