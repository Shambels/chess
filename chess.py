import pygame as pg

SQUARE_SIZE = 80
WHITE = [232,210,150]
BLACK = [156,99,56]
FPS = 5

class Game:
    def __init__(self):
        self.playing = False
        self.players = [Player("white", self), Player("black", self)]
        self.board = Board(self.players)


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
            self.board.draw()
            pg.display.flip()
        pg.quit()

class Board:
    def __init__(self, players):
        self.files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.file_indexes = range(1,9)
        self.ranks = range(1,9)
        self.squares_list = []
        self.squares = self.init_squares()
        self.height = len(self.ranks) * SQUARE_SIZE
        self.width = len(self.files) * SQUARE_SIZE
        self.surface = pg.display.set_mode((self.width, self.height))
        self.players = players
        self.init_pieces()
        


    def init_squares(self):
        squares = {}
        for index, file in enumerate(self.files):
            squares[file] = {}
            for rank in self.ranks:
                color = [WHITE, BLACK][(rank + index) % 2]
                square = Square(file, index, rank, color, self)
                squares[file][rank] = square
                self.squares_list.append(square)
        return squares

    def init_pieces(self):
        for player in self.players:
            player.board = self
            player.init_pieces(self)



    def draw(self):
        # self.surface.fill(WHITE)
        for square in self.squares_list:
            square.draw()
        
        for player in self.players:
            for piece in player.pieces:
                piece.draw()


    def square_at(self, pos):
        # print(self.squares)
        print(pos[0])
        print(pos[1])
        return self.squares[pos[0]][pos[1]]
        
        

class Square:
    def __init__(self, file, file_index, rank, color, board):
        self.file = file
        self.file_index = file_index
        self.position = [file, rank]
        self.rank = rank
        self.color = color
        self.board = board
        self.piece = None

    @property
    def rect(self):
        # rank 1 at the bottom, rank 8 at the top
        return pg.Rect(self.file_index * SQUARE_SIZE, # x position
                       (len(self.board.ranks) - self.rank) * SQUARE_SIZE, # y position
                       SQUARE_SIZE, # x size - width
                       SQUARE_SIZE)  #y size - height

    def draw(self):
        pg.draw.rect(self.board.surface, self.color, self.rect, 0)

        if self.piece:
            self.piece.draw()


class Player:
    def __init__(self, color, game):
        self.color = color
        self.set_piece_color()
        self.turn = False
        self.game = game
        self.board = None # Empty on Initialize, fill later
        self.pieces = [] # self.init_pieces()

    def init_pieces(self, board):
        for file in (board.files):
            for rank in board.ranks:
                position = [file, rank]
                square = board.square_at(position)
                if (self.color == "white" and rank == 2) or (self.color == "black" and rank == 7):
                        self.pieces.append(Pawn(square, self))
                elif (self.color == "white" and rank == 1) or (self.color == "black" and rank == 8):
                    if file == "a" or file == "h":
                        self.pieces.append(Rook(square,self))
                    elif file == "b" or file == "g":
                        self.pieces.append(Knight(square,self))
                    elif file == "c" or file == "f":
                        self.pieces.append(Bishop(square,self))
                    elif file == "d":
                        self.pieces.append(Queen(square, self))
                    elif file == "e":
                        self.pieces.append(King(square, self))

                
    def set_piece_color(self):
        if self.color == "white":
            self.piece_color = [WHITE[0] -40, WHITE[1] - 40,WHITE[2] -40 ]
        if self.color == "black":
            self.piece_color = [BLACK[0] -50, BLACK[1] - 50,BLACK[2] -50 ]


class Piece:
    def __init__(self, square, player):
        self.player = player
        self.board = player.board
        self.color = player.piece_color
        self.position = square.position
        self.square = square
        # self.square = self.board.square_at(position)


class Pawn(Piece):
    def __init__(self, *args):
        super().__init__(*args)

    def draw(self):
        pg.draw.circle(self.board.surface, self.color, self.square.rect.center , SQUARE_SIZE // 6)


class Rook(Piece):
    def __init__(self, *args):
        super().__init__(*args)

    def draw(self):
        x_pos = self.square.rect[0] + SQUARE_SIZE // 4
        y_pos = self.square.rect[1] + SQUARE_SIZE // 4
        width = self.square.rect[2]
        height = self.square.rect[3]

        pg.draw.rect(self.board.surface, self.color, [x_pos, y_pos, width // 2, height // 2])

class Bishop(Piece):
    def __init__(self, *args):
        super().__init__(*args)

    def draw(self):
        x_pos = self.square.rect[0] + SQUARE_SIZE / 2.7
        y_pos = self.square.rect[1] + SQUARE_SIZE // 8
        width = self.square.rect[2]
        height = self.square.rect[3] - SQUARE_SIZE // 4
        pg.draw.rect(self.board.surface, self.color, [x_pos, y_pos, width // 4, height ])


class Knight(Piece):
    def __init__(self, *args):
        super().__init__(*args)

    def draw(self):
        pg.draw.circle(self.board.surface, self.color, self.square.rect.center, SQUARE_SIZE // 3)


class Queen(Piece):
    def __init__(self, *args):
        super().__init__(*args)

    def draw(self):
        pg.draw.circle(self.board.surface, self.color, self.square.rect.center, SQUARE_SIZE // 3)

class King(Piece):
    def __init__(self, *args):
        super().__init__(*args)

    def draw(self):
        pg.draw.circle(self.board.surface, self.color, self.square.rect.center, SQUARE_SIZE // 3)


if __name__ == "__main__":
    game = Game()
    game.start()
