import json
import aiofiles
from database.requests import User

async def translate(tg_id, key: str):
    language = (await User.get(tg_id=tg_id)).language
    async with aiofiles.open(f"translations/{language}.json", mode="r", encoding="utf-8") as file:
        data = json.loads(await file.read())
        return data.get(key)