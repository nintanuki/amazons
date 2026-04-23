"""AI players for Amazons."""

from __future__ import annotations

import random

from amazons.game_state import GameState, Move


class RandomAI:
    """Simple random-move AI for Amazons.

    Args:
        seed: Optional random seed.

    Returns:
        None
    """

    def __init__(self, seed: int | None = None) -> None:
        self._random = random.Random(seed)

    def choose_move(self, game_state: GameState, player: str) -> Move | None:
        """Choose a legal move for a player.

        Args:
            game_state: Current game state.
            player: Player color for whom to select a move.

        Returns:
            A legal move, or None when no move is available.
        """

        legal_moves = game_state.generate_legal_moves(player)
        if not legal_moves:
            return None
        return self._random.choice(legal_moves)
