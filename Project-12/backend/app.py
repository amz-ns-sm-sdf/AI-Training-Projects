from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Game state
game_state = {
    'board': [' ' for _ in range(9)],
    'human': 'X',
    'agent': 'O',
    'current_turn': 'human',
    'game_over': False,
    'winner': None,
    'moves': []
}

def print_board(board):
    """Return board as list of 9 cells"""
    return board

def check_winner(board):
    """Check if there's a winner"""
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    
    return None

def is_board_full(board):
    """Check if board is full"""
    return ' ' not in board

def agent_move(board):
    """Agent (O) makes a move using strategy"""
    # Check if agent can win
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if check_winner(board) == 'O':
                return i
            board[i] = ' '
    
    # Block human from winning
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if check_winner(board) == 'X':
                board[i] = ' '
                return i
            board[i] = ' '
    
    # Take center
    if board[4] == ' ':
        return 4
    
    # Take corners
    corners = [0, 2, 6, 8]
    available_corners = [i for i in corners if board[i] == ' ']
    if available_corners:
        return random.choice(available_corners)
    
    # Take any available
    available = [i for i in range(9) if board[i] == ' ']
    return random.choice(available) if available else -1

@app.route('/api/game/new', methods=['POST'])
def new_game():
    """Start new game"""
    global game_state
    game_state = {
        'board': [' ' for _ in range(9)],
        'human': 'X',
        'agent': 'O',
        'current_turn': 'human',
        'game_over': False,
        'winner': None,
        'moves': []
    }
    return jsonify({"status": "success", "board": game_state['board']})

@app.route('/api/game/state', methods=['GET'])
def get_state():
    """Get current game state"""
    return jsonify(game_state)

@app.route('/api/game/move', methods=['POST'])
def make_move():
    """Human makes a move"""
    global game_state
    try:
        data = request.json
        position = data.get('position')
        
        if position < 0 or position > 8 or game_state['board'][position] != ' ':
            return jsonify({"error": "Invalid move"}), 400
        
        # Human move
        game_state['board'][position] = 'X'
        game_state['moves'].append({'player': 'human', 'position': position})
        
        # Check if human won
        if check_winner(game_state['board']) == 'X':
            game_state['game_over'] = True
            game_state['winner'] = 'human'
            return jsonify({"status": "success", "result": "human_wins", "board": game_state['board']})
        
        # Check if board full
        if is_board_full(game_state['board']):
            game_state['game_over'] = True
            game_state['winner'] = 'draw'
            return jsonify({"status": "success", "result": "draw", "board": game_state['board']})
        
        # Agent move
        agent_pos = agent_move(game_state['board'])
        game_state['board'][agent_pos] = 'O'
        game_state['moves'].append({'player': 'agent', 'position': agent_pos})
        
        # Check if agent won
        if check_winner(game_state['board']) == 'O':
            game_state['game_over'] = True
            game_state['winner'] = 'agent'
            return jsonify({"status": "success", "result": "agent_wins", "agent_move": agent_pos, "board": game_state['board']})
        
        # Check if board full
        if is_board_full(game_state['board']):
            game_state['game_over'] = True
            game_state['winner'] = 'draw'
            return jsonify({"status": "success", "result": "draw", "agent_move": agent_pos, "board": game_state['board']})
        
        return jsonify({"status": "success", "agent_move": agent_pos, "board": game_state['board']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5011, use_reloader=False)
