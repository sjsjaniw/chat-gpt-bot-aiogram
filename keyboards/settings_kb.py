from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.requests import User
from ai import ai_list


async def settings_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать нейросеть", callback_data="select_ai")],
        [InlineKeyboardButton(text="Язык", callback_data="language")]
    ])
    return keyboard

async def select_ai_kb():
    keyboard = InlineKeyboardBuilder()
    for index, button in enumerate(ai_list):
        keyboard.add(InlineKeyboardButton(text=button, callback_data=f"ai_{index}"))

    return keyboard.adjust(1).as_markup()
