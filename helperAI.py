from openai import OpenAI
import httpx as _httpx
from settings import API_KEY,PROXIES

async def get_ai_text(messages):
    client = await get_gpt_client()
    try:
        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=messages,
                            )
        gpt_message= response.choices[0].message.content
    except Exception as e:
        print(e)
        gpt_message = "Извините, произошла ошибка."
    return gpt_message

async def get_ai_image(prompt : str):
    client = await get_gpt_client()
    try: 
        response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
        image_url = response.data[0].url
    except Exception as e:
        print(e)
        image_url = "Извините, произошла ошибка."
    return image_url

async def get_gpt_client():
    _http_client = _httpx.Client(proxies=PROXIES)
    return OpenAI(api_key=API_KEY,
                http_client=_http_client
                )
