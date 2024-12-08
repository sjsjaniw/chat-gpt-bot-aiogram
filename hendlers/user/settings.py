from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.settings_kb import settings_kb, select_ai_kb
from database.requests import User
from ai import ai_list

router = Router()

@router.message(F.text == "Настройки")
async def setting(message: Message):
    await message.answer(text="settings", reply_markup=await settings_kb())

@router.callback_query(F.data == "select_ai")
async def select_ai(callback_query: CallbackQuery):
    await callback_query.message.answer(text="Выберете нейросеть:", reply_markup=await select_ai_kb(tg_id=callback_query.from_user.id))

@router.callback_query(lambda callback_query: callback_query.data.startswith("ai_"))
async def select_ai_id(callback_query: CallbackQuery, state: FSMContext):
    ai_id = int(callback_query.data.split("_")[1])
    tg_id = callback_query.from_user.id
    await User.edit.ai_id(tg_id=tg_id, ai_id=ai_id)
    await callback_query.message.delete()
    await callback_query.message.answer(f"Была выбрана {ai_list[ai_id]}")
    