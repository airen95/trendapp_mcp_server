import requests
from typing import List, Dict

from .base import BaseAsyncRequest
from app.const.url import HUGGINGFACE
from app.schemas.posts import BasePost


class HuggingFaceCrawler(BaseAsyncRequest):
    def __init__(self):
        super().__init__(HUGGINGFACE, {})

    async def get_trending_papers(self) -> List[Dict]:
        """
        Get trending models from Hugging Face
        """
        url = "https://huggingface-paper-explorer.vercel.app/api/papers?timeFrame=today"
        
        try:

            response = await self.get(
                path="papers?timeFrame=today",
            )
            
            trending_list = []
            for paper in response:
                trending_list.append(paper)
            
            return trending_list
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching trending models: {e}")
            return []
        
    async def health_check(self):
        return await super().health_check()