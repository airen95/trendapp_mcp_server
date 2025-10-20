import requests
from app.settings import settings
from .base import BaseAsyncRequest
from app.const.url import YOUTUBE
from app.schemas.posts import YoutubePost, BasePost
from loguru import logger


class YoutubeTrendingCrawler(BaseAsyncRequest):
    def __init__(self):
        headers = {
            "Authorization": f"Bearer {settings.YOUTUBE_API_KEY}",
        }
        super().__init__(YOUTUBE, headers)

    async def health_check(self) -> dict:
        """Health check for YouTube API."""
        try:
            _ = await self.get(
                "/videos",
                params={"part": "snippet", "chart": "mostPopular", "maxResults": 1}
            )
            return {"status": "healthy", "service": "youtube"}
        except Exception as e:
            logger.error(f"YouTube health check failed: {e}")
            return {"status": "unhealthy", "service": "youtube", "error": str(e)}

    async def get_trending_videos(self, region_code: str = 'US', max_results: int = 10) -> list[dict]:
        """
        Fetch trending videos from YouTube for a specific region.
        
        Args:
            region_code: ISO 3166-1 alpha-2 country code (default: 'US')
            max_results: Number of videos to fetch (default: 10, max: 50)
            category_id: Optional YouTube category ID to filter results
        
        Returns:
            List of trending videos with metadata
        """

        params = {
            'part': 'snippet,contentDetails,statistics',
            'chart': 'mostPopular',
            'regionCode': region_code,
            'maxResults': max_results,
        }
        
        try:
            response = await self.get(
                "/videos",
                params=params,
                timeout=30.0
            )

            trending_videos = []
            for item in response.get('items', []):
                trending_videos.append(
                    BasePost(
                        title=item['snippet']['title'],
                        content=item['snippet']['description'],
                        created_at=item['snippet']['publishedAt'],
                        author=item['snippet']['channelTitle'],
                        metadata=YoutubePost(
                            video_id=item['id'],
                            view_count=item['statistics'].get('viewCount', 0),
                            like_count=item['statistics'].get('likeCount', 0),
                            thumbnail=item['snippet']['thumbnails']['high']['url']
                        ),
                        relevance_score=self._calculate_relevance(item["statistics"])
                    )
                )
            return trending_videos
        
        except Exception as e:
            logger.warning(f"Cannot crawl youtube trending: {e}")
            return []
        
    @staticmethod
    def _calculate_relevance(statistics: dict) -> float:
        """Calculate relevance score based on views and likes."""
        view_count = int(statistics.get("viewCount", 0))
        like_count = int(statistics.get("likeCount", 0))
        
        if view_count == 0:
            return 0.0
        
        like_ratio = like_count / view_count if view_count > 0 else 0
        # Normalize to 0-1 scale (typical like ratio is 1-5%)
        return min(like_ratio * 20, 1.0)
