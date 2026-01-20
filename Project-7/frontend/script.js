const API_URL = 'http://localhost:5006/api';
const md = window.markdownit();
let selectedDocument = null;
let documents = [];

async function loadSampleDocuments() {
    try {
        const response = await fetch(`${API_URL}/documents/sample`, {
            method: 'POST'
        });
        
        const data = await response.json();
        if (response.ok) {
            await loadDocuments();
        } else {
            alert('Error loading samples: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error);
        console.error('Error:', error);
    }
}

async function loadDocuments() {
    try {
        const response = await fetch(`${API_URL}/documents`);
        const data = await response.json();
        
        documents = data.documents || [];
        const docList = document.getElementById('documentList');
        docList.innerHTML = '';
        
        if (documents && documents.length > 0) {
            documents.forEach(doc => {
                const div = document.createElement('div');
                div.className = 'document-item';
                if (doc.id === selectedDocument) {
                    div.classList.add('active');
                }
                
                div.innerHTML = `
                    <div>
                        <div class="doc-name" onclick="selectDocument('${doc.id}')" style="cursor: pointer;">${doc.name}</div>
                        <div class="doc-info">${doc.chunks} chunks</div>
                    </div>
                    <button class="delete-btn" onclick="deleteDocument('${doc.id}')">Delete</button>
                `;
                docList.appendChild(div);
            });
        } else {
            docList.innerHTML = '<p style="color: #95a5a6; font-size: 12px; text-align: center; padding: 20px;">No documents loaded</p>';
        }
        
        updateSelectedDocDisplay();
    } catch (error) {
        console.error('Error loading documents:', error);
    }
}

function selectDocument(docId) {
    selectedDocument = docId;
    loadDocuments();
    clearMessages();
}

function updateSelectedDocDisplay() {
    const docDiv = document.getElementById('selectedDoc');
    if (selectedDocument) {
        const doc = documents.find(d => d.id === selectedDocument);
        docDiv.textContent = `📖 ${doc ? doc.name : 'Unknown'}`;
    } else {
        docDiv.textContent = 'Select a document to start';
    }
}

async function deleteDocument(docId) {
    if (!confirm('Delete this document?')) return;
    
    try {
        const response = await fetch(`${API_URL}/documents/${docId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            if (selectedDocument === docId) {
                selectedDocument = null;
            }
            await loadDocuments();
        }
    } catch (error) {
        console.error('Error deleting document:', error);
    }
}

function clearAllDocs() {
    if (!confirm('Delete ALL documents?')) return;
    documents.forEach(doc => deleteDocument(doc.id));
}

async function sendMessage() {
    if (!selectedDocument) {
        alert('Please load and select a document first');
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
                message: message,
                doc_id: selectedDocument
            })
        });
        
        const data = await response.json();
        if (response.ok) {
            displayMessage(data.response, 'bot');
        } else {
            displayMessage('Error: ' + data.error, 'bot');
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
        messageDiv.innerHTML = md.render(text);
    } else {
        messageDiv.textContent = text;
    }
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function clearMessages() {
    document.getElementById('messages').innerHTML = '';
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Load documents on page load
window.addEventListener('load', loadDocuments);

