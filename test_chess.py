import chess

board = type("FakeBoard", (), {"ranks": range(1, 9)})()
S = chess.SQUARE_SIZE

assert chess.Square("a", 0, 1, None, board).rect.bottomleft == (0, 8 * S)  # a1 bottom-left
assert chess.Square("a", 0, 8, None, board).rect.topleft == (0, 0)  # a8 top-left

import pygame as pg  # noqa: E402

pg.display.set_mode((S, S))
for color in "wb":
    for piece in (chess.Pawn, chess.Rook, chess.Bishop, chess.Knight, chess.Queen, chess.King):
        assert chess.piece_image(color + piece.letter).get_size() == (S, S)
print("ok")
