from aiogram import Router, F
from aiogram.types import Message
from keyboards.other_kb import donate_button

router = Router()

@router.message(F.text == "Задонатить нам 👉👈")
async def setting(message: Message):
    await message.answer_photo(photo = "AgACAgIAAxkBAAIOZWdDXl5yfp1b18b5ljMcwsrQxRUjAAL96jEbAowYSug-7gd0F-J2AQADAgADbQADNgQ",
                               caption="Представляем вам иновационную функцию ДОНАТА! Ещё никто такого не делал.\nБот позволяет полностью бесплатно пользоваться Chat GPT версией 4o-mini и так как прибыли от него нет, была введена функция доната.\nЕсли вам нравится этот бот и вы хотите помочь в его развитии и дальнейшем существовании, вы можете задонатить нам. Все средства пойдут на оплату сервера и улучшение функционала.\nСпасибо за вашу поддержку!",
                               reply_markup=await donate_button())


