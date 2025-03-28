from g4f.client import AsyncClient
from g4f.Provider import Blackbox
import aiofiles
import io
import redis
import json


ai_list = ["o3-mini"]

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

async def add_message(key: str, role: str, content: str) -> None:
    message = {"role": role, "content": content}
    r.rpush(key, json.dumps(message))

async def get_all_messages(key: str) -> list:
    raw_messages = r.lrange(key, 0, -1)
    return [json.loads(msg) for msg in raw_messages]
    
async def response_to_ai(tg_id: int, text: str, image_path: str | None = None, web_search: bool = False) -> str:
    client = AsyncClient()
    key = f"messages_{tg_id}"

    if text == None: text = ""
    await add_message(key, "user", text)
    messages = await get_all_messages(key)
    
    image = None
    if image_path: 
        with open(image_path, "rb") as image:
            image_data = image.read()
        image_io = io.BytesIO(image_data)
        
        response = client.chat.completions.create(
            model=ai_list[0],
            provider=Blackbox,
            messages=messages,
            web_search=web_search,
            image=image_io,
            stream=True)      
    else:
        response = client.chat.completions.create(
            model=ai_list[0],
            provider=Blackbox,
            messages=messages,
            web_search=web_search,
            image=image,
            stream=True)
        
    if image_path: 
        await aiofiles.os.remove(path=image_path)
    
    full_response = ""
    async for completion in response:
        chunk = completion.choices[0].delta.content or ""
        full_response += chunk
    
    messages = await get_all_messages(key)
    await add_message(key, "assistant", full_response)
    return full_response