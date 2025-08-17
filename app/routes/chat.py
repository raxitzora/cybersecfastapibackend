from fastapi import APIRouter,HTTPException
from app.models import ChatRequest,ChatResponse
from app.services.groq_service import get_groq_response

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        reply = await get_groq_response(request.message, request.history)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))