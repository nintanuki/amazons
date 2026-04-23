"""Input processing for keyboard, mouse, and controller."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from amazons import settings


@dataclass(frozen=True)
class InputAction:
    """Represents one normalized gameplay action."""

    action_type: str
    board_position: tuple[int, int] | None = None


class InputHandler:
    """Collects and normalizes player input events."""

    ACTION_QUIT = "quit"
    ACTION_SELECT = "select"

    def __init__(self) -> None:
        self.cursor_position = (0, 0)
        pygame.joystick.init()
        self.joysticks = [
            pygame.joystick.Joystick(index)
            for index in range(pygame.joystick.get_count())
        ]

    def _clamp_cursor(self, row_delta: int, col_delta: int) -> None:
        """Move cursor while keeping it on board.

        Args:
            row_delta: Row step to apply.
            col_delta: Column step to apply.

        Returns:
            None
        """

        row, col = self.cursor_position
        new_row = min(max(row + row_delta, 0), settings.BOARD_SIZE - 1)
        new_col = min(max(col + col_delta, 0), settings.BOARD_SIZE - 1)
        self.cursor_position = (new_row, new_col)

    def _pixel_to_board(self, pixel_position: tuple[int, int]) -> tuple[int, int]:
        """Convert window pixel coordinates to board coordinates.

        Args:
            pixel_position: Position in screen pixels.

        Returns:
            Board row/column tuple.
        """

        x_pos, y_pos = pixel_position
        row = y_pos // settings.TILE_SIZE
        col = x_pos // settings.TILE_SIZE
        row = min(max(row, 0), settings.BOARD_SIZE - 1)
        col = min(max(col, 0), settings.BOARD_SIZE - 1)
        return row, col

    def poll_actions(self) -> list[InputAction]:
        """Read pygame events and return normalized actions.

        Args:
            None

        Returns:
            A list of parsed input actions.
        """

        actions: list[InputAction] = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions.append(InputAction(self.ACTION_QUIT))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board_pos = self._pixel_to_board(event.pos)
                self.cursor_position = board_pos
                actions.append(InputAction(self.ACTION_SELECT, board_pos))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    actions.append(InputAction(self.ACTION_QUIT))
                elif event.key == pygame.K_UP:
                    self._clamp_cursor(-1, 0)
                elif event.key == pygame.K_DOWN:
                    self._clamp_cursor(1, 0)
                elif event.key == pygame.K_LEFT:
                    self._clamp_cursor(0, -1)
                elif event.key == pygame.K_RIGHT:
                    self._clamp_cursor(0, 1)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    actions.append(
                        InputAction(self.ACTION_SELECT, self.cursor_position)
                    )
            elif event.type == pygame.JOYHATMOTION:
                x_dir, y_dir = event.value
                self._clamp_cursor(-y_dir, x_dir)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button in settings.JOY_SELECT_BUTTONS:
                    actions.append(
                        InputAction(self.ACTION_SELECT, self.cursor_position)
                    )

        return actions
