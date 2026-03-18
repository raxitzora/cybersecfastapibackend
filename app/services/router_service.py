import httpx
from app.config import settings

async def get_router_response(message: str, prompt_text: str) -> str:
    url = "https://api.mistral.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-small",
        "messages": [
            {"role": "system", "content": prompt_text},
            {"role": "user", "content": message}
        ],
        "max_tokens": 10
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, headers=headers, json=data)

        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        response.raise_for_status()

        category = response.json()["choices"][0]["message"]["content"].strip().lower()

        if category not in ["research", "teaching", "coding", "general"]:
            category = "general"

        return category