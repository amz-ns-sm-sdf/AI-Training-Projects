# Project 4: Chat with Conversation Memory

## Description
Add conversation memory to maintain context from 5 previous messages.

## Features
- Chat remembers last 5 conversations
- Context-aware responses using conversation history
- Built on Project 3

## Tech Stack
- **Frontend**: HTML/CSS/JavaScript
- **Backend**: Python with Flask + Langchain
- **Database**: PostgreSQL
- **LLM**: Google Gemini with memory chain

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Configure Langchain with memory buffer
3. Run: `python app.py`

## Implementation Notes
- Use Langchain's ConversationBufferMemory (limit to 5 previous messages)
- Pass memory context to Gemini API
- Store full conversation for reference

## Folder Structure
```
Project-4/
├── backend/          # Backend with memory chain
├── frontend/         # UI
├── README.md
```
