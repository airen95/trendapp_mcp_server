from typing import List, Dict, Optional, Set
from dataclasses import dataclass


# Predefined tags that LLMs can return
PREDEFINED_TAGS = [
    # Reddit-focused tags
    "discussion",
    "community",
    "news",
    "social",
    "meme",
    "ask",
    
    # YouTube video types
    "video",
    "entertainment",
    "music",
    "tutorial",
    "vlog",
    "channel",
    
    # HuggingFace/AI tags
    "model",
    "dataset",
    "paper",
    "ai",
    "machine learning",
    "computer vision",
    "nlp",
    "computer_vision",
    "machine_learning",
    
    # Cross-platform content tags
    "technology",
    "gaming",
    "sports",
    "movies",
    "education",
    "science",
    "health",
    "politics",
    "politician",
    "business",
    "finance",
    "comedy",
    "travel",
    "food",
    "fashion",
    "climate",
    "animals",
    "pets",
]

@dataclass
class CrawlerMapping:
    """Defines which crawler(s) and category to use for a tag"""
    crawler: str  # "youtube", "google_trends", "reddit", "huggingface"
    category_id: Optional[str] = None
    priority: int = 1  # Higher priority = more relevant


# Tag to Crawler/Category mappings
TAG_MAPPINGS: Dict[str, List[CrawlerMapping]] = {
    # Entertainment
    "movies": [
        CrawlerMapping("youtube", "30", priority=3),  # Movies
        CrawlerMapping("google_trends", "4", priority=2),  # Entertainment
        CrawlerMapping("reddit", priority=1),
    ],
    "music": [
        CrawlerMapping("youtube", "10", priority=3),  # Music
        CrawlerMapping("google_trends", "4", priority=2),  # Entertainment
        CrawlerMapping("reddit", priority=1),
    ],
    "entertainment": [
        CrawlerMapping("youtube", "24", priority=3),  # Entertainment
        CrawlerMapping("google_trends", "4", priority=2),  # Entertainment
        CrawlerMapping("reddit", priority=1),
    ],
    "comedy": [
        CrawlerMapping("youtube", "23", priority=3),  # Comedy
        CrawlerMapping("google_trends", "4", priority=2),  # Entertainment
        CrawlerMapping("reddit", priority=1),
    ],
    
    # Technology & AI
    "technology": [
        CrawlerMapping("youtube", "28", priority=2),  # Science & Technology
        CrawlerMapping("google_trends", "18", priority=3),  # Technology
        CrawlerMapping("reddit", priority=2),
    ],
    "ai": [
        CrawlerMapping("huggingface", priority=3),
        CrawlerMapping("youtube", "28", priority=2),  # Science & Technology
        CrawlerMapping("google_trends", "18", priority=2),  # Technology
    ],
    "ml": [
        CrawlerMapping("huggingface", priority=3),
        CrawlerMapping("youtube", "28", priority=2),  # Science & Technology
        CrawlerMapping("google_trends", "18", priority=2),  # Technology
    ],
    "machine_learning": [
        CrawlerMapping("huggingface", priority=3),
        CrawlerMapping("youtube", "28", priority=2),  # Science & Technology
        CrawlerMapping("google_trends", "18", priority=2),  # Technology
    ],
    "nlp": [
        CrawlerMapping("huggingface", priority=3),
        CrawlerMapping("youtube", "28", priority=2),  # Science & Technology
    ],
    "computer_vision": [
        CrawlerMapping("huggingface", priority=3),
        CrawlerMapping("youtube", "28", priority=2),  # Science & Technology
    ],
    
    # HuggingFace specific
    "model": [
        CrawlerMapping("huggingface", priority=3),
    ],
    "dataset": [
        CrawlerMapping("huggingface", priority=3),
    ],
    "paper": [
        CrawlerMapping("huggingface", priority=3),
    ],
    
    # Gaming
    "gaming": [
        CrawlerMapping("youtube", "20", priority=3),  # Gaming
        CrawlerMapping("google_trends", "6", priority=2),  # Games
        CrawlerMapping("reddit", priority=2),
    ],
    
    # Sports
    "sports": [
        CrawlerMapping("youtube", "17", priority=3),  # Sports
        CrawlerMapping("google_trends", "17", priority=3),  # Sports
        CrawlerMapping("reddit", priority=2),
    ],
    
    # Education & Learning
    "education": [
        CrawlerMapping("youtube", "27", priority=3),  # Education
        CrawlerMapping("google_trends", "9", priority=2),  # Jobs and Education
        CrawlerMapping("reddit", priority=1),
    ],
    "tutorial": [
        CrawlerMapping("youtube", "27", priority=3),  # Education
        CrawlerMapping("reddit", priority=1),
    ],
    "science": [
        CrawlerMapping("youtube", "28", priority=3),  # Science & Technology
        CrawlerMapping("google_trends", "15", priority=3),  # Science
        CrawlerMapping("reddit", priority=2),
    ],
    
    # Politics & News
    "politics": [
        CrawlerMapping("youtube", "25", priority=2),  # News & Politics
        CrawlerMapping("google_trends", "14", priority=3),  # Politics
        CrawlerMapping("reddit", priority=3),
    ],
    "politician": [
        CrawlerMapping("youtube", "25", priority=2),  # News & Politics
        CrawlerMapping("google_trends", "14", priority=3),  # Politics
        CrawlerMapping("reddit", priority=2),
    ],
    "news": [
        CrawlerMapping("youtube", "25", priority=2),  # News & Politics
        CrawlerMapping("google_trends", "14", priority=2),  # Politics
        CrawlerMapping("reddit", priority=3),
    ],
    
    # Health & Wellness
    "health": [
        CrawlerMapping("youtube", "26", priority=2),  # Howto & Style
        CrawlerMapping("google_trends", "7", priority=3),  # Health
        CrawlerMapping("reddit", priority=2),
    ],
    
    # Business & Finance
    "business": [
        CrawlerMapping("youtube", "28", priority=2),  # Science & Technology
        CrawlerMapping("google_trends", "3", priority=3),  # Business and Finance
        CrawlerMapping("reddit", priority=2),
    ],
    "finance": [
        CrawlerMapping("youtube", "28", priority=2),  # Science & Technology
        CrawlerMapping("google_trends", "3", priority=3),  # Business and Finance
        CrawlerMapping("reddit", priority=2),
    ],
    
    # Lifestyle
    "food": [
        CrawlerMapping("youtube", "26", priority=3),  # Howto & Style
        CrawlerMapping("google_trends", "5", priority=3),  # Food and Drink
        CrawlerMapping("reddit", priority=2),
    ],
    "travel": [
        CrawlerMapping("youtube", "19", priority=3),  # Travel & Events
        CrawlerMapping("google_trends", "19", priority=3),  # Travel and Transportation
        CrawlerMapping("reddit", priority=2),
    ],
    "fashion": [
        CrawlerMapping("youtube", "26", priority=3),  # Howto & Style
        CrawlerMapping("google_trends", "2", priority=3),  # Beauty and Fashion
        CrawlerMapping("reddit", priority=1),
    ],
    
    # Environment
    "climate": [
        CrawlerMapping("youtube", "28", priority=2),  # Science & Technology
        CrawlerMapping("google_trends", "20", priority=3),  # Climate
        CrawlerMapping("reddit", priority=2),
    ],
    
    # Animals
    "animals": [
        CrawlerMapping("youtube", "15", priority=3),  # Pets & Animals
        CrawlerMapping("google_trends", "13", priority=3),  # Pets and Animals
        CrawlerMapping("reddit", priority=2),
    ],
    "pets": [
        CrawlerMapping("youtube", "15", priority=3),  # Pets & Animals
        CrawlerMapping("google_trends", "13", priority=3),  # Pets and Animals
        CrawlerMapping("reddit", priority=2),
    ],
    
    # Reddit-specific tags (no category needed)
    "discussion": [
        CrawlerMapping("reddit", priority=3),
    ],
    "community": [
        CrawlerMapping("reddit", priority=3),
    ],
    "social": [
        CrawlerMapping("reddit", priority=3),
    ],
    "meme": [
        CrawlerMapping("reddit", priority=3),
        CrawlerMapping("youtube", "23", priority=1),  # Comedy
    ],
    "ask": [
        CrawlerMapping("reddit", priority=3),
    ],
    
    # Video-related (generic)
    "video": [
        CrawlerMapping("youtube", priority=2),
        CrawlerMapping("reddit", priority=1),
    ],
    "vlog": [
        CrawlerMapping("youtube", "21", priority=3),  # Videoblogging
    ],
    "channel": [
        CrawlerMapping("youtube", priority=2),
    ],
}


def get_predefined_tags_prompt() -> str:
    """
    Generate a prompt for LLMs to return only predefined tags.
    """
    tags_list = ", ".join(f'"{tag}"' for tag in sorted(PREDEFINED_TAGS))
    
    return f"""You must return ONLY tags from this predefined list:
{tags_list}

Return your response as a JSON array of tags, for example:
["politician", "movies", "climate", "discussion"]

Do NOT create new tags. Only use tags from the list above."""


if __name__ == "__main__":
    # Test the predefined tags
    print("Available Tags:")
    print("-" * 50)
    for tag in sorted(PREDEFINED_TAGS):
        print(f"  - {tag}")
    
    print("\n" + "=" * 50)
    print("LLM Prompt:")
    print("=" * 50)
    print(get_predefined_tags_prompt())