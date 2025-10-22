from fastmcp import FastMCP
from app.crawlers import (RedditTrendingCrawler, 
                          YoutubeTrendingCrawler,
                          HuggingFaceCrawler)
from app.tools.tool_routers import DetermineTags
from app.schemas.posts import ToolResponse

reddit_crawler = RedditTrendingCrawler()
youtube_crawler = YoutubeTrendingCrawler()
hugging_crawler = HuggingFaceCrawler()

mcp = FastMCP("trending-crawlers")

@mcp.tool()
async def process_interest(
    tags: list[str] = None,
) -> dict:
    """
    Process user interest and fetch trending content from appropriate crawlers.
    
    This is the ONLY exposed MCP tool - the main entry point for clients.
    
    Args:
        tags: List of tags (e.g., ["python", "discussion", "tutorial"])
        user_query: Natural language query (e.g., "Show me trending AI discussions")
    
    Returns:
        Trending content from appropriate crawlers based on interest
    """
    if not tags:
        return {"error": "tags must be provided"}
    
    crawl_router = DetermineTags(tags=tags)

    # Determine crawlers
    route = crawl_router.determine_crawler_from_tags()
    crawlers = route["crawlers"]
    
    data = []
    
    # Fetch from determined crawlers
    if "reddit" in crawlers:
        reddit_result = await reddit_crawler.get_trending_posts(
            subreddit_name="Vietnam",
            limit=20
        )

        data.extend(reddit_result)
    if "youtube" in crawlers:
        youtube_result = await youtube_crawler.get_trending_videos(
            region_code='VN',
            max_results=10
        )

        data.extend(youtube_result)
    
    if "huggingface" in crawlers:
        hf_result = await hugging_crawler.get_trending_papers()

        data.extend(hf_result)
    return ToolResponse(
        data=data,
        total=len(data)
    )

if __name__ == "__main__":
    mcp.run(transport="http")