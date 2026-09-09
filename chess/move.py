class Move:
    def __init__(self, player, piece, from_square, to_square, capture):
        self.player = player
        self.piece = piece
        self.from_square = from_square
        self.to_square = to_square
        self.capture = capture
        self.order = self.increment_order

    @staticmethod
    def get_all_moves(player=None):
        if player:
            return player.moves
        else:
            # return all_moves
            pass

    def increment_order(self):
        self.order = len(Move.get_all_moves)

    def cancel(self):
        # restore capture / square_to
        self.piece.square = self.from_square
        if self.capture:
            self.player.opponent().pieces.append(self.capture)
            self.to_square.piece = self.capture
            self.capture.square = self.to_square

        # restore square from
        self.from_square.piece = self.piece
        self.piece.square = self.from_square

        # restore history
        self.player.moves.remove(self)
