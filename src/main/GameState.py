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
        self.in_check = False
        self.pins = []
        self.checks = []

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
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.whiteToMove:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]

        if self.in_check:

            # Only 1 check = block check or move king
            if len(self.checks) == 1:
                moves = self.get_all_possible_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]

                piece_checking = self.board[check_row][check_col]
                valid_squares = []

                if piece_checking[1] == 'N':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break

                    for i in range(len(moves) -1, -1, -1):
                        if moves[i].piece_moved[1] != 'K':
                            if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                                moves.remove(moves[i])
            # Two or more checks = move king
            else:
                self.get_king_moves(king_row, king_col, moves)

        # No check = all moves are valid
        else:
            moves = self.get_all_possible_moves()

        return moves


        # # 1. Get all possible moves
        # moves = self.get_all_possible_moves()
        #
        # # 2. for each move, make the move
        # for i in range(len(moves)-1, -1, -1): # when removing elements from list, go backwards through the list
        #     self.make_move(moves[i])
        #
        #     # Generate all opponents moves
        #     # for each of opponent moves, see if they attack king
        #     self.whiteToMove = not self.whiteToMove # needed to reverse make_move switch turns to check for current player
        #     if self.in_check():
        #         moves.remove(moves[i])
        #     self.whiteToMove = not self.whiteToMove
        #     self.undo_move()
        #
        # if len(moves) == 0:
        #     if self.in_check():
        #         self.check_mate = True
        #     else:
        #         self.stale_mate = True
        #
        # # In case player undoes check/stale mate move - could move to undo move
        # else:
        #     self.check_mate = False
        #     self.stale_mate = False

    # Complex algo - checks all possible attackers from kings perspective
    # Faster than checking every possible move to see if it attacks king
    def check_for_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False

        if self.whiteToMove:
            enemy_colour = "b"
            friendly_colour = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]

        else:
            enemy_colour = "w"
            friendly_colour = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pins = ()
            for i in range (1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[0] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == friendly_colour and end_piece[1] != 'K':
                        if possible_pins == ():
                            possible_pins = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_colour:
                        piece_type = end_piece[1]
                        # 5 possibilities here in complex conditional

                        # 1. orthogonally away from king and piece is a rook
                        # 2. diagonally away from king and piece is bishop
                        # 3. 1 sq away diagonally from king and piece is pawn
                        # 4. any direction away from king and piece is queen
                        # 5. any direction 1 square away and piece is king (necessary to prevent a king move here)

                        if (9 <= j <= 3 and piece_type == 'R') or \
                                (4 <= j <= 7 and piece_type == 'B') or \
                                (i == 1 and piece_type == 'p' and ((enemy_colour == 'w' and 6 <= j <= 7) or (enemy_colour == 'b' and 4 <= j <= 5))) or \
                                (piece_type == 'Q') or (i == 1 and piece_type == 'K'):
                            if possible_pins == ():
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pins)
                                break
                        else:
                            break
                else:
                    break # if off board

        knight_moves = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_row + m[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_colour and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))
        return in_check, pins, checks


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

        piece_pinned = False
        pin_direction = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break


        if self.whiteToMove:
            if not piece_pinned or pin_direction == (-1, 0):
                if self.board[row - 1][col] == "--": # One square pawn advance
                    moves.append(Move((row, col), (row - 1, col), self.board))
                    if row == 6 and self.board[row - 2][col] == "--": # Two square pawn advance
                        moves.append(Move((row, col), (row - 2, col), self.board))

                if col - 1 >= 0:
                    if self.board[row - 1][col - 1][0] == 'b':
                        if not piece_pinned or pin_direction == (-1, -1):
                            moves.append(Move((row, col), (row - 1, col -1 ), self.board))
                if col + 1 <= 7:
                    if self.board[row - 1][col + 1][0] == 'b':
                        if not piece_pinned or pin_direction == (-1, 1):
                            moves.append(Move((row, col), (row - 1, col + 1), self.board))

        else:
            if self.board[row + 1][col] == "--":  # One square pawn advance
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":  # Two square pawn advance
                    moves.append(Move((row, col), (row + 2, col), self.board))

            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    if not piece_pinned or pin_direction == (1, -1):
                        moves.append(Move((row, col), (row + 1, col -1 ), self.board))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    if not piece_pinned or pin_direction == (1, 1):
                        moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def get_rook_moves(self, row, col, moves):

        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != "Q":  # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        enemy_color = "b" if self.whiteToMove else "w"  # Determine opponent's pieces
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Up, Down, Left, Right

        for direction_row, direction_col in directions:
            new_row, new_col = row + direction_row, col + direction_col

            while 0 <= new_row <= 7 and 0 <= new_col <= 7:  # Stay within board limits
                if not piece_pinned or pin_direction == direction_row or pin_direction == (-direction_row[0], -direction_row[1]):
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

        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        enemy_color = "b" if self.whiteToMove else "w"  # Determine opponent's pieces

        directions = [(-2, -1), (-2, 1), (2, -1), (2, 1),
                      (-1, -2), (-1, 2), (1, -2), (1, 2)]  # Up, Down, Left, Right

        for direction_row, direction_col in directions:
            new_row, new_col = row + direction_row, col + direction_col

            while 0 <= new_row <= 7 and 0 <= new_col <= 7:  # Stay within board limits
                if not piece_pinned:
                    if self.board[new_row][new_col] == "--":
                        moves.append(Move((row, col), (new_row, new_col), self.board))  # Empty square

                    elif self.board[new_row][new_col][0] == enemy_color:
                        moves.append(Move((row, col), (new_row, new_col), self.board))  # Capture enemy piece
                        break  # Stop after capturing

                    else:
                        break  # Stop at friendly piece
                    break


    def get_bishop_moves(self, row, col, moves):

        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        enemy_color = "b" if self.whiteToMove else "w"  # Determine opponent's pieces

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction_row, direction_col in directions:
            new_row, new_col = row + direction_row, col + direction_col

            while 0 <= new_row <= 7 and 0 <= new_col <= 7:  # Stay within board limits
                if not piece_pinned or pin_direction == direction_row  or pin_direction == (-direction_row[0], -direction_row[1]):
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
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        """
        Get all the king moves for the king located at row col and add the moves to the list.
        """
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.whiteToMove else "b"
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    if ally_color == "w":
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    # place king back on original location
                    if ally_color == "w":
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)
