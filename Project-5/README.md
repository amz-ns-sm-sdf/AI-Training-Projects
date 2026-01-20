# Project 5: Rich Media Support

## Description
Add support for displaying images, videos, tables, formulas, and code in chat.

## Features
- Display images in chat
- Embed videos (YouTube, etc.)
- Render tables with proper formatting
- Display mathematical formulas (LaTeX)
- Syntax highlighted code blocks
- Built on Project 4

## Tech Stack
- **Frontend**: HTML/CSS/JavaScript with:
  - Markdown parser
  - LaTeX/MathJax for formulas
  - Highlight.js for code syntax
  - Video.js for video embedding
- **Backend**: Python Flask

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Install frontend libraries (included in CDN links)
3. Run: `python app.py`

## Libraries to Include
- markdown-it for markdown rendering
- MathJax for LaTeX formulas
- Highlight.js for code highlighting
- video.js for video support

## Folder Structure
```
Project-5/
├── backend/          # Backend
├── frontend/         # UI with rich media support
├── README.md
```
