from random import randint


class Game:
    def __init__(self):
        self.score = [0, 0]     # index 0 is white, index 1 is black
        self.backgammon = Backgammon()


class Backgammon:
    def __init__(self, *args, **kwargs):
        if "board" in kwargs:
            self._board = kwargs["board"]    # board with custom size and custom number of pieces
        else:
            # standard backgammon board
            self._board = [0 for i in range(26)]     # index 1 to 24 are fields, 0 is for white pieces that have been
                                                    # kicked out of the game, and so is index 25 for black pieces
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
        self._dice = self.roll_dice()    # store last dice roll
        while self.dice[0] == self.dice[1]:
            self.dice = self.roll_dice()
        if self.dice[0] > self.dice[1]:
            self._player = 1     # 1 -> white
        elif self.dice[0] < self.dice[1]:
            self._player = -1     # -1 -> black

        self.dice_left = self.dice

        # number by which points are multiplied at the end
        self.multiply = 1
        self.multiply_player = 0    # stores which player is allowed to multiply
                                    # 0 -> both
                                    # 1 -> white
                                    # -1 -> black

        print(self)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        if player == -1 or player == 1:
            self._player = player

    @property
    def dice(self):
        return self._dice

    @dice.setter
    def dice(self, dice):
        for num in dice:
            if num not in [i+1 for i in range(6)]:
                raise ValueError("Invalid dice roll: Number must be between 1 and 6.")
        self._dice = dice
        self.dice_left = dice

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        if len(board) != len(self.board):
            raise ValueError("Invalid board: Board has a different size.")
        self._board = board

    @staticmethod
    def roll_dice():
        dice = [randint(1, 6), randint(1, 6)]
        if dice[0] == dice[1]:
            return [dice[0]] * 4
        return dice

    def move(self, *args, **kwargs):
        if "move" in kwargs:
            move = kwargs["move"]
            # check for validity of move
            self.check_move(move)
            # move is valid
            self.board[move[0]] -= self.player
            if self.board[move[1]]*self.player == -1:
                # kick opposing piece
                self.board[move[1]] += self.player
                if self.player == 1:
                    self.board[25] -= self.player
                else:
                    self.board[0] -= self.player
            self.board[move[1]] += self.player
            self.dice_left.remove(self.player*(move[1]-move[0]))
        else:
            # TODO: engine makes a move
            pass
        if len(self.dice_left) == 0:
            # no moves left => roll dice and switch player
            self.dice = self.roll_dice()
            self.player = -self.player
        print(self)
        self.check_win()

    def check_move(self, move):
        if len(move) != 2:
            raise ValueError("Invalid move: Every move has to be list with two elements.")
        elif self.board[move[0]] * self.player <= 0:
            raise ValueError("Invalid move: You tried to move a piece from field {}, but there are no pieces."
                             .format(move[0]))
        elif self.board[move[1]] * self.player < -1:
            raise ValueError("Invalid move: You tried to move a piece to field {},"
                             "but there are already opposing pieces.".format(move[1]))
        elif self.player*(move[1]-move[0]) not in self.dice_left:
            raise ValueError("Invalid move: You have no move with length {} left."
                             .format(self.player*(move[1]-move[0])))
        return True

    def check_win(self):
        white, black = True, True
        for field in self.board:
            if field > 0:
                white = False
            if field < 0:
                black = False
        return white or black

    def __str__(self):
        rep = str(self.board[0]) + " | "
        for i in range(int(len(self.board)/2)-1, 0, -1):
            if self.board[i] >= 0:
                rep += " "
            rep += str(self.board[i]) + " "
        rep += "\n"
        rep += str(self.board[25]) + " | "
        for i in range(int(len(self.board)/2), len(self.board)-1):
            if self.board[i] >= 0:
                rep += " "
            rep += str(self.board[i]) + " "
        rep += "\n"
        rep += "dices: "
        for num in self.dice_left:
            rep += str(num) + " "
        rep += "\n"
        rep += "player: " + str(self.player)
        return rep
