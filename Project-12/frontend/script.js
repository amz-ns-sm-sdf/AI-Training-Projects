const API_URL = 'http://localhost:5011/api';
let gameState = {};

async function newGame() {
    try {
        const response = await fetch(`${API_URL}/game/new`, {
            method: 'POST'
        });
        const data = await response.json();
        gameState = { board: data.board };
        updateBoard();
        document.getElementById('status').textContent = 'Your Turn (X)';
        document.getElementById('moveLog').innerHTML = '';
    } catch (error) {
        console.error('Error:', error);
    }
}

async function getGameState() {
    try {
        const response = await fetch(`${API_URL}/game/state`);
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

async function playerMove(position) {
    const state = await getGameState();
    if (state && state.game_over) {
        alert('Game is over. Start a new game!');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/game/move`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ position })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            gameState.board = data.board;
            updateBoard();
            
            addMoveLog('X', position);
            
            if (data.agent_move !== undefined) {
                addMoveLog('O', data.agent_move);
            }
            
            // Handle game result
            if (data.result === 'human_wins') {
                document.getElementById('status').textContent = '🎉 You Win!';
            } else if (data.result === 'agent_wins') {
                document.getElementById('status').textContent = '🤖 Agent Wins!';
            } else if (data.result === 'draw') {
                document.getElementById('status').textContent = '🤝 Draw!';
            } else {
                document.getElementById('status').textContent = 'Agent Turn...';
                setTimeout(() => {
                    document.getElementById('status').textContent = 'Your Turn (X)';
                }, 1000);
            }
        } else {
            alert('Invalid move');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function updateBoard() {
    const cells = document.querySelectorAll('.cell');
    gameState.board.forEach((value, index) => {
        cells[index].textContent = value;
        cells[index].className = 'cell';
        if (value === 'X') cells[index].classList.add('x');
        if (value === 'O') cells[index].classList.add('o');
    });
}

function addMoveLog(player, position) {
    const log = document.getElementById('moveLog');
    const item = document.createElement('div');
    item.className = 'move-item';
    const playerText = player === 'X' ? '<span class="player-x">You (X)</span>' : '<span class="player-o">Agent (O)</span>';
    const posName = ['Top-Left', 'Top', 'Top-Right', 'Left', 'Center', 'Right', 'Bottom-Left', 'Bottom', 'Bottom-Right'][position];
    item.innerHTML = `${playerText} → ${posName}`;
    log.appendChild(item);
    log.scrollTop = log.scrollHeight;
}

// Initialize game
window.addEventListener('load', newGame);
