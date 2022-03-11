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