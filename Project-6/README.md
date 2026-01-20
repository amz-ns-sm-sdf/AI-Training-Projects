# Project 6: Image Generation with Gemini 2.0

## Description
Enable the chatbot to generate images using Google Gemini 2.0 Image Generation model.

## Features
- Generate images from text prompts
- Display generated images in chat
- Save generated images
- Built on Project 5

## Tech Stack
- **Frontend**: HTML/CSS/JavaScript
- **Backend**: Python Flask
- **API**: Google Gemini 2.0 Image Generation Model

## Setup Instructions
1. Get Gemini 2.0 API access
2. Add API key to `.env`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python app.py`

## Implementation Notes
- Detect image generation requests (e.g., "generate image of...")
- Call Gemini 2.0 Image Generation API
- Return image URL or base64 encoded image
- Display in chat interface

## Folder Structure
```
Project-6/
├── backend/          # Backend with image generation
├── frontend/         # UI with image display
├── generated_images/ # Store generated images
├── README.md
```
