from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.settings_kb import settings_kb, select_ai_kb
from keyboards.main_kb import main_reply_keyboard
from keyboards.other_kb import set_language_keyboard
from database.requests import User
from ai import ai_list
from translations.translate import translate as _

router = Router()

@router.message((F.text == "⚙️ Настройки") | (F.text == "⚙️ Settings"))
async def setting(message: Message):
    await message.answer(text="settings", reply_markup=await settings_kb(tg_id=message.from_user.id))

@router.callback_query(F.data == "select_ai")
async def select_ai(callback_query: CallbackQuery):
    await callback_query.message.answer(text=await _(tg_id=callback_query.from_user.id, key="🤖 Выберете нейросеть:"), reply_markup=await select_ai_kb(tg_id=callback_query.from_user.id))

@router.callback_query(lambda callback_query: callback_query.data.startswith("ai_"))
async def select_ai_id(callback_query: CallbackQuery, state: FSMContext):
    ai_id = int(callback_query.data.split("_")[1])
    tg_id = callback_query.from_user.id
    await User.edit.ai_id(tg_id=tg_id, ai_id=ai_id)
    await callback_query.message.delete()
    await callback_query.message.answer(await _(tg_id=tg_id, key="🤖 Была выбрана")+f"\n{ai_list[ai_id]}")
    
@router.callback_query(F.data == "set_language")
async def set_language_settings(callback_query: CallbackQuery):
    await callback_query.message.answer(text=await _(tg_id=callback_query.from_user.id, key="Выберете язык:"), reply_markup=await set_language_keyboard())

@router.callback_query(lambda callback_query: callback_query.data.startswith("lang_"))
async def set_language(callback_query: CallbackQuery):
    language = str(callback_query.data.split("_")[1])
    if await User.get(tg_id=callback_query.from_user.id):
        await User.edit.language(tg_id=callback_query.from_user.id, language=language)
        await callback_query.message.delete()
        if language == "ru":
            await callback_query.message.answer(text="Был выбран русский язык", reply_markup=await main_reply_keyboard(tg_id=callback_query.from_user.id))
        if language == "en":
            await callback_query.message.answer(text="Selected English language", reply_markup=await main_reply_keyboard(tg_id=callback_query.from_user.id))
    else:
        await User.add(tg_id=callback_query.from_user.id, language=language)
        await callback_query.message.answer(text=await _(tg_id=callback_query.from_user.id, key="Добро пожадловать впервые! 😊"), reply_markup=await main_reply_keyboard(tg_id=callback_query.from_user.id))