import httpx
from app.utils.prompt import system_prompt_groq
from app.config import settings
from app.utils.text_utils import clean_output

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


async def get_groq_response(message: str, history: list):
    messages = [{"role": "system", "content": system_prompt_groq.strip()}]

    if history:
        messages.extend(history)

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 2048
    }

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("PAYLOAD:", payload)

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(GROQ_API_URL, headers=headers, json=payload)

        print("Groq STATUS:", response.status_code)
        print("Groq BODY:", response.text)

    response.raise_for_status()
    data = response.json()

    if "choices" in data and len(data["choices"]) > 0:
        reply = data["choices"][0]["message"]["content"]
    else:
        raise ValueError(f"Unexpected Groq response: {data}")

    return clean_output(reply)