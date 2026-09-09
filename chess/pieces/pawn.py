from __future__ import annotations
from typing import TYPE_CHECKING

from chess.pieces.piece import Piece
from chess.move import Move
from chess.types import Color, PieceType

if TYPE_CHECKING:
    from chess.board import Board


class Pawn(Piece):
    piece_type = PieceType.PAWN

    def attacked_squares(self, transparent=None):
        """A pawn controls its two forward diagonals, occupied or not."""
        direction = 1 if self.player.color == Color.WHITE else -1
        file, rank = self.position
        squares = [
            self.board.square_at([file - 1, rank + direction]),
            self.board.square_at([file + 1, rank + direction]),
        ]
        return [square for square in squares if square]

    def calculate_playable_squares(self):
        if self.player.color == Color.WHITE:
            direction = 1
        elif self.player.color == Color.BLACK:
            direction = -1

        squares = []
        # 1 square forward
        square_forward = self.board.square_at(
            [self.position[0], self.position[1] + (1 * direction)]
        )

        if square_forward and not square_forward.piece:
            squares.append(
                self.board.square_at(
                    [self.position[0], self.position[1] + (1 * direction)]
                )
            )

            # 2 squares forward
            if self.has_moved == False:
                square_2_forward = self.board.square_at(
                    [self.position[0], self.position[1] + (2 * direction)]
                )
                if square_2_forward and not square_2_forward.piece:
                    squares.append(square_2_forward)

        # captures
        up_left_square = self.board.square_at(
            [self.position[0] - 1, self.position[1] + (1 * direction)]
        )
        up_right_square = self.board.square_at(
            [self.position[0] + 1, self.position[1] + (1 * direction)]
        )

        if (
            up_right_square
            and up_right_square.piece
            and up_right_square.piece.player != self.player
        ):  # TODO add en-passant rule
            squares.append(up_right_square)
        if (
            up_left_square
            and up_left_square.piece
            and up_left_square.piece.player != self.player
        ):  # TODO add en-passant rule
            squares.append(up_left_square)

        self.playable_squares = squares
        return squares
