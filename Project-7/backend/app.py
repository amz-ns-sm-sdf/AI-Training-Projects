from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import os
import chromadb
from chromadb.config import Settings
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import openai
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Initialize ChromaDB
CHROMA_DB_PATH = 'chroma_db'
os.makedirs(CHROMA_DB_PATH, exist_ok=True)
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb",
    persist_directory=CHROMA_DB_PATH,
    anonymized_telemetry=False
))

# File uploads directory
UPLOADS_DIR = 'uploads'
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Initialize embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Text splitter for chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""]
)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Upload and process a PDF file
    Expected: multipart/form-data with 'file' field
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if not file or not file.filename.endswith('.pdf'):
            return jsonify({"error": "Only PDF files are supported"}), 400
        
        # Save file
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(UPLOADS_DIR, filename)
        file.save(filepath)
        
        # Extract text from PDF
        texts = extract_pdf_text(filepath)
        
        # Split into chunks
        chunks = text_splitter.split_text(texts)
        
        # Create embeddings and store in ChromaDB
        collection_name = filename.replace('.pdf', '').replace(' ', '_')
        collection = client.get_or_create_collection(name=collection_name)
        
        for i, chunk in enumerate(chunks):
            embedding = embeddings.embed_query(chunk)
            collection.add(
                documents=[chunk],
                metadatas=[{"source": filename, "chunk": i}],
                ids=[f"{filename}_{i}"],
                embeddings=[embedding]
            )
        
        return jsonify({
            "status": "success",
            "filename": filename,
            "collection": collection_name,
            "chunks": len(chunks)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_document():
    """
    Chat about uploaded documents using RAG
    Expected JSON: {"message": "...", "collection": "..."}
    """
    try:
        data = request.json
        message = data.get('message', '')
        collection_name = data.get('collection', '')
        
        if not collection_name:
            return jsonify({"error": "No document collection specified"}), 400
        
        # Get collection from ChromaDB
        collection = client.get_collection(name=collection_name)
        
        # Embed the query
        query_embedding = embeddings.embed_query(message)
        
        # Retrieve relevant chunks
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )
        
        # Build context from retrieved chunks
        context = "\n".join(results['documents'][0]) if results['documents'] else ""
        
        # Generate response using Gemini with context
        # TODO: Replace with Gemini API call
        response = f"Based on the document: {context[:200]}... {message}"
        
        return jsonify({
            "response": response,
            "context_used": len(results['documents'][0]) if results['documents'] else 0
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all uploaded documents/collections"""
    try:
        collections = client.list_collections()
        return jsonify({
            "documents": [c.name for c in collections]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/documents/<collection_name>', methods=['DELETE'])
def delete_document(collection_name):
    """Delete a document and its embeddings"""
    try:
        client.delete_collection(name=collection_name)
        return jsonify({"status": "deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_pdf_text(filepath):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    return text

if __name__ == '__main__':
    app.run(debug=True, port=5000)
