# Project 7: RAG with PDF Upload & File Chat

## Description
Upload files (starting with PDF) and chat about their content using RAG (Retrieval Augmented Generation).

## Features
- Upload PDF files to chat
- Extract and vectorize PDF content
- Retrieve relevant context from documents
- Answer questions about document content
- Store vectors in ChromaDB
- Use OpenAI Embeddings Large

## Tech Stack
- **Frontend**: HTML/CSS/JavaScript with file upload
- **Backend**: Python Flask with RAG
- **Vector DB**: ChromaDB
- **Embeddings**: OpenAI Embeddings Large
- **PDF Processing**: PyPDF2 or pdfplumber
- **RAG Framework**: Langchain

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Add OpenAI API key to `.env`
3. Create uploads directory: `mkdir uploads`
4. Initialize ChromaDB: `python init_db.py`
5. Run: `python app.py`

## Implementation Notes
- Extract text from PDF using PyPDF2
- Split text into chunks (500 tokens with 50 token overlap)
- Create embeddings using OpenAI Embeddings Large
- Store embeddings in ChromaDB
- Retrieve relevant chunks for user queries
- Generate responses with context from documents

## Folder Structure
```
Project-7/
├── backend/          # RAG backend
│   ├── app.py
│   ├── rag_engine.py
│   ├── uploads/      # Store uploaded PDFs
│   ├── chroma_db/    # ChromaDB storage
│   └── requirements.txt
├── frontend/         # UI with file upload
├── README.md
```
