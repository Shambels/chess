from __future__ import annotations
from typing import TYPE_CHECKING

from chess.square import Square
from chess.move import Move
from chess.types import Color, PieceType
from chess.ui.assets import piece_image

if TYPE_CHECKING:
    from chess.board import Board


class Piece:
    piece_type = None  # set by subclasses, second half of the svg filename
    attack_steps = ()  # single-step attackers (king, knight)
    attack_directions = ()  # sliding attackers (rook, bishop, queen)

    def __init__(self, square, player, has_moved=False):
        self.player = player
        self.board = player.board
        self.has_moved = has_moved
        self.square = square
        self.playable_squares = []

    @property
    def position(self):
        return self.square.position

    def calculate_playable_squares(self):
        pass

    def attacked_squares(self, transparent=None):
        """Squares this piece controls, friendly-occupied ones included.

        Pure geometry: it never asks whether a move would be legal, so it can
        never recurse back into King.calculate_playable_squares(). Friendly
        squares count because a piece standing on one is *defended*, and an
        enemy king may not capture it.

        `transparent` names a square that sliding pieces see through. The king
        passes its own square so a ray is not truncated by the very king whose
        safety is being evaluated -- otherwise it could illegally step back
        along the checking line.
        """
        file, rank = self.position
        squares = []

        for step_file, step_rank in self.attack_steps:
            square = self.board.square_at([file + step_file, rank + step_rank])
            if square:
                squares.append(square)

        for step_file, step_rank in self.attack_directions:
            for i in range(1, 8):
                square = self.board.square_at(
                    [file + (i * step_file), rank + (i * step_rank)]
                )
                if not square:
                    break
                squares.append(square)
                if square.piece and square is not transparent:
                    break  # blocked: the blocker is attacked, nothing beyond it

        return squares

    def draw(self):
        image = piece_image(self.player.color, self.piece_type)
        self.board.surface.blit(image, self.square.rect)

    def move_to(self, square):

        # capture opponent piece
        capture = square.piece
        if capture:
            capture.player.pieces.remove(capture)
            # del capture

        # clear square from
        from_square = self.square
        from_square.piece = None

        # update new square
        self.square = square
        # self.position = square.position  # no_longer_needed because reflects square.position
        square.piece = self

        # update state
        # self.calculate_playable_squares()
        # register_move
        move = Move(self.player, self, from_square, square, capture)
        self.player.moves.append(move)
        self.calculate_playable_squares()
        return move

    def restrict_squares(self, squares, square):
        # TODO Remove squares that would put king in danger if moving there
        if not square:
            return True
        if square.piece and square.piece.player == self.player:
            return True
        if square.piece and square.piece.player != self.player:
            squares.append(square)
            return True
        else:
            squares.append(square)
            return False

    def squares_in_range(self, start, end, step, axis):
        squares = []
        for i in range(start + step, end, step):
            square = self._square_on_axis(axis, i)
            if self.restrict_squares(squares, square):
                break
        return squares

    def squares_in_range_diagonal(self, file, rank, direction, diag):
        squares = []
        for i in range(1, 8):
            square = self._square_on_diagonal(diag, direction, i)
            if self.restrict_squares(squares, square):
                break

        return squares

    def _square_on_axis(self, axis, i):
        if axis == "file":
            return self.board.square_at([i, self.position[1]])
        elif axis == "rank":
            return self.board.square_at([self.position[0], i])

    def _square_on_diagonal(self, diag, direction, i):
        file = self.position[0]
        rank = self.position[1]
        if diag == "main":
            return self.board.square_at(
                [file + (i * direction), rank + (i * direction)]
            )
        elif diag == "anti":
            return self.board.square_at(
                [file - (i * direction), rank + (i * direction)]
            )
