from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from ai import response_to_ai
import re
from translations.translate import translate as _


pattern = f"([{re.escape(r'_\*\[\]\(\)~>\#+\-=|{}\.!')}])"
router = Router()



@router.message(F.text)
async def request_to_ai(message: Message):
    if message.text.startswith("/"): 
        return
    
    enter_ai = await response_to_ai(tg_id=message.from_user.id, text=message.text)
    if enter_ai == "":
        await message.reply(text="Empty text returned, try again")
        return
    
    text = re.sub(pattern, 
                  r"\\\1", 
                  enter_ai) #shielding
    
    await message.reply(text=str(text), 
                        parse_mode=ParseMode.MARKDOWN_V2)
    
@router.message(F.photo)
async def request_to_ai_photo(message: Message):
    image =f"images/photo_{message.photo[-1].file_id}.png"
    # print(message.caption)

    await message.bot.download(    
        file=message.photo[-1].file_id, 
        destination=image
        )
    enter_ai = await response_to_ai(
        tg_id=message.from_user.id,
        text=message.caption, 
        image_path=image)
    
    text = re.sub(pattern, 
                  r"\\\1", 
                  enter_ai) #shielding
    await message.reply(text=str(text), 
                        parse_mode=ParseMode.MARKDOWN_V2)