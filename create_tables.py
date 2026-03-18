import asyncio
from app.db.database import engine, Base
from app.db import models


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())