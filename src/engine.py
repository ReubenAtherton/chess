from src.dimen.dimen import DIMENSION


class GameState:
    def __init__(self):

        # chess board set up
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

        self.whiteToMove = True
        self.moveLog = []

    # Takes a move as a parameter and executes it
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)
        print(self.moveLog[-1].start_col)

        self.whiteToMove = False

    def undo_move(self):

        if len(self.moveLog) != 0:
            move = self.moveLog.pop()

            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured

            self.whiteToMove = not self.whiteToMove


    def get_valid_moves(self):
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        moves = [Move((6, 4), (4, 4), self.board)]
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]

                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    if piece == 'p':
                        self.get_pawn_moves(row, col, moves)

                    if piece == 'R':
                        self.get_rook_moves(row, col, moves)
        return moves

    def get_pawn_moves(self, row, col, moves):
        pass

    def get_rook_moves(self, row, col, moves):
        pass

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
        self.move_id = self.start_row * 1000 + self.start_col + self.end_row * 10 + self.end_col
        print(self.move_id)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]