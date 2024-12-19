from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translations.translate import translate as _


async def premium():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Beginner", callback_data="premium_beginner")],
        [InlineKeyboardButton(text="Basic", callback_data="premium_basic")],
        [InlineKeyboardButton(text="Master", callback_data="premium_master")],
    ])
    return keyboard

async def donate_button(lvl: int, tg_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Stars ⭐️", pay=True, callback_data=f"payStars_{lvl}")],
        [InlineKeyboardButton(text=await _(tg_id=tg_id, key="Криптоволюта TON (CryptoBot) 💸"), callback_data=f"payCrypto_{lvl}")]
    ])
    return keyboard

async def set_language_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="English", callback_data=f"lang_en")],
        [InlineKeyboardButton(text="Русский", callback_data=f"lang_ru")]
    ])
    return keyboard