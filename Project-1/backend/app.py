from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Gemini LLM
# TODO: Initialize Langchain with Gemini

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat requests
    Expected JSON: {"message": "user message"}
    """
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # TODO: Process message with Langchain + Gemini
        # response = chain.run(user_message)
        
        return jsonify({"response": "Response from Gemini"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
