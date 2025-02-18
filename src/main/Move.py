# Keeps track of information of particular moves to help with legal moves, captures etc
class Move:

    # Conversion of ranks to rows for chess notation  (0, 0 = a8)
    ranks_to_rows = { "1": 7, "2": 6, "3": 5, "4": 4,
                      "5": 3, "6": 2, "7": 1, "8": 0 }

    # Reverses the conversion for converting rows -> ranks
    rows_to_ranks = { value: key for key, value in ranks_to_rows.items() }

    # Conversion of files to columns for chess notation (0, 0 = a8)
    files_to_cols = { "a": 0, "b": 1, "c": 2, "d": 3,
                      "e": 4, "f": 5, "g": 6, "h": 7 }

    # Reverses the conversion for converting col -> files
    cols_to_files = { value: key for key, value in files_to_cols.items() }

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = (self.start_row * 1000) + (self.start_col * 100) + (self.end_row * 10) + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]