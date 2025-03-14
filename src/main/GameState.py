from src.main.Castling import Castling
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
        self.in_check_var = False
        self.pins = []
        self.checks = []
        self.check_mate = False
        self.stale_mate = False
        self.enpassant_possible = ()  # coordinates for the square where en-passant capture is possible
        self.enpassant_possible_log = [self.enpassant_possible]
        self.current_castle_rights = Castling(True, True, True, True)
        self.castle_right_log = [
            Castling(
                self.current_castle_rights.w_king_side,
                self.current_castle_rights.b_king_side,
                self.current_castle_rights.w_queen_side,
                self.current_castle_rights.b_queen_side
            )
        ]

    # Takes a move as a parameter and executes it
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)

        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'

        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = '--'

        # Update enpassant possible var
        if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.enpassant_possible = ()

        if move.is_castle_move:
            if move.end_col - move.start_col == 2: # King side castle
                self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1] # Move rook
                self.board[move.end_row][move.end_col+1] = '--' # Erase old rook
            else: # Queen side castle
                self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2]
                self.board[move.end_row][move.end_col-2] = '--'

        self.enpassant_possible_log.append(self.enpassant_possible)

        self.update_castle_rights(move)
        self.castle_right_log.append(Castling(
                self.current_castle_rights.w_king_side,
                self.current_castle_rights.b_king_side,
                self.current_castle_rights.w_queen_side,
                self.current_castle_rights.b_queen_side,
            )
        )

    def update_castle_rights(self, move):
        if move.piece_moved == 'wK':
            self.current_castle_rights.w_king_side = False
            self.current_castle_rights.w_queen_side = False

        if move.piece_moved == 'bK':
            self.current_castle_rights.b_king_side = False
            self.current_castle_rights.b_queen_side = False

        if move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:
                    self.current_castle_rights.w_queen_side = False
                if move.start_col == 7:
                    self.current_castle_rights.w_king_side = False

        if move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0:
                    self.current_castle_rights.b_queen_side = False
                if move.start_col == 7:
                    self.current_castle_rights.b_king_side = False

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

            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = '--'
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.enpassant_possible = (move.end_row, move.end_col)

            if move.piece_moved[1] == 'R' or 'K':
                # Undo castle rights
                self.castle_right_log.pop()
                self.current_castle_rights = self.castle_right_log[-1]

            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # King side castle
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = '--'
                else:
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = '--'

    def get_valid_moves(self):

        temp_castle_rights = Castling(self.current_castle_rights.w_king_side, self.current_castle_rights.b_king_side,
                                          self.current_castle_rights.w_queen_side, self.current_castle_rights.b_queen_side)

        moves = []
        self.in_check_var, self.pins, self.checks = self.check_for_pins_and_checks()

        if self.whiteToMove:
            self.get_castle_moves(self.white_king_location[0], self. white_king_location[1], moves)
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            self.get_castle_moves(self.black_king_location[0], self. black_king_location[1], moves)
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]

        if self.in_check_var:
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
            if self.whiteToMove:
                self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
            else:
                self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)

        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True

        # In case player undoes check/stale-mate move - could move to undo move
        else:
            self.check_mate = False
            self.stale_mate = False

        self.current_castle_rights = temp_castle_rights

        return moves

    # Complex algo - checks all possible attackers from kings perspective
    # Faster than checking every possible move to see if it attacks king
    def check_for_pins_and_checks(self):
        pins, checks  = [], []
        is_checked_temp = False

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

        # All moves king can be attacked from
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

        for j in range(len(directions)):
            d = directions[j]
            possible_pins = ()
            for i in range (1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == friendly_colour and end_piece[1] != "K":
                        if possible_pins == ():
                            possible_pins = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_colour:
                        enemy_type = end_piece[1]
                        # Checks the 5 possibilities here in complex conditional
                        if (
                                (0 <= j <= 3 and enemy_type == "R") # Rook check using 0, 1, 2 and 3 indexes of directions list above
                                or (4 <= j <= 7 and enemy_type == "B") # Bishop check using 4, 5, 6 and 7  indexes of directions list above
                                or (i == 1 and enemy_type == "p" # Pawn check using 6 and 3 indexes of directions list above
                                    and ((enemy_colour == "w" and 6 <= j <= 7) or (enemy_colour == "b" and 4 <= j <= 5)))
                                or (enemy_type == "Q")  # Queen check - queens can attack from any direction
                                or (i == 1 and enemy_type == "K")   # King attack - kings can attack from any direction
                        ):
                            if possible_pins == ():
                                is_checked_temp = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pins)
                                break
                        else:
                            break
                else:
                    break # If off board

        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_colour and end_piece[1] == 'N':  # enemy knight attacking a king
                    is_checked_temp = True
                    checks.append((end_row, end_col, move[0], move[1]))

        return is_checked_temp, pins, checks

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
        """
        Generates all possible pawn moves from the given (row, col).
        """
        piece_pinned = False
        pin_direction = ()

        # Check if the pawn is pinned
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        # Determine movement direction (White moves up, Black moves down)
        direction = -1 if self.whiteToMove else 1
        start_row = 6 if self.whiteToMove else 1  # Starting row for double move
        enemy_colour = 'b' if self.whiteToMove else 'w'

        # Single and double pawn advance (only if not blocked)
        if not piece_pinned or pin_direction == (direction, 0):
            if self.board[row + direction][col] == "--":  # One square advance
                moves.append(Move((row, col), (row + direction, col), self.board))

                if row == start_row and self.board[row + 2 * direction][col] == "--":  # Two square advance
                    moves.append(Move((row, col), (row + 2 * direction, col), self.board))

        # Pawn captures (diagonal moves)
        for dc in [-1, 1]:  # Left (-1) and right (1) diagonal captures
            new_col = col + dc
            if 0 <= new_col < 8:  # Ensure within board limits
                if self.board[row + direction][new_col][0] == enemy_colour:  # Enemy piece to capture
                    if not piece_pinned or pin_direction == (direction, dc):
                        moves.append(Move((row, col), (row + direction, new_col), self.board))
                elif (row + direction, new_col) == self.enpassant_possible:
                    moves.append(Move((row, col), (row + direction, new_col), self.board, is_enpassant_move=True))

                elif (row - direction, new_col) == self.enpassant_possible:
                    moves.append(Move((row, col), (row - direction, new_col), self.board, is_enpassant_move=True))

    def get_rook_moves(self, row, col, moves):
        """
        Get all the rook moves for the rook located at row, col and add the moves to the list.
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != "Q":  # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check for possible moves only in boundaries of the board
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                            -direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def get_knight_moves(self, row, col, moves):
        """
        Get all the knight moves for the knight located at row col and add the moves to the list.
        """
        piece_pinned = False

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))

        ally_color = "w" if self.whiteToMove else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:  # so its either enemy piece or empty square
                        moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_bishop_moves(self, row, col, moves):
        """
        Get all the bishop moves for the bishop located at row col and add the moves to the list.
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # diagonals: up/left up/right down/right down/left
        enemy_color = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check if the move is on board
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                            -direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def get_queen_moves(self, row, col, moves):
        """
        Get all the queen moves for the queen located at row col and add the moves to the list.
        """
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        """
        Get all the king moves for the king located at row col and add the moves to the list.
        """
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        friendly_colour = "w" if self.whiteToMove else "b"
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != friendly_colour:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    if friendly_colour == "w":
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    # place king back on original location
                    if friendly_colour == "w":
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)

    def get_castle_moves(self, row, col, moves):
        if self.square_under_attack(row, col):
            return # Cannot castle when in check
        if (self.whiteToMove and self.current_castle_rights.w_king_side) or (
                not self.whiteToMove and self.current_castle_rights.b_king_side):
            self.get_king_side_castle_moves(row, col, moves)

        if (self.whiteToMove and self.current_castle_rights.w_queen_side) or (
                not self.whiteToMove and self.current_castle_rights.b_queen_side):
            self.get_queen_side_castle_moves(row, col, moves)

    def get_king_side_castle_moves(self, row, col, moves):
        if self.board[row][col+1] and self.board[row][col + 2] == '--':
            if not self.square_under_attack(row, col+1) and not self.square_under_attack(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, is_castle_move = True))

    def get_queen_side_castle_moves(self, row, col, moves):
        if self.board[row][col-1] and self.board[row][col-2] and self.board[row][col-3] == '--':
            if not self.square_under_attack(row, col-1) and not self.square_under_attack(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, is_castle_move = True))