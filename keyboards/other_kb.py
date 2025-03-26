from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translations.translate import translate as _

async def set_language_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="English", callback_data=f"lang_en")],
        [InlineKeyboardButton(text="Русский", callback_data=f"lang_ru")]
    ])
    return keyboard