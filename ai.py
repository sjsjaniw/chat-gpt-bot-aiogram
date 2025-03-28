from g4f.client import AsyncClient
from g4f.Provider import Blackbox
import aiofiles
import io

ai_list = ["o3-mini"]

messages = []
async def response_to_ai(text: str, image_path: str | None = None, web_search: bool = False):
    client = AsyncClient()

    if text == None: text = ""
    messages.append({"role": "user", "content": text})
    
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
        
    messages.append({"role": "assistant", "content": full_response})
    return full_response