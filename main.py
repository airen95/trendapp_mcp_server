from fastmcp import FastMCP
from app.crawlers import (
    RedditTrendingCrawler,
    YoutubeTrendingCrawler,
    HuggingFaceCrawler,
    SERPCrawler
)
from app.tools.tag_parser import parse_tags
from app.const.tags import get_predefined_tags_prompt
from app.schemas.posts import ToolResponse
from loguru import logger
from typing import Any

# Initialize crawlers
reddit_crawler = RedditTrendingCrawler()
youtube_crawler = YoutubeTrendingCrawler()
hugging_crawler = HuggingFaceCrawler()
google_crawler = SERPCrawler()

mcp = FastMCP("trending-crawlers")


@mcp.tool()
async def get_predefined_tags() -> dict:
    """
    Get the list of predefined tags and prompt for LLM.
    
    LLMs should call this first to know which tags are available.
    
    Returns:
        dictionary with available tags and usage instructions
    """
    from app.const.tags import PREDEFINED_TAGS
    
    return {
        "available_tags": sorted(PREDEFINED_TAGS),
        "total_tags": len(PREDEFINED_TAGS),
        "instructions": get_predefined_tags_prompt(),
        "example_usage": [
            ["politician", "movies", "climate", "discussion"],
            ["ai", "machine_learning", "paper"],
            ["music", "gaming", "entertainment"]
        ]
    }


@mcp.tool()
async def process_interest(
    tags: list[str],
    region_code: str = "VN",
    max_results_per_crawler: int = 20,
) -> dict:
    """
    Process user interest and fetch trending content from appropriate crawlers.
    
    This is the main entry point for fetching trending content.
    
    Args:
        tags: list of PREDEFINED tags (call get_predefined_tags() to see available tags)
              Example: ["politician", "movies", "climate", "discussion"]
        region_code: Region code for YouTube/Google (default: "VN")
        max_results_per_crawler: Maximum results per crawler (default: 20)
        
    Returns:
        Trending content from appropriate crawlers based on tags
    """
    if not tags:
        return {
            "error": "tags must be provided",
            "hint": "Call get_predefined_tags() to see available tags"
        }
    
    # Parse tags into crawler configurations
    crawler_configs = parse_tags(tags)
    
    logger.info(f"Input tags: {tags}")
    logger.info(f"Generated {len(crawler_configs)} crawler configs")
    
    all_data = []
    metadata = {
        "input_tags": tags,
        "region": region_code,
        "crawler_configs": crawler_configs
    }
    
    # Execute each crawler configuration
    for config in crawler_configs:
        crawler_name = config["crawler"]
        assigned_tags = config["assigned_tags"]
        params = config.get("params", {})
        
        logger.info(f"Executing {crawler_name} with tags: {assigned_tags}")
        
        try:
            if crawler_name == "youtube":
                results = await _fetch_youtube(
                    max_results=max_results_per_crawler,
                    category_ids=params.get("category_ids", []),
                    tags=assigned_tags
                )
                all_data.extend(results)
                
            elif crawler_name == "google_trends":
                results = await _fetch_google_trends(
                    category_id=params.get("category_id"),
                    tags=assigned_tags
                )
                all_data.extend(results)
                
            elif crawler_name == "reddit":
                results = await _fetch_reddit(
                    max_results=max_results_per_crawler,
                    tags=assigned_tags
                )
                all_data.extend(results)
                
            elif crawler_name == "huggingface":
                results = await _fetch_huggingface(
                    tags=assigned_tags
                )
                all_data.extend(results)
                
        except Exception as e:
            logger.error(f"Error fetching from {crawler_name}: {e}")
            # Continue with other crawlers even if one fails
    
    return ToolResponse(
        data=all_data,
        total=len(all_data),
        metadata=metadata
    )


async def _fetch_youtube(
    max_results: int,
    category_ids: list[str],
    tags: list[str]
) -> list[dict[str, Any]]:
    """Fetch from YouTube, potentially multiple calls for multiple categories"""
    all_videos = []
    
    if category_ids:
        # Fetch for each category
        for category_id in category_ids:
            logger.info(f"Fetching YouTube category {category_id}")
            videos = await youtube_crawler.get_trending_videos(
                max_results=max_results // len(category_ids),
                category_id=category_id,
                tags=tags
            )
            all_videos.extend(videos)
    else:
        # Fetch without category filter
        videos = await youtube_crawler.get_trending_videos(
            max_results=max_results,
        )
        all_videos.extend(videos)
    
    logger.info(f"YouTube returned {len(all_videos)} videos")
    return all_videos


async def _fetch_google_trends(
    category_id: str,
    tags: list[str]
) -> list[dict[str, Any]]:
    """Fetch from Google Trends"""
    trends = await google_crawler.get_trending_now(
        category_id=category_id,
        tags=tags
    )
    
    logger.info(f"Google Trends returned {len(trends)} items")
    if category_id:
        logger.info(f"Used category: {category_id}")
    
    return trends


async def _fetch_reddit(
    max_results: int,
    tags: list[str]
) -> list[dict[str, Any]]:
    """Fetch from Reddit"""
    # Use first tag as subreddit or default to 'all'
    subreddit = tags[0] if tags else "Vietnam"
    
    posts = await reddit_crawler.get_trending_posts(
        subreddit_name=subreddit,
        limit=max_results,
        tags=tags
    )
    
    logger.info(f"Reddit returned {len(posts)} posts")
    return posts


async def _fetch_huggingface(
    tags: list[str]
) -> list[dict[str, Any]]:
    """Fetch from HuggingFace"""
    papers = await hugging_crawler.get_trending_papers(
        tags=tags
    )

    logger.info(f"HuggingFace returned {len(papers)} papers")
    return papers


if __name__ == "__main__":
    mcp.run(transport="http")