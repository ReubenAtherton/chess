import random
from platform import machine

from pydantic_core.core_schema import ChainSchema

piece_score = { 'K': 0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'p': 1 }

# Black trying to lower score, White trying to higher score
CHECKMATE = 1000
STALEMATE = 0

def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]

def find_best_move(game_state, valid_moves):
    turn_multiplier = 1 if game_state.whiteToMove else -1
    opp_min_max_score = CHECKMATE
    best_player_move = None
    random.shuffle(valid_moves)  # adds some variety in some cases

    for player_move in valid_moves:
        game_state.make_move(player_move)
        opponents_moves = game_state.get_valid_moves()
        opp_max_score = -CHECKMATE

        for opp_move in opponents_moves:
            game_state.make_move(opp_move)

            if game_state.check_mate:
                score = -turn_multiplier * CHECKMATE
            elif game_state.stale_mate:
                score = STALEMATE
            else:
                score = -turn_multiplier * score_material(game_state.board.board)
            if score > opp_max_score:
                opp_max_score = score
            game_state.undo_move()

        if opp_max_score < opp_min_max_score:
            opp_min_max_score = opp_max_score
            best_player_move = player_move
        game_state.undo_move()
    return best_player_move

'''
Score board based on material
'''
def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]

    return score