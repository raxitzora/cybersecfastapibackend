import httpx
import os
from app.utils.prompt import model_selection_prompt  # fixed import

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

async def get_router_response(message: str, prompt_text: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": prompt_text},
            {"role": "user", "content": message}
        ],
        "max_tokens": 5
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()
        category = response.json()["choices"][0]["message"]["content"].strip().lower()
        if category not in ["research", "teaching", "coding", "general"]:
            category = "general"
        # print(f"[Router] Message: {message} → Category: {category}")
        return category
