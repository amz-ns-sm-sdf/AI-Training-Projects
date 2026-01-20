const API_URL = 'http://localhost:5000/api';
const md = window.markdownit({
    html: true,
    linkify: true,
    typographer: true,
    highlight: function (str, lang) {
        if (lang && window.hljs.getLanguage(lang)) {
            try {
                return '<pre class="hljs"><code>' +
                    window.hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
                    '</code></pre>';
            } catch (__) {}
        }
        return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
    }
});

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Display user message
    displayMessage(message, 'user');
    userInput.value = '';
    
    try {
        // Send to backend
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
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
    
    if (sender === 'bot') {
        // Render markdown for bot messages
        messageDiv.innerHTML = md.render(text);
        // Trigger MathJax to render formulas
        if (window.MathJax) {
            MathJax.typesetPromise([messageDiv]).catch(err => console.log(err));
        }
    } else {
        messageDiv.textContent = text;
    }
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
