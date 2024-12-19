from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from database.requests import User
from keyboards.main_kb import main_reply_keyboard
from keyboards.other_kb import set_language_keyboard
from translations.translate import translate as _

router = Router()

@router.message(CommandStart())
async def command_start(message: Message):
    if await User.get(tg_id=message.from_user.id):
        await message.answer(await _(tg_id=message.from_user.id, key="Рады видеть вас снова! 🤗"), reply_markup=await main_reply_keyboard(tg_id=message.from_user.id))
    else:
        await message.answer(text="Select language: | Выберите язык:", reply_markup=await set_language_keyboard())