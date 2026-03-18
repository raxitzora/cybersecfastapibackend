import httpx
from app.config import settings
from app.utils.prompt import system_prompt_deepseek
from app.utils.text_utils import clean_output

DEEPSEEK_API_URL = "https://api.deepseek.com"

async def get_deepseek_response(message: str, history: list):
    messages = [{"role": "system", "content": system_prompt_deepseek.strip()}]

    if history:
        messages.extend(history)

    payload = {
        "model": "deepseek-coder",  # ✅ HARDCODED
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload  # ✅ correct way
        )

        print("DeepSeek STATUS:", response.status_code)
        print("DeepSeek BODY:", response.text)

    response.raise_for_status()
    data = response.json()

    if "choices" not in data or not data["choices"]:
        raise ValueError(f"Unexpected response: {data}")

    reply = data["choices"][0]["message"]["content"]
    return clean_output(reply)