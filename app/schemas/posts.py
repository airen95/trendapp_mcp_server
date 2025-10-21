from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class BasePost(BaseModel):
    source: str = Field(...)
    title: str
    content: Optional[str] = None
    author: str
    url: Optional[str] = None
    tags: list[str] = []
    created_at: datetime = Field(datetime.now())
    relevance_score: Optional[float] = None
    metadata: Optional[Any] = None

class YoutubePost(BaseModel):
    video_id: str
    view_count: int
    like_count: int
    thumbnail: str

class RedditPost(BaseModel):
    post_id: str
    permalink: Optional[str] = None
    upvote_ratio: Optional[float] = None