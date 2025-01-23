from contextlib import asynccontextmanager
from .models import async_session, UserOrm, AiUserOrm
from sqlalchemy import select, update
from datetime import datetime, timezone
from ai import ai_list

LEVELS_CONFIG = {
    0: [20, 0, 0, 0, 1, 3],
    1: [50, 20, 30, 30, 10, 15],
    2: [100, 50, 75, 75, 20, 30],
    3: [200, 100, 150, 150, 40, 60]
}

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


    class ai:
        @classmethod
        async def get_requests(cls, tg_id: int, ai_model_id: int):
            async with get_session() as session:
                user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                orm_name = model_to_orm(ai_list[ai_model_id])
                
                return getattr(user, orm_name)
        
        @classmethod
        async def set_base_requests(cls, tg_id: int, level):
            async with get_session() as session:
                user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                config = LEVELS_CONFIG[level]
                
                for id, model in enumerate(ai_list):
                    orm_name = model_to_orm(model)
                    setattr(user, orm_name, config[id])

        @classmethod
        async def remove_requests(cls, tg_id: int, ai_model_id: int, quantity_of_requests: int):
            async with get_session() as session:
                user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                orm_name = model_to_orm(ai_list[ai_model_id])
                current = getattr(user, orm_name)
                setattr(user, orm_name, current - quantity_of_requests)

        class level:
            @classmethod
            async def get(cls, tg_id):
                async with get_session() as session:
                    user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                    return user.level
            
            @classmethod
            async def set(cls, tg_id, level):
                async with get_session() as session:
                    user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                    user.level = level

        class issued_requests_date:
            @classmethod
            async def get(cls, tg_id: int):
                async with get_session() as session:
                    user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                    return user.date_of_issued_requests

            @classmethod
            async def set(cls, tg_id, date = datetime.now(timezone.utc).replace(tzinfo=None)):
                async with get_session() as session:
                    user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                    user.date_of_issued_requests = date

        class subscription_date:
            @classmethod
            async def get(cls, tg_id):
                async with get_session() as session:
                    user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                    return user.date_of_subscription

            @classmethod
            async def set(cls, tg_id: int, date = datetime.now(timezone.utc).replace(tzinfo=None)):
                async with get_session() as session:
                    user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                    user.date_of_subscription = date               