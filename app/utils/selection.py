from app.utils.prompt import model_selection_prompt
from app.services.router_service import get_router_response

async def select_model(message: str) -> str:
    prompt = model_selection_prompt["model_selector"]

    category = await get_router_response(message, prompt)

    mapping = {
        "research": "meta",
        "teaching": "deepseek_chat",
        "coding": "deepseek_coder",
        "general": "groq"
    }

    return mapping.get(category, "groq")
