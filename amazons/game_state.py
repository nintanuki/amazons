"""Game state and rule validation for Amazons."""

from __future__ import annotations

from dataclasses import dataclass

from amazons import settings


@dataclass(frozen=True)
class Move:
    """Represents one full Amazons move.

    Args:
        from_pos: Coordinates of the moving amazon before the move.
        to_pos: Coordinates of the amazon after movement.
        arrow_pos: Coordinates where the arrow lands.

    Returns:
        None
    """

    from_pos: tuple[int, int]
    to_pos: tuple[int, int]
    arrow_pos: tuple[int, int]


class GameState:
    """Stores board data and validates/apply game moves.

    Args:
        board_size: Width/height of the square board.
        white_positions: Initial white amazon positions.
        black_positions: Initial black amazon positions.
        current_player: Which player is to move.

    Returns:
        None
    """

    def __init__(
        self,
        board_size: int = settings.BOARD_SIZE,
        white_positions: tuple[tuple[int, int], ...] = settings.DEFAULT_WHITE_POSITIONS,
        black_positions: tuple[tuple[int, int], ...] = settings.DEFAULT_BLACK_POSITIONS,
        current_player: str = settings.WHITE,
    ) -> None:
        self.board_size = board_size
        self.current_player = current_player
        self.board = [
            [settings.EMPTY for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]

        for row, col in white_positions:
            self.board[row][col] = settings.WHITE_AMAZON
        for row, col in black_positions:
            self.board[row][col] = settings.BLACK_AMAZON

    def in_bounds(self, position: tuple[int, int]) -> bool:
        """Check whether a position is inside the board.

        Args:
            position: Position to validate.

        Returns:
            True when position is valid; otherwise False.
        """

        row, col = position
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def piece_at(self, position: tuple[int, int]) -> str:
        """Return the board token at a given position.

        Args:
            position: Coordinates to inspect.

        Returns:
            The token currently stored in the board cell.
        """

        row, col = position
        return self.board[row][col]

    def _player_token(self, player: str) -> str:
        """Map player color to board token.

        Args:
            player: Player color value.

        Returns:
            The board token that represents that player's amazon.
        """

        return settings.WHITE_AMAZON if player == settings.WHITE else settings.BLACK_AMAZON

    def _direction_delta(
        self, start: tuple[int, int], end: tuple[int, int]
    ) -> tuple[int, int] | None:
        """Compute a queen-like direction from start to end.

        Args:
            start: Start coordinates.
            end: End coordinates.

        Returns:
            Unit step direction if queen move is valid, else None.
        """

        start_row, start_col = start
        end_row, end_col = end

        delta_row = end_row - start_row
        delta_col = end_col - start_col

        if delta_row == 0 and delta_col == 0:
            return None

        abs_row = abs(delta_row)
        abs_col = abs(delta_col)
        if not (delta_row == 0 or delta_col == 0 or abs_row == abs_col):
            return None

        step_row = 0 if delta_row == 0 else delta_row // abs_row
        step_col = 0 if delta_col == 0 else delta_col // abs_col
        return step_row, step_col

    def _path_is_clear(self, start: tuple[int, int], end: tuple[int, int]) -> bool:
        """Check whether the queen path between start and end is unobstructed.

        Args:
            start: Path start coordinates.
            end: Path end coordinates.

        Returns:
            True when move shape is queen-like and no blocking pieces exist.
        """

        direction = self._direction_delta(start, end)
        if direction is None:
            return False

        step_row, step_col = direction
        current_row = start[0] + step_row
        current_col = start[1] + step_col

        while (current_row, current_col) != end:
            if not self.in_bounds((current_row, current_col)):
                return False
            if self.board[current_row][current_col] != settings.EMPTY:
                return False
            current_row += step_row
            current_col += step_col

        return self.in_bounds(end) and self.piece_at(end) == settings.EMPTY

    def generate_queen_moves(self, start: tuple[int, int]) -> list[tuple[int, int]]:
        """Generate all legal queen-like destinations from a start square.

        Args:
            start: Start coordinates.

        Returns:
            A list of legal destination coordinates.
        """

        moves: list[tuple[int, int]] = []
        start_row, start_col = start

        for delta_row, delta_col in settings.DIRECTIONS:
            row = start_row + delta_row
            col = start_col + delta_col
            while self.in_bounds((row, col)) and self.board[row][col] == settings.EMPTY:
                moves.append((row, col))
                row += delta_row
                col += delta_col

        return moves

    def generate_legal_moves(self, player: str) -> list[Move]:
        """Generate all full legal moves for a player.

        Args:
            player: Player color to generate moves for.

        Returns:
            List of complete moves (amazon move + arrow shot).
        """

        legal_moves: list[Move] = []
        player_token = self._player_token(player)

        for row in range(self.board_size):
            for col in range(self.board_size):
                from_pos = (row, col)
                if self.board[row][col] != player_token:
                    continue

                destinations = self.generate_queen_moves(from_pos)
                for to_pos in destinations:
                    self.board[row][col] = settings.EMPTY
                    self.board[to_pos[0]][to_pos[1]] = player_token

                    try:
                        for arrow_pos in self.generate_queen_moves(to_pos):
                            legal_moves.append(Move(from_pos, to_pos, arrow_pos))
                    finally:
                        self.board[to_pos[0]][to_pos[1]] = settings.EMPTY
                        self.board[row][col] = player_token

        return legal_moves

    def can_player_move(self, player: str) -> bool:
        """Check whether the given player has at least one legal move.

        Args:
            player: Player color to evaluate.

        Returns:
            True if at least one legal move exists, else False.
        """

        return bool(self.generate_legal_moves(player))

    def winner(self) -> str | None:
        """Return winner if current player is blocked.

        Args:
            None

        Returns:
            Winning player's color or None if game is still active.
        """

        if self.can_player_move(self.current_player):
            return None
        return settings.BLACK if self.current_player == settings.WHITE else settings.WHITE

    def apply_move(self, move: Move) -> bool:
        """Validate and apply a move for the current player.

        Args:
            move: Full move to validate and apply.

        Returns:
            True when move was valid and applied, else False.
        """

        from_pos, to_pos, arrow_pos = move.from_pos, move.to_pos, move.arrow_pos
        if not (
            self.in_bounds(from_pos)
            and self.in_bounds(to_pos)
            and self.in_bounds(arrow_pos)
        ):
            return False

        player_token = self._player_token(self.current_player)
        if self.piece_at(from_pos) != player_token:
            return False

        if not self._path_is_clear(from_pos, to_pos):
            return False

        from_row, from_col = from_pos
        to_row, to_col = to_pos
        self.board[from_row][from_col] = settings.EMPTY
        self.board[to_row][to_col] = player_token

        if not self._path_is_clear(to_pos, arrow_pos):
            self.board[to_row][to_col] = settings.EMPTY
            self.board[from_row][from_col] = player_token
            return False

        arrow_row, arrow_col = arrow_pos
        self.board[arrow_row][arrow_col] = settings.ARROW
        self.current_player = (
            settings.BLACK if self.current_player == settings.WHITE else settings.WHITE
        )
        return True
