from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, PollAnswer, SuccessfulPayment
from keyboards.other_kb import donate_button, premium
from database.requests import User

router = Router()

@router.message(F.text == "Премиум 👉👈")
async def setting(message: Message):
    await message.answer_photo(photo = "AgACAgIAAxkBAAIOZWdDXl5yfp1b18b5ljMcwsrQxRUjAAL96jEbAowYSug-7gd0F-J2AQADAgADbQADNgQ",
                               caption="Представляем вам иновационную функцию ДОНАТА! Ещё никто такого не делал.\nБот позволяет полностью бесплатно пользоваться Chat GPT версией 4o-mini и так как прибыли от него нет, была введена функция доната.\nЕсли вам нравится этот бот и вы хотите помочь в его развитии и дальнейшем существовании, вы можете задонатить нам. Все средства пойдут на оплату сервера и улучшение функционала.\nСпасибо за вашу поддержку!",
                               reply_markup=await premium())
    
@router.callback_query(lambda callback_query: callback_query.data.startswith("premium_"))
async def select_premium(callback_query: CallbackQuery):
    premium = callback_query.data.split("_")[1]
    if premium == "beginner":
        await callback_query.message.answer(text="beginner", reply_markup=await donate_button(1))
    if premium == "basic":
        await callback_query.message.answer(text="basic", reply_markup=await donate_button(2))
    if premium == "master":
        await callback_query.message.answer(text="master", reply_markup=await donate_button(3))

@router.callback_query(lambda callback_query: callback_query.data.startswith("payStars_"))
async def returnqwe(callback_query: CallbackQuery):
    level = int(callback_query.data.split("_")[1])
    if level == 1: payload = 50
    if level == 2: payload = 150
    if level == 3: payload = 300
    await callback_query.message.answer_invoice(title="Премиум", 
                                                description="Премиум", 
                                                payload=str(payload),
                                                currency="XTR", 
                                                prices=[LabeledPrice(label="XTR", amount=payload)])

@router.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery):
    await query.answer(True)

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    payload = int(message.successful_payment.invoice_payload)
    if payload == 50:
        await User.ai.level.set(tg_id=message.from_user.id, level=1)
    if payload == 150:
        await User.ai.level.set(tg_id=message.from_user.id, level=2)
    if payload == 300:
        await User.ai.level.set(tg_id=message.from_user.id, level=3)
    await User.ai.subscription_date.set(tg_id=message.from_user.id)