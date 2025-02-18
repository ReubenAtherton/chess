from src.main.Move import Move

class GameState:
    def __init__(self):

        # chess board set up
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "bR", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "wR", "--"],
            ["--", "--", "wR", "--", "bp", "--", "--", "--"],
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

        self.whiteToMove = not self.whiteToMove

    def undo_move(self):

        if len(self.moveLog) != 0:
            move = self.moveLog.pop()

            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured

            self.whiteToMove = not self.whiteToMove

    def get_valid_moves(self):
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]

                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    if piece == 'p':
                        self.get_pawn_moves(row, col, moves)

                    if piece == 'R':
                        self.get_rook_moves(row, col, moves)
        return moves

    def get_pawn_moves(self, row, col, moves):
        if self.whiteToMove:
            if self.board[row - 1][col] == "--": # One square pawn advance
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--": # Two square pawn advance
                    moves.append(Move((row, col), (row - 2, col), self.board))

            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col -1 ), self.board))
            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))

        else:
            if self.board[row + 1][col] == "--":  # One square pawn advance
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":  # Two square pawn advance
                    moves.append(Move((row, col), (row + 2, col), self.board))

            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col -1 ), self.board))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def get_rook_moves(self, row, col, moves):
        enemy_color = "b" if self.whiteToMove else "w"  # Determine opponent's pieces
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for direction_row, direction_col in directions:
            new_row, new_col = row + direction_row, col + direction_col

            while 0 <= new_row <= 7 and 0 <= new_col <= 7:  # Stay within board limits
                if self.board[new_row][new_col] == "--":
                    moves.append(Move((row, col), (new_row, new_col), self.board))  # Empty square

                elif self.board[new_row][new_col][0] == enemy_color:
                    moves.append(Move((row, col), (new_row, new_col), self.board))  # Capture enemy piece
                    break  # Stop after capturing

                else:
                    break  # Stop at friendly piece

                new_row += direction_row
                new_col += direction_col  # Continue in the same direction
