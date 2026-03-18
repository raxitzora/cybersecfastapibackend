from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse
from app.services.groq_service import get_groq_response
from app.services.deepseek_service import get_deepseek_response
from app.utils.selection import select_model
from app.db.crud import (
    get_chat_history,
    save_message,
    get_memory,
    save_memory
)
from app.utils.memory import summarize_history  # create this file

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_router(request: ChatRequest):
    try:
        # 1. Fetch history
        history = await get_chat_history(request.user_id)

        # 2. Fetch long-term memory
        memory = await get_memory(request.user_id)
        print("MEMORY:", memory)

        # 3. Inject memory (IMPORTANT)
        if memory:
            history.insert(0, {
                "role": "system",
                "content": f"Previous context about user: {memory}"
            })

        # 4. Add current user message
        history.append({
            "role": "user",
            "content": request.message
        })

        # 5. Router decision
        model_type = await select_model(request.message)
        print("ROUTER DECISION:", model_type)

        # 6. Call correct model with fallback
        try:
            if model_type == "coding":
                reply = await get_deepseek_response(request.message, history)
            else:
                reply = await get_groq_response(request.message, history)

        except Exception as e:
            print("Model failed, fallback to Groq:", e)
            reply = await get_groq_response(request.message, history)

        # 7. Save messages
        await save_message(request.user_id, "user", request.message)
        await save_message(request.user_id, "assistant", reply)

        # 8. Update memory (IMPORTANT)
        if len(history) >= 6:
            summary = await summarize_history(history)
            await save_memory(request.user_id, summary)

        # 9. Return response
        return ChatResponse(reply=reply, model_used=model_type)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))