import httpx
from app.config import settings
from app.utils.prompt import system_prompt_meta
from app.utils.text_utils import clean_output

GROQ_API_URL = "https://api.groq.com/openai/v1"

async def get_metallama_response(message: str, history: list):
    messages = [{"role": "system", "content": system_prompt_meta.strip()}]

    if history:
        messages.extend(history)

    payload = {
        "model": "llama-3.3-70b-versatile",  # ✅ HARDCODED (strong model for research)
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",  # ✅ reuse Groq
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            GROQ_API_URL,
            headers=headers,
            json=payload
        )

        print("Meta STATUS:", response.status_code)
        print("Meta BODY:", response.text)

    response.raise_for_status()
    data = response.json()

    if "choices" not in data or not data["choices"]:
        raise ValueError(f"Unexpected response: {data}")

    reply = data["choices"][0]["message"]["content"]
    return clean_output(reply)