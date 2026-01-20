from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime
from collections import deque

load_dotenv()

app = Flask(__name__)
CORS(app)

# In-memory storage for demo
users = {}
threads = {}
messages = {}
memory_buffers = {}  # Stores last 5 messages per thread
thread_counter = 0

def get_memory_for_thread(thread_id):
    """Get or create memory buffer for a thread (last 5 messages)"""
    if thread_id not in memory_buffers:
        memory_buffers[thread_id] = deque(maxlen=5)
    return memory_buffers[thread_id]

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat with memory context
    Expected JSON: {"user_id": "...", "thread_id": "...", "message": "..."}
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        thread_id = data.get('thread_id')
        message = data.get('message', '')
        
        # Get memory for this thread
        memory = get_memory_for_thread(thread_id)
        
        # Build context from previous messages
        context = "\n".join([f"User: {m[0]}\nBot: {m[1]}" for m in memory])
        
        # Generate response with context
        if context:
            response = f"[Context aware] Response to: {message} (considering previous: {len(memory)} messages)"
        else:
            response = f"[New conversation] Response to: {message}"
        
        # Add to memory
        memory.append((message, response))
        
        # Store in messages
        if thread_id not in messages:
            messages[thread_id] = []
        
        messages[thread_id].append({
            "message": message,
            "response": response,
            "created_at": str(datetime.utcnow())
        })
        
        return jsonify({
            "response": response,
            "memory_size": len(memory)
        })
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
        memory_buffers[thread_id] = deque(maxlen=5)
        
        return jsonify({"thread_id": thread_id, "name": thread_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/threads/<thread_id>/messages', methods=['GET'])
def get_thread_messages(thread_id):
    """Get all messages in a thread"""
    try:
        thread_msgs = messages.get(thread_id, [])
        memory = memory_buffers.get(thread_id, [])
        return jsonify({
            "messages": thread_msgs,
            "memory_size": len(memory),
            "memory_max": 5
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5003, use_reloader=False)
