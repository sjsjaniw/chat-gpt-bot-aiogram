from g4f.client import AsyncClient
from g4f.Provider import Airforce #only for flux

ai_list = ["gpt-4o-mini", "gpt-4o", "llama-3.2-90b", "claude-3.5-sonnet", "flux", "flux-realism", "flux-anime", "flux-pixel", "sd-3"]


async def response_to_ai(text: str, ai_id: int = 0):
    client = AsyncClient()
    
    if ai_id < 4:
        response = await client.chat.completions.create(
            model=ai_list[ai_id],
            messages=[
                {
                    "role": "user",
                    "content": f"кратко {text}"
                }
            ])
        return response.choices[0].message.content
    
    elif ai_id > 3:
        provider = None
        if ai_id == 4: #flux
            provider=Airforce
        model = ai_list[ai_id]

        response = await client.images.generate(
            prompt=f"{text}",
            provider=provider,
            model=model
        )
    return response.data[0].url