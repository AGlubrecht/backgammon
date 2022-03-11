from random import randint
from itertools import permutations, combinations
from copy import copy

#To Do:
# test all changes especially the finding legal moves part -DONE!
# store perspective in the board
# complete the rewrite of the Backgammon class
# -str method, winning, move method
# write an IOmove method and Player class, that allows players to make moves via console. This is where commit move etc should live
# write a naive bot that is able to complete the game

#Milestones:
# Console interface
# GUI
# Tournaments/multi-round-matches/Doubling-Cube
# AI

#Known Bugs:
# dice sublist prioritization is different when bearing of

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
    
    return dice

def unique_permutations(l: list):
    return list(set(permutations(l)))

def subsets_by_priority(l: list):
    #outputs all sublists in the order in which they need to be considered
    #only interesting if no move using all dice is possible

    subsets = []
    l.sort()

    for i in range(len(l)+1):
        subsets += combinations(l, i)

    subsets.reverse()

    return subsets


class Player:
    def __init__(self, name, make_move, avatar=None):
        self.name = name
        self.points = 0
        self.make_move = make_move
        self.avatar = avatar #unused so far


class Leap:
    def __init__(self, start, distance, direction):
        #if 1 <= distance <= 6:
            self.direction = direction
            self.start = start
            self.end = start+distance*direction
        #else:
            #raise ValueError("Invalid leap: Distance has to be between 1 and 6.")


class Board:
    default_board = [0, 2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0]

    def __init__(self, content=default_board):
        self.content = copy(content)

    def bar_index(self, perspective):
      return (len(self.content)-1)*(perspective-1)//(-2)

    def leap(self, leap):

        self.content[leap.start] -= leap.direction
        if 25 > leap.end > 0:
            if self.content[leap.end] * leap.direction == -1:
                # kick opposing piece
                self.content[leap.end] += leap.direction
                self.content[self.bar_index(-leap.direction)] -= leap.direction
                # if leap.direction == 1:
                #     self.content[(len(self.content)-1)*(leap.direction+1)/2] -= leap.direction
                # else:
                #     self.content[0] -= leap.direction
            self.content[leap.end] += leap.direction

    #TODO: move kicked pieces in first -DONE

    def check_leap(self, leap):

        if not isinstance(leap, Leap):
            return False
          
        #check if there is a piece that can be moved
        elif self.content[leap.start] * leap.direction <= 0:
            return False
            
        #check if pieces can currently be borne off
        elif leap.end >= len(self.content) - 1:
            if not self.check_last_quarter(leap.direction):
                return False
        elif leap.end <= 0:
            if not self.check_last_quarter(leap.direction):
                return False

        #check if leap is blocked by opposing pieces
        elif self.content[leap.end] * leap.direction < -1:
            return False

        #check if pieces need to be brought in from the bar
        elif self.content[self.bar_index(leap.direction)] != 0 and leap.start != self.bar_index(leap.direction):
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
        dice_permutations = unique_permutations(diceThrow)

        legal_moves = []

        print(dice_permutations)

        for dice_order in dice_permutations:
            print(dice_order)
            legal_moves += self.get_ordered_dice_application_results(dice_order, perspective)

        return legal_moves


    def get_ordered_dice_application_results(self, ordered_dice, perspective): #returns all possible results of applying the dice in order
        if len(ordered_dice) == 0:
            return [self]

        result_boards = []

        for i in range(len(self.content)):
            if self.content[i] * perspective > 0:
                leap = Leap(i, ordered_dice[0], perspective)
                if self.check_leap(leap):
                    transient_board = Board(self.content)
                    transient_board.leap(leap)
                    result_boards += transient_board.get_ordered_dice_application_results(ordered_dice[1:], perspective)

        return result_boards

    def check_last_quarter(self, perspective):
        check = True
        if perspective == 1:
            rg = (0, int(3 * len(self.content) / 4))
        else:
            rg = (int(len(self.content) / 4), len(self.content))
        for i in range(*rg):
            if self.content[i] * perspective > 0:
                check = False
        return check

    def check_win(self): #faulty
        win = True
        for field in self.content:
            if field * self.player_sign > 0:
                win = False
                break
        return win

    def __str__(self):
        rep = ""
        for i in range(int(len(self.content) / 2) - 1, 0, -1):
            if self.content[i] >= 0:
                rep += " "
            rep += str(self.content[i]) + " "
        
        rep += " | " + str(self.content[0]) + "\n"

        for i in range(int(len(self.content) / 2), len(self.content) - 1):
            if self.content[i] >= 0:
                rep += " "
            rep += str(self.content[i]) + " "

        rep += " | " + str(self.content[len(self.content) - 1]) + "\n"

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


    def move(self, next_board_state): #TODO
        self.board = next_board_state
        self.check_win() #not enough
        self.player_sign *= -1

    def __str__(self):
        pass #TODO
        # rep += "\n"
        # rep += "dices: "
        # for num in self.dices_left:
        #     rep += str(num) + " "
        # rep += "\n"
        # rep += "player: " + str(self.player_sign)


    def win(self):
        if self.player_sign == 1:
            print("White won the game!")
        else:
            print("Black won the game!")
