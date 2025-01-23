from g4f.client import AsyncClient
from g4f.Provider import Airforce, ChatGptEs, Blackbox, ChatGptt, Liaobots, ChatGptEs
from database.models import UserOrm

ai_list = ["gpt-4o-mini", "gpt-4o", "llama-3.1-405b", "claude-3.5-sonnet", "playground-v2.5", "sd-3"]
# ai_dict = {UserOrm.gpt4omini: "gpt-4o-mini", UserOrm.gpt4o:"gpt-4o", UserOrm.llama31405b: "llama-3.1-405b", UserOrm.claude35sonnet: "claude-3.5-sonnet", "playground-v2.5", "sd-3" }


async def response_to_ai(text: str, ai_id: int = 0):
    client = AsyncClient()
    if ai_id < 4:
        provider = None
        if ai_id < 3: provider = ChatGptEs
        response = await client.chat.completions.create(
            model=ai_list[ai_id],
            provider=provider,
            messages=[
                {
                    "role": "user",
                    "content":f"{text}"
                }
            ])
        return response.choices[0].message.content
    
    elif ai_id > 3:
        model = ai_list[ai_id]

        response = await client.images.generate(
            prompt=f"{text}",
            model=model
        )
    return response.data[0].url