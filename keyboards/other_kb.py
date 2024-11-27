from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os


async def donate_button():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Задонатить 👉👈", url=os.getenv("DONATE_URL"))],
    ])
    return keyboard