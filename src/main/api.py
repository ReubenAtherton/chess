from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Tuple, Any
from src.main.Board import Board
from src.main.GameRules import GameRules
from src.main.MoveValidator import MoveValidator
from src.main.ChessAI import ChessAI
from src.main.Move import Move

app = Flask(__name__)
CORS(app)

# Piece mapping for FEN conversion
PIECE_MAP = {
    'wp': 'P', 'wN': 'N', 'wB': 'B', 'wR': 'R', 'wQ': 'Q', 'wK': 'K',
    'bp': 'p', 'bN': 'n', 'bB': 'b', 'bR': 'r', 'bQ': 'q', 'bK': 'k'
}

# File to column mapping
FILE_MAP = {chr(97 + i): i for i in range(8)}

# Store game states
games: Dict[str, Dict[str, Any]] = {}

def get_fen(board: Board) -> str:
    """Convert board state to FEN notation."""
    fen_parts = []
    empty_count = 0
    
    for rank in range(8):
        for file in range(8):
            piece = board.get_piece(rank, file)
            if piece == "--":
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_parts.append(str(empty_count))
                    empty_count = 0
                fen_parts.append(PIECE_MAP[piece])
        if empty_count > 0:
            fen_parts.append(str(empty_count))
            empty_count = 0
        if rank < 7:
            fen_parts.append("/")
    
    return "".join(fen_parts) + " w KQkq - 0 1"

def convert_to_coords(square: str) -> Tuple[int, int]:
    """Convert algebraic notation (e.g., 'e2') to board coordinates (row, col)."""
    return (8 - int(square[1]), FILE_MAP[square[0]])

def get_game_status(game_rules: GameRules) -> str:
    """Get the current game status."""
    if game_rules.check_mate:
        return 'checkmate'
    if game_rules.stale_mate:
        return 'stalemate'
    return 'in_progress'

def create_game_response(game_id: str, board: Board) -> Dict[str, str]:
    """Create a standardized game response."""
    return {
        'game_id': game_id,
        'fen': get_fen(board),
        'message': 'Game started'
    }

@app.route('/game/start', methods=['POST'])
def start_game():
    try:
        game_id = str(len(games) + 1)
        board = Board()
        game_rules = GameRules(board)
        
        games[game_id] = {
            'board': board,
            'game_rules': game_rules,
            'validator': MoveValidator(board, game_rules),
            'ai': ChessAI(game_rules, board)
        }
        
        return jsonify(create_game_response(game_id, board))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/game/<game_id>/player-move', methods=['POST'])
def player_move(game_id: str):
    try:
        if game_id not in games:
            return jsonify({'error': 'Game not found'}), 404
            
        game = games[game_id]
        board = game['board']
        game_rules = game['game_rules']
        validator = game['validator']
        
        move = request.json.get('move')
        from_square, to_square = move[:2], move[2:]
        chess_move = Move(
            start_sq=convert_to_coords(from_square),
            end_sq=convert_to_coords(to_square),
            board=board
        )
        
        valid_moves = validator.get_valid_moves()
        if chess_move not in valid_moves:
            return jsonify({'error': 'Invalid move'}), 400
            
        current_color = 'w' if game_rules.whiteToMove else 'b'
        if chess_move.piece_moved[0] != current_color:
            return jsonify({'error': 'Not your turn'}), 400
            
        game_rules.make_move(chess_move)
        
        return jsonify({
            'fen': get_fen(board),
            'game_status': get_game_status(game_rules)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/game/<game_id>/ai-move', methods=['POST'])
def ai_move(game_id: str):
    try:
        if game_id not in games:
            return jsonify({'error': 'Game not found'}), 404
            
        game = games[game_id]
        board = game['board']
        game_rules = game['game_rules']
        validator = game['validator']
        ai = game['ai']
        
        if game_rules.whiteToMove:
            return jsonify({'error': 'Not AI\'s turn'}), 400
            
        valid_moves = validator.get_valid_moves()
        ai_move = ai.find_best_move(valid_moves) or ai.find_random_move(valid_moves)
        
        if ai_move:
            game_rules.make_move(ai_move)
            return jsonify({
                'fen': get_fen(board),
                'ai_move': ai_move.get_chess_notation(),
                'game_status': get_game_status(game_rules)
            })
        return jsonify({
            'error': 'No valid moves for AI',
            'game_status': get_game_status(game_rules)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/game/<game_id>/status', methods=['GET'])
def get_status(game_id: str):
    try:
        if game_id not in games:
            return jsonify({'error': 'Game not found'}), 404
            
        game = games[game_id]
        return jsonify({
            'fen': get_fen(game['board']),
            'status': get_game_status(game['game_rules'])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 