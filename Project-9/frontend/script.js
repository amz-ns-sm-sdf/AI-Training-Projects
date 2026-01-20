const API_URL = 'http://localhost:5008/api';
let currentSheet = 'Sales';

async function loadSheets() {
    try {
        const response = await fetch(`${API_URL}/sheets`);
        const data = await response.json();
        
        const sheetsList = document.getElementById('sheetsList');
        let html = '';
        data.sheets.forEach(sheet => {
            html += `
                <div class="sheet-item ${sheet.name === 'Sales' ? 'active' : ''}" onclick="selectSheet('${sheet.name}')">
                    <div class="sheet-name">${sheet.name}</div>
                    <div class="sheet-desc">${sheet.description}</div>
                </div>
            `;
        });
        sheetsList.innerHTML = html;
        loadSheetPreview('Sales');
    } catch (error) {
        console.error('Error loading sheets:', error);
    }
}

async function selectSheet(sheetName) {
    currentSheet = sheetName;
    document.querySelectorAll('.sheet-item').forEach(el => el.classList.remove('active'));
    event.target.closest('.sheet-item').classList.add('active');
    loadSheetPreview(sheetName);
}

async function loadSheetPreview(sheetName) {
    try {
        const response = await fetch(`${API_URL}/sheet/${sheetName}`);
        const data = await response.json();
        
        const preview = document.getElementById('sheetPreview');
        let html = `<strong>${data.name}</strong> (${data.row_count} rows)<br>`;
        html += '<table class="preview-table"><tr>';
        
        data.headers.forEach(header => {
            html += `<th>${header}</th>`;
        });
        html += '</tr>';
        
        data.rows.slice(0, 3).forEach(row => {
            html += '<tr>';
            row.forEach(cell => {
                html += `<td>${cell}</td>`;
            });
            html += '</tr>';
        });
        html += '</table>';
        
        preview.innerHTML = html;
    } catch (error) {
        console.error('Error loading sheet preview:', error);
    }
}

function loadSampleQueries() {
    const sampleQueries = [
        "Show north region sales",
        "What is total revenue",
        "List laptop sales",
        "Engineering department",
        "Highest salary"
    ];
    
    const samplesDiv = document.getElementById('sampleQueries');
    let html = '';
    sampleQueries.forEach(query => {
        html += `<div class="sample-query" onclick="useSample('${query}')">${query}</div>`;
    });
    samplesDiv.innerHTML = html;
}

function useSample(query) {
    document.getElementById('userInput').value = query;
    sendQuery();
}

async function sendQuery() {
    const userInput = document.getElementById('userInput');
    const query = userInput.value.trim();
    
    if (!query) return;
    
    displayMessage(query, 'user');
    userInput.value = '';
    
    try {
        const response = await fetch(`${API_URL}/query-sheet`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                sheet: currentSheet,
                query: query 
            })
        });
        
        const data = await response.json();
        if (response.ok) {
            displayQueryResult(data);
        } else {
            displayMessage('Error: ' + data.error, 'bot');
        }
    } catch (error) {
        displayMessage('Error: ' + error, 'bot');
        console.error('Error:', error);
    }
}

function displayQueryResult(data) {
    const messagesDiv = document.getElementById('messages');
    const resultDiv = document.createElement('div');
    resultDiv.className = 'message bot-message';
    
    let html = `<strong>${data.result.description}</strong><br>`;
    
    if (data.result.filtered_data) {
        const headers = data.headers;
        html += '<table class="result-table"><tr>';
        headers.forEach(h => html += `<th>${h}</th>`);
        html += '</tr>';
        data.result.filtered_data.forEach(row => {
            html += '<tr>';
            row.forEach(cell => html += `<td>${cell}</td>`);
            html += '</tr>';
        });
        html += '</table>';
    } else if (data.result.all_data) {
        const headers = data.headers;
        html += '<table class="result-table"><tr>';
        headers.forEach(h => html += `<th>${h}</th>`);
        html += '</tr>';
        data.result.all_data.forEach(row => {
            html += '<tr>';
            row.forEach(cell => html += `<td>${cell}</td>`);
            html += '</tr>';
        });
        html += '</table>';
    } else if (data.result.result) {
        if (Array.isArray(data.result.result)) {
            html += `<strong>${data.result.result.join(' - ')}</strong>`;
        } else {
            html += `<strong>${data.result.result}</strong>`;
        }
    }
    
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

window.addEventListener('load', () => {
    loadSheets();
    loadSampleQueries();
});
