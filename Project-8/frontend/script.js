const API_URL = 'http://localhost:5007/api';

async function loadSchema() {
    try {
        const response = await fetch(`${API_URL}/schema`);
        const data = await response.json();
        const schemaDiv = document.getElementById('schemaInfo');
        
        let html = '';
        for (const [table, columns] of Object.entries(data.tables)) {
            html += `<div class="table-name">📊 ${table}</div>`;
            columns.forEach(col => {
                html += `<div class="column">• ${col}</div>`;
            });
        }
        schemaDiv.innerHTML = html;
    } catch (error) {
        console.error('Error loading schema:', error);
    }
}

async function loadSampleQueries() {
    try {
        const response = await fetch(`${API_URL}/samples`);
        const data = await response.json();
        const samplesDiv = document.getElementById('sampleQueries');
        
        let html = '';
        data.samples.forEach((sample, idx) => {
            html += `
                <div class="sample-query" onclick="useSample('${sample.prompt}')">
                    <div class="query-text">${idx + 1}. ${sample.prompt}</div>
                    <div class="query-desc">${sample.description}</div>
                </div>
            `;
        });
        samplesDiv.innerHTML = html;
    } catch (error) {
        console.error('Error loading samples:', error);
    }
}

function useSample(prompt) {
    document.getElementById('userInput').value = prompt;
    sendQuery();
}

async function sendQuery() {
    const userInput = document.getElementById('userInput');
    const query = userInput.value.trim();
    
    if (!query) return;
    
    displayMessage(query, 'user');
    userInput.value = '';
    
    try {
        const response = await fetch(`${API_URL}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        if (response.ok) {
            displayQueryResult(data);
        } else {
            displayMessage('Error: ' + data.error, 'bot');
        }
    } catch (error) {
        displayMessage('Connection error: ' + error, 'bot');
        console.error('Error:', error);
    }
}

function displayQueryResult(data) {
    const messagesDiv = document.getElementById('messages');
    const resultDiv = document.createElement('div');
    resultDiv.className = 'message bot-message';
    
    let html = '<strong>Query Result:</strong>';
    html += `<div class="sql-display">SQL: ${data.sql_generated}</div>`;
    
    // Display results as table
    if (Array.isArray(data.results) && data.results.length > 0) {
        const firstRow = data.results[0];
        const keys = Object.keys(firstRow);
        
        html += '<table class="result-table"><tr>';
        keys.forEach(key => {
            html += `<th>${key}</th>`;
        });
        html += '</tr>';
        
        data.results.forEach(row => {
            html += '<tr>';
            keys.forEach(key => {
                html += `<td>${row[key]}</td>`;
            });
            html += '</tr>';
        });
        html += '</table>';
    }
    
    html += `<div class="row-count">✓ Returned ${data.row_count} row(s)</div>`;
    
    resultDiv.innerHTML = html;
    messagesDiv.appendChild(resultDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
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
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendQuery();
    }
}

// Load on page load
window.addEventListener('load', () => {
    loadSchema();
    loadSampleQueries();
});
