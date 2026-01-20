from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# In-memory storage for demo (replace with database in production)
users = {}
chat_messages = {}

# Models (using in-memory storage)
class ChatMessage:
    def __init__(self, user_id, message, response):
        self.user_id = user_id
        self.message = message
        self.response = response
        self.created_at = datetime.utcnow()

class User:
    def __init__(self, user_id, email, name):
        self.id = user_id
        self.email = email
        self.name = name
        self.created_at = datetime.utcnow()

# Create tables
# Base.metadata.create_all(engine)

@app.route('/api/login', methods=['POST'])
def login():
    """
    Amzur employee login
    Expected JSON: {"email": "employee@amzur.com"}
    """
    try:
        data = request.json
        email = data.get('email', '')
        
        # TODO: Validate Amzur employee email
        # For demo, accept any email
        user_id = email.replace('@', '_').replace('.', '_')
        
        if user_id not in users:
            users[user_id] = {
                'email': email,
                'name': email.split('@')[0],
                'created_at': str(datetime.utcnow())
            }
            chat_messages[user_id] = []
        
        return jsonify({"status": "logged_in", "user_id": user_id, "name": users[user_id]['name']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat-history/<user_id>', methods=['GET'])
def get_chat_history(user_id):
    """Get all chats for a user from database"""
    try:
        chats = chat_messages.get(user_id, [])
        
        return jsonify({
            "chats": chats
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests and store in DB"""
    try:
        data = request.json
        user_id = data.get('user_id')
        message = data.get('message', '')
        
        # TODO: Process with Gemini
        response = f"Bot response to: {message}"
        
        # Store in memory
        if user_id not in chat_messages:
            chat_messages[user_id] = []
        
        chat_messages[user_id].append({
            "message": message,
            "response": response,
            "created_at": str(datetime.utcnow())
        })
        
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
