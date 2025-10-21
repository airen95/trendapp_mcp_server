from typing import Optional
from loguru import logger

from app.const.tags import TAG_ROUTES
from app.llm.gemini import LangChainGoogleGenerative
from app.settings import settings

gemini_llm = LangChainGoogleGenerative(
    apiKey=settings.GEMINI_KEY
)

class DetermineTags:
    def __init__(self, tags: Optional[list[str]] = None, user_query: Optional[str] = None):
        self.tags = tags
        self.user_query = user_query

    def determine_crawler_from_tags(self) -> dict:
        tags_lower = [t.lower() for t in self.tags]
        
        reddit_match = sum(1 for t in tags_lower if any(rt in t for rt in TAG_ROUTES["reddit"]))
        youtube_match = sum(1 for t in tags_lower if any(yt in t for yt in TAG_ROUTES["youtube"]))
        huggingface_match = sum(1 for t in tags_lower if any(hf in t for hf in TAG_ROUTES["huggingface"]))
        both_match = sum(1 for t in tags_lower if any(bt in t for bt in TAG_ROUTES["both"]))
        
        crawlers = []
        
        if both_match > 0:
            # Use all crawlers if "trending" or "popular" tags are present
            crawlers = ["reddit", "youtube", "huggingface"]
        elif huggingface_match >= 2:
            crawlers = ["huggingface"]
        elif youtube_match >= 2:
            crawlers = ["youtube"]
        elif reddit_match >= 2:
            crawlers = ["reddit"]
        elif huggingface_match > 0:
            crawlers = ["huggingface", "reddit"]
        elif youtube_match > 0:
            crawlers = ["youtube", "reddit"]
        else:
            crawlers = ["reddit"]  # default to reddit
        
        return {
            "crawlers": crawlers,
            "reddit_subreddit": tags_lower[0] if tags_lower else "all",
            "youtube_search_query": " ".join(tags_lower) if tags_lower else None,
            "huggingface_search_query": " ".join(tags_lower) if tags_lower else None
        }


    async def extract_tags_with_gemini(self) -> list[str]:

        try:
            prompt = f"""Extract 3-5 relevant tags from this query. Return only the tags separated by commas, no explanation.
                    Query: {self.user_query}
                    Tags:"""
            
            response = await gemini_llm.generate_response(user_message=prompt)
            
            tags = [t.strip() for t in response.text.split(",")]
            logger.info(f"Extracted tags from query: {tags}")
            return tags
        
        except Exception as e:
            logger.error(f"Error extracting tags with Gemini: {e}")
            return []
        
    async def extract_input(self):
        if not self.tags:
            self.tags = await self.extract_tags_with_gemini()
        return self.determine_crawler_from_tags()
