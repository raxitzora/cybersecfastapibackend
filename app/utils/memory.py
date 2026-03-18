from app.services.groq_service import get_groq_response

async def summarize_history(history: list):
    prompt = "Summarize this conversation in 2-3 lines with key points:\n"

    for msg in history[-6:]:  # only recent
        prompt += f"{msg['role']}: {msg['content']}\n"

    summary = await get_groq_response(prompt, [])
    return summary