from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import io
import base64
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Create generated_images directory if it doesn't exist
IMAGES_DIR = 'generated_images'
os.makedirs(IMAGES_DIR, exist_ok=True)

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat requests with image generation capability
    Expected JSON: {"message": "user message"}
    """
    try:
        data = request.json
        message = data.get('message', '')
        
        # Check if this is an image generation request
        if 'generate' in message.lower() and 'image' in message.lower():
            return generate_image(message)
        else:
            # Regular text response
            return text_chat(message)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def text_chat(message):
    """Handle regular text chat"""
    try:
        # TODO: Use Gemini for text responses
        response = f"Response to: {message}"
        return jsonify({"response": response, "type": "text"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_image(prompt):
    """Generate image using Gemini 2.0"""
    try:
        # Extract image prompt from user message
        image_prompt = prompt.replace('generate image of', '').replace('generate', '').strip()
        
        # TODO: Use Gemini 2.0 Image Generation API
        # For now, placeholder implementation
        
        # Save image with timestamp
        filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(IMAGES_DIR, filename)
        
        # TODO: Save generated image to file
        
        return jsonify({
            "response": f"Generated image: {image_prompt}",
            "type": "image",
            "image_url": f"/images/{filename}",
            "prompt": image_prompt
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    """Serve generated images"""
    try:
        filepath = os.path.join(IMAGES_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                img_data = f.read()
            return img_data, 200, {'Content-Type': 'image/png'}
        return jsonify({"error": "Image not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
