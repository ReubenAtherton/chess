import random
from copy import deepcopy

from src.constants.Operational import CHECKMATE, STALEMATE, piece_score, DEPTH
from src.main.MoveValidator import MoveValidator

class ChessAI:
    def __init__(self, game_rules, board):
        self.game_rules = game_rules
        self.board = board
        self.next_move = None
        self.counter = 0

    '''
    Helper method to make first recursive call
    '''
    def find_best_move(self, valid_moves):
        self.counter = 0
        self.next_move = None
        random.shuffle(valid_moves)
        # Create temporary board and game_rules for evaluation
        temp_board = deepcopy(self.board)
        temp_game_rules = deepcopy(self.game_rules)
        temp_game_rules.board = temp_board
        temp_validator = MoveValidator(temp_board, temp_game_rules)
        self.find_move_negative_max_alpha_beta(
            valid_moves,
            DEPTH,
            -CHECKMATE,
            CHECKMATE,
            1 if temp_game_rules.whiteToMove else -1,
            temp_validator,
            temp_game_rules,
            temp_board)
        # self.find_move_negative_max(
        #     valid_moves,
        #     DEPTH,
        #     1 if temp_game_rules.whiteToMove else -1,
        #     temp_validator,
        #     temp_game_rules,
        #     temp_board)

        # print(self.counter)
        # self.counter = 0

        return self.next_move

    def find_random_move(self, valid_moves):
        return valid_moves[random.randint(0, len(valid_moves)-1)]

    def find_best_move_min_max(self, valid_moves):
        validator = MoveValidator(self.board, self.game_rules)
        turn_multiplier = 1 if self.game_rules.whiteToMove else -1
        opp_min_max_score = CHECKMATE
        best_player_move = None
        random.shuffle(valid_moves)
        for player_move in valid_moves:
            self.game_rules.make_move(player_move)
            opponents_moves = validator.get_valid_moves()
            if self.game_rules.stale_mate:
                opp_max_score = STALEMATE
            elif self.game_rules.check_mate:
                opp_max_score = -CHECKMATE
            else:
                opp_max_score = -CHECKMATE
                for opp_move in opponents_moves:
                    self.game_rules.make_move(opp_move)
                    validator.get_valid_moves()
                    if self.game_rules.check_mate:
                        score = CHECKMATE
                    elif self.game_rules.stale_mate:
                        score = STALEMATE
                    else:
                        score = -turn_multiplier * self.score_board()
                    if score > opp_max_score:
                        opp_max_score = score
                    self.game_rules.undo_move()

            if opp_max_score < opp_min_max_score:
                opp_min_max_score = opp_max_score
                best_player_move = player_move
            self.game_rules.undo_move()
        return best_player_move

    def find_move_negative_max(self, valid_moves, depth, turn_multiplier, validator, game_rules, board):
        self.counter += 1
        if depth == 0:
            return turn_multiplier * self.score_board(board)
        max_score = -CHECKMATE
        for move in valid_moves:
            game_rules.make_move(move)
            next_set_of_moves = validator.get_valid_moves()
            score = -self.find_move_negative_max(next_set_of_moves, depth - 1, -turn_multiplier, validator, game_rules,
                                                 board)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    self.next_move = move
            game_rules.undo_move()
        return max_score

    def find_move_negative_max_alpha_beta(self, valid_moves, depth, alpha, beta, turn_multiplier, validator, game_rules, board):
        self.counter += 1
        if depth == 0:
            return turn_multiplier * self.score_board(board)

        #move ordering - implement later
        max_score = -CHECKMATE
        for move in valid_moves:
            game_rules.make_move(move)
            next_set_of_moves = validator.get_valid_moves()
            score = -self.find_move_negative_max_alpha_beta(next_set_of_moves, depth - 1, -beta, -alpha, -turn_multiplier, validator, game_rules,
                                                 board)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    self.next_move = move
            game_rules.undo_move()

            # Pruning
            if max_score > alpha:
                alpha = max_score
            if alpha >= beta:
                break
        return max_score

    def find_move_min_max(self, valid_moves, depth):
        self.counter += 1

        validator = MoveValidator(self.board, self.game_rules)
        random.shuffle(valid_moves)
        if depth == 0:
            return self.score_board()
        if self.game_rules.whiteToMove:  # Fixed to match attribute name
            max_score = -CHECKMATE
            for move in valid_moves:
                self.game_rules.make_move(move)
                next_moves = validator.get_valid_moves()  # Fixed parameter
                score = self.find_move_min_max(next_moves, depth - 1)
                if score > max_score:
                    max_score = score
                    if depth == DEPTH:
                        self.next_move = move
                self.game_rules.undo_move()
            return max_score  # Moved outside loop
        else:
            min_score = CHECKMATE
            for move in valid_moves:
                self.game_rules.make_move(move)
                next_moves = validator.get_valid_moves()  # Fixed parameter
                score = self.find_move_min_max(next_moves, depth - 1)
                if score < min_score:
                    min_score = score
                    if depth == DEPTH:
                        self.next_move = move
                self.game_rules.undo_move()
            return min_score

    '''
    positive score good for white
    negative score bad for white
    '''

    def score_board(self, board):
        if self.game_rules.check_mate:
            if self.game_rules.whiteToMove:
                return -CHECKMATE
            else:
                return CHECKMATE
        elif self.game_rules.stale_mate:
            return STALEMATE
        score = 0
        for row in board.board:
            for square in row:
                if square[0] == 'w':
                    score += piece_score[square[1]]
                elif square[0] == 'b':
                    score -= piece_score[square[1]]
        return score