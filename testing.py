from backgammon import *


def test_dice():
  dice_throw = throw_dice(3)
  print(dice_throw)
  print(subsets_by_priority(dice_throw))
  print(unique_permutations(subsets_by_priority(dice_throw)[1]))

def test_board():
  board = Board()
  board.leap(Leap(6, 1, -1))
  board.leap(Leap(1, 4, 1))
  print(board)

  print(board.check_leap(Leap(6, 5, -1))) #False
  board.leap(Leap(25, 2, -1))
  print(board)
  print(board.check_leap(Leap(6, 5, -1))) #True


  print(board.check_leap(Leap(1, 5, 1))) #False
  print(board.check_leap(Leap(1, 4, 1))) #True
  print(board.check_leap(Leap(1, 5, -1))) #False
  print(board.check_leap(Leap(5, 5, -1))) #False
  print(board.check_leap(Leap(1, 5, 1))) #False


def test_move_finder():
  board = Board()
  # for b in board.get_ordered_dice_application_results([1, 3], 1):
  #   print(b)

  # for b in board.get_legal_moves_that_use_up_all_dice([1, 3], 1):
  #     print(b)

  #correctly discards the 26 because its to early to bear off
  for b in board.get_legal_moves([1, 3, 26], 1): 
     print(b)

  

  

test_move_finder()

