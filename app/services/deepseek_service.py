import httpx
import json
from app.config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL
from app.utils.prompt import system_prompt_deepseek
from app.utils.text_utils import clean_output

async def get_deepseek_response(message: str, history: list):
    messages = [{"role": "system", "content": system_prompt_deepseek.strip()}]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": message.strip()})

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 2048
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",   # change in production
        "X-Title": "MyFastAPIApp"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            DEEPSEEK_API_URL,
            headers=headers,
            data=json.dumps(payload)
        )

    # Debug print BEFORE parsing
    # print("DeepSeek raw response:", response.text)

    try:
        response.raise_for_status()
        data = response.json()
    except Exception:
        raise RuntimeError(f"Non-JSON response: {response.text}")

    if "choices" not in data or not data["choices"]:
        raise ValueError(f"Unexpected response: {data}")

    reply = data["choices"][0]["message"]["content"]
    return clean_output(reply)
