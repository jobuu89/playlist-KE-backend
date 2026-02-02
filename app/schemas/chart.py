from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.song import SongResponse
    from app.schemas.playlist import PlaylistSongResponse


class ChartBase(BaseModel):
    name: str
    week: int
    year: int
    region: Optional[str] = None


class ChartCreate(ChartBase):
    pass


class ChartResponse(ChartBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChartEntryBase(BaseModel):
    song_id: int
    rank: int
    previous_rank: Optional[int] = None
    trend: Optional[str] = None


class ChartEntryCreate(ChartEntryBase):
    chart_id: int


class ChartEntryResponse(ChartEntryBase):
    id: int
    chart_id: int
    created_at: datetime
    song: Optional["SongResponse"] = None
    
    class Config:
        from_attributes = True


class ChartDetailResponse(ChartResponse):
    entries: List[ChartEntryResponse] = []
    
    class Config:
        from_attributes = True


class WeeklyChartResponse(BaseModel):
    week: int
    year: int
    region: Optional[str] = None
    entries: List[ChartEntryResponse] = []

