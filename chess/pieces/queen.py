from chess.pieces import Piece
from chess.geometry import STAR
from chess.types import PieceType


class Queen(Piece):
    piece_type = PieceType.QUEEN
    attack_directions = STAR

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

        squares_down_left = self.squares_in_range_diagonal(file, rank, -1, "main")
        squares_up_right = self.squares_in_range_diagonal(
            file, rank, 1, "main"
        )  # end should should be min between x delta to end and y delta to end
        squares_up_left = self.squares_in_range_diagonal(
            file, rank, 1, "anti"
        )  #  end should should be min between x delta to end and y delta to end
        squares_down_right = self.squares_in_range_diagonal(file, rank, -1, "anti")

        squares = (
            squares_left
            + squares_right
            + squares_up
            + squares_down
            + squares_down_left
            + squares_up_right
            + squares_up_left
            + squares_down_right
        )
        self.playable_squares = squares
        return squares
