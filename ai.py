from g4f.client import AsyncClient
from g4f.Provider import Blackbox
from aiofiles.os import remove
import aiofiles
import io
import redis.asyncio as redis
import json

client = AsyncClient()
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


async def add_message(key: str, role: str, content: str) -> None:
    message = {"role": role, "content": content}
    await redis_client.rpush(key, json.dumps(message))

async def get_all_messages(key: str) -> list:
    raw_messages = await redis_client.lrange(key, 0, -1)
    return [json.loads(msg) for msg in raw_messages]
    
async def response_to_ai(tg_id: int, text: str, image_path: str | None = None, web_search: bool = False) -> str:
    key = f"messages_{tg_id}"

    if text == None: text = ""
    await add_message(key, "user", text)
    messages = await get_all_messages(key)
    
    image = None
    if image_path: 
        with aiofiles.open(image_path, "rb") as image:
            image_data = await image.read()
        image_io = io.BytesIO(image_data)
        
        response = client.chat.completions.create(
            model="o3-mini",
            provider=Blackbox,
            messages=messages,
            web_search=web_search,
            image=image_io,
            stream=True)      
    else:
        response = client.chat.completions.create(
            model="o3-mini",
            provider=Blackbox,
            messages=messages,
            web_search=web_search,
            image=image,
            stream=True)
        
    if image_path: 
        await remove(path=image_path)
    
    full_response = ""
    async for completion in response:
        chunk = completion.choices[0].delta.content or ""
        full_response += chunk

    await add_message(key, "assistant", full_response)
    return full_response