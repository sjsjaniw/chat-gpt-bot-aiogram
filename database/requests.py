from contextlib import asynccontextmanager
from .models import async_session, UserOrm, AiUserOrm
from sqlalchemy import select

def model_to_orm(name: str):
    return name.replace("-", "").replace(".", "")

@asynccontextmanager
async def get_session():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

class User:
    @classmethod
    async def add(cls, tg_id, language):
        async with get_session() as session:
            session.add(UserOrm(tg_id=tg_id, language=language))
            session.add(AiUserOrm(tg_id=tg_id))

    @classmethod
    async def get(cls, tg_id: int):
        async with get_session() as session:
            return await session.scalar(
                select(UserOrm).where(UserOrm.tg_id == tg_id)
            )
    class edit:
        @classmethod
        async def ai_id(cls, tg_id, ai_id):
            async with get_session() as session:
                user = await session.scalar(select(UserOrm).where(UserOrm.tg_id == tg_id))
                user.ai_id = ai_id

        @classmethod
        async def language(cls, tg_id, language):
            async with get_session() as session:
                user = await session.scalar(select(UserOrm).where(UserOrm.tg_id == tg_id))
                user.language = language