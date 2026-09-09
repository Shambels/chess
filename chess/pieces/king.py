from chess.pieces import Piece
from chess.geometry import STAR
from chess.types import PieceType


class King(Piece):
    piece_type = PieceType.KING
    attack_steps = STAR

    def calculate_playable_squares(self):
        """Adjacent squares the king may legally occupy.

        Legality is decided against the opponent's ATTACKS, not against the
        opponent's legal moves. Attack generation stops at the enemy king (it
        simply controls its 8 neighbours), so this can never recurse back into
        the opponent king's playable squares -- and no move has to be made and
        undone on the board to find out.
        """
        danger_squares = self.board.attacked_squares(
            self.player.opponent(), transparent=self.square
        )

        file, rank = self.position
        candidate_square_positions = [
            [file - 1, rank - 1],
            [file - 1, rank],
            [file - 1, rank + 1],
            [file, rank - 1],
            [file, rank + 1],
            [file + 1, rank - 1],
            [file + 1, rank],
            [file + 1, rank + 1],
        ]

        safe_squares = []
        for position in candidate_square_positions:
            square = self.check_square(position)
            if square and square not in danger_squares:
                safe_squares.append(square)

        self.playable_squares = safe_squares
        return safe_squares

    def check_square(self, position):
        """The square at `position` if the king could stand on it, else None.

        Only occupancy is considered here; danger is filtered by the caller.
        """
        square = self.board.square_at(position)
        if not square:
            return None
        if square.piece and square.piece.player == self.player:
            return None
        return square
