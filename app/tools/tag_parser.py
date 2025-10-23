from typing import List, Dict, Any, Set
from collections import defaultdict
from app.const.tags import TAG_MAPPINGS, PREDEFINED_TAGS

class TagParser:
    """
    Parse predefined tags from LLM and generate crawler configurations.
    
    Example input: ["politician", "movies", "climate", "discussion"]
    
    Example output:
    [
        {
            "crawler": "youtube",
            "params": {"category_ids": ["30", "25"]},
            "assigned_tags": ["movies", "politician"]
        },
        {
            "crawler": "google_trends",
            "params": {"category_id": "14"},
            "assigned_tags": ["politician"]
        },
        {
            "crawler": "reddit",
            "assigned_tags": ["discussion"]
        }
    ]
    """
    
    def __init__(self, tags: List[str]):
        self.tags = tags
        self.validated_tags = self._validate_tags()
    
    def _validate_tags(self) -> List[str]:
        """Validate that tags are from the predefined list"""
        valid_tags = []
        invalid_tags = []
        
        for tag in self.tags:
            tag_lower = tag.lower().strip()
            if tag_lower in PREDEFINED_TAGS:
                valid_tags.append(tag_lower)
            else:
                invalid_tags.append(tag)
        
        if invalid_tags:
            print(f"Warning: Invalid tags ignored: {invalid_tags}")
        
        return valid_tags
    
    def parse_to_crawler_configs(self) -> List[Dict[str, Any]]:
        """
        Parse tags and generate crawler configurations.
        
        Returns:
            List of crawler configs with assigned tags and params
        """
        if not self.validated_tags:
            # Default to reddit if no valid tags
            return [{
                "crawler": "reddit",
                "assigned_tags": []
            }]
        
        # Collect mappings per crawler
        crawler_data = defaultdict(lambda: {
            "category_ids": set(),
            "tags": [],
            "max_priority": 0
        })
        
        # Process each tag
        for tag in self.validated_tags:
            if tag not in TAG_MAPPINGS:
                continue
            
            mappings = TAG_MAPPINGS[tag]
            
            for mapping in mappings:
                crawler = mapping.crawler
                
                # Track the tag for this crawler
                crawler_data[crawler]["tags"].append(tag)
                
                # Track category if present
                if mapping.category_id:
                    crawler_data[crawler]["category_ids"].add(mapping.category_id)
                
                # Track max priority
                if mapping.priority > crawler_data[crawler]["max_priority"]:
                    crawler_data[crawler]["max_priority"] = mapping.priority
        
        # Convert to final format
        configs = []
        
        # Sort by priority (higher priority first)
        sorted_crawlers = sorted(
            crawler_data.items(),
            key=lambda x: x[1]["max_priority"],
            reverse=True
        )
        
        for crawler, data in sorted_crawlers:
            config = {
                "crawler": crawler,
                "assigned_tags": data["tags"]
            }
            
            # Add params based on crawler type
            if crawler == "youtube":
                if data["category_ids"]:
                    # YouTube can handle multiple category IDs
                    config["params"] = {
                        "category_ids": sorted(list(data["category_ids"]))
                    }
            elif crawler == "google_trends":
                if data["category_ids"]:
                    # Google Trends uses single category, pick the first one
                    # (or you could pick based on tag priority)
                    config["params"] = {
                        "category_id": list(data["category_ids"])[0]
                    }
            elif crawler == "huggingface":
                # HuggingFace uses search query
                config["params"] = {
                    "search_query": " ".join(data["tags"])
                }
            # Reddit doesn't need category params
            
            configs.append(config)
        
        return configs
    
    def get_all_tags(self) -> List[str]:
        """Get all validated tags"""
        return self.validated_tags


# Convenience function
def parse_tags(tags: List[str]) -> List[Dict[str, Any]]:
    """
    Parse tags into crawler configurations.
    
    Args:
        tags: List of predefined tags from LLM
        
    Returns:
        List of crawler configurations
    """
    parser = TagParser(tags)
    return parser.parse_to_crawler_configs()
