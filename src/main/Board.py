class Board:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

    def get_piece(self, row, col):
        try:
            if self.board[row][col]:
                return self.board[row][col]
        except IndexError:
            return "--"  # Return a default value (e.g., empty square) if out of bounds

    def set_piece(self, row, col, piece):
        self.board[row][col] = piece

    def move_piece(self, row, col, piece):
        self.set_piece(row, col, piece)