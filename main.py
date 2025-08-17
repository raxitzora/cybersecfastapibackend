from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat

app = FastAPI(title="Cyber Chatbot using Groq + LLaMA 3")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Cyber Chatbot API is running with Groq + LLaMA 3!"}
