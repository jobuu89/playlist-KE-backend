from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.song import SongResponse


class AnalyticsBase(BaseModel):
    song_id: Optional[int] = None
    region: Optional[str] = None
    date: Optional[datetime] = None


class AnalyticsCreate(AnalyticsBase):
    stream_count: int = 0
    unique_listeners: int = 0
    likes_count: int = 0
    shares_count: int = 0


class AnalyticsResponse(AnalyticsBase):
    id: int
    stream_count: int
    unique_listeners: int
    likes_count: int
    shares_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnalyticsOverview(BaseModel):
    total_streams: int
    total_unique_listeners: int
    total_likes: int
    total_shares: int
    top_songs: List[SongResponse] = []
    top_regions: List[dict] = []


class RegionAnalytics(BaseModel):
    region: str
    total_streams: int
    unique_listeners: int
    share_percentage: float

