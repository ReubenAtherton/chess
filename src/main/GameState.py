from src.main.Move import Move

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

        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves,
                               'B': self.get_bishop_moves, 'N': self.get_knight_moves,
                               'Q': self.get_queen_moves, 'K': self.get_king_moves}

        self.whiteToMove = True
        self.moveLog = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.check_mate = False
        self.stale_mate = False

    # Takes a move as a parameter and executes it
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.piece_moved =='wK':
            self.white_king_location = (move.end_row, move.end_col)

        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.whiteToMove = not self.whiteToMove

            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)

            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)

    def get_valid_moves(self):
        # 1. Get all possible moves
        moves = self.get_all_possible_moves()

        # 2. for each move, make the move
        for i in range(len(moves)-1, -1, -1): # when removing elements from list, go backwards through the list
            self.make_move(moves[i])

            # Generate all opponents moves
            # for each of opponent moves, see if they attack king
            self.whiteToMove = not self.whiteToMove # needed to reverse make_move switch turns to check for current player
            if self.in_check():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undo_move()

        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True

        # In case player undoes check/stale mate move - could move to undo move
        else:
            self.check_mate = False
            self.stale_mate = False

        return moves

    # Determines if current player is in check
    def in_check(self):
        if self.whiteToMove:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    # Determines if enemy can attack the square (row, col)
    def square_under_attack(self, row, col):
        self.whiteToMove = not self.whiteToMove
        opp_moves = self.get_all_possible_moves()
        self.whiteToMove = not self.whiteToMove

        for move in opp_moves:
            if move.end_row == row and move.end_col == col:
                return True

    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]

                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]

                    self.move_functions[piece](row, col, moves)
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
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Up, Down, Left, Right

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

    def get_knight_moves(self, row, col, moves):
        enemy_color = "b" if self.whiteToMove else "w"  # Determine opponent's pieces

        directions = [(-2, -1), (-2, 1), (2, -1), (2, 1),
                      (-1, -2), (-1, 2), (1, -2), (1, 2)]  # Up, Down, Left, Right

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
                break


    def get_bishop_moves(self, row, col, moves):
        enemy_color = "b" if self.whiteToMove else "w"  # Determine opponent's pieces

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

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

    def get_queen_moves(self, row, col, moves):
        enemy_color = "b" if self.whiteToMove else "w"  # Determine opponent's pieces

        directions = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, 0),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

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


    def get_king_moves(self, row, col, moves):
        enemy_color = "b" if self.whiteToMove else "w"  # Determine opponent's pieces

        directions = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, 0),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

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

                break