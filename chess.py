from functools import lru_cache
from pathlib import Path

import pygame as pg

PIECES_DIR = Path(__file__).parent / "pieces"
SQUARE_SIZE = 100
WHITE = [232,210,150]
BLACK = [156,99,56]
HIGHLIGHT_COLOR = [WHITE[0] - BLACK[0], WHITE[1] - BLACK[1], WHITE[2] - BLACK[2]]
FPS = 5


@lru_cache
def piece_image(name):
    """name is like "wp" or "bn"; matches the svg filenames in pieces/."""
    image = pg.image.load(PIECES_DIR / f"{name}.svg").convert_alpha()
    return pg.transform.smoothscale(image, (SQUARE_SIZE * 3, SQUARE_SIZE * 3))


class Game:
    def __init__(self):
        self.playing = False
        self.players = [Player("white", self), Player("black", self)]
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
                        self._handle_player_turn(self.players[1], event )
            self.board.draw()
            pg.display.flip()
            # pg.transform.flip(self.board.surface, True, True) not working
           
        pg.quit()


    def _handle_player_turn(self, player, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for square in self.board.squares_list:
                square.playable = False
            square = self.board.square_at_click_position(event.pos)
            piece = square.piece
            if piece in player.pieces:
                self.select_piece(piece)
                playable_squares = piece.playable_squares()
                if playable_squares:
                    for square in playable_squares:
                        square.playable = True


    # listen for click
    # get square where click position is
    # get piece on that square
    # if piece is player's
        # touched_piece = piece
        # highlight square
        # get playable_squares (v1 ignore ennemy obstacles, v2 incorporate)
        # draw a dot for square in playable_squares
        # listen for click again
        # get square where click position is
        # if square in playable_squares:
            # move that piece to that square
            # remove piece if there was one on that square
        # else:
            # cancel move / touched_piece = None

    def select_piece(self, piece):
        for square in self.board.squares_list:
            if square == piece.square:
                square.highlighted = True
            else:
                square.highlighted = False


class Board:
    def __init__(self, players):
        self.file_names = {1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}
        self.files = range(0,8)
        self.ranks = range(0,8)
        self.squares_list = []
        self.squares = self.init_squares()
        self.height = (len(self.ranks)) * SQUARE_SIZE
        self.width = (len(self.files)) * SQUARE_SIZE
        self.surface = pg.display.set_mode((self.width, self.height))
        self.players = players
        self.init_pieces()
        


    def init_squares(self):
        squares = {}
        for file in self.files:
            squares[file] = {}
            for rank in self.ranks:
                color = [WHITE, BLACK][(rank + file) % 2 == 0]
                square = Square(file, rank, color, self)
                squares[file][rank] = square
                self.squares_list.append(square)
        return squares

    def init_pieces(self):
        for player in self.players:
            player.board = self
            player.init_pieces(self)



    def draw(self):
        for square in self.squares_list:
            square.draw()
        
        for player in self.players:
            for piece in player.pieces:
                piece.draw()


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

class Square:
    def __init__(self, file, rank, color, board):
        self.file = file
        self.position = [file, rank]
        self.rank = rank
        self.color = color
        self.board = board
        self.piece = None
        self.highlighted = False
        self.playable = False

    @property
    def rect(self):
        return pg.Rect(self.file * SQUARE_SIZE, # x position
                       self.rank * SQUARE_SIZE, # y position
                       SQUARE_SIZE, # x size - width
                       SQUARE_SIZE)  #y size - height

    def draw(self):
        pg.draw.rect(self.board.surface, self._color() , self.rect, 0)

        if self.piece:
            self.piece.draw()

        if self.playable:
            pg.draw.circle(self.board.surface, [255,0,0], self.rect.center, SQUARE_SIZE // 6 )

    def _color(self):
        if self.highlighted:
             return HIGHLIGHT_COLOR
        return self.color


class Player:
    def __init__(self, color, game):
        self.color = color
        self.turn = False
        self.game = game
        self.board = None # Empty on Initialize, fill later
        self.pieces = [] # self.init_pieces()

    def init_pieces(self, board):
        for file in (board.files):
            for rank in board.ranks:
                position = [file, rank]
                square = board.square_at(position)
                piece = None
                if (self.color == "white" and rank == 1) or (self.color == "black" and rank == 6):
                    pass
                    piece = Pawn(square, self)
                elif (self.color == "white" and rank == 0) or (self.color == "black" and rank == 7):
                    if file == 0 or file == 7:
                        pass
                        piece = Rook(square,self)
                    elif file == 1 or file == 6:
                        pass
                        piece = Knight(square,self)
                    elif file == 2 or file == 5:
                        pass
                        piece = Bishop(square,self)
                    elif file == 3:
                        pass
                        piece = Queen(square, self)
                    elif file == 4:
                        piece = King(square, self)
                if piece:
                    self.pieces.append(piece)
                    square.piece = piece



class Piece:
    letter = ""  # set by subclasses, second half of the svg filename

    def __init__(self, square, player, has_moved=False):
        self.player = player
        self.board = player.board
        self.position = square.position
        self.has_moved = has_moved
        self.square = square

    def draw(self):
        image = piece_image(self.player.color[0] + self.letter)
        self.board.surface.blit(image, self.square.rect)

    def restrict_squares(self, squares, square):
        # TODO Remove squares that would put king in danger if moving there
        if not square:
            return True
        if square.piece and square.piece.player == self.player:
            return True
        if square.piece and square.piece.player != self.player:
            squares.append(square)
            return True
        else:
            squares.append(square)
            return False

    def squares_in_range(self, start, end, step, axis):
        squares = []
        for i in range(start + step, end, step):
            square = self._square_on_axis(axis, i)
            if self.restrict_squares(squares, square):
                break
        return squares

    def squares_in_range_diagonal(self, file, rank, direction, diag):
            squares = []
            for i in range(1, 8):
                square = self._square_on_diagonal(diag, direction, i)
                if self.restrict_squares(squares, square):
                    break
    
            return squares

    def _square_on_axis(self, axis, i):
            if axis == "file":
                return self.board.square_at([i,self.position[1]])
            elif axis == "rank":
                return self.board.square_at([self.position[0], i])

    def _square_on_diagonal(self, diag, direction, i):
            file = self.position[0]
            rank = self.position[1]
            if diag == "main":
                return self.board.square_at([file + (i * direction), rank + (i * direction)])
            elif diag == "anti":
                return self.board.square_at([file - (i* direction), rank + (i*direction)])
    
    

class Pawn(Piece):
    letter = "p"

    def playable_squares(self):
        if self.player.color == "white":
            direction = 1
        elif self.player.color == "black":
            direction = -1  

        squares = []

        # 1 square forward
        square_forward = self.board.square_at([self.position[0], self.position[1] + (1*direction)])
        if not square_forward.piece:
            squares.append(self.board.square_at([self.position[0], self.position[1] + (1*direction)]))

            # 2 squares forward
            if self.has_moved == False:
                square_2_forward = self.board.square_at([self.position[0], self.position[1] + (2*direction)])
                if not square_2_forward.piece:
                    squares.append(square_2_forward)

        # captures
        up_left_square = self.board.square_at([self.position[0] - 1, self.position[1] + (1*direction)])
        up_right_square = self.board.square_at([self.position[0] + 1, self.position[1] + (1*direction)])

        if up_right_square and up_right_square.piece and up_right_square.piece.player != self.player: # TODO add en-passant rule
            squares.append(up_right_square)
        if up_left_square and up_left_square.piece and up_left_square.piece.player != self.player: # TODO add en-passant rule
            squares.append(up_left_square)
        return squares


class Rook(Piece):
    letter = "r"

    def playable_squares(self):
        file = self.position[0]
        rank = self.position[1]
        squares_left = self.squares_in_range(file, 0, - 1, "file" )
        squares_right = self.squares_in_range(file, len(self.board.files) - self.position[0], 1, "file" )
        squares_up = self.squares_in_range(rank, len(self.board.ranks) - self.position[1], 1, "rank")
        squares_down = self.squares_in_range(rank, 0, -1, "rank")

        return squares_left + squares_right + squares_up + squares_down



class Bishop(Piece):
    letter = "b"

    def playable_squares(self):
        file = self.position[0]
        rank = self.position[1]
    
        squares_down_left = self.squares_in_range_diagonal(file, rank, - 1, "main" )
        squares_up_right = self.squares_in_range_diagonal(file, rank, 1, "main" ) # end should should be min between x delta to end and y delta to end
        squares_up_left = self.squares_in_range_diagonal(file, rank, 1, "anti") #  end should should be min between x delta to end and y delta to end
        squares_down_right = self.squares_in_range_diagonal(file, rank, -1, "anti")

        squares = squares_down_left  + squares_up_right + squares_up_left + squares_down_right

        
        return squares
    

class Knight(Piece):
    letter = "n"

    def playable_squares(self):
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

        return [x for x in squares if x is not None and not (x.piece and x.piece.player == self.player)]


class Queen(Piece):
    letter = "q"

    def playable_squares(self):
        file = self.position[0]
        rank = self.position[1]
        squares_left = self.squares_in_range(file, 0, - 1, "file" )
        squares_right = self.squares_in_range(file, len(self.board.files) - self.position[0], 1, "file" )
        squares_up = self.squares_in_range(rank, len(self.board.ranks) - self.position[1], 1, "rank")
        squares_down = self.squares_in_range(rank, 0, -1, "rank")

        squares_down_left = self.squares_in_range_diagonal(file, rank, - 1, "main" )
        squares_up_right = self.squares_in_range_diagonal(file, rank, 1, "main" ) # end should should be min between x delta to end and y delta to end
        squares_up_left = self.squares_in_range_diagonal(file, rank, 1, "anti") #  end should should be min between x delta to end and y delta to end
        squares_down_right = self.squares_in_range_diagonal(file, rank, -1, "anti")

        squares = squares_left + squares_right + squares_up + squares_down + squares_down_left + squares_up_right + squares_up_left + squares_down_right
        return squares

class King(Piece):
    letter = "k"

    def playable_squares(self):
        file = self.position[0]
        rank = self.position[1] 

        candidate_squares = []

        candidate_squares.append(self.board.square_at([file - 1, rank - 1]))
        candidate_squares.append(self.board.square_at([file - 1, rank]))
        candidate_squares.append(self.board.square_at([file - 1, rank + 1]))

        candidate_squares.append(self.board.square_at([file, rank - 1]))
        candidate_squares.append(self.board.square_at([file, rank + 1]))

        candidate_squares.append(self.board.square_at([file + 1, rank - 1]))
        candidate_squares.append(self.board.square_at([file + 1, rank]))
        candidate_squares.append(self.board.square_at([file + 1, rank + 1]))

        # danger_squares = []
        # for player in self.board.players:
        #     if player == self.player:
        #         continue
        #     opponent = player
        #     for piece in opponent.pieces:
        #         danger_squares.extend(piece.playable_squares())

        # print(danger_squares)
        # danger_squares = list(set(danger_squares))
        # print (danger_squares)

        squares = []
        for square in candidate_squares:
            if square is None:
                continue
            if square.piece and square.piece.player == self.player:
                continue
            # if square in danger_squares:
            #     continue

            squares.append(square)

        return squares
                    







if __name__ == "__main__":
    game = Game()
    game.start()
