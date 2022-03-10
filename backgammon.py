from random import randint
from itertools import permutations, combinations
from copy import copy

#To Do:
# test all changes especially the finding legal moves part
# store perspective in the board
# complete the rewrite of the Backgammon class
# complete move method
# write an IOmove method, that allows players to make moves via console. This is where commit move etc should live
# write a naive bot that is able to complete the game
# 

#class Game:
#    def __init__(self):
#        self.score = [0, 0]  # index 0 is white, index 1 is black
#        self.backgammon = Backgammon()


def throw_dice(num=2, max_points_per_die = 6):
    dice = [randint(1, max_points_per_die) for i in range(num)]
    equal = True
    for die in dice:
        if die != dice[0]:
            equal = False
    if equal:
        dice = dice * 2

def unique_permutations(l: list):
    list(set(permutations(l)))

def subsets_by_priority(l: list):
    subsets = []
    l.sort(reverse=True)

    for i in range(len(l)+1):
        subsets += combinations(l, i)


class Player:
    def __init__(self, name, make_move, avatar=None):
        self.name = name
        self.points = 0
        self.make_move = make_move
        self.avatar = avatar #unused so far


class Leap:
    def __init__(self, start, distance):
        if 1 <= distance <= 6:
            self.start = start
            self.end = start+distance
        else:
            raise ValueError("Invalid leap: Distance has to be between 1 and 6.")


class Board:
    default_board = [0, 2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0]

    def __init__(self, content=default_board):
        self.content = copy(content)

    def leap(self, *args, **kwargs):
        if "leap" in kwargs: #why kwarg??
            leap = kwargs["leap"]
            # check for validity of move
            if self.check_leap(leap):
                # move is valid
                self.content[leap.start] -= self.player_sign #fix
                if 25 > leap.end > 0:
                    if self.content[leap.end] * self.player_sign == -1:
                        # kick opposing piece
                        self.content[leap.end] += self.player_sign
                        if self.player_sign == 1:
                            self.content[25] -= self.player_sign
                        else:
                            self.content[0] -= self.player_sign
                    self.board[leap.end] += self.player_sign
        else:
            # TODO: engine makes a move
            pass
        if self.check_win():
            self.win()
        print(self)

    #TODO: move pieces in the game first
    def check_leap(self, leap, perspective):

        if perspective != -1 and perspective != 1:
            return False

        elif not leap.isclass(Leap):
            return False
        elif self.content[leap[0]] * perspective <= 0:
            return False
        # bring
        elif leap.end >= len(self.content) - 1:
            if not self.check_last_quarter():
                return False
        elif leap.end <= 0:
            if not self.check_last_quarter():
                return False
        else:
            if self.content[leap.end] * perspective < -1:
                return False
        return True


    def get_legal_moves(self, diceThrow, perspective): #try to use all dice first, iteratively decrease the number of dice until a move is possi
        moves = []
        dice_subsets = subsets_by_priority(diceThrow)
        for dice_subset in dice_subsets:
            moves += self.get_legal_moves_that_use_up_all_dice(dice_subset, perspective)
            if moves != []:
                break
        
        return moves



    def get_legal_moves_that_use_up_all_dice(self, diceThrow, perspective):
        dice_permutations = diceThrow.uniquePermutations()

        legal_moves = []

        for dice_order in dice_permutations:
            legal_moves += self.get_ordered_dice_application_results(dice_order, perspective)


    def get_ordered_dice_application_results(self, ordered_dice, perspective): #returns all possible results of applying the dice in order
        if len(ordered_dice) == 0:
            return [self]

        result_bords = []

        for i in range(len(self.content)):
            if self.content[i] * perspective > 0:
                if self.check_leap(Leap(i, ordered_dice[0])):
                    transient_board = copy(self.content).leap(Leap(i, ordered_dice[0]))
                    result_boards += transient_board.get_ordered_dice_application_results(ordered_dice[1:], perspective)

        return result_boards

    def check_last_quarter(self, perspective):
        check = True
        if self.player_sign == 1:
            rg = (0, int(3 * len(self.content) / 4))
        else:
            rg = (int(len(self.content) / 4), len(self.content))
        for i in range(*rg):
            if self.content[i] * perspective > 0:
                check = False
        return check

    def check_win(self):
        win = True
        for field in self.content:
            if field * self.player_sign > 0:
                win = False
                break
        return win

    def __str__(self):
        rep = str(self.content[0]) + " | "
        for i in range(int(len(self.content) / 2) - 1, 0, -1):
            if self.content[i] >= 0:
                rep += " "
            rep += str(self.content[i]) + " "
        rep += "\n"
        rep += str(self.content[len(self.content) - 1]) + " | "
        for i in range(int(len(self.content) / 2), len(self.content) - 1):
            if self.content[i] >= 0:
                rep += " "
            rep += str(self.content[i]) + " "
        rep += "\n"
        rep += "dices: "
        for num in self.dices_left:
            rep += str(num) + " "
        rep += "\n"
        rep += "player: " + str(self.player_sign)
        return rep

class Backgammon:
    def __init__(self, *args, **kwargs):
        if "board" in kwargs:
            self._board = Board(kwargs["board"])  # board with custom size and custom number of pieces
        else:
            self.board = Board()

        if "num_dices" in kwargs:
            self.num_dices = kwargs["num_dices"]
        else:
            self.num_dices = 2

        # decide which player starts
        self.player_sign = randint(1, 2)*2-1

        print(self)


    def move(self, next_board_state):
        self.board = next_board_state
        self.check_win() #not enough
        self.player_sign *= -1



    # def undo_move(self):
    #     self.board = self.board_old
    #     self.dices_left = self.dices
    #     print(self)

    # def commit_move(self):
    #     if len(self.dices_left) == 0:
    #         # no moves left => roll dice and switch player
    #         self.dices = self.roll_dices()
    #         self.player_sign *= -1
    #         self.board_old = self.board
    #         print(self)
    #         # make sure there are valid moves
    #         while len(self.get_valid_moves()) == 0:
    #             # no moves available
    #             self.dices = self.roll_dices()
    #             self.player_sign = -self.player_sign
    #             print(self)



    # check if pieces are in the last quarter of the board

    def win(self):
        if self.player_sign == 1:
            print("White won the game!")
        else:
            print("Black won the game!")

bg = Backgammon()
