import aiohttp
from .base import LLMProvider

class OllamaProvider(LLMProvider):

    def __init__(
        self,
        model="granite4.0-h-tiny",
        ### url="http://localhost:11434/api/chat",
        url="http://localhost:11435/api/chat",
    ):
        self.model = model
        self.url = url
        self.session = aiohttp.ClientSession()

    async def chat(self, messages, tools=None):

        payload ={
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        if tools:
            payload["tools"] = tools

        async with self.session.post(
            self.url,
            json=payload,
        ) as resp:

            return await resp.json()
    
    async def close(self):
        await self.session.close()