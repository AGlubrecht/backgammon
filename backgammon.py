from random import randint


class Game:
    def __init__(self):
        self.score = [0, 0]     # index 0 is white, index 1 is black
        self.backgammon = Backgammon()


class Backgammon:
    def __init__(self, *args, **kwargs):
        if "board" in kwargs.keys:
            self.board = kwargs["board"]    # board with custom size and custom number of pieces
        else:
            # standard backgammon board
            self.board = [0] * 26   # index 1 to 24 are fields, 0 is for white pieces that have been kicked out of the
                                    # game, and so is index 25 for black pieces
                                    # pieces, which are already in the "safe zone", are no longer stored
            self.board[1] = 2   # positive numbers stand for white pieces
            self.board[12] = 5
            self.board[17] = 3
            self.board[19] = 5

            self.board[24] = -2     # negative numbers stand for black pieces
            self.board[13] = -5
            self.board[8] = -3
            self.board[6] = -5

        # decide which player starts
        self.dice = self.roll_dice()    # store last dice roll
        while self.dice[0]==self.dice[1]:
            self.dice = self.roll_dice()
        if self.dice[0] > self.dice[1]:
            self.player = 1     # 1 -> white
        elif self.dice[0] < self.dice[1]:
            self.player = -1     # -1 -> black

        self.dice_left = self.dice

        # number by which points are multiplied at the end
        self.multiply = 1
        self.multiply_player = 0    # stores which play is allowed to multiply
                                    # 0 -> both
                                    # 1 -> white
                                    # -1 -> black

    @property
    def player(self):
        return self.player

    @player.setter
    def player(self, player):
        if player == -1 or player == 1:
            self.player = player

    @property
    def dice(self):
        return self.dice

    @dice.setter
    def dice(self):
        self.dice = self.roll_dice()

    @property
    def board(self):
        return self.board

    @board.setter
    def board(self, board_new):
        if len(board_new) != len(self.board):
            raise ValueError("Board has a different size!")
        self.board = board_new

    @staticmethod
    def roll_dice(self):
        dice = [randint(1, 6), randint(1, 6)]
        if dice[0] == dice[1]:
            return [dice[0]] * 4
        return dice

    def move(self, *args, **kwargs):
        if "move" in kwargs.keys:
            move = kwargs["move"]
            # check for validity of move
            self.check_move(move)
            # move is valid
            self.board[move[0]] -= self.player
            if self.board[move[1]]*self.player == -1:   # kick opposing piece
                self.board[move[1]] += self.player
                if self.player == 1:
                    self.board[25] -= self.player
                else:
                    self.board[0] -= self.player
            self.board[move[1]] += self.player
            self.check_win()
        else:
            # TODO: engine makes a move

    def check_move(self, move):
        if len(move) != 2:
            raise ValueError("Invalid move: Every move has to be list with two elements.")
        elif self.board[move[0]] * self.player <= 0:
            raise ValueError("Invalid move: You tried to move a piece from field %s, but there are no pieces."
                             % move[0])
        elif self.board[move[1]] * self.player < -1:
            raise ValueError("Invalid move: You tried to move a piece to field %s,"
                             "but there are already opposing pieces." % move[1])
        elif move[1]-move[0] not in self.dice_left:
            raise ValueError("Invalid move: You have no move with length %s left."
                             % move[1]-move[0])
        return True

    def check_win(self):
        white, black = True
        for field in self.board:
            if field > 0:
                white = False
            if field < 0:
                black = False
        return white or black
