from Move import Move

class MoveValidator:
    
    def __init__(self, check_detector, board):
        self.board = board
        self.check_detector = check_detector

        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves,
                               'B': self.get_bishop_moves, 'N': self.get_knight_moves,
                               'Q': self.get_queen_moves, 'K': self.get_king_moves}

    def get_move_functions(self, piece, row, col, moves, pins, white_to_move, enpassant_possible):
        self.move_functions[piece](row, col, moves, pins, white_to_move, enpassant_possible)

    def get_all_possible_moves(self, board, white_to_move, pins, enpassant_possible):
        moves = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                turn = self.board.get_piece(row, col)[0]

                if (turn == 'w' and white_to_move) or (turn == 'b' and not white_to_move):
                    piece = self.board.get_piece(row, col)[1]

                    self.move_functions[piece](row, col, moves, pins, white_to_move, enpassant_possible)
        return moves

        # Determines if enemy can attack the square (row, col)

    def square_under_attack(self, row, col, white_to_move):
        white_to_move = not white_to_move
        opp_moves = self.get_all_possible_moves(self.board, white_to_move)

        for move in opp_moves:
            if move.end_row == row and move.end_col == col:
                return True

    def get_pawn_moves(self, row, col, moves, pins, white_to_move, enpassant_possible):
        """
        Generates all possible pawn moves from the given (row, col).
        """
        piece_pinned = False
        pin_direction = ()

        # Check if the pawn is pinned
        for i in range(len(pins) - 1, -1, -1):
            if pins[i][0] == row and pins[i][1] == col:
                piece_pinned = True
                pin_direction = (pins[i][2], pins[i][3])
                pins.remove(pins[i])
                break

        # Determine movement direction (White moves up, Black moves down)
        direction = -1 if white_to_move else 1
        start_row = 6 if white_to_move else 1  # Starting row for double move
        enemy_colour = 'b' if white_to_move else 'w'

        # Single and double pawn advance (only if not blocked)
        if not piece_pinned or pin_direction == (direction, 0):
            if self.board.get_piece(row + direction, col) == "--":  # One square advance
                moves.append(Move((row, col), (row + direction, col), self.board))

                if row == start_row and self.board.get_piece(row + 2 * direction, col) == "--":  # Two square advance
                    moves.append(Move((row, col), (row + 2 * direction, col), self.board))

        # Pawn captures (diagonal moves)
        for dc in [-1, 1]:  # Left (-1) and right (1) diagonal captures
            new_col = col + dc
            if 0 <= new_col < 8:  # Ensure within board limits
                if self.board.get_piece(row + direction, new_col)[0] == enemy_colour:  # Enemy piece to capture
                    if not piece_pinned or pin_direction == (direction, dc):
                        moves.append(Move((row, col), (row + direction, new_col), self.board))
                elif (row + direction, new_col) == enpassant_possible:
                    moves.append(Move((row, col), (row + direction, new_col), self.board, is_enpassant_move=True))

                elif (row - direction, new_col) == enpassant_possible:
                    moves.append(Move((row, col), (row - direction, new_col), self.board, is_enpassant_move=True))

    def get_rook_moves(self, row, col, moves, pins, white_to_move, enpassant_possible = False):
        """
        Get all the rook moves for the rook located at row, col and add the moves to the list.
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(pins) - 1, -1, -1):
            if pins[i][0] == row and pins[i][1] == col:
                piece_pinned = True
                pin_direction = (pins[i][2], pins[i][3])
                if self.board.get_piece(row, col)[1] != "Q":  # can't remove queen from pin on rook moves, only remove it on bishop moves
                    pins.remove(pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if white_to_move else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check for possible moves only in boundaries of the board
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                            -direction[0], -direction[1]):
                        end_piece = self.board.get_piece(end_row, end_col)
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def get_knight_moves(self, row, col, moves, pins, white_to_move, enpassant_possible = False):
        """
        Get all the knight moves for the knight located at row col and add the moves to the list.
        """
        piece_pinned = False

        for i in range(len(pins) - 1, -1, -1):
            if pins[i][0] == row and pins[i][1] == col:
                piece_pinned = True
                pins.remove(pins[i])
                break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))

        ally_color = "w" if white_to_move else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if not piece_pinned:
                    end_piece = self.board.get_piece(end_row, end_col)
                    if end_piece[0] != ally_color:  # so its either enemy piece or empty square
                        moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_bishop_moves(self, row, col, moves, pins, white_to_move, enpassant_possible = False):
        """
        Get all the bishop moves for the bishop located at row col and add the moves to the list.
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(pins) - 1, -1, -1):
            if pins[i][0] == row and pins[i][1] == col:
                piece_pinned = True
                pin_direction = (pins[i][2], pins[i][3])
                pins.remove(pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # diagonals: up/left up/right down/right down/left
        enemy_color = "b" if white_to_move else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check if the move is on board
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                            -direction[0], -direction[1]):
                        end_piece = self.board.get_piece(end_row, end_col)
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def get_queen_moves(self, row, col, moves, pins, white_to_move, enpassant_possible = False):
        """
        Get all the queen moves for the queen located at row col and add the moves to the list.
        """
        self.get_rook_moves(row, col, moves, pins, white_to_move, enpassant_possible)
        self.get_bishop_moves(row, col, moves, pins, white_to_move, enpassant_possible)

    def get_king_moves(self, row, col, moves, pins, white_to_move, enpassant_possible = False):
        """
        Get all the king moves for the king located at row col and add the moves to the list.
        """
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        friendly_colour = "w" if white_to_move else "b"
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board.get_piece(end_row, end_col)
                if end_piece[0] != friendly_colour:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    if friendly_colour == "w":
                        self.board.set_white_king_location(end_row, end_col)
                    else:
                        self.board.set_black_king_location(end_row, end_col)
                    in_check, pins, checks = self.check_detector.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    # place king back on original location
                    if friendly_colour == "w":
                        self.board.set_white_king_location(row, col)
                    else:
                        self.board.set_black_king_location(row, col)

    def get_castle_moves(self, row, col, moves, pins, white_to_move, enpassant_possible):
        if self.square_under_attack(row, col):
            return # Cannot castle when in check
        if (white_to_move and self.current_castle_rights.w_king_side) or (
                not white_to_move and self.current_castle_rights.b_king_side):
            self.get_king_side_castle_moves(row, col, moves)

        if (white_to_move and self.current_castle_rights.w_queen_side) or (
                not white_to_move and self.current_castle_rights.b_queen_side):
            self.get_queen_side_castle_moves(row, col, moves)

    def get_king_side_castle_moves(self, row, col, moves):
        if self.board.get_piece(row, col+1) and self.board.get_piece(row, col + 2) == '--':
            if not self.square_under_attack(row, col+1) and not self.square_under_attack(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, is_castle_move = True))

    def get_queen_side_castle_moves(self, row, col, moves):
        if self.board.get_piece(row, col-1) and self.board.get_piece(row, col-2) and self.board.get_piece(row, col-3) == '--':
            if not self.square_under_attack(row, col-1) and not self.square_under_attack(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, is_castle_move = True))

