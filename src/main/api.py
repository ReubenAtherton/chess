from flask import Flask, request, jsonify
from flask_cors import CORS
from src.main.Board import Board
from src.main.GameRules import GameRules
from src.main.MoveValidator import MoveValidator
from src.main.ChessAI import ChessAI
from src.main.Move import Move

app = Flask(__name__)
CORS(app)  # Add this line


def get_fen(board):
    """Convert board state to FEN notation"""
    fen = ""
    empty_count = 0
    
    for rank in range(8):
        for file in range(8):
            piece = board.get_piece(rank, file)
            if piece == "--":
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                piece_map = {
                    'wp': 'P', 'wN': 'N', 'wB': 'B', 'wR': 'R', 'wQ': 'Q', 'wK': 'K',
                    'bp': 'p', 'bN': 'n', 'bB': 'b', 'bR': 'r', 'bQ': 'q', 'bK': 'k'
                }
                fen += piece_map[piece]
        if empty_count > 0:
            fen += str(empty_count)
            empty_count = 0
        if rank < 7:
            fen += "/"
    
    fen += " w KQkq - 0 1"
    return fen

def convert_to_coords(square):
    """Convert algebraic notation (e.g., 'e2') to board coordinates (row, col)"""
    file_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    rank = 8 - int(square[1])
    file = file_map[square[0]]
    return (rank, file)

# Store game states (in production, use Redis or DynamoDB)
games = {}

@app.route('/game/start', methods=['POST'])
def start_game():
    try:
        # Initialize new game
        board = Board()
        game_rules = GameRules(board)
        validator = MoveValidator(board, game_rules)
        ai = ChessAI(game_rules, board)
        
        # Generate game ID
        game_id = str(len(games) + 1)
        
        # Store game state
        games[game_id] = {
            'board': board,
            'game_rules': game_rules,
            'validator': validator,
            'ai': ai
        }
        
        return jsonify({
            'game_id': game_id,
            'fen': get_fen(board),  # You'll need to implement this
            'message': 'Game started'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/game/<game_id>/player-move', methods=['POST'])
def player_move(game_id):
    try:
        data = request.json
        move = data.get('move')
        
        if game_id not in games:
            return jsonify({'error': 'Game not found'}), 404
            
        game = games[game_id]
        board = game['board']
        game_rules = game['game_rules']
        validator = game['validator']
        
        # Convert move from algebraic notation to coordinates
        from_square = move[:2]
        to_square = move[2:]
        
        # Create move object
        chess_move = Move(
            start_sq=convert_to_coords(from_square),
            end_sq=convert_to_coords(to_square),
            board=board
        )
        
        # Validate and make move
        valid_moves = validator.get_valid_moves()
        if chess_move not in valid_moves:
            return jsonify({'error': 'Invalid move'}), 400
            
        # Only allow moves for the current player's color
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
def ai_move(game_id):
    try:
        if game_id not in games:
            return jsonify({'error': 'Game not found'}), 404
            
        game = games[game_id]
        board = game['board']
        game_rules = game['game_rules']
        validator = game['validator']
        ai = game['ai']
        
        # Only allow AI to move if it's black's turn
        if game_rules.whiteToMove:
            return jsonify({'error': 'Not AI\'s turn'}), 400
            
        # Get AI's move
        valid_moves = validator.get_valid_moves()
        ai_move = ai.find_best_move(valid_moves)
        if ai_move is None:  # If no best move found, try random move
            ai_move = ai.find_random_move(valid_moves)
            
        if ai_move:
            game_rules.make_move(ai_move)
            return jsonify({
                'fen': get_fen(board),
                'ai_move': ai_move.get_chess_notation(),
                'game_status': get_game_status(game_rules)
            })
        else:
            return jsonify({
                'error': 'No valid moves for AI',
                'game_status': get_game_status(game_rules)
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/game/<game_id>/status', methods=['GET'])
def get_status(game_id):
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

def get_game_status(game_rules):
    if game_rules.check_mate:
        return 'checkmate'
    elif game_rules.stale_mate:
        return 'stalemate'
    return 'in_progress'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 