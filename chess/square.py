from chess.ui.theme import SQUARE_SIZE, HIGHLIGHT_COLOR
import pygame as pg


class Square:
    def __init__(self, file, rank, color, board):
        self.file = file
        self.rank = rank
        self.position = [file, rank]
        self.color = color
        self.board = board
        self.piece = None
        self.highlighted = False
        self.playable = False

    @property
    def rect(self):
        return pg.Rect(
            self.file * SQUARE_SIZE,  # x position
            self.rank * SQUARE_SIZE,  # y position
            SQUARE_SIZE,  # x size - width
            SQUARE_SIZE,
        )  # y size - height

    def draw(self):
        pg.draw.rect(self.board.surface, self._color(), self.rect, 0)

        if self.piece:
            self.piece.draw()

        if self.playable:
            pg.draw.circle(
                self.board.surface, [255, 0, 0], self.rect.center, SQUARE_SIZE // 6
            )

    def _color(self):
        if self.highlighted:
            return HIGHLIGHT_COLOR
        return self.color
