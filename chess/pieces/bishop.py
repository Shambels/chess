from chess.pieces import Piece
from chess.geometry import DIAGONAL
from chess.types import Color, PieceType


class Bishop(Piece):
    piece_type = PieceType.BISHOP
    attack_directions = DIAGONAL

    def calculate_playable_squares(self):
        file = self.position[0]
        rank = self.position[1]

        squares_down_left = self.squares_in_range_diagonal(file, rank, -1, "main")
        squares_up_right = self.squares_in_range_diagonal(
            file, rank, 1, "main"
        )  # end should should be min between x delta to end and y delta to end
        squares_up_left = self.squares_in_range_diagonal(
            file, rank, 1, "anti"
        )  #  end should should be min between x delta to end and y delta to end
        squares_down_right = self.squares_in_range_diagonal(file, rank, -1, "anti")

        squares = (
            squares_down_left + squares_up_right + squares_up_left + squares_down_right
        )

        self.playable_squares = squares
        return squares
