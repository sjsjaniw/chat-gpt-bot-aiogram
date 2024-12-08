from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os


async def premium():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="beginner", callback_data="premium_beginner")],
        [InlineKeyboardButton(text="basic", callback_data="premium_basic")],
        [InlineKeyboardButton(text="master", callback_data="premium_master")],
    ])
    return keyboard

async def donate_button(lvl: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Stars", pay=True, callback_data=f"payStars_{lvl}")],
        [InlineKeyboardButton(text="Криптаволюта", callback_data=f"payCrypto_{lvl}")]
    ])
    return keyboard