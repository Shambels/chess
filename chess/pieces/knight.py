from chess.pieces import Piece
from chess.geometry import KNIGHT_STEPS
from chess.types import PieceType


class Knight(Piece):
    piece_type = PieceType.KNIGHT
    attack_steps = KNIGHT_STEPS

    def calculate_playable_squares(self):
        file = self.position[0]
        rank = self.position[1]
        pass
        squares = [
            self.board.square_at([file + 2, rank + 1]),
            self.board.square_at([file + 2, rank - 1]),
            self.board.square_at([file - 2, rank + 1]),
            self.board.square_at([file - 2, rank - 1]),
            self.board.square_at([file - 1, rank + 2]),
            self.board.square_at([file + 1, rank + 2]),
            self.board.square_at([file - 1, rank - 2]),
            self.board.square_at([file + 1, rank - 2]),
        ]
        squares = [
            x
            for x in squares
            if x is not None and not (x.piece and x.piece.player == self.player)
        ]
        self.playable_squares = squares
        return squares
