import os
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from .db import Base, engine
from .models import AppUser, User, UserActivity
from .auth import router as auth_router
from .schemas import ChatRequest
from .utils import decode_token
from .agent import GeminiAgent

# Create tables on startup (for demo); in prod use alembic
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SQLite + Gemini Agent API", version="1.0.0")

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

# Auth dependency

def require_auth(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split()[1]
    try:
        email = decode_token(token)
        return email
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def root():
    return {"ok": True, "service": "SQLite + Gemini Agent API"}

@app.post("/chat")
def chat(req: ChatRequest, user_email: str = Depends(require_auth), x_api_key: Optional[str] = Header(None)):
    api_key = x_api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="Missing Gemini API key. Provide via X-Api-Key header or GEMINI_API_KEY env.")

    agent = GeminiAgent(api_key=api_key)
    history = None
    if req.history:
        history = [{"role": m.role, "content": m.content} for m in req.history]
    result = agent.chat(req.message, history)
    return result