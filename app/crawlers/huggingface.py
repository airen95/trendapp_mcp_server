import requests
from typing import List, Dict
import asyncio

from .base import BaseAsyncRequest, BaseHTMLRequest
from app.const.url import HUGGINGFACE
from app.schemas.posts import BasePost, HFPost

class HuggingFaceCrawler(BaseAsyncRequest):
    def __init__(self):
        super().__init__(HUGGINGFACE, {})
        self.parser = BaseHTMLRequest()

    async def get_trending_papers(self, tags: list[str] = ['paper']) -> List[Dict]:
        """
        Get trending models from Hugging Face
        """
        url = "https://huggingface-paper-explorer.vercel.app/api/papers?timeFrame=today"
        
        try:

            response = await self.get(
                path="papers?timeFrame=today",
            )
            
            trending_list = []
            for paper in response[:3]:
                paper_url = paper.get("link")
                content = await self.get_paper_content(paper_url)
                trending_list.append(BasePost(
                    source = "hf",
                    title=paper.get("title"),
                    url = paper_url,
                    author=paper.get("submittedBy"),
                    content=content,
                    metadata_=HFPost(
                        thumbnail=paper.get("image"),
                        upvotes=paper.get("upvotes")
                    ),
                    tags=set(tags)
                ),
                )
                await asyncio.sleep(0.5)
            return trending_list
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching trending models: {e}")
            return []
        
    async def health_check(self):
        return await super().health_check()
    
    async def get_paper_content(self,paper_url: str) -> str:
        return await self.parser.find_one(paper_url, 'text-blue')