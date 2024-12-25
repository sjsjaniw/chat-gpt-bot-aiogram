from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, PollAnswer, SuccessfulPayment
from keyboards.other_kb import donate_button, premium
from database.requests import User
from crypto_pay_api_sdk import cryptopay
from aiogram.fsm.context import FSMContext
from translations.translate import translate as _
import os

router = Router()
Crypto = cryptopay.Crypto(os.getenv("CRYPTO_BOT_API"), testnet = True)

@router.message((F.text == "Премиум 👉👈") | (F.text == "Premium 👉👈"))
async def setting(message: Message):
    await message.answer_photo(photo = "AgACAgIAAxkBAAIOZWdDXl5yfp1b18b5ljMcwsrQxRUjAAL96jEbAowYSug-7gd0F-J2AQADAgADbQADNgQ",
                               caption=await _(tg_id=message.from_user.id, key="Бот позволяет пользовать Chatgpt 4o mini бесплатно 20 запросов а так же позволяет генерировать 4 изображения в день используя Playground-v2.5 и sd-3.\nВы можете увеличить количество запросов купив премиум на 30 дней.😊\n\n🧑‍🦽‍➡️Beginner:\n- Chatgpt 4o mini - 50 сообщений в день 📝\n- Chatgpt 4o - 20 сообщений в день 📝\n- Llama-3.1-405b - 30 сообщений в день 📝\n- Claude 3.5-sonnet - 30 сообщений в день 📝\n- Playground-v2.5 - 10 изображений в день 🖼\n- sd-3 - 15 изображений в день 🖼\n\n🚶‍➡️Basic:\n- Chatgpt 4o mini - 100 сообщений в день 📝\n- Chatgpt 4o - 50 сообщений в день 📝\n- Llama-3.1-405b - 75 сообщений в день 📝\n- Claude 3.5-sonnet - 75 сообщений в день 📝\n- Playground-v2.5 - 20 изображений в день 🖼\n- sd-3 - 30 изображений в день 🖼\n\n🏃‍➡️Master:\n- Chatgpt 4o mini - 100 сообщений в день 📝\n- Chatgpt 4o - 50 сообщений в день 📝\n- Llama-3.1-405b - 75 сообщений в день 📝\n- Claude 3.5-sonnet - 75 сообщений в день 📝\n- Playground-v2.5 - 20 изображений в день 🖼\n- sd-3 - 30 изображений в день 🖼"),
                               reply_markup=await premium())
    
@router.callback_query(lambda callback_query: callback_query.data.startswith("premium_"))
async def select_premium(callback_query: CallbackQuery):
    premium = callback_query.data.split("_")[1]
    if premium == "beginner":
        await callback_query.message.answer(text="beginner", reply_markup=await donate_button(lvl=1, tg_id=callback_query.from_user.id))
    if premium == "basic":
        await callback_query.message.answer(text="basic", reply_markup=await donate_button(lvl=2, tg_id=callback_query.from_user.id))
    if premium == "master":
        await callback_query.message.answer(text="master", reply_markup=await donate_button(lvl=3, tg_id=callback_query.from_user.id))

@router.callback_query(lambda callback_query: callback_query.data.startswith("payStars_"))
async def paystars(callback_query: CallbackQuery):
    level = int(callback_query.data.split("_")[1])
    if level == 1: payload = 25
    if level == 2: payload = 75
    if level == 3: payload = 150
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
    if payload == 25:
        await User.ai.level.set(tg_id=message.from_user.id, level=1)
    if payload == 75:
        await User.ai.level.set(tg_id=message.from_user.id, level=2)
    if payload == 150:
        await User.ai.level.set(tg_id=message.from_user.id, level=3)
    await User.ai.subscription_date.set(tg_id=message.from_user.id)

@router.callback_query(lambda callback_query: callback_query.data.startswith("payCrypto_"))
async def paycrypto(callback_query: CallbackQuery, state: FSMContext):
    if (await state.get_data()).get("invoice_id"):
        data = await state.get_data()
        get_invoice_status = (Crypto.getInvoices(params = {"asset": "TON", "invoice_ids": int(data.get("invoice_id"))})).get('result', {}).get('items', [{}])[0].get("status")

        if get_invoice_status == "paid":
            await User.ai.level.set(tg_id=callback_query.from_user.id, level=int(data.get("level")))
            await User.ai.subscription_date.set(tg_id=callback_query.from_user.id)
            await state.clear()
        if get_invoice_status == "active":
            print("not paid")
        else:
            print("expired")
    else:
        level = int(callback_query.data.split("_")[1])

        if level == 1: amount = 0.075
        if level == 2: amount = 0.15
        if level == 3: amount = 0.225

        invoice = Crypto.createInvoice("TON", amount=str(amount), params={"description": "a", "expires_in": 300})
        invoice_id = int(invoice.get('result').get('invoice_id'))
        await state.update_data(invoice_id=invoice_id)
        await state.update_data(level=level)

        await callback_query.message.answer(text=await _(tg_id=callback_query.from_user.id, key="Можете оплатить криптовалютой прейдя по ссылке 💰")+f"\n{(Crypto.getInvoices(params={{'asset': 'TON', 'invoice_ids': invoice_id}})).get('result', {}).get('items', [{}])[0].get('pay_url')}")
@router.callback_query()
async def give_premium(callback_query: CallbackQuery, state: FSMContext):
    if (await state.get_data()).get("invoice_id"):
        data = await state.get_data()
        get_invoice_status = (Crypto.getInvoices(params = {"asset": "TON", "invoice_ids": int(data.get("invoice_id"))})).get('result', {}).get('items', [{}])[0].get("status")
        if get_invoice_status == "paid":
            await User.ai.level.set(tg_id=callback_query.from_user.id, level=int(data.get("level")))
            await User.ai.subscription_date.set(tg_id=callback_query.from_user.id)
            await state.clear()