const API_URL = 'http://localhost:5000/api';
let selectedDocument = null;

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file || !file.name.endsWith('.pdf')) {
        alert('Please select a PDF file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        if (response.ok) {
            alert(`File uploaded successfully! ${data.chunks} chunks created.`);
            fileInput.value = '';
            loadDocuments();
        } else {
            alert('Error uploading file: ' + data.error);
        }
    } catch (error) {
        alert('Error uploading file: ' + error);
        console.error('Error:', error);
    }
}

async function loadDocuments() {
    try {
        const response = await fetch(`${API_URL}/documents`);
        const data = await response.json();
        
        const docList = document.getElementById('documentList');
        docList.innerHTML = '';
        
        if (data.documents && data.documents.length > 0) {
            data.documents.forEach(doc => {
                const div = document.createElement('div');
                div.className = 'document-item';
                if (doc === selectedDocument) {
                    div.classList.add('active');
                }
                
                div.innerHTML = `
                    <span onclick="selectDocument('${doc}')" style="flex: 1; cursor: pointer;">${doc}</span>
                    <button class="delete-btn" onclick="deleteDocument('${doc}')">Delete</button>
                `;
                docList.appendChild(div);
            });
        } else {
            docList.innerHTML = '<p style="color: #95a5a6; font-size: 12px;">No documents uploaded yet</p>';
        }
    } catch (error) {
        console.error('Error loading documents:', error);
    }
}

function selectDocument(docName) {
    selectedDocument = docName;
    loadDocuments();
}

async function deleteDocument(docName) {
    if (!confirm(`Delete document "${docName}"?`)) return;
    
    try {
        const response = await fetch(`${API_URL}/documents/${docName}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            selectedDocument = null;
            loadDocuments();
        }
    } catch (error) {
        console.error('Error deleting document:', error);
    }
}

async function sendMessage() {
    if (!selectedDocument) {
        alert('Please upload and select a document first');
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
                collection: selectedDocument
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

// Load documents on page load
window.addEventListener('load', loadDocuments);
