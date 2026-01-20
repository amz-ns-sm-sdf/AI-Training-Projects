const API_URL = 'http://localhost:5010/api';

async function loadAgentInfo() {
    try {
        const response = await fetch(`${API_URL}/agent-info`);
        const data = await response.json();
        
        const infoDiv = document.getElementById('agentInfo');
        infoDiv.innerHTML = `
            <div><span class="agent-name">${data.agent_name}</span></div>
            <div><span class="info-label">Type:</span> ${data.model_type}</div>
            <div><span class="info-label">Tools:</span> ${data.available_tools.length}</div>
            <div><span class="info-label">Memory:</span> ${data.memory_size} items</div>
        `;
        
        const toolsList = document.getElementById('toolsList');
        let html = '';
        data.available_tools.forEach(tool => {
            html += `
                <div class="tool-item">
                    <div class="tool-name">🔧 ${tool.name}</div>
                    <div class="tool-desc">${tool.description}</div>
                </div>
            `;
        });
        toolsList.innerHTML = html;
    } catch (error) {
        console.error('Error loading agent info:', error);
    }
}

async function updateMemory() {
    try {
        const response = await fetch(`${API_URL}/memory`);
        const data = await response.json();
        
        const memoryDiv = document.getElementById('memoryInfo');
        memoryDiv.innerHTML = `
            <div><span class="memory-count">Size: ${data.size}</span></div>
            <div style="font-size: 11px; color: #95a5a6; margin-top: 5px;">
                ${data.size > 0 ? `Last: ${new Date(data.last_updated).toLocaleTimeString()}` : 'Empty'}
            </div>
        `;
    } catch (error) {
        console.error('Error updating memory:', error);
    }
}

async function queryAgent() {
    const userInput = document.getElementById('userInput');
    const query = userInput.value.trim();
    
    if (!query) return;
    
    displayMessage(query, 'user');
    userInput.value = '';
    
    try {
        const response = await fetch(`${API_URL}/act`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        if (response.ok) {
            displayAgentResponse(data.result);
            updateMemory();
        } else {
            displayMessage('Error: ' + data.error, 'agent');
        }
    } catch (error) {
        displayMessage('Connection error: ' + error, 'agent');
    }
}

function displayMessage(text, sender) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender === 'user' ? 'user-query' : 'agent-response'}`;
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function displayAgentResponse(result) {
    const messagesDiv = document.getElementById('messages');
    const responseDiv = document.createElement('div');
    responseDiv.className = 'message agent-response';
    
    let html = '<strong>Agent Thinking Process:</strong><br>';
    
    // Thought process
    html += '<div class="thought-box">';
    result.thought_process.forEach((thought, idx) => {
        html += `<div class="thought-item">→ ${thought}</div>`;
    });
    html += '</div>';
    
    // Tool selection
    html += `<div class="tool-box">
        <div class="tool-selected">🔧 Selected Tool: ${result.tool_selected}</div>
        <div style="margin-top: 5px; color: #333;">Input: ${result.tool_response.input}</div>
        <div style="color: #333;">Output: ${result.tool_response.output}</div>
    </div>`;
    
    // Final answer
    html += `<div class="final-answer">✓ ${result.final_answer}</div>`;
    
    responseDiv.innerHTML = html;
    messagesDiv.appendChild(responseDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        queryAgent();
    }
}

window.addEventListener('load', () => {
    loadAgentInfo();
    updateMemory();
});
