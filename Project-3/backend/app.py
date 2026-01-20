from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid

load_dotenv()

app = Flask(__name__)
CORS(app)

# In-memory storage for demo
users = {}
threads = {}
messages = {}
thread_counter = 0

@app.route('/api/auth/google', methods=['POST'])
def google_login():
    """Handle Google OAuth login"""
    try:
        data = request.json
        email = data.get('email')
        name = data.get('name')
        
        user_id = email.replace('@', '_').replace('.', '_')
        
        if user_id not in users:
            users[user_id] = {
                'email': email,
                'name': name,
                'created_at': str(datetime.utcnow())
            }
            threads[user_id] = []
        
        return jsonify({"status": "logged_in", "user_id": user_id, "name": name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/threads/<user_id>', methods=['GET'])
def get_threads(user_id):
    """Get all threads for a user"""
    try:
        user_threads = threads.get(user_id, [])
        return jsonify({"threads": user_threads})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/threads', methods=['POST'])
def create_thread():
    """Create a new chat thread"""
    try:
        global thread_counter
        data = request.json
        user_id = data.get('user_id')
        
        thread_counter += 1
        thread_id = str(thread_counter)
        thread_name = f"Thread {thread_counter}"
        
        thread_obj = {
            'id': thread_id,
            'name': thread_name,
            'created_at': str(datetime.utcnow())
        }
        
        if user_id not in threads:
            threads[user_id] = []
        
        threads[user_id].append(thread_obj)
        messages[thread_id] = []
        
        return jsonify({"thread_id": thread_id, "name": thread_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/threads/<thread_id>', methods=['PUT'])
def update_thread(thread_id):
    """Update thread name"""
    try:
        data = request.json
        name = data.get('name')
        
        # Find and update thread
        for user_id in threads:
            for thread in threads[user_id]:
                if thread['id'] == thread_id:
                    thread['name'] = name
                    return jsonify({"status": "updated"})
        
        return jsonify({"error": "Thread not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/threads/<thread_id>', methods=['DELETE'])
def delete_thread(thread_id):
    """Delete a thread"""
    try:
        # Find and delete thread
        for user_id in threads:
            threads[user_id] = [t for t in threads[user_id] if t['id'] != thread_id]
        
        if thread_id in messages:
            del messages[thread_id]
        
        return jsonify({"status": "deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/threads/<thread_id>/messages', methods=['GET'])
def get_thread_messages(thread_id):
    """Get all messages in a thread"""
    try:
        thread_msgs = messages.get(thread_id, [])
        return jsonify({"messages": thread_msgs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat in a thread"""
    try:
        data = request.json
        thread_id = data.get('thread_id')
        message = data.get('message', '')
        
        response = f"Response to: {message}"
        
        if thread_id not in messages:
            messages[thread_id] = []
        
        messages[thread_id].append({
            "message": message,
            "response": response,
            "created_at": str(datetime.utcnow())
        })
        
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5002, use_reloader=False)
