from src.main.Castling import Castling
from src.main.Move import Move


class MoveValidator:
    def __init__(self, board, game_rules):
        self.board = board
        self.game_rules = game_rules
        self.in_check_var = False
        self.pins = []
        self.checks = []
        self.move_functions = {
            'p': self.get_pawn_moves, 'R': self.get_rook_moves,
            'B': self.get_bishop_moves, 'N': self.get_knight_moves,
            'Q': self.get_queen_moves, 'K': self.get_king_moves
        }

    def get_valid_moves(self):
        temp_castle_rights = Castling(self.game_rules.current_castle_rights.w_king_side,
                                     self.game_rules.current_castle_rights.b_king_side,
                                     self.game_rules.current_castle_rights.w_queen_side,
                                     self.game_rules.current_castle_rights.b_queen_side)
        moves = []
        self.in_check_var, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.game_rules.whiteToMove:
            self.get_castle_moves(self.game_rules.white_king_location[0], self.game_rules.white_king_location[1], moves)
            king_row = self.game_rules.white_king_location[0]
            king_col = self.game_rules.white_king_location[1]
        else:
            self.get_castle_moves(self.game_rules.black_king_location[0], self.game_rules.black_king_location[1], moves)
            king_row = self.game_rules.black_king_location[0]
            king_col = self.game_rules.black_king_location[1]
        if self.in_check_var:
            if len(self.checks) == 1:
                moves = self.get_all_possible_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board.get_piece(check_row, check_col)
                valid_squares = []
                if piece_checking[1] == 'N':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != 'K':
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_possible_moves()
            if self.game_rules.whiteToMove:
                self.get_castle_moves(self.game_rules.white_king_location[0], self.game_rules.white_king_location[1], moves)
            else:
                self.get_castle_moves(self.game_rules.black_king_location[0], self.game_rules.black_king_location[1], moves)
        if len(moves) == 0:
            if self.in_check():
                self.game_rules.check_mate = True
            else:
                self.game_rules.stale_mate = True
        else:
            self.game_rules.check_mate = False
            self.game_rules.stale_mate = False
        self.game_rules.current_castle_rights = temp_castle_rights
        return moves

    def check_for_pins_and_checks(self):
        pins, checks = [], []
        is_checked_temp = False
        if self.game_rules.whiteToMove:
            enemy_colour = "b"
            friendly_colour = "w"
            start_row = self.game_rules.white_king_location[0]
            start_col = self.game_rules.white_king_location[1]
        else:
            enemy_colour = "w"
            friendly_colour = "b"
            start_row = self.game_rules.black_king_location[0]
            start_col = self.game_rules.black_king_location[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pins = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board.get_piece(end_row, end_col)
                    if end_piece[0] == friendly_colour and end_piece[1] != "K":
                        if possible_pins == ():
                            possible_pins = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_colour:
                        enemy_type = end_piece[1]
                        if (
                            (0 <= j <= 3 and enemy_type == "R") or
                            (4 <= j <= 7 and enemy_type == "B") or
                            (i == 1 and enemy_type == "p" and
                             ((enemy_colour == "w" and 6 <= j <= 7) or (enemy_colour == "b" and 4 <= j <= 5))) or
                            (enemy_type == "Q") or
                            (i == 1 and enemy_type == "K")
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
                    break
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board.get_piece(end_row, end_col)
                if end_piece[0] == enemy_colour and end_piece[1] == 'N':
                    is_checked_temp = True
                    checks.append((end_row, end_col, move[0], move[1]))
        return is_checked_temp, pins, checks

    def in_check(self):
        if self.game_rules.whiteToMove:
            return self.square_under_attack(self.game_rules.white_king_location[0], self.game_rules.white_king_location[1])
        else:
            return self.square_under_attack(self.game_rules.black_king_location[0], self.game_rules.black_king_location[1])

    def square_under_attack(self, row, col):
        self.game_rules.whiteToMove = not self.game_rules.whiteToMove
        opp_moves = self.get_all_possible_moves()
        self.game_rules.whiteToMove = not self.game_rules.whiteToMove
        for move in opp_moves:
            if move.end_row == row and move.end_col == col:
                return True
        return False

    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board.board)):
            for col in range(len(self.board.board[row])):
                turn = self.board.get_piece(row, col)[0]
                if (turn == 'w' and self.game_rules.whiteToMove) or (turn == 'b' and not self.game_rules.whiteToMove):
                    piece = self.board.get_piece(row, col)[1]
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
        direction = -1 if self.game_rules.whiteToMove else 1
        start_row = 6 if self.game_rules.whiteToMove else 1
        enemy_colour = 'b' if self.game_rules.whiteToMove else 'w'
        if not piece_pinned or pin_direction == (direction, 0):
            if self.board.get_piece(row + direction, col) == "--":
                moves.append(Move((row, col), (row + direction, col), self.board))
                if row == start_row and self.board.get_piece(row + 2 * direction, col) == "--":
                    moves.append(Move((row, col), (row + 2 * direction, col), self.board))
        for dc in [-1, 1]:
            new_col = col + dc
            if 0 <= new_col < 8:
                if self.board.get_piece(row + direction, new_col)[0] == enemy_colour:
                    if not piece_pinned or pin_direction == (direction, dc):
                        moves.append(Move((row, col), (row + direction, new_col), self.board))
                elif (row + direction, new_col) == self.game_rules.enpassant_possible:
                    moves.append(Move((row, col), (row + direction, new_col), self.board, is_enpassant_move=True))
                elif (row - direction, new_col) == self.game_rules.enpassant_possible:
                    moves.append(Move((row, col), (row - direction, new_col), self.board, is_enpassant_move=True))

    def get_rook_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board.get_piece(row, col)[1] != "Q":
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = "b" if self.game_rules.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board.get_piece(end_row, end_col)
                        if end_piece == "--":
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_knight_moves(self, row, col, moves):
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = "w" if self.game_rules.whiteToMove else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if not piece_pinned:
                    end_piece = self.board.get_piece(end_row, end_col)
                    if end_piece[0] != ally_color:
                        moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_bishop_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        enemy_color = "b" if self.game_rules.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board.get_piece(end_row, end_col)
                        if end_piece == "--":
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        friendly_colour = "w" if self.game_rules.whiteToMove else "b"
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board.get_piece(end_row, end_col)
                if end_piece[0] != friendly_colour:
                    if friendly_colour == "w":
                        self.game_rules.white_king_location = (end_row, end_col)
                    else:
                        self.game_rules.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    if friendly_colour == "w":
                        self.game_rules.white_king_location = (row, col)
                    else:
                        self.game_rules.black_king_location = (row, col)

    def get_castle_moves(self, row, col, moves):
        if self.square_under_attack(row, col):
            return
        if (self.game_rules.whiteToMove and self.game_rules.current_castle_rights.w_king_side) or \
           (not self.game_rules.whiteToMove and self.game_rules.current_castle_rights.b_king_side):
            self.get_king_side_castle_moves(row, col, moves)
        if (self.game_rules.whiteToMove and self.game_rules.current_castle_rights.w_queen_side) or \
           (not self.game_rules.whiteToMove and self.game_rules.current_castle_rights.b_queen_side):
            self.get_queen_side_castle_moves(row, col, moves)

    def get_king_side_castle_moves(self, row, col, moves):
        if self.board.get_piece(row, col+1) and self.board.get_piece(row, col + 2) == '--':
            if not self.square_under_attack(row, col+1) and not self.square_under_attack(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, is_castle_move=True))

    def get_queen_side_castle_moves(self, row, col, moves):
        if self.board.get_piece(row, col-1) and self.board.get_piece(row, col-2) and self.board.get_piece(row, col-3) == '--':
            if not self.square_under_attack(row, col-1) and not self.square_under_attack(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, is_castle_move=True))