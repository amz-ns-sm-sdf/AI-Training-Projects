const API_URL = 'http://localhost:5005/api';
let currentUserId = null;
let currentUserName = null;
let currentThreadId = null;
let userThreads = [];

// Initialize Markdown-it
const md = window.markdownit({
    html: true,
    linkify: true,
    typographer: true
});

async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('emailInput').value.trim();
    
    if (!email) {
        alert('Please enter an email');
        return;
    }
    
    currentUserId = email.replace('@', '_').replace('.', '_');
    currentUserName = email.split('@')[0];
    
    document.getElementById('emailInput').value = '';
    document.getElementById('userDisplay').textContent = `👤 ${currentUserName}`;
    document.getElementById('loginScreen').classList.remove('active');
    document.getElementById('chatScreen').classList.add('active');
    
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
        div.textContent = thread.name;
        div.onclick = () => selectThread(thread.id);
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
        document.getElementById('threadTitle').textContent = thread.name;
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
            if (msg.image_url) {
                displayImageMessage(msg.response, msg.image_url);
            } else {
                displayMessage(msg.response, 'bot');
            }
        });
    } catch (error) {
        console.error('Error loading messages:', error);
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
                user_id: currentUserId,
                thread_id: currentThreadId,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (data.type === 'image') {
            displayImageMessage(data.response, data.image_url);
        } else {
            displayMessage(data.response || data.error, 'bot');
        }
    } catch (error) {
        displayMessage('Error connecting to server', 'bot');
        console.error('Error:', error);
    }
}

function displayMessage(text, sender) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    if (sender === 'bot') {
        // Render markdown for bot messages
        messageDiv.innerHTML = md.render(text);
    } else {
        messageDiv.textContent = text;
    }
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function displayImageMessage(text, imageUrl) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message image-message';
    
    // Render markdown for text content
    messageDiv.innerHTML = md.render(text);
    
    // Ensure image is displayed
    const images = messageDiv.querySelectorAll('img');
    images.forEach(img => {
        img.style.maxWidth = '100%';
        img.style.borderRadius = '8px';
        img.style.marginTop = '15px';
        img.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
    });
    
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
