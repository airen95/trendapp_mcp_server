from mcp.server.fastmcp import FastMCP
from app.crawlers import (RedditTrendingCrawler, 
                          YoutubeTrendingCrawler,
                          HuggingFaceCrawler)
from datetime import datetime
from typing import Optional
from app.tools.tool_routers import DetermineTags

reddit_crawler = RedditTrendingCrawler()
youtube_crawler = YoutubeTrendingCrawler()
hugging_crawler = HuggingFaceCrawler()

mcp = FastMCP("trending-crawlers")

@mcp.tool()
async def process_interest(
    tags: Optional[list[str]] = None,
    user_query: Optional[str] = None
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
    if not tags and not user_query:
        return {"error": "Either tags or user_query must be provided"}
    
    crawl_router = DetermineTags(tags=tags, user_query=user_query)

    # Determine crawlers
    route = crawl_router.extract_input()
    crawlers = route["crawlers"]
    
    results = {
        "tags": tags,
        "crawlers_used": crawlers,
        "data": {},
        "fetched_at": datetime.now().isoformat()
    }
    
    # Fetch from determined crawlers
    if "reddit" in crawlers:
        reddit_result = await reddit_crawler.get_trending_posts(
            subreddit_name=route["reddit_subreddit"],
            limit=20
        )

        results["data"]["reddit"] = {
            "subreddit": route["reddit_subreddit"],
            "count": len(reddit_result),
            "posts": reddit_result
        }
    
    if "youtube" in crawlers:
        youtube_result = await youtube_crawler.get_trending_videos(
            region_code='VN',
            max_results=10
        )

        results["data"]["youtube"] = {
            "query": route["youtube_search_query"],
            "count": len(youtube_result),
            "videos": youtube_result
        }
    
    if "huggingface" in crawlers:
        hf_result = await hugging_crawler.get_trending_papers()

        results["data"]["huggingface"] = {
            "query": route["huggingface_search_query"],
            "count": len(hf_result),
            "results": hf_result
        }
    
    return results

if __name__ == "__main__":
    mcp.run(transport="stdio")