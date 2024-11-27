from .models import async_session, UserOrm
from sqlalchemy import select, update

class User:
    async def add(tg_id):
        async with async_session() as session:
            session.add(UserOrm(tg_id=tg_id))
            await session.commit()

    async def get(tg_id):
        async with async_session() as session:
            user = await session.scalar(select(UserOrm).where(UserOrm.tg_id == tg_id))
            return user
        
    class edit:
        async def ai_id(tg_id, ai_id):
            async with async_session() as session:
                user = await session.scalar(select(UserOrm).where(UserOrm.tg_id == tg_id))
                user.ai_id = ai_id
                await session.commit()

        async def language():
            pass
