from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translations.translate import translate as _

async def settings_kb(tg_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=await _(tg_id=tg_id, key="🏳️ Язык"), callback_data="set_language")]
    ])
    return keyboard
