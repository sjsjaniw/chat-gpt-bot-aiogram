from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode
from ai import response_to_ai
from database.requests import User
import aiofiles.os

router = Router()

@router.message(F.text)
async def request_to_ai(message: Message):
    if message.text.startswith("/"): 
        return None
    
    ai_id = (await User.get(tg_id=message.from_user.id)).ai_id
    ai_requests = await User.ai.check_requests(tg_id=message.from_user.id, ai_model_id=ai_id)
    
    if ai_requests: 
        enter_ai = await response_to_ai(text=message.text, ai_id=ai_id)
    else:
        await message.answer("У вас кончились запросы")
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

    await User.ai.remove_requests(tg_id=message.from_user.id, ai_model_id=ai_id, quantity_of_requests=1)