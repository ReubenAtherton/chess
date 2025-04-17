from src.main.Castling import Castling


class GameRules:
    def __init__(self, board):
        self.board = board
        self.whiteToMove = True
        self.moveLog = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.check_mate = False
        self.stale_mate = False
        self.enpassant_possible = ()
        self.enpassant_possible_log = [self.enpassant_possible]
        self.current_castle_rights = Castling(True, True, True, True)
        self.castle_right_log = [Castling(self.current_castle_rights.w_king_side,
                                         self.current_castle_rights.b_king_side,
                                         self.current_castle_rights.w_queen_side,
                                         self.current_castle_rights.b_queen_side)]

    def make_move(self, move):
        self.board.set_piece(move.start_row, move.start_col, "--")
        self.board.move_piece(move.end_row, move.end_col, move.piece_moved)
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)
        if move.is_pawn_promotion:
            self.board.set_piece(move.end_row, move.end_col, move.piece_moved[0] + 'Q')
        if move.is_enpassant_move:
            self.board.set_piece(move.start_row, move.end_col, '--')
        if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.enpassant_possible = ()
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:
                self.board.set_piece(move.end_row, move.end_col-1, self.board.get_piece(move.end_row, move.end_col+1))
                self.board.set_piece(move.end_row, move.end_col+1, '--')
            else:
                self.board.set_piece(move.end_row, move.end_col+1, self.board.get_piece(move.end_row, move.end_col-2))
                self.board.set_piece(move.end_row, move.end_col-2, '--')
        self.enpassant_possible_log.append(self.enpassant_possible)
        self.update_castle_rights(move)
        self.castle_right_log.append(Castling(self.current_castle_rights.w_king_side,
                                             self.current_castle_rights.b_king_side,
                                             self.current_castle_rights.w_queen_side,
                                             self.current_castle_rights.b_queen_side))

    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board.set_piece(move.start_row, move.start_col, move.piece_moved)
            self.board.set_piece(move.end_row, move.end_col, move.piece_captured)
            self.whiteToMove = not self.whiteToMove
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)
            if move.is_enpassant_move:
                self.board.set_piece(move.end_row, move.end_col, '--')
                self.board.set_piece(move.start_row, move.end_col, move.piece_captured)
                self.enpassant_possible = (move.end_row, move.end_col)
            if move.piece_moved[1] == 'R' or move.piece_moved[1] == 'K':  # Fixed syntax
                self.castle_right_log.pop()
                self.current_castle_rights = self.castle_right_log[-1]
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:
                    self.board.set_piece(move.end_row, move.end_col + 1,
                                         self.board.get_piece(move.end_row, move.end_col - 1))
                    self.board.set_piece(move.end_row, move.end_col - 1, '--')
                else:
                    self.board.set_piece(move.end_row, move.end_col - 2,
                                         self.board.get_piece(move.end_row, move.end_col + 1))
                    self.board.set_piece(move.end_row, move.end_col + 1, '--')
            self.check_mate = False
            self.stale_mate = False

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