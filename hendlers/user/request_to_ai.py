from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode
from ai import response_to_ai
from database.requests import User
import aiofiles.os

router = Router()

@router.message(F.text)
async def test(message: Message):
    ai_id = (await User.get(tg_id=message.from_user.id)).ai_id

    if message.text.startswith("/"): 
        return None 
    enter_ai = await response_to_ai(text=message.text, ai_id = ai_id)
    
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