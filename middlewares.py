from aiogram import BaseMiddleware
from aiogram.types import Message
import time

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: int = 2):
        self.rate_limit = rate_limit
        self.users = {}

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        current_time = time.time()

        if user_id in self.users:
            last_time = self.users[user_id]
            if current_time - last_time < self.rate_limit:
                await event.reply("Пожалуйста, не спамьте")
                return

        self.users[user_id] = current_time
        return await handler(event, data)