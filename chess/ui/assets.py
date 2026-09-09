from functools import lru_cache
from pathlib import Path

import pygame as pg

from chess.types import Color, PieceType
from chess.ui.theme import SQUARE_SIZE

PIECES_DIR = Path(__file__).resolve().parent / "pieces"


@lru_cache(maxsize=None)
def piece_image(color: Color, piece_type: PieceType) -> pg.Surface:
    """Load and scale the sprite for a piece, e.g. Color.WHITE + PAWN -> wp.svg."""
    path = PIECES_DIR / f"{color.value}{piece_type.value}.svg"
    image = pg.image.load(path).convert_alpha()
    return pg.transform.smoothscale(image, (SQUARE_SIZE, SQUARE_SIZE))
