"""Global settings and constants for the Amazons game."""

from __future__ import annotations

BOARD_SIZE = 10
TILE_SIZE = 72
WINDOW_WIDTH = BOARD_SIZE * TILE_SIZE
WINDOW_HEIGHT = BOARD_SIZE * TILE_SIZE
FPS = 60
AI_TURN_DELAY_MS = 250

WHITE = "white"
BLACK = "black"
EMPTY = "."
ARROW = "X"

WHITE_AMAZON = "W"
BLACK_AMAZON = "B"

DEFAULT_WHITE_POSITIONS = ((0, 3), (0, 6), (3, 0), (3, 9))
DEFAULT_BLACK_POSITIONS = ((6, 0), (6, 9), (9, 3), (9, 6))

COLOR_LIGHT = (240, 217, 181)
COLOR_DARK = (181, 136, 99)
COLOR_WHITE_AMAZON = (245, 245, 245)
COLOR_BLACK_AMAZON = (35, 35, 35)
COLOR_ARROW = (180, 30, 30)
COLOR_SELECTION = (90, 200, 255)
COLOR_TARGET = (140, 220, 140)
COLOR_CURSOR = (255, 210, 30)

JOY_SELECT_BUTTONS = (0, 1)

DIRECTIONS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)
