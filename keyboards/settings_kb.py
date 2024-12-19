from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.requests import User
from ai import ai_list
from translations.translate import translate as _

async def settings_kb(tg_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=await _(tg_id=tg_id, key="🤖 Выбрать нейросеть"), callback_data="select_ai")],
        [InlineKeyboardButton(text=await _(tg_id=tg_id, key="🏳️ Язык"), callback_data="set_language")]
    ])
    return keyboard

async def select_ai_kb(tg_id):
    keyboard = InlineKeyboardBuilder()
    for index, button in enumerate(ai_list):
        quantity_of_requests = await User.ai.get_requests(tg_id, ai_model_id=index)
        if index > 3: emoji = "🖼"
        else: emoji = "📝"
        keyboard.add(InlineKeyboardButton(text=f"{emoji}{button} ({quantity_of_requests})", callback_data=f"ai_{index}"))

    return keyboard.adjust(1).as_markup()
