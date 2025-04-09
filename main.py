from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HTML_DIR = "html_pages"

class ChatRequest(BaseModel):
    session_id: str
    user_input: str

def load_random_html(prefix: str):
    files = [f for f in os.listdir(HTML_DIR) if f.startswith(prefix) and f.endswith(".html")]
    if not files:
        return "<html><body><p>No HTML files found.</p></body></html>"
    chosen = random.choice(files)
    with open(os.path.join(HTML_DIR, chosen), "r", encoding="utf-8") as f:
        return f.read()

@app.get("/welcome/{session_id}")
async def welcome(session_id: str):
    html = load_random_html("welcome")
    return {"html": html}

@app.post("/chat")
async def chat(request: ChatRequest):
    html = load_random_html("page")
    return 
