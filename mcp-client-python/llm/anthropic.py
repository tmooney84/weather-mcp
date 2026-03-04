import os
from anthropic import Anthropic
from .base import LLMProvider

class AnthropicProvider(LLMProvider):

    def __init__(
            self,
            model="claude-sonnet-4-5",
    ):
        
        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        self.model = model
    
    async def chat(self, messages, tools=None):

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=messages,
            tools=tools,
        )

        return response