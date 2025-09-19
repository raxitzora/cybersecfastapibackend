from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse
from app.services.groq_service import get_groq_response
from app.services.metallama_service import get_metallama_response
from app.services.deepseek_service import get_deepseek_response
from app.utils.selection import select_model  # <--- import here

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_router(request: ChatRequest):
    try:
        # await select_model since it's async
        model = await select_model(request.message)

        if model == "meta":
            reply = await get_metallama_response(request.message, request.history)
        elif model == "deepseek":
            reply = await get_deepseek_response(request.message, request.history)
        else:
            reply = await get_groq_response(request.message, request.history)

        return ChatResponse(reply=reply, model_used=model)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Keep direct routes for manual testing
@router.post("/meta", response_model=ChatResponse)
async def chat_meta(request: ChatRequest):
    try:
        reply = await get_metallama_response(request.message, request.history)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/deepseek", response_model=ChatResponse)
async def chat_deepseek(request: ChatRequest):
    try:
        reply = await get_deepseek_response(request.message, request.history)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
