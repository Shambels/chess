from chess.pieces import Piece
from chess.geometry import ORTHOGONAL
from chess.types import PieceType


class Rook(Piece):
    piece_type = PieceType.ROOK
    attack_directions = ORTHOGONAL

    def calculate_playable_squares(self):
        file = self.position[0]
        rank = self.position[1]

        squares_left = self.squares_in_range(file, 0, -1, "file")
        squares_right = self.squares_in_range(
            file, len(self.board.files) - self.position[0], 1, "file"
        )
        squares_up = self.squares_in_range(
            rank, len(self.board.ranks) - self.position[1], 1, "rank"
        )
        squares_down = self.squares_in_range(rank, 0, -1, "rank")

        squares = squares_left + squares_right + squares_up + squares_down
        self.playable_squares = squares
        return squares
