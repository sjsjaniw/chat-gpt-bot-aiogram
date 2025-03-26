from g4f.client import AsyncClient
from g4f.Provider import Airforce, ChatGptEs, Blackbox, ChatGptt, Liaobots, ChatGptEs
from database.models import UserOrm
import aiofiles
import io

ai_list = ["o3-mini"]
# ai_dict = {UserOrm.gpt4omini: "gpt-4o-mini", UserOrm.gpt4o:"gpt-4o", UserOrm.llama31405b: "llama-3.1-405b", UserOrm.claude35sonnet: "claude-3.5-sonnet", "playground-v2.5", "sd-3" }


# async def response_to_ai(text: str, ai_id: int = 0):
#     client = AsyncClient()
#     if ai_id < 4:
#         provider = None
#         if ai_id < 3: provider = ChatGptEs
#         response = await client.chat.completions.create(
#             model=ai_list[ai_id],
#             provider=provider,
#             messages=[
#                 {
#                     "role": "user",
#                     "content":f"{text}"
#                 }
#             ])
#         return response.choices[0].message.content
    
#     elif ai_id > 3:
#         model = ai_list[ai_id]

#         response = await client.images.generate(
#             prompt=f"{text}",
#             model=model
#         )
#     return response.data[0].url

messages = []
async def response_to_ai(text: str, image_path: str | None = None, web_search: bool = False):
    print(image_path)
    client = AsyncClient()
    if text == None: text = ""
    messages.append({"role": "user", "content": text})
    print(messages)
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
    if image_path: await aiofiles.os.remove(path=image_path)
    full_response = ""
    async for completion in response:
        chunk = completion.choices[0].delta.content or ""
        print(chunk, end="", flush=True)
        full_response += chunk
    messages.append({"role": "assistant", "content": full_response})
    return full_response

    # model = ai_list[ai_id]

    # response = await client.images.generate(
    #     prompt=f"{text}",
    #     model="sdxl-turbo"
    # )
    # return response.data[0].url