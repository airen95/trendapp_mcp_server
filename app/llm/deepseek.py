from .base import BaseGenerative
from  openai import AsyncOpenAI
import json
import httpx
from loguru import logger

class LangchainDeepSeek(BaseGenerative):
    def __init__(self, 
                 api_key: str,
                 name: str = "deepseek/deepseek-r1:free",
                 base_url: str = "https://openrouter.ai/api/v1",
                 temperature: float = 0.3 ):
        super().__init__(name)

        self.api_key = api_key
        self.base_url = f"{base_url}/chat/completions"
        self.temperature = temperature
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)  # Initialize once

    # def __init_model(self) -> AsyncGenerator:
    #     client = AsyncOpenAI(api_key=self.api_key,
    #                          base_url=self.base_url)
    #     return client

    async def generate_response(self, messages: list[dict[str, str]], max_tokens: int = 1000) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.name,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": max_tokens
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(self.base_url, headers=headers, json=payload, timeout=60)
                response.raise_for_status()
                content = response.json()

                content = content["choices"][0]["message"]["content"]

                # Remove markdown code block if exists
                if content.startswith("```"):
                    content = content.strip("```").replace("json", "").strip()
                return content
            
        except Exception as e:
            logger.error(f"JSON decode error: {e} \nRaw response:\n{content}")
            raise e