from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton
from translations.translate import translate as _

async def main_reply_keyboard(tg_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text=await _(tg_id=tg_id, key="⚙️ Настройки"))],
        [KeyboardButton(text=await _(tg_id=tg_id, key="Премиум 👉👈"))]
    ])
    return keyboard