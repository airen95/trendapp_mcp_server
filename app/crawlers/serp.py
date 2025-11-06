from .base import BaseAsyncRequest
from app.const.url import SERP
from app.settings import settings
from app.schemas.posts import BasePost, GoogleSearchMetadata
from app.llm import LangchainDeepSeek
from loguru import logger
from datetime import datetime
import asyncio

summarizer = LangchainDeepSeek(
    api_key=settings.LLM_TOKEN,
    name="deepseek/deepseek-r1"
)

class SERPCrawler(BaseAsyncRequest):
    def __init__(self):
        super().__init__(SERP, {})
    
    async def get_trending_now(self, category_id: int | str, tags: list[str] = "trending") -> list[dict]:
        """
        Perform a search query on SERP and return results.
        
        Args:
            query: Search query string
            num_results: Number of results to return (default: 10)
        
        Returns:
            List of search results with metadata
        """
        try:
            params = {
                "engine": "google_trends_trending_now",
                "geo":"VN",
                "hours": "24",
                "category_id": category_id,
                "api_key": settings.SERP_TOKEN
            }

            response = await self.get(
                path="/search.json",
                params=params
                )
            data = []
            search_id = response.get("search_metadata", {}).get("id", "")
            for item in response.get("trending_searches", [])[:5]:
                news_supp = await self.get_trend_description(item.get("news_page_token"))
                categories = [i.get('name').lower() for i in item.get("categories", [])] or tags

                data.append(BasePost(
                    source="serp",
                    title=item.get("query"),
                    uid=f"{search_id}_{item.get('start_timestamp')}",
                    url=item.get(""),
                    author="",
                    content=news_supp.get("start_timestamp", ""),
                    tags=set(categories),
                    created_at=datetime.fromtimestamp(item.get("start_timestamp", 0)),
                    metadata_=GoogleSearchMetadata(thumbnail=news_supp.get("thumbnail", "")),
                    ))
                await asyncio.sleep(0.5)
            return data
        except Exception as e:
            logger.error(f"Error fetching SERP results: {e}")
            return []
    
    async def health_check(self):
        return await super().health_check()
    
    async def get_trend_description(self, news_page_token: str) -> dict[str, str]:
        try:
            params = {
                "engine": "google_trends_news",
                "page_token": news_page_token,
                "api_key": settings.SERP_TOKEN
            }

            response = await self.get(
                path="/search.json",
                params=params
                )

            news = response.get('news', [])
            news_title = [i.get('title') for i in news[:5]]
            thumbnail = news[0].get('thumbnail') if news else ''


            content = await self.general_content(news_title)
            return {
                "content": content,
                "thumbnail": thumbnail
            }
        except Exception as e:
            logger.error(f"Error summarizing content from SERP: {e}")
            return {}
        
    async def general_content(self, content: list[str]) -> str:
        try:
            messages = [
                {"role": "system",
                "content": "Only return answer. no explain"},
                {
                "role": "user",
                "content": f"Generate a short Vietnamese description for the following content: {content}"
                }
            ]
            response = await summarizer.generate_response(messages)
            return response
        except Exception as e:
            logger.error(f"Error summarizing content from SERP: {e}")
            return ""