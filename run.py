import asyncio
from aiogram import Bot, Dispatcher
# from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.utils.chat_action import ChatActionMiddleware

from dotenv import load_dotenv
import os
import logging

from hendlers import router as main_router

from database.models import async_db_main

load_dotenv()
async def main():
    bot = Bot(token=os.getenv("TOKEN"))
    # dp = Dispatcher(storage=RedisStorage.from_url(os.getenv("REDIS_URL")))
    
    dp = Dispatcher()
    dp.include_router(main_router)
    dp.message.middleware(ChatActionMiddleware())
    await async_db_main()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
    except Exception as e:
        import sys
        print(e)
        sys.exit()