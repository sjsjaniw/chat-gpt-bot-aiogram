from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode
from ai import response_to_ai
from database.requests import User
import re
from translations.translate import translate as _

router = Router()

@router.message(F.text)
async def request_to_ai(message: Message):
    if message.text.startswith("/"): 
        return
    
    enter_ai = await response_to_ai(text=message.text)
    if enter_ai == "":
        await message.reply(text="Empty text, try again", parse_mode=ParseMode.MARKDOWN_V2)
        return
    pattern = f"([{re.escape(r'_\*\[\]\(\)~>\#+\-=|{}\.!')}])"
    text = re.sub(pattern, r"\\\1", enter_ai) #shielding
    await message.reply(text=str(text), parse_mode=ParseMode.MARKDOWN_V2)
    
@router.message(F.photo)
async def request_to_ai_photo(message: Message):
    print(message.caption)
    await message.bot.download(file=message.photo[-1].file_id, destination=f"images/photo_{message.photo[-1].file_id}.png")
    enter_ai = await response_to_ai(text=message.caption, image_path=f"images/photo_{message.photo[-1].file_id}.png")
    pattern = f"([{re.escape(r'_\*\[\]\(\)~>\#+\-=|{}\.!')}])"
    text = re.sub(pattern, r"\\\1", enter_ai) #shielding
    await message.reply(text=str(text), parse_mode=ParseMode.MARKDOWN_V2)