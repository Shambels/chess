from chess.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chess.types import Color


class Player:
    def __init__(self, color, game):
        self.color = color
        self.turn = False
        self.game = game
        self.board = None  # Empty on Initialize, fill later
        self.pieces = []  # self.init_pieces()
        self.touched_piece = None
        self.moves = []

    def init_pieces(self, board):
        for file in board.files:
            for rank in board.ranks:
                position = [file, rank]
                square = board.square_at(position)
                piece = None
                if (self.color == Color.WHITE and rank == 1) or (
                    self.color == Color.BLACK and rank == 6
                ):
                    pass
                    piece = Pawn(square, self)
                elif (self.color == Color.WHITE and rank == 0) or (
                    self.color == Color.BLACK and rank == 7
                ):
                    if file == 0 or file == 7:
                        pass
                        piece = Rook(square, self)
                    elif file == 1 or file == 6:
                        pass
                        piece = Knight(square, self)
                    elif file == 2 or file == 5:
                        pass
                        piece = Bishop(square, self)
                    elif file == 3:
                        pass
                        piece = Queen(square, self)
                    elif file == 4:
                        piece = King(square, self)
                if piece:
                    self.pieces.append(piece)
                    square.piece = piece

    def select_piece(self, piece):
        for square in self.board.squares_list:
            if square == piece.square:
                square.highlighted = True
            else:
                square.highlighted = False
        self.touched_piece = piece

    def opponent(self):
        return next(player for player in self.board.players if player != self)
