from app.const.tags import TAG_ROUTES


class DetermineTags:
    def __init__(self, tags: list[str]):
        self.tags = tags

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

