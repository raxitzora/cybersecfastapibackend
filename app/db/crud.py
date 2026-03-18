from sqlalchemy.future import select
from app.db.models import Message, Memory
from app.db.database import AsyncSessionLocal
from app.db import models

async def get_memory(user_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Memory).where(Memory.user_id == user_id)
        )
        mem = result.scalar_one_or_none()
        return mem.summary if mem else ""


async def save_memory(user_id: str, summary: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Memory).where(Memory.user_id == user_id)
        )
        mem = result.scalar_one_or_none()

        if mem:
            mem.summary = summary
        else:
            mem = Memory(user_id=user_id, summary=summary)
            session.add(mem)

        await session.commit()




# ✅ THIS FUNCTION MUST EXIST
async def get_chat_history(user_id: str, limit: int = 6):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Message)
            .where(Message.user_id == user_id)
            .order_by(Message.timestamp.desc())
            .limit(limit)
        )

        messages = result.scalars().all()
        messages.reverse()

        return [
    {"role": m.role, "content": m.content.strip()}
    for m in messages
    if m.content and m.content.strip()
]

# ✅ THIS ALSO MUST EXIST
async def save_message(user_id: str, role: str, content: str):
    async with AsyncSessionLocal() as session:
        msg = Message(
            user_id=user_id,
            role=role,
            content=content
        )
        session.add(msg)
        await session.commit()