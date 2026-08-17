# Ask Talal — Personal AI Agent

A capstone project: an AI agent that answers questions about Talal Noor's
projects, skills, and experience, embedded in a standalone site.

## Structure
- `backend/` — FastAPI + Groq LLM, serves the `/chat` endpoint
- `frontend/` — Plain HTML/CSS/JS chat UI, dark GitHub-inspired theme

## Setup

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your Groq API key (get one free at console.groq.com)
4. `uvicorn main:app --reload`
5. Backend runs at http://localhost:8000

### Frontend
1. Open `frontend/index.html` in your browser (or use Live Server in VS Code)
2. It talks to the backend at the URL set in `frontend/script.js` (BACKEND_URL)

## Deployment
- Backend: Railway (set root dir to `backend/`, add GROQ_API_KEY env var)
- Frontend: GitHub Pages or Railway — after deploying, update BACKEND_URL in script.js

## Editing the agent's knowledge
Edit `backend/knowledge_base.py` — add/update facts, projects, skills, tone. The agent only answers from what's in there.
