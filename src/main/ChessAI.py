import random

from src.dimen.dimen import CHECKMATE, STALEMATE, piece_score
from src.main.MoveValidator import MoveValidator

class ChessAI:
    def __init__(self, game_rules, board):
        self.game_rules = game_rules
        self.board = board

    def find_random_move(self, valid_moves):
        return valid_moves[random.randint(0, len(valid_moves)-1)]

    def find_best_move(self, valid_moves):
        validator = MoveValidator(self.board, self.game_rules)
        turn_multiplier = 1 if self.game_rules.whiteToMove else -1
        opp_min_max_score = CHECKMATE
        best_player_move = None
        random.shuffle(valid_moves)
        for player_move in valid_moves:
            self.game_rules.make_move(player_move)
            opponents_moves = validator.get_valid_moves()
            opp_max_score = -CHECKMATE
            for opp_move in opponents_moves:
                self.game_rules.make_move(opp_move)
                if self.game_rules.check_mate:
                    score = -turn_multiplier * CHECKMATE
                elif self.game_rules.stale_mate:
                    score = STALEMATE
                else:
                    score = -turn_multiplier * self.score_material(self.board.board)
                if score > opp_max_score:
                    opp_max_score = score
                self.game_rules.undo_move()
            if opp_max_score < opp_min_max_score:
                opp_min_max_score = opp_max_score
                best_player_move = player_move
            self.game_rules.undo_move()
        return best_player_move

    def score_material(self, board):
        score = 0
        for row in board:
            for square in row:
                if square[0] == 'w':
                    score += piece_score[square[1]]
                elif square[0] == 'b':
                    score -= piece_score[square[1]]
        return score