import asyncio
from app.db.crud import get_memory, save_memory

async def test():
    user_id = "test_user"

    print("Saving memory...")
    await save_memory(user_id, "User is learning cybersecurity and Python.")

    print("Fetching memory...")
    mem = await get_memory(user_id)

    print("Memory:", mem)

asyncio.run(test())