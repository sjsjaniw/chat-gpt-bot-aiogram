from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton

async def main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="Настройки")],
        [KeyboardButton(text="Задонатить нам 👉👈")]
    ])
    return keyboard