from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from database.requests import User
from keyboards.main_kb import main_reply_keyboard

router = Router()

@router.message(CommandStart())
async def command_start(message: Message):
    if await User.get(tg_id=message.from_user.id):
        await message.answer("Рады видеть вас снова!", reply_markup=await main_reply_keyboard())
    else:
        await User.add(tg_id=message.from_user.id)
        await message.answer("Добро пожадловать впервые!", reply_markup=await main_reply_keyboard())