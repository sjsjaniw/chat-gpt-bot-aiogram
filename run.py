import asyncio
from aiogram import Bot, Dispatcher
# from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv
import os
import logging

from hendlers import router as main_router

from database.models import async_db_main

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    # dp = Dispatcher(storage=RedisStorage.from_url(os.getenv("REDIS_URL")))
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_router)
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