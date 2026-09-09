from chess.square import Square
from chess.move import Move
from chess.pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King
from chess.types import Color, PieceType
from chess.ui.theme import SQUARE_SIZE, LIGHT_SQUARE, DARK_SQUARE
import pygame as pg


class Board:
    def __init__(self, players):
        self.file_names = {
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
            6: "f",
            7: "g",
            8: "h",
        }
        self.files = range(0, 8)
        self.ranks = range(0, 8)
        self.squares_list = []
        self.squares = self.init_squares()
        self.height = (len(self.ranks)) * SQUARE_SIZE
        self.width = (len(self.files)) * SQUARE_SIZE
        self.surface = pg.display.set_mode((self.width, self.height))
        self.players = players
        self.init_pieces()
        self.init_pieces_playable_squares()

    def init_squares(self):
        squares = {}
        for file in self.files:
            squares[file] = {}
            for rank in self.ranks:
                color = [LIGHT_SQUARE, DARK_SQUARE][(rank + file) % 2 == 0]
                square = Square(file, rank, color, self)
                squares[file][rank] = square
                self.squares_list.append(square)
        return squares

    def init_pieces(self):
        for player in self.players:
            player.board = self
            player.init_pieces(self)

    def init_pieces_playable_squares(self):
        for player in self.players:
            for piece in player.pieces:
                piece.playable_squares = piece.calculate_playable_squares()

    def draw(self):
        for square in self.squares_list:
            square.draw()

        for player in self.players:
            for piece in player.pieces:
                piece.draw()

    def attacked_squares(self, player, transparent=None):
        """Every square controlled by `player`, in one pass over its pieces."""
        squares = set()
        for piece in player.pieces:
            squares.update(piece.attacked_squares(transparent))
        return squares

    def square_at(self, pos):
        file = pos[0]
        rank = pos[1]

        if file not in self.files or rank not in self.ranks:
            return

        return self.squares[file][rank]

    def square_at_click_position(self, pos):
        file = pos[0] // SQUARE_SIZE
        rank = pos[1] // SQUARE_SIZE
        return self.squares[file][rank]
