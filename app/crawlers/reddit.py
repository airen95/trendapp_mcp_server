import asyncpraw
from datetime import datetime
from app.settings import settings
from app.schemas.posts import BasePost, RedditPost
from loguru import logger

class RedditTrendingCrawler:
    def __init__(self, user_agent: str = "trending_analyzer_v1.0"):
        self.user_agent = user_agent
        self.reddit = None

    async def _initialize_reddit(self):
        """Initialize Reddit client lazily."""
        if self.reddit is None:
            try:
                self.reddit = asyncpraw.Reddit(
                    client_id=settings.REDDIT_CLIENT,
                    client_secret=settings.REDDIT_TOKEN,
                    user_agent=self.user_agent
                )
            except Exception as e:
                logger.error(f"Failed to initialize Reddit client: {e}")
                raise e
    
    async def get_trending_posts(self, subreddit_name='all', limit=50, time_filter='day') -> list[dict]:
        """
        Fetch trending posts from a Reddit subreddit.
        
        Args:
            subreddit_name: Subreddit to fetch from (default: 'all')
            limit: Number of posts to fetch (default: 50)
            time_filter: Time filter - 'day', 'week', 'month', 'year', 'all' (default: 'day')
        
        Returns:
            List of trending posts with metadata
        """
        try:
            await self._initialize_reddit()

            subreddit = await self.reddit.subreddit(subreddit_name)
            trending_posts = []
            
            async for post in subreddit.top(time_filter=time_filter, limit=limit):
                trending_posts.append(
                    BasePost(
                        source="reddit",
                        title=post.title,
                        content=post.selftext,
                        url=post.url,
                        created_at=datetime.fromtimestamp(post.created_utc),
                        author=post.subreddit.display_name,
                        metadata=RedditPost(
                            post_id=post.id,
                            permalink=f"https://reddit.com{post.permalink}",
                            upvote_ratio=post.upvote_ratio
                        ),
                        relevance_score=post.upvote_ratio * post.score / 100 if post.upvote_ratio else 0
                    )
                )            
            return trending_posts
        except Exception as e:
            print(f"Error fetching trending posts from r/{subreddit_name}: {e}")
            return []
    
    

