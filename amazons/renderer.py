"""Rendering for Amazons using pygame."""

from __future__ import annotations

import pygame

from amazons import settings
from amazons.game_state import GameState


class Renderer:
    """Draws board state and selection cues.

    Args:
        surface: Pygame display surface.

    Returns:
        None
    """

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface

    def draw(
        self,
        game_state: GameState,
        cursor: tuple[int, int],
        selected_amazon: tuple[int, int] | None,
        selected_destination: tuple[int, int] | None,
    ) -> None:
        """Render full game frame.

        Args:
            game_state: Current game state.
            cursor: Current input cursor position.
            selected_amazon: Selected amazon, if any.
            selected_destination: Selected move destination, if any.

        Returns:
            None
        """

        for row in range(game_state.board_size):
            for col in range(game_state.board_size):
                color = (
                    settings.COLOR_LIGHT if (row + col) % 2 == 0 else settings.COLOR_DARK
                )
                rect = pygame.Rect(
                    col * settings.TILE_SIZE,
                    row * settings.TILE_SIZE,
                    settings.TILE_SIZE,
                    settings.TILE_SIZE,
                )
                pygame.draw.rect(self.surface, color, rect)

                token = game_state.board[row][col]
                center = (
                    col * settings.TILE_SIZE + settings.TILE_SIZE // 2,
                    row * settings.TILE_SIZE + settings.TILE_SIZE // 2,
                )
                radius = settings.TILE_SIZE // 3

                if token == settings.WHITE_AMAZON:
                    pygame.draw.circle(self.surface, settings.COLOR_WHITE_AMAZON, center, radius)
                elif token == settings.BLACK_AMAZON:
                    pygame.draw.circle(self.surface, settings.COLOR_BLACK_AMAZON, center, radius)
                elif token == settings.ARROW:
                    margin = settings.TILE_SIZE // 4
                    start_a = (rect.left + margin, rect.top + margin)
                    end_a = (rect.right - margin, rect.bottom - margin)
                    start_b = (rect.right - margin, rect.top + margin)
                    end_b = (rect.left + margin, rect.bottom - margin)
                    pygame.draw.line(self.surface, settings.COLOR_ARROW, start_a, end_a, 3)
                    pygame.draw.line(self.surface, settings.COLOR_ARROW, start_b, end_b, 3)

        self._draw_highlight(cursor, settings.COLOR_CURSOR)
        if selected_amazon is not None:
            self._draw_highlight(selected_amazon, settings.COLOR_SELECTION)
        if selected_destination is not None:
            self._draw_highlight(selected_destination, settings.COLOR_TARGET)

    def _draw_highlight(self, board_position: tuple[int, int], color: tuple[int, int, int]) -> None:
        """Draw an outline highlight around one board square.

        Args:
            board_position: Position to highlight.
            color: RGB color for the border.

        Returns:
            None
        """

        row, col = board_position
        rect = pygame.Rect(
            col * settings.TILE_SIZE,
            row * settings.TILE_SIZE,
            settings.TILE_SIZE,
            settings.TILE_SIZE,
        )
        pygame.draw.rect(self.surface, color, rect, 3)
