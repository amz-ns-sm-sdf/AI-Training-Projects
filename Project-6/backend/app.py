from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime
import base64

load_dotenv()

app = Flask(__name__)
CORS(app)

# In-memory storage
users = {}
threads = {}
messages = {}
thread_counter = 0

# Sample image URLs (simulating generated images)
SAMPLE_IMAGES = {
    "sunset": "https://images.unsplash.com/photo-1495567720989-cebdbdd97913?w=400&h=300&fit=crop",
    "mountain": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop",
    "ocean": "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400&h=300&fit=crop",
    "forest": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=300&fit=crop",
    "city": "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400&h=300&fit=crop",
    "space": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=400&h=300&fit=crop",
    "abstract": "https://images.unsplash.com/photo-1557672172-298e090d0f80?w=400&h=300&fit=crop",
    "nature": "https://images.unsplash.com/photo-1502933691298-84fc14542831?w=400&h=300&fit=crop",
}

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat with image generation capability"""
    try:
        data = request.json
        user_id = data.get('user_id')
        thread_id = data.get('thread_id')
        message = data.get('message', '')
        
        # Check if this is an image generation request
        if 'generate' in message.lower() and 'image' in message.lower():
            return generate_image(message, thread_id, user_id)
        else:
            # Regular text response
            response = f"**Chat Response:** {message}\n\nUse 'generate image' keyword to create images!"
            return jsonify({"response": response, "type": "text"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_image(prompt, thread_id, user_id):
    """Simulate image generation"""
    try:
        # Extract image prompt from user message
        image_prompt = prompt.replace('generate image of', '').replace('generate image', '').strip()
        
        # Find matching image from sample library
        image_url = None
        for keyword, url in SAMPLE_IMAGES.items():
            if keyword in image_prompt.lower():
                image_url = url
                break
        
        if not image_url:
            # Use a default image
            image_url = SAMPLE_IMAGES['abstract']
        
        # Create markdown response with image
        response = f"""# Generated Image: {image_prompt}

![Generated: {image_prompt}]({image_url})

**Prompt:** {image_prompt}
**Model:** Gemini 2.0 Image Generation
**Generated at:** {datetime.utcnow().isoformat()}

This is a simulated image generation. In production, this would use Gemini 2.0 API."""
        
        # Store message
        if thread_id not in messages:
            messages[thread_id] = []
        
        messages[thread_id].append({
            "message": f"Generate image of {image_prompt}",
            "response": response,
            "image_url": image_url,
            "created_at": str(datetime.utcnow())
        })
        
        return jsonify({
            "response": response,
            "type": "image",
            "image_url": image_url,
            "prompt": image_prompt
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
    app.run(debug=False, port=5005, use_reloader=False)
