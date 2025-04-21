#uvicorn api_agent:app --reload
from fastapi import FastAPI, Path, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
from llm_formatter import format_response_to_html

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

BACKEND_URL = "http://localhost:8081"

@app.get("/welcome/{session_id}")
async def get_welcome(session_id: str = Path(...)):
    async with httpx.AsyncClient(timeout=50.0) as client:
        backend_response = await client.get(f"{BACKEND_URL}/welcome/{session_id}")
        backend_data = backend_response.json()
    
    content = backend_data.get("welcome_message", "")
    html = format_response_to_html(content)
    print(f"\nGenerated HTML (WELCOME):\n{html}\n")  
    return { "html": html }

@app.post("/chat")
async def post_chat(request: Request):
    payload = await request.json()
    
    async with httpx.AsyncClient(timeout=50.0) as client:
        backend_response = await client.post(f"{BACKEND_URL}/chat", json=payload)
        backend_data = backend_response.json()
    
    content = backend_data.get("response", "")
    html = format_response_to_html(content)
    print(f"\nGenerated HTML (Response):\n{html}\n") 
    return { "html": html }
