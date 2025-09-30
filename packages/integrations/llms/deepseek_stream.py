import aiohttp
from typing import AsyncGenerator

class DeepSeekStreamClient:
    def __init__(self, api_key: str):
        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def stream_chat(self, messages: list, model: str = "deepseek-chat") -> AsyncGenerator[str, None]:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": model,
                "messages": messages,
                "stream": True
            }
            async with session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=self.headers
            ) as resp:
                async for chunk in resp.content:
                    if chunk:
                        yield chunk.decode()