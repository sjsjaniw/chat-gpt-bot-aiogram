from .models import async_session, UserOrm, AiUserOrm
from sqlalchemy import select, update
from datetime import datetime, timezone

class User:
    async def add(tg_id):
        async with async_session() as session:
            session.add(UserOrm(tg_id=tg_id))
            session.add(AiUserOrm(tg_id=tg_id))
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


    class ai:
        async def get_requests(tg_id: int, ai_model_id: int):
            async with async_session() as session:
                user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                if ai_model_id == 0: return user.gpt4omini
                if ai_model_id == 1: return user.gpt4o
                if ai_model_id == 2: return user.llama31405b
                if ai_model_id == 3: return user.claude35sonnet
                if ai_model_id == 4: return user.flux
                if ai_model_id == 5: return user.fluxrealism
                if ai_model_id == 6: return user.fluxanime
                if ai_model_id == 7: return user.fluxpixel
                if ai_model_id == 8: return user.sd3

        async def set_base_requests(tg_id: int, level):
            async with async_session() as session:
                user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                if level == 0:
                    user.gpt4omini = 20
                    user.gpt4o = 0
                    user.llama31405b = 0
                    user.claude35sonnet = 0
                    user.flux = 3
                    user.fluxrealism = 0
                    user.fluxanime = 0
                    user.fluxpixel = 0
                    user.sd3 = 0
                if level == 1:
                    user.gpt4omini = 0
                    user.gpt4o = 0
                    user.llama31405b = 0
                    user.claude35sonnet = 0
                    user.flux = 0
                    user.fluxrealism = 0
                    user.fluxanime = 0
                    user.fluxpixel = 0
                    user.sd3 = 0
                if level == 2:
                    user.gpt4omini = 0
                    user.gpt4o = 0
                    user.llama31405b = 0
                    user.claude35sonnet = 0
                    user.flux = 0
                    user.fluxrealism = 0
                    user.fluxanime = 0
                    user.fluxpixel = 0
                    user.sd3 = 0
                if level == 3:
                    user.gpt4omini = 0
                    user.gpt4o = 0
                    user.llama31405b = 0
                    user.claude35sonnet = 0
                    user.flux = 0
                    user.fluxrealism = 0
                    user.fluxanime = 0
                    user.fluxpixel = 0
                    user.sd3 = 0
                await session.commit()

        async def remove_requests(tg_id: int, ai_model_id: int, quantity_of_requests: int):
            async with async_session() as session:
                user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                if ai_model_id == 0: user.gpt4omini -= quantity_of_requests
                if ai_model_id == 1: user.gpt4o -= quantity_of_requests
                if ai_model_id == 2: user.llama31405b -= quantity_of_requests
                if ai_model_id == 3: user.claude35sonnet -= quantity_of_requests
                if ai_model_id == 4: user.flux -= quantity_of_requests
                if ai_model_id == 5: user.fluxrealism -= quantity_of_requests
                if ai_model_id == 6: user.fluxanime -= quantity_of_requests
                if ai_model_id == 7: user.fluxpixel -= quantity_of_requests
                if ai_model_id == 8: user.sd3 -= quantity_of_requests
                await session.commit()

        class level:
            async def get(tg_id):
                async with async_session() as session:
                    user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                    return user.level
                
            async def set(tg_id, level):
                async with async_session() as session:
                    user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                    user.level = level
                    await session.commit()

        class issued_requests_date:
            async def get(tg_id: int):
                async with async_session() as session:
                    user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                    return user.date_of_issued_requests

            async def set(tg_id, date = datetime.now(timezone.utc).replace(tzinfo=None)):
                async with async_session() as session:
                    user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                    user.date_of_issued_requests = date
                    await session.commit()

        class subscription_date:
            async def get(tg_id):
                async with async_session() as session:
                    user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                    return user.date_of_subscription

            async def set(tg_id: int, date = datetime.now(timezone.utc).replace(tzinfo=None)):
                async with async_session() as session:
                    user = await session.scalar(select(AiUserOrm).where(AiUserOrm.tg_id == tg_id))
                    user.date_of_subscription = date
                    await session.commit()
