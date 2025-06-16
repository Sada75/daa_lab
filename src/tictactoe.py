import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)

    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        return self.board

    def mark_square(self, row, col, player):
        if self.board[row][col] == 0:
            self.board[row][col] = player

    def available_square(self, row, col):
        return self.board[row][col] == 0

    def is_board_full(self):
        return not (self.board == 0).any()

    def check_win(self, player):
        for i in range(3):
            if all(self.board[i, :] == player): return True
            if all(self.board[:, i] == player): return True
        if all([self.board[i, i] == player for i in range(3)]): return True
        if all([self.board[i, 2 - i] == player for i in range(3)]): return True
        return False