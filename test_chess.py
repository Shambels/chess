import chess

board = type("FakeBoard", (), {"ranks": range(1, 9)})()
S = chess.SQUARE_SIZE

assert chess.Square("a", 0, 1, None, board).rect.bottomleft == (0, 8 * S)  # a1 bottom-left
assert chess.Square("a", 0, 8, None, board).rect.topleft == (0, 0)  # a8 top-left
print("ok")
