from .base import BaseGenerative
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from .base import BaseGenerative
from typing import Optional
import os
from loguru import logger

class LangChainGoogleGenerative(BaseGenerative):
    def __init__(
        self,
        name: str = "gemini-2.5-flash",
        apiKey: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: Optional[int] = None
    ):
        super().__init__(name=name)
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        
        # Set environment variable if apiKey is provided
        if apiKey:
            os.environ["GOOGLE_API_KEY"] = apiKey
        
        self._init_chat_model()

    def _init_chat_model(self):
        try:
            chat_config = {
                "model": self.name,
                "temperature": self.temperature
            }
            if self.max_output_tokens:
                chat_config["max_output_tokens"] = self.max_output_tokens
                
            self.chat_model = ChatGoogleGenerativeAI(**chat_config)
        except Exception as e:
            logger.error(f"Failed to initialize chat model: {str(e)}")
            raise

    async def generate_response(self, user_message: str, **kwargs) -> str:
        try:
            response = await self.chat_model.ainvoke(user_message, **kwargs)
            return response.content
        except Exception as e:
            logger.error(f"Failed to generate response: {str(e)}")
            raise