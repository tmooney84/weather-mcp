from abc import ABC, abstractmethod

class LLMProvider(ABC):
    
    @abstractmethod
    async def chat(self, messages, tools=None):
        pass