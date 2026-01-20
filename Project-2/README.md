# Project 2: Chatbot with Database Layer

## Description
Add PostgreSQL database integration to store chat history. Implement employee login for Amzur.

## Features
- PostgreSQL database for storing chats
- Amzur employee login system
- Load chat history from DB on login
- Built on Project 1

## Tech Stack
- **Frontend**: HTML/CSS/JavaScript
- **Backend**: Python with Flask
- **Database**: PostgreSQL
- **LLM**: Google Gemini

## Database Setup
1. Install PostgreSQL
2. Create database: `createdb chatbot_db`
3. Run migrations: `python migrations.py`
4. Update `.env` with DB connection string

## Setup Instructions
1. Copy Project 1 files
2. Install dependencies: `pip install -r requirements.txt`
3. Configure database connection
4. Run: `python app.py`

## Folder Structure
```
Project-2/
├── backend/          # Python backend with DB
├── frontend/         # UI with login
├── migrations/       # Database migrations
├── README.md
```
