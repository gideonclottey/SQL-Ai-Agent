# SQL AI Agent — Local (FastAPI + Vite/Tailwind)

Local-first AI agent with:
- FastAPI backend (JWT auth, SQLite seed, Gemini tools)
- Vite + React + Tailwind frontend (login, chat, **Settings to paste API key**)
- Two key modes:
  - **Server mode** — store API key encrypted on backend
  - **Local mode** — keep API key in this browser only (sent as headers)

## Run

### Backend
```bash
cd apps/backend
python -m venv .venv
# Win: .venv\Scripts\activate   # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
python -m app.seed_db
uvicorn app.main:app --reload --port 8000
