from random import randint
from itertools import permutations
from copy import copy

class Game:
    def __init__(self):
        self.score = [0, 0]  # index 0 is white, index 1 is black
        self.backgammon = Backgammon()


class DiceThrow:
    def __init__(self, num):
        self.dice = [randint(1,6) for i in range(num)]
        equal = True
        for die in self.dice:
            if die != self.dice[0]:
                equal = False
        if equal:
            self.dice = self.dice * 2

    def permutations(self):
        list(set(permutations(self.dice)))


class Player:
    def __init__(self, name, make_move, avatar=None):
        self.name = name
        self.points = 0
        self.make_move = make_move
        self.avatar = avatar


class Leap:
    def __init__(self, starting_index, distance):
        if 1 <= distance <= 6:
            self.starting_index = starting_index
            self.end_index = starting_index+distance
        else:
            raise ValueError("Invalid leap: Distance has to be between 1 and 6.")


class Board:
    default_board = [0, 2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0]

    def __init__(self, board=default_board):
        self.board = board

    # TODO: move pieces in the game first
    def check_leap(self, leap, perspective):

        if perspective != -1 and perspective != 1:
            return False

        elif not leap.isclass(Leap):
            return False
        elif self.board[leap[0]] * perspective <= 0:
            return False
        # bring
        elif leap.end_index >= len(self.board) - 1:
            if not self.check_last_quarter():
                return False
        elif leap.end_index <= 0:
            if not self.check_last_quarter():
                return False
        else:
            if self.board[leap.end_index] * perspective < -1:
                return False
        return True


    def get_valid_moves(self, dice_permutation, perspective): #returns all ways of applying the dice in order
        if len(dice_permutation) == 0:
            return [self]
        possible_boards = []
        for i in range(len(self.board)):
            if self.board[i] * perspective >= 0:
                if self.check_leap(Leap(i, dice_permutation[0])):
                    possible_board = Board(copy(self.board))
                    possible_board.leap(Leap(i, dice_permutation[0]))
                    possible_boards += possible_board.get_valid_moves(dice_permutation[1:], perspective)
        return possible_boards


class Backgammon:
    def __init__(self, *args, **kwargs):
        if "board" in kwargs:
            self._board = kwargs["board"]  # board with custom size and custom number of pieces
        else:
            # standard backgammon board
            self._board = [0 for i in range(26)]  # index 1 to 24 are fields, 0 is for white pieces that have been
            # kicked out of the game, and so is index 25 for black pieces,
            # which are already in the "safe zone", are no longer stored

            self.board[1] = 2  # positive numbers stand for white pieces
            self.board[12] = 5
            self.board[17] = 3
            self.board[19] = 5

            self.board[24] = -2  # negative numbers stand for black pieces
            self.board[13] = -5
            self.board[8] = -3
            self.board[6] = -5

        if "num_dices" in kwargs:
            self.num_dices = kwargs["num_dices"]
        else:
            self.num_dices = 2

        # store board before move
        self._board_old = copy(self.board)

        # decide which player starts
        self.dices = self.roll_dices()  # store last dice roll
        self.dices_left = copy(self.dices)    # is set automatically when dices are set
        while self.dices[0] == self.dices[1]:
            self.dices = self.roll_dices()
        if self.dices[0] > self.dices[1]:
            self.player = 1  # 1 -> white
        elif self.dices[0] < self.dices[1]:
            self.player = -1  # -1 -> black

        print(self)

        # make sure there are valid moves
        while len(self.get_valid_moves()) == 0:
            # no moves available
            self.dices = self.roll_dices()
            self.player = -self.player
            print(self)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        if player == -1 or player == 1:
            self._player = player

    @property
    def dices(self):
        return self._dices

    @dices.setter
    def dices(self, dices):
        for num in dices:
            if num not in [i + 1 for i in range(6)]:
                raise ValueError("Invalid dice roll: Number must be between 1 and 6.")
        self._dices = dices
        self.dices_left = dices

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        if len(board) != len(self._board):
            raise ValueError("Invalid board: Board has a different size.")
        self._board = copy(board)

    @property
    def board_old(self):
        return self._board_old

    @board_old.setter
    def board_old(self, board):
        if len(board) != len(self._board_old):
            raise ValueError("Invalid board: Board has a different size.")
        self._board_old = copy(board)

    def roll_dices(self):
        dices = []
        for i in range(self.num_dices):
            dices.append(randint(1, 6))
        equal = True
        for dice in dices:
            if dice != dices[0]:
                equal = False
        if equal:
            return dices * 2
        return dices

    def entire_move(self, move):    # move = [[starting_point1, starting_point2], [dice1, dice2]]


    def move(self, *args, **kwargs):
        if "move" in kwargs:
            move = kwargs["move"]
            # check for validity of move
            if self.check_move(move):
                # move is valid
                self.board[move[0]] -= self.player
                if 25 > move[1] > 0:
                    if self.board[move[1]] * self.player == -1:
                        # kick opposing piece
                        self.board[move[1]] += self.player
                        if self.player == 1:
                            self.board[25] -= self.player
                        else:
                            self.board[0] -= self.player
                    self.board[move[1]] += self.player
                self.dices_left.remove(self.player * (move[1] - move[0]))
        else:
            # TODO: engine makes a move
            pass
        if self.check_win():
            self.win()
        print(self)

    def undo_move(self):
        self.board = self.board_old
        self.dices_left = self.dices
        print(self)

    def commit_move(self):
        if len(self.dices_left) == 0:
            # no moves left => roll dice and switch player
            self.dices = self.roll_dices()
            self.player = -self.player
            self.board_old = self.board
            print(self)
            # make sure there are valid moves
            while len(self.get_valid_moves()) == 0:
                # no moves available
                self.dices = self.roll_dices()
                self.player = -self.player
                print(self)

    def get_valid_moves(self):
        valid_moves = []
        for i in range(len(self.board)):
            for dice in self.dices_left:
                try:
                    if self.check_move([i, i + dice*self.player]):
                        valid_moves.append([i, i + dice*self.player])
                except ValueError:
                    pass

        return valid_moves

    # TODO: move pieces in the game first
    def check_move(self, move):
        if len(move) != 2:
            raise ValueError("Invalid move: Every move has to be list with two elements.")
        elif self.board[move[0]] * self.player <= 0:
            raise ValueError("Invalid move: You tried to move a piece from field {}, but there are no pieces."
                             .format(move[0]))
        # bring
        if move[1] >= len(self.board) - 1:
            if not self.check_last_quarter():
                raise ValueError("Invalid move: You tried to move in the safe zone, even though you have pieces "
                                 "that are not in your last quarter.")
        elif move[1] <= 0:
            if not self.check_last_quarter():
                raise ValueError("Invalid move: You tried to move in the safe zone, even though you have pieces "
                                 "that are not in your last quarter.")
        else:
            if self.board[move[1]] * self.player < -1:
                raise ValueError("Invalid move: You tried to move a piece to field {},"
                                 "but there are already opposing pieces.".format(move[1]))
        if self.player * (move[1] - move[0]) not in self.dices_left:
            raise ValueError("Invalid move: You have no move with length {} left."
                             .format(self.player * (move[1] - move[0])))
        return True

    # check if pieces are in the last quarter of the board
    def check_last_quarter(self):
        check = True
        if self.player == 1:
            rg = (0, int(3 * len(self.board) / 4))
        else:
            rg = (int(len(self.board) / 4), len(self.board))
        for i in range(*rg):
            if self.board[i] * self.player > 0:
                check = False
        return check

    def check_win(self):
        win = True
        for field in self.board:
            if field * self.player > 0:
                win = False
        return win

    def win(self):
        if self.player == 1:
            print("White won the game!")
        else:
            print("Black won the game!")

    def __str__(self):
        rep = str(self.board[0]) + " | "
        for i in range(int(len(self.board) / 2) - 1, 0, -1):
            if self.board[i] >= 0:
                rep += " "
            rep += str(self.board[i]) + " "
        rep += "\n"
        rep += str(self.board[len(self.board) - 1]) + " | "
        for i in range(int(len(self.board) / 2), len(self.board) - 1):
            if self.board[i] >= 0:
                rep += " "
            rep += str(self.board[i]) + " "
        rep += "\n"
        rep += "dices: "
        for num in self.dices_left:
            rep += str(num) + " "
        rep += "\n"
        rep += "player: " + str(self.player)
        return rep
