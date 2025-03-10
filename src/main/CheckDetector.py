class CheckDetector:
    def __init__(self, board):
        self.board = board

    # Complex algo - checks all possible attackers from kings perspective
    # Faster than checking every possible move to see if it attacks king
    def check_for_pins_and_checks(self, white_to_move, white_king_location, black_king_location):
        pins, checks  = [], []
        is_checked_temp = False

        if white_to_move:
            enemy_colour = "b"
            friendly_colour = "w"
            start_row = white_king_location[0]
            start_col = white_king_location[1]

        else:
            enemy_colour = "w"
            friendly_colour = "b"
            start_row = black_king_location[0]
            start_col = black_king_location[1]

        # All moves king can be attacked from
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

        for j in range(len(directions)):
            d = directions[j]
            possible_pins = ()
            for i in range (1, 8):
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
                end_piece = self.board.get_piece(end_row, end_col)
                if end_piece[0] == enemy_colour and end_piece[1] == 'N':  # enemy knight attacking a king
                    is_checked_temp = True
                    checks.append((end_row, end_col, move[0], move[1]))

        return is_checked_temp, pins, checks