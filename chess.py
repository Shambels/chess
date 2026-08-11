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

    def draw(self):
        rect = (self.file_index * SQUARE_SIZE, self.rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pg.draw.rect(self.board.surface, self.color , rect, 0)

        if self.piece:
            self.piece.draw()


class Player:
    def __init__(self, color_title, game):
        self.color_title = color_title
        self.set_piece_color()
        self.turn = False
        self.game = game
        self.board = None # Empty on Initialize, fill later
        self.pieces = [] # self.init_pieces()

    def init_pieces(self, board):
        pass
        if self.color_title == "white":
            for file in (board.files):
                position = [file, 2]
                square = board.square_at(position)
                pawn = Pawn(square, self)
                self.pieces.append(pawn)
                # pawn.draw()
                
    def set_piece_color(self):
        if self.color_title == "white":
            self.piece_color = [WHITE[0] -20, WHITE[1] - 20,WHITE[2] -20 ]
        if self.color_title == "black":
            self.piece_color = [BLACK[0] -20, BLACK[1] - 20,BLACK[2] -20 ]


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
        center =  (self.square.file_index * SQUARE_SIZE + SQUARE_SIZE // 2,
                   self.position[1] * SQUARE_SIZE + SQUARE_SIZE // 2)
        radius = SQUARE_SIZE // 3


        pg.draw.circle(self.board.surface, self.color, center, radius)

game = Game()
game.start()
