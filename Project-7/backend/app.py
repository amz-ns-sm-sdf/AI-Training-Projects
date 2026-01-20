from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
from collections import defaultdict
import hashlib

app = Flask(__name__)
CORS(app)

# In-memory storage for documents and conversations
documents = {}  # {doc_id: {name, content, chunks, uploaded_at}}
conversations = defaultdict(list)  # {doc_id: [{role, content}]}
doc_counter = 0

# File uploads directory
UPLOADS_DIR = 'uploads'
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Sample PDF content for demo (simulating PDF extraction)
SAMPLE_DOCUMENTS = {
    'sample_ai.txt': {
        'name': 'AI Fundamentals',
        'content': '''Artificial Intelligence (AI) is transforming industries.
        Machine Learning enables systems to learn from data.
        Deep Learning uses neural networks with multiple layers.
        Natural Language Processing helps computers understand human language.
        Computer Vision allows machines to interpret visual information.
        Reinforcement Learning trains agents through reward signals.
        Supervised learning requires labeled training data.
        Unsupervised learning finds patterns in unlabeled data.
        Transformer models revolutionized NLP with attention mechanisms.
        Large Language Models can perform few-shot learning.
        Transfer learning leverages pre-trained models.
        Prompt engineering optimizes AI model outputs.'''
    },
    'sample_ml.txt': {
        'name': 'Machine Learning Basics',
        'content': '''Machine learning is a subset of AI.
        Training data quality impacts model performance.
        Overfitting occurs when models memorize rather than generalize.
        Cross-validation assesses model robustness.
        Regularization prevents overfitting in models.
        Feature engineering improves model accuracy.
        Hyperparameter tuning optimizes learning algorithms.
        Ensemble methods combine multiple models.
        Gradient descent minimizes loss functions.
        Backpropagation trains neural networks.
        Activation functions introduce nonlinearity.
        Batch normalization stabilizes training.
        Dropout prevents co-adaptation in networks.
        Learning rate affects convergence speed.'''
    }
}

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Simulate PDF upload and document loading"""
    global doc_counter
    try:
        data = request.json
        doc_name = data.get('name', f'Document {doc_counter}')
        doc_content = data.get('content', '')
        
        if not doc_content:
            return jsonify({"error": "No content provided"}), 400
        
        doc_counter += 1
        doc_id = f"doc_{doc_counter}"
        
        # Chunk content by sentences
        chunks = [s.strip() for s in doc_content.split('.') if s.strip()]
        
        documents[doc_id] = {
            'id': doc_id,
            'name': doc_name,
            'content': doc_content,
            'chunks': chunks,
            'uploaded_at': datetime.now().isoformat()
        }
        
        return jsonify({
            "status": "success",
            "doc_id": doc_id,
            "name": doc_name,
            "chunks": len(chunks)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_document():
    """Chat about uploaded documents using simulated RAG"""
    try:
        data = request.json
        message = data.get('message', '')
        doc_id = data.get('doc_id', '')
        
        if not doc_id or doc_id not in documents:
            return jsonify({"error": "Document not found"}), 400
        
        doc = documents[doc_id]
        
        # Simple semantic matching: find chunks containing message keywords
        keywords = message.lower().split()
        relevant_chunks = []
        
        for chunk in doc['chunks']:
            chunk_lower = chunk.lower()
            if any(keyword in chunk_lower for keyword in keywords):
                relevant_chunks.append(chunk)
        
        # Use first 3 relevant chunks as context
        context = '. '.join(relevant_chunks[:3]) if relevant_chunks else doc['chunks'][0]
        
        # Build response
        response = f"About '{message}': Based on {doc['name']}, {context}. This simulates RAG retrieval augmented generation with retrieved context from the document."
        
        # Store conversation
        conversations[doc_id].append({"role": "user", "content": message})
        conversations[doc_id].append({"role": "assistant", "content": response})
        
        return jsonify({
            "response": response,
            "context_chunks": len(relevant_chunks),
            "doc_name": doc['name']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all uploaded documents"""
    try:
        return jsonify({
            "documents": [
                {
                    'id': doc['id'],
                    'name': doc['name'],
                    'chunks': len(doc['chunks']),
                    'uploaded_at': doc['uploaded_at']
                }
                for doc in documents.values()
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/documents/sample', methods=['POST'])
def load_sample_documents():
    """Load sample documents for demo"""
    global doc_counter
    try:
        loaded = []
        for filename, doc_data in SAMPLE_DOCUMENTS.items():
            doc_counter += 1
            doc_id = f"doc_{doc_counter}"
            chunks = [s.strip() for s in doc_data['content'].split('.') if s.strip()]
            documents[doc_id] = {
                'id': doc_id,
                'name': doc_data['name'],
                'content': doc_data['content'],
                'chunks': chunks,
                'uploaded_at': datetime.now().isoformat()
            }
            loaded.append({'id': doc_id, 'name': doc_data['name']})
        
        return jsonify({"status": "success", "documents": loaded})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/documents/<doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a document"""
    try:
        if doc_id in documents:
            del documents[doc_id]
            if doc_id in conversations:
                del conversations[doc_id]
            return jsonify({"status": "deleted"})
        return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5006, use_reloader=False)

