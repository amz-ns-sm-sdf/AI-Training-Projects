const API_URL = 'http://localhost:5001/api';
let currentUserId = null;
let currentUserName = null;

async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('emailInput').value.trim();
    
    if (!email) {
        alert('Please enter an email');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        if (response.ok) {
            currentUserId = data.user_id;
            currentUserName = data.name;
            document.getElementById('userName').textContent = `Welcome, ${data.name}`;
            document.getElementById('emailInput').value = '';
            document.getElementById('loginScreen').classList.remove('active');
            document.getElementById('chatScreen').classList.add('active');
            loadChatHistory();
        } else {
            alert('Login failed: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error);
        console.error('Error:', error);
    }
}

async function loadChatHistory() {
    try {
        const response = await fetch(`${API_URL}/chat-history/${currentUserId}`);
        const data = await response.json();
        
        const historyDiv = document.getElementById('chatHistory');
        if (data.chats && data.chats.length > 0) {
            historyDiv.innerHTML = `<strong>Previous conversations:</strong><br>` + 
                data.chats.slice(-3).map(c => `"${c.message}"<br>`).join('');
        } else {
            historyDiv.innerHTML = 'No previous conversations';
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (!message) return;
    
    displayMessage(message, 'user');
    userInput.value = '';
    
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: currentUserId,
                message: message
            })
        });
        
        const data = await response.json();
        displayMessage(data.response || data.error, 'bot');
        loadChatHistory();
    } catch (error) {
        displayMessage('Error connecting to server', 'bot');
        console.error('Error:', error);
    }
}

function displayMessage(text, sender) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        currentUserId = null;
        currentUserName = null;
        document.getElementById('messages').innerHTML = '';
        document.getElementById('chatHistory').innerHTML = '';
        document.getElementById('emailInput').value = '';
        document.getElementById('chatScreen').classList.remove('active');
        document.getElementById('loginScreen').classList.add('active');
    }
}
