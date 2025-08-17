import httpx
from app.config import GROQ_API_KEY, GROQ_API_URL, GROQ_MODEL
from app.utils.prompt import system_prompt
from app.utils.text_utils import clean_output

async def get_groq_response(message:str,history:list):
    messages = [{"role": "system", "content": system_prompt.strip()}]

    if history:
        messages.extend(history)
    
    messages.append({"role": "user", "content": message.strip()})

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 2048
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, headers=headers, json=payload)

    response.raise_for_status()
    reply = response.json()["choices"][0]["message"]["content"]
    
    return clean_output(reply)


