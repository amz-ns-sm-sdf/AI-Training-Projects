const API_URL = 'http://localhost:5002/api';
let currentUserId = null;
let currentUserName = null;
let currentThreadId = null;
let userThreads = [];

function simulateGoogleLogin() {
    // Simulate Google login
    const email = prompt('Enter email:', 'user@example.com');
    if (!email) return;
    
    const name = email.split('@')[0];
    
    // Simulate Google authentication
    currentUserId = email.replace('@', '_').replace('.', '_');
    currentUserName = name;
    
    // Switch to chat screen
    document.getElementById('loginScreen').classList.remove('active');
    document.getElementById('chatScreen').classList.add('active');
    document.getElementById('userDisplay').textContent = `👤 ${name}`;
    
    loadThreads();
}

async function loadThreads() {
    try {
        const response = await fetch(`${API_URL}/threads/${currentUserId}`);
        const data = await response.json();
        userThreads = data.threads || [];
        renderThreadsList();
    } catch (error) {
        console.error('Error loading threads:', error);
    }
}

function renderThreadsList() {
    const threadsList = document.getElementById('threadsList');
    threadsList.innerHTML = '';
    
    if (userThreads.length === 0) {
        threadsList.innerHTML = '<p style="color: #95a5a6; padding: 10px; font-size: 12px;">No threads yet</p>';
        return;
    }
    
    userThreads.forEach(thread => {
        const div = document.createElement('div');
        div.className = 'thread-item' + (thread.id === currentThreadId ? ' active' : '');
        div.innerHTML = `
            <span class="thread-name" onclick="selectThread('${thread.id}')">${thread.name}</span>
            <button class="thread-delete" onclick="deleteThread('${thread.id}', event)">Delete</button>
        `;
        threadsList.appendChild(div);
    });
}

async function createNewThread() {
    try {
        const response = await fetch(`${API_URL}/threads`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: currentUserId })
        });
        
        const data = await response.json();
        userThreads.push({
            id: data.thread_id,
            name: data.name,
            created_at: new Date().toISOString()
        });
        renderThreadsList();
        selectThread(data.thread_id);
    } catch (error) {
        console.error('Error creating thread:', error);
    }
}

function selectThread(threadId) {
    currentThreadId = threadId;
    const thread = userThreads.find(t => t.id === threadId);
    if (thread) {
        document.getElementById('threadTitle').value = thread.name;
    }
    document.getElementById('messages').innerHTML = '';
    document.getElementById('userInput').value = '';
    renderThreadsList();
    loadThreadMessages();
}

async function loadThreadMessages() {
    try {
        const response = await fetch(`${API_URL}/threads/${currentThreadId}/messages`);
        const data = await response.json();
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML = '';
        
        data.messages.forEach(msg => {
            displayMessage(msg.message, 'user');
            displayMessage(msg.response, 'bot');
        });
    } catch (error) {
        console.error('Error loading messages:', error);
    }
}

async function updateThreadName() {
    const newName = document.getElementById('threadTitle').value.trim();
    if (!currentThreadId || !newName) return;
    
    try {
        await fetch(`${API_URL}/threads/${currentThreadId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: newName })
        });
        
        const thread = userThreads.find(t => t.id === currentThreadId);
        if (thread) {
            thread.name = newName;
            renderThreadsList();
        }
    } catch (error) {
        console.error('Error updating thread:', error);
    }
}

async function deleteThread(threadId, event) {
    event.stopPropagation();
    if (!confirm('Delete this thread?')) return;
    
    try {
        await fetch(`${API_URL}/threads/${threadId}`, { method: 'DELETE' });
        userThreads = userThreads.filter(t => t.id !== threadId);
        if (currentThreadId === threadId) {
            currentThreadId = null;
            document.getElementById('messages').innerHTML = '';
            document.getElementById('threadTitle').value = '';
        }
        renderThreadsList();
    } catch (error) {
        console.error('Error deleting thread:', error);
    }
}

async function sendMessage() {
    if (!currentThreadId) {
        alert('Please select or create a thread first');
        return;
    }
    
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
                thread_id: currentThreadId,
                message: message
            })
        });
        
        const data = await response.json();
        displayMessage(data.response || data.error, 'bot');
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
        currentThreadId = null;
        userThreads = [];
        document.getElementById('chatScreen').classList.remove('active');
        document.getElementById('loginScreen').classList.add('active');
    }
}
