from random import randint


class Game:
    def __init__(self):
        self.score = [0, 0]     # index 0 is white, index 1 is black
        self.backgammon = Backgammon()


class Backgammon:
    def __init__(self, *args, **kwargs):
        if "board" in kwargs:
            self.board = kwargs["board"]    # Custom board with custom size and custom number of pieces
        else:
            # standard backgammon board
            self.board = []
            for i in range(26):
                self.board.append(0)
            self.board[1] = 2   # positive numbers stand for white pieces
            self.board[12] = 5
            self.board[17] = 3
            self.board[19] = 5

            self.board[24] = -2     # negative numbers stand for black pieces
            self.board[13] = -5
            self.board[8] = -3
            self.board[6] = -5

        # decide which player starts
        dice_white, dice_black = self.roll_dice()
        while dice_white==dice_black:
            dice_white, dice_black = self.roll_dice()
        if dice_white > dice_black:
            self.player = 0     # 0 stands for white
        elif dice_black > dice_white:
            self.player = 1     # 1 stands for black

        # number by which points are multiplied at the end
        self.multiply = 1

    @staticmethod
    def roll_dice(self):
        return [randint(1, 6), randint(1, 6)]

    def move(self):
