from enum import Enum


class Color(Enum):
    WHITE = "w"
    BLACK = "b"

    @property
    def opponent(self) -> "Color":
        return Color.BLACK if self is Color.WHITE else Color.WHITE


class PieceType(Enum):
    PAWN = "p"
    KNIGHT = "n"
    BISHOP = "b"
    ROOK = "r"
    QUEEN = "q"
    KING = "k"
