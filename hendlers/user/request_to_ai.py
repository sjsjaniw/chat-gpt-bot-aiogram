from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode
from ai import response_to_ai
from database.requests import User
import aiofiles.os
from datetime import timedelta, datetime, timezone

router = Router()

@router.message(F.text)
async def request_to_ai(message: Message):
    if message.text.startswith("/"): 
        return None
    
    tg_id = message.from_user.id
    ai_id = (await User.get(tg_id=tg_id)).ai_id
    ai_requests = await User.ai.get_requests(tg_id=tg_id, ai_model_id=ai_id)
    issued_requests_date = await User.ai.issued_requests_date.get(tg_id=tg_id)
    subscription_date = await User.ai.subscription_date.get(tg_id=tg_id)

    if subscription_date != None:
        if subscription_date+timedelta(days=30) <= datetime.now(timezone.utc).replace(tzinfo=None):
            await User.ai.subscription_date.set(tg_id=tg_id, date=None)
            await User.ai.level.set(tg_id=tg_id, level=0)

    if issued_requests_date+timedelta(days=1) <= datetime.now(timezone.utc).replace(tzinfo=None):
        print(issued_requests_date)
        await User.ai.issued_requests_date.set(tg_id=tg_id)
        await User.ai.set_base_requests(tg_id=tg_id, level=await User.ai.level.get(tg_id=tg_id))
        enter_ai = await response_to_ai(text=message.text, ai_id=ai_id)

    if ai_requests:
        enter_ai = await response_to_ai(text=message.text, ai_id=ai_id)
    else:
        await message.answer("У вас кончились запросы на сегодня")
        return

    if ai_id < 4:
        if enter_ai == "":
            await message.reply(text="error", parse_mode=ParseMode.MARKDOWN)
            return 0
        await message.reply(text=str(enter_ai), parse_mode=ParseMode.MARKDOWN)

    else:
        url = f"generated_images{str(enter_ai)[7:]}"
        photo = FSInputFile(path=url)
        await message.reply_photo(photo=photo)
        await aiofiles.os.remove(path=url)

    await User.ai.remove_requests(tg_id=tg_id, ai_model_id=ai_id, quantity_of_requests=1)