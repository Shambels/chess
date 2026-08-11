import pygame as pg

SQUARE_SIZE = 80
WHITE = [232,210,150]
BLACK = [156,99,56]
FPS = 5

class Game:
    def __init__(self):
        self.playing = False
        self.board = Board()
        self.players = [Player("white", self.board), Player("black", self.board)]


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
    def __init__(self):
        self.files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.file_indexes = range(1,9)
        self.ranks = range(1,9)
        self.squares_list = []
        self.squares = self.init_squares()
        self.height = len(self.ranks) * SQUARE_SIZE
        self.width = len(self.files) * SQUARE_SIZE
        self.surface = pg.display.set_mode((self.width, self.height))
        


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




    def draw(self):
        # self.surface.fill(WHITE)
        for square in self.squares_list:
            square.draw()
        

    def square_at(self, pos):
        # print(self.squares)
        print(pos[0])
        print(pos[1])
        return self.squares[pos[0]][pos[1]]
        
        

class Square:
    def __init__(self, file, file_index, rank, color, board):
        self.file = file
        self.file_index = file_index
        self.rank = rank
        self.color = color
        self.board = board
        self.piece = None

    def draw(self):
        rect = (self.file_index * SQUARE_SIZE, self.rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pg.draw.rect(self.board.surface, self.color , rect, 0)


class Player:
    def __init__(self, color, board):
        self.color = color
        self.turn = False
        self.board = board
        self.pieces = self.init_pieces(board)

    def init_pieces(self, board):
        pass
        if self.color == "white":
            for file in (board.files):
                pawn = Pawn([file, 2], self)
                pawn.draw()
                


class Piece:
    def __init__(self, position, player):
        self.player = player
        self.board = player.board
        self.color = player.color
        self.position = position
        self.square = self.board.square_at(position)


class Pawn(Piece):
    def __init__(self, *args):
        super().__init__(*args)

    def draw(self):
        center =  (self.square.file_index * SQUARE_SIZE + SQUARE_SIZE // 2,
                   self.position[1] * SQUARE_SIZE + SQUARE_SIZE // 2)
        radius = SQUARE_SIZE * 4


        pg.draw.circle(self.board.surface, [255,0,0], center, radius)

game = Game()
game.start()
