from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# In-memory storage
users = {}
threads = {}
messages = {}
thread_counter = 0

# Sample rich media responses
SAMPLE_RESPONSES = {
    "image": """# Here's an image example:
![Sample Image](https://via.placeholder.com/400x300?text=Generated+Image)
This demonstrates image embedding in chat.""",
    
    "video": """# Video Example:
<iframe width="400" height="300" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>""",
    
    "table": """# Here's a table:
| Feature | Status | Progress |
|---------|--------|----------|
| Auth | ✅ Done | 100% |
| Chat | ✅ Done | 100% |
| Memory | ✅ Done | 100% |
| Media | 🔄 WIP | 75% |""",
    
    "formula": """# Mathematical Formula:
Here's the quadratic formula:

$$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$$

And an inline formula: $E=mc^2$""",
    
    "code": """# Code Example:
Here's some Python code:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(f"Result: {result}")
```""",
    
    "default": """# Welcome to Rich Media Chat!

This chat supports:
- **Images** (markdown format)
- **Videos** (embedded iframes)  
- **Tables** (markdown tables)
- **Formulas** (LaTeX with MathJax)
- **Code** (syntax highlighted)

Try asking about any of these features!"""
}

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat with rich media responses"""
    try:
        data = request.json
        user_id = data.get('user_id')
        thread_id = data.get('thread_id')
        message = data.get('message', '')
        
        # Determine response type based on message
        message_lower = message.lower()
        response = SAMPLE_RESPONSES['default']
        
        if 'image' in message_lower or 'photo' in message_lower:
            response = SAMPLE_RESPONSES['image']
        elif 'video' in message_lower or 'youtube' in message_lower:
            response = SAMPLE_RESPONSES['video']
        elif 'table' in message_lower or 'data' in message_lower:
            response = SAMPLE_RESPONSES['table']
        elif 'formula' in message_lower or 'equation' in message_lower or 'math' in message_lower:
            response = SAMPLE_RESPONSES['formula']
        elif 'code' in message_lower or 'python' in message_lower or 'javascript' in message_lower:
            response = SAMPLE_RESPONSES['code']
        
        # Store message
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

@app.route('/api/threads/<thread_id>/messages', methods=['GET'])
def get_thread_messages(thread_id):
    """Get all messages in a thread"""
    try:
        thread_msgs = messages.get(thread_id, [])
        return jsonify({"messages": thread_msgs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5004, use_reloader=False)
