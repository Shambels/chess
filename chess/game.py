import pygame as pg
from chess.board import Board
from chess.ui.theme import FPS
from chess.player import Player
from chess.types import Color


class Game:
    def __init__(self):
        self.playing = False
        self.players = [Player(Color.WHITE, self), Player(Color.BLACK, self)]
        self.board = Board(self.players)
        self.white_to_play = True

    def start(self):
        print("Start game")
        clock = pg.time.Clock()
        self.playing = True
        while self.playing:
            clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = False
                    continue
                if self.white_to_play:
                    self._handle_player_turn(self.players[0], event)
                else:
                    self._handle_player_turn(self.players[1], event)
            self.board.draw()
            pg.display.flip()
            # pg.transform.flip(self.board.surface, True, True) not working

        pg.quit()

    def _handle_player_turn(self, player, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            print(player.color)
            for square in self.board.squares_list:
                square.playable = False

            square = self.board.square_at_click_position(event.pos)
            piece = square.piece

            if player.touched_piece:
                if square in player.touched_piece.playable_squares:
                    player.touched_piece.move_to(square)
                    player.touched_piece.has_moved = True
                    player.touched_piece = None
                    self.white_to_play = not self.white_to_play
            if piece in player.pieces:
                player.select_piece(piece)
                if piece.calculate_playable_squares():
                    for square in piece.playable_squares:
                        square.playable = True
